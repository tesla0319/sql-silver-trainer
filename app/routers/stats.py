"""統計 API エンドポイント。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud.stats import get_category_stats
from app.database import get_db
from app.schemas.stats import CategoryStatResponse, CategoryStatsResponse
from app.services.stats import CategoryStat, compute_accuracy

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/categories", response_model=CategoryStatsResponse)
def category_stats(
    user_name: str = Query(default="guest", min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    """カテゴリ別の正答率を返す（user_name 単位）。

    - answered_count=0 のカテゴリは含めない（SPEC: 未着手と区別するため）
    - フロントは accuracy=0.0〜1.0 を受け取り、%表示に変換する
    """
    raw_stats = get_category_stats(db, user_name=user_name)

    stats = [
        CategoryStatResponse(
            category=row.category,
            answered_count=row.answered_count,
            correct_count=row.correct_count,
            accuracy=compute_accuracy(row.answered_count, row.correct_count),
        )
        for row in raw_stats
    ]

    return CategoryStatsResponse(stats=stats)
