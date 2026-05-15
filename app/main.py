from fastapi import FastAPI

from app.routers import questions, answers, stats

app = FastAPI(
    title="SQL Silver 学習支援アプリ",
    description="SQL Silver 試験のルール・制約・用語理解を強化する学習支援 Web アプリ",
)

app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(stats.router)


@app.get("/health")
def health_check():
    """起動確認用ヘルスチェックエンドポイント。"""
    return {"status": "ok"}
