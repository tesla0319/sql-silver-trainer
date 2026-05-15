"""回答送信・判定 API エンドポイント。"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import config
from app.crud.answer import create_user_answer, delete_all_answers
from app.crud.question import get_question_by_id
from app.database import get_db
from app.schemas.answer import AnswerRequest, AnswerResponse
from app.services.grading import grade_answer

router = APIRouter(prefix="/api/answers", tags=["answers"])


@router.post("", response_model=AnswerResponse)
def submit_answer(body: AnswerRequest, db: Session = Depends(get_db)):
    """回答を送信して正誤を判定し、履歴を記録する。

    バリデーション順序（早期リターン優先）:
    1. selected_choice_ids が空 / 重複 → Pydantic が 422 を返す（schemas/answer.py）
    2. question_id が存在しない → 404
    3. selected_choice_ids に問題に属さない choice_id がある → 422
    4. 選択数不一致 + mode="warn" → 422（記録しない）
    5. 選択数不一致 + mode="reject" → 不正解として記録
    """
    question = get_question_by_id(db, body.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # 問題に属する choice_id の集合
    question_choice_ids = {c.id for c in question.choices}
    for cid in body.selected_choice_ids:
        if cid not in question_choice_ids:
            raise HTTPException(
                status_code=422,
                detail=f"choice_id {cid} does not belong to question {body.question_id}",
            )

    correct_choice_ids = [c.id for c in question.choices if c.is_correct]

    result = grade_answer(
        selected_ids=body.selected_choice_ids,
        correct_ids=correct_choice_ids,
        multi_select_count=question.multi_select_count,
        # config から実行時に読み込む（テスト時に monkeypatch で切り替え可能にするため）
        mode=config.INSUFFICIENT_SELECTION_MODE,
    )

    if result.should_warn:
        raise HTTPException(
            status_code=422,
            detail=f"Please select exactly {question.multi_select_count} choice(s)",
        )

    create_user_answer(
        db=db,
        question_id=question.id,
        selected_choice_ids=body.selected_choice_ids,
        is_correct=result.is_correct,
    )

    return AnswerResponse(
        is_correct=result.is_correct,
        correct_choice_ids=correct_choice_ids,
        explanation=question.explanation,
        trap_reason=question.trap_reason,
    )


@router.delete("")
def reset_answers(db: Session = Depends(get_db)):
    """全回答履歴をリセットする（テスト用。UIには表示しない）。"""
    deleted_count = delete_all_answers(db)
    return {"deleted_count": deleted_count}
