from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import DATABASE_URL


# SQLite はデフォルトでスレッド間のセッション共有を禁止しているが、
# FastAPI は1リクエスト1スレッドで動くため check_same_thread=False で許可する
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """全モデルが継承する基底クラス。SQLAlchemy 2.x スタイル。"""
    pass


def get_db():
    """FastAPI の Depends で使う DB セッションジェネレータ。
    リクエスト終了時に必ずセッションをクローズする。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
