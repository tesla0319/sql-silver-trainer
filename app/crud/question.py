"""問題テーブルの DB 操作層。"""

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from app.models.question import Question


def get_random_question(db: Session, category: str | None = None) -> Question | None:
    """ランダムに1問取得する。category 指定時はそのカテゴリに絞る。"""
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    return query.order_by(func.random()).first()


def get_question_by_id(db: Session, question_id: int) -> Question | None:
    """ID で問題を取得する。"""
    return db.query(Question).filter(Question.id == question_id).first()
