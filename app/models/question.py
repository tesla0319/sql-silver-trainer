from datetime import datetime

from sqlalchemy import Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class Question(Base):
    """問題テーブル: SQL Silver 試験の各問題を格納する。

    設計判断:
    - category に INDEX を付与: 苦手分析クエリで GROUP BY するため
    - multi_select_count: 「2つ選べ」「3つ選べ」に対応するための選択数定義
    - trap_reason は NULL 可: すべての問題に記述が難しいケースを想定
    """

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    multi_select_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    trap_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    choices: Mapped[list["Choice"]] = relationship(
        "Choice", back_populates="question", order_by="Choice.display_order"
    )
    user_answers: Mapped[list["UserAnswer"]] = relationship(
        "UserAnswer", back_populates="question"
    )
