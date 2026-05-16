"""回答送信リクエスト / レスポンスの Pydantic スキーマ。"""

from pydantic import BaseModel, Field, field_validator


class AnswerRequest(BaseModel):
    question_id: int
    # min_length=1 で空リストを 422 として弾く
    selected_choice_ids: list[int] = Field(min_length=1)
    # user_name: デフォルト "guest"。前後空白は strip、空白のみは 422
    user_name: str = Field(default="guest", min_length=1, max_length=50)

    @field_validator("selected_choice_ids")
    @classmethod
    def no_duplicates(cls, v: list[int]) -> list[int]:
        """重複した choice_id を 422 として弾く（仕様確定事項 #1）。"""
        if len(v) != len(set(v)):
            raise ValueError("selected_choice_ids must not contain duplicates")
        return v

    @field_validator("user_name")
    @classmethod
    def strip_and_reject_blank(cls, v: str) -> str:
        """前後空白を除去し、空白のみは 422 として弾く。"""
        v = v.strip()
        if not v:
            raise ValueError("user_name must not be empty or whitespace only")
        return v


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_choice_ids: list[int]
    explanation: str
    trap_reason: str | None
