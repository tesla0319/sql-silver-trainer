"""問題取得 API エンドポイント。"""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.question import get_random_question
from app.database import get_db
from app.schemas.question import QuestionResponse

router = APIRouter(prefix="/api/questions", tags=["questions"])


@router.get("/random", response_model=QuestionResponse)
def random_question(
    mode: Literal["normal", "weak"] = "normal",
    category: str | None = None,
    db: Session = Depends(get_db),
):
    """ランダムに1問取得する。

    - mode="normal": 全問題からランダム出題
    - mode="weak"  : 苦手カテゴリから出題（Phase 1c 実装予定）
      Phase 1b では通常モードにフォールバックする（SPEC 6.2）
    - category 指定時: 該当カテゴリに絞って出題
    """
    # Phase 1b: weak モードは Phase 1c で実装。現時点では normal と同じ動作にフォールバック。
    question = get_random_question(db, category=category)
    if question is None:
        raise HTTPException(status_code=404, detail="No questions found")
    return question
