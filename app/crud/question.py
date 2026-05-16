"""問題テーブルの DB 操作層。"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.user_answer import UserAnswer


def get_random_question(
    db: Session,
    category: str | None = None,
    exclude_ids: list[int] | None = None,
) -> Question | None:
    """ランダムに1問取得する。

    Args:
        category:    指定時はそのカテゴリに絞る
        exclude_ids: 除外する question_id のリスト（セッション除外に使用）
                     除外後に候補が0件になった場合はフォールバックしない（呼び出し側で制御）
    """
    query = db.query(Question)
    if category:
        query = query.filter(Question.category == category)
    if exclude_ids:
        query = query.filter(Question.id.notin_(exclude_ids))
    return query.order_by(func.random()).first()


def get_question_by_id(db: Session, question_id: int) -> Question | None:
    """ID で問題を取得する。"""
    return db.query(Question).filter(Question.id == question_id).first()


def get_wrong_question_ids(db: Session, user_name: str = "guest") -> list[int]:
    """最直近の回答が不正解だった question_id のリストを返す（user_name 単位）。

    「最直近」の定義: question_id ごとに user_answers.id が最大の行（= 最後に挿入した回答）。
    その行が is_correct=False であれば復習対象とする。
    一度正解した問題（最直近が正解）は克服済みとして除外する。
    """
    # user_name で絞った上で question_id ごとの最大 id（= 最新の回答）をサブクエリで取得
    latest_subq = (
        db.query(
            UserAnswer.question_id,
            func.max(UserAnswer.id).label("max_id"),
        )
        .filter(UserAnswer.user_name == user_name)
        .group_by(UserAnswer.question_id)
        .subquery()
    )

    rows = (
        db.query(UserAnswer.question_id)
        .join(
            latest_subq,
            (UserAnswer.question_id == latest_subq.c.question_id)
            & (UserAnswer.id == latest_subq.c.max_id),
        )
        .filter(UserAnswer.is_correct == False)  # noqa: E712 - SQLAlchemy は == で比較する
        .filter(UserAnswer.user_name == user_name)
        .all()
    )

    return [r.question_id for r in rows]
