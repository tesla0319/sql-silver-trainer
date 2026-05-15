"""回答履歴テーブルの DB 操作層。"""

import json

from sqlalchemy.orm import Session

from app.models.user_answer import UserAnswer


def create_user_answer(
    db: Session,
    question_id: int,
    selected_choice_ids: list[int],
    is_correct: bool,
) -> UserAnswer:
    """回答を記録して返す。selected_choice_ids は JSON 文字列に変換して保存。"""
    answer = UserAnswer(
        question_id=question_id,
        selected_choices=json.dumps(selected_choice_ids),
        is_correct=is_correct,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def delete_all_answers(db: Session) -> int:
    """全回答履歴を削除して削除件数を返す（テスト用リセット）。"""
    deleted_count = db.query(UserAnswer).delete()
    db.commit()
    return deleted_count
