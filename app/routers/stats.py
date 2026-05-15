"""統計 API エンドポイント。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.stats import get_category_stats
from app.database import get_db
from app.schemas.stats import CategoryStatResponse, CategoryStatsResponse
from app.services.stats import CategoryStat, compute_accuracy

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/categories", response_model=CategoryStatsResponse)
def category_stats(db: Session = Depends(get_db)):
    """カテゴリ別の正答率を返す。

    - answered_count=0 のカテゴリは含めない（SPEC: 未着手と区別するため）
    - フロントは accuracy=0.0〜1.0 を受け取り、%表示に変換する
    """
    raw_stats = get_category_stats(db)

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
