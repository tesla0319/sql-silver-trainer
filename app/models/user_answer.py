from datetime import datetime

from sqlalchemy import Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class UserAnswer(Base):
    """回答履歴テーブル: ユーザーの回答を記録する。

    設計判断:
    - selected_choices は JSON 文字列で保持 (例: "[3, 5]")
      MVPでは正規化（別テーブル化）せずシンプルに保持。
      苦手分析は question_id 経由の JOIN で十分なため問題なし。
      Phase2 以降で正規化を検討。
    - question_id に INDEX: 苦手分析クエリで GROUP BY question_id を使うため
    """

    __tablename__ = "user_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(
        Text, nullable=False, default="guest", server_default="guest", index=True
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id"), nullable=False, index=True
    )
    selected_choices: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    answered_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    question: Mapped["Question"] = relationship("Question", back_populates="user_answers")
