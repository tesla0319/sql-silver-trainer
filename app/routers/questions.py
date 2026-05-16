"""問題取得 API エンドポイント。"""

import random
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import config
from app.crud.question import (
    get_question_by_id,
    get_random_question,
    get_wrong_question_ids,
)
from app.crud.stats import get_category_stats
from app.database import get_db
from app.schemas.question import QuestionResponse
from app.services.stats import CategoryStat, compute_accuracy, get_weak_categories

router = APIRouter(prefix="/api/questions", tags=["questions"])


def _random_with_fallback(
    db: Session,
    *,
    category: str | None,
    exclude_ids: list[int],
):
    """exclude_ids を適用してランダム取得。候補が尽きた場合は除外なしでフォールバック。

    フォールバックした場合、フロントエンドは「返ってきた question.id が
    sessionExcludeIds に含まれている」ことを検知してセッションをリセットする。
    """
    question = get_random_question(db, category=category, exclude_ids=exclude_ids or None)
    if question is None and exclude_ids:
        # セッションの問題が全て出題済み → 除外なしでフォールバック
        question = get_random_question(db, category=category, exclude_ids=None)
    return question


@router.get("/random", response_model=QuestionResponse)
def random_question(
    mode: Literal["normal", "weak", "review"] = "normal",
    category: str | None = None,
    exclude_ids: list[int] = Query(default=[]),
    user_name: str = Query(default="guest", min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    """ランダムに1問取得する。

    mode:
      "normal": 全問題（またはcategory指定）からランダム出題
      "weak"  : 苦手カテゴリから出題（user_name 単位）。苦手なし → 通常モードにフォールバック
      "review": 最直近の回答が不正解の問題から出題（user_name 単位）。対象なし → 通常モードにフォールバック

    exclude_ids:
      フロントエンドがセッション中に出題済みの question_id を送信する。
      該当問題を除いてランダム選択する。全問除外された場合はフォールバックして返す。
      フロントエンドは返ってきた問題が sessionExcludeIds に含まれていればセッションリセットを行う。
    """
    question = None

    if mode == "weak":
        question = _resolve_weak(db, exclude_ids, user_name=user_name)

    elif mode == "review":
        question = _resolve_review(db, exclude_ids, user_name=user_name)

    # normal または上記モードがフォールバックした場合
    if question is None:
        question = _random_with_fallback(db, category=category, exclude_ids=exclude_ids)

    if question is None:
        raise HTTPException(status_code=404, detail="No questions found")

    return question


def _resolve_weak(db: Session, exclude_ids: list[int], user_name: str = "guest"):
    """苦手カテゴリから問題を選ぶ（user_name 単位）。苦手カテゴリなし → None を返しフォールバックさせる。"""
    raw_stats = get_category_stats(db, user_name=user_name)
    stats = [
        CategoryStat(
            category=row.category,
            answered_count=row.answered_count,
            correct_count=row.correct_count,
            accuracy=compute_accuracy(row.answered_count, row.correct_count),
        )
        for row in raw_stats
    ]
    weak_cats = get_weak_categories(
        stats,
        weak_threshold=config.WEAK_THRESHOLD,
        min_answers=config.MIN_ANSWERS,
    )
    if not weak_cats:
        return None  # フォールバックを呼び出し側に委ねる

    target_category = random.choice(weak_cats)
    return _random_with_fallback(db, category=target_category, exclude_ids=exclude_ids)


def _resolve_review(db: Session, exclude_ids: list[int], user_name: str = "guest"):
    """最直近が不正解の問題から選ぶ（user_name 単位）。対象なし → None を返しフォールバックさせる。

    exclude_ids で全ての復習候補が尽きた場合は、除外を無視して復習候補から選び直す
    （セッションリセットをフロントエンドに検知させる）。
    """
    wrong_ids = get_wrong_question_ids(db, user_name=user_name)
    if not wrong_ids:
        return None  # 間違い問題なし → 通常モードにフォールバック

    exclude_set = set(exclude_ids)
    candidates = [qid for qid in wrong_ids if qid not in exclude_set]

    if not candidates:
        # セッション内で全復習問題を消化 → 復習候補全体からリセット
        candidates = wrong_ids

    chosen_id = random.choice(candidates)
    return get_question_by_id(db, chosen_id)
