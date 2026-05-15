from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import questions, answers, stats

app = FastAPI(
    title="SQL Silver 学習支援アプリ",
    description="SQL Silver 試験のルール・制約・用語理解を強化する学習支援 Web アプリ",
)

# API ルーターを先に登録し、/api/* へのリクエストが静的ファイルに干渉しないようにする
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(stats.router)

# 静的ファイル（CSS・JS）は /static/* で配信
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
def health_check():
    """起動確認用ヘルスチェックエンドポイント。"""
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def serve_index():
    """フロントエンドのエントリポイント。"""
    return FileResponse("static/index.html")
