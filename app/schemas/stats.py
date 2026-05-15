"""カテゴリ別統計レスポンスの Pydantic スキーマ。"""

from pydantic import BaseModel


class CategoryStatResponse(BaseModel):
    category: str
    answered_count: int
    correct_count: int
    accuracy: float  # 0.0〜1.0。表示側で%変換する。


class CategoryStatsResponse(BaseModel):
    stats: list[CategoryStatResponse]
