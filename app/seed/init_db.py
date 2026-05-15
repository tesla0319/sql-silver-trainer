"""DB 初期化スクリプト。

実行方法:
    python -m app.seed.init_db

処理内容:
    1. テーブルを作成（既存テーブルはスキップ）
    2. サンプル問題を投入（既にデータがある場合はスキップ）

二重投入防止: questions テーブルの件数をチェックし、1件以上あればスキップする。
"""

from sqlalchemy.orm import Session

# モデルをインポートすることで Base のメタデータに全テーブルが登録される
from app.database import engine, SessionLocal, Base
from app.models import Question, Choice  # noqa: F401 - Base へのモデル登録に必要
from app.seed.sample_questions import SAMPLE_QUESTIONS


def create_tables() -> None:
    """全テーブルを作成する。既存テーブルは変更しない。"""
    Base.metadata.create_all(bind=engine)
    print("テーブルを作成しました（既存テーブルはスキップ）。")


def seed_questions(db: Session) -> None:
    """サンプル問題を投入する。既にデータがある場合はスキップする。"""
    existing_count = db.query(Question).count()
    if existing_count > 0:
        print(f"既に {existing_count} 件の問題が存在するためスキップします。")
        return

    for q_data in SAMPLE_QUESTIONS:
        # 元のリストを変更しないようにコピーを使う
        q_dict = dict(q_data)
        choices_data = q_dict.pop("choices")

        question = Question(**q_dict)
        db.add(question)
        db.flush()  # ID を確定させてから Choice に question_id を設定する

        for c_data in choices_data:
            choice = Choice(question_id=question.id, **c_data)
            db.add(choice)

    db.commit()
    print(f"{len(SAMPLE_QUESTIONS)} 件の問題を投入しました。")


def main() -> None:
    create_tables()
    db = SessionLocal()
    try:
        seed_questions(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
