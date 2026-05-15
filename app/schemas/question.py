"""問題取得レスポンスの Pydantic スキーマ。

カンニング防止のため is_correct・explanation はレスポンスに含めない。
"""

from pydantic import BaseModel


class ChoiceResponse(BaseModel):
    """選択肢レスポンス。is_correct は除外（カンニング防止）。"""

    id: int
    choice_text: str
    display_order: int

    model_config = {"from_attributes": True}


class QuestionResponse(BaseModel):
    """問題取得レスポンス。explanation・trap_reason は除外（カンニング防止）。"""

    id: int
    category: str
    difficulty: int
    question_text: str
    multi_select_count: int
    choices: list[ChoiceResponse]

    model_config = {"from_attributes": True}
