"""統計集計のDB操作層。

設計判断:
- user_answers を起点に questions を INNER JOIN することで、
  answered_count=0 のカテゴリを自動的に除外する（SPEC: 未着手カテゴリは含めない）。
- selected_choices は JSON 文字列で保存しているが、統計クエリでは
  question_id と is_correct しか使わないので問題なし（SPEC §9 リスク#1）。
"""

from sqlalchemy import func, case
from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.user_answer import UserAnswer


def get_category_stats(db: Session, user_name: str = "guest") -> list:
    """カテゴリ別の回答数・正答数を集計して返す（user_name 単位）。

    返り値: Row オブジェクトのリスト
      各 Row の属性: .category, .answered_count, .correct_count
    """
    return (
        db.query(
            Question.category,
            func.count(UserAnswer.id).label("answered_count"),
            # SQLite の BOOLEAN は 0/1 で格納されるため case で int に変換してから SUM する
            func.sum(case((UserAnswer.is_correct, 1), else_=0)).label("correct_count"),
        )
        .join(Question, UserAnswer.question_id == Question.id)
        .filter(UserAnswer.user_name == user_name)
        .group_by(Question.category)
        .all()
    )
