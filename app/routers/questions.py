"""問題取得 API エンドポイント。"""

import random
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import config
from app.crud.question import get_random_question
from app.crud.stats import get_category_stats
from app.database import get_db
from app.schemas.question import QuestionResponse
from app.services.stats import CategoryStat, compute_accuracy, get_weak_categories

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("/random", response_model=QuestionResponse)
def random_question(
    mode: Literal["normal", "weak"] = "normal",
    category: str | None = None,
    db: Session = Depends(get_db),
):
    """ランダムに1問取得する。

    mode="normal": 全問題（またはcategory指定）からランダム出題
    mode="weak"  :
      1. カテゴリ別統計を取得し苦手カテゴリを算出
      2. 苦手カテゴリが1つ以上あれば、そこからランダムに1カテゴリを選んで出題
      3. 苦手カテゴリが存在しない場合は通常モードにフォールバック（SPEC 6.2）
      ※ mode=weak 指定時は category パラメータを無視する
    """
    target_category = category

    if mode == "weak":
        raw_stats = get_category_stats(db)
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
        if weak_cats:
            target_category = random.choice(weak_cats)
        else:
            # 苦手カテゴリなし → 通常モードにフォールバック
            target_category = None

    question = get_random_question(db, category=target_category)
    if question is None:
        raise HTTPException(status_code=404, detail="No questions found")
    return question
