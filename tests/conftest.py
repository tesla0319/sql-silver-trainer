"""pytest フィクスチャ定義。

テスト方針:
- インメモリ SQLite を使用し、本番の app.db と完全に分離する
- 各テスト関数は独立して動く（フィクスチャスコープは function）
- FastAPI の Depends(get_db) を dependency_overrides で差し替えてテスト用 DB を使う

注意点:
- インメモリ SQLite は接続ごとに別の DB になるため、同一エンジン・セッションを
  テスト中ずっと使い続ける必要がある（check_same_thread=False も必要）
- app.dependency_overrides はテスト後に必ずクリアすること
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
import app.models as _models  # noqa: F401 - Base へのモデル登録に必要（'app' 名を上書きしないよう as でエイリアス）
from app.models.question import Question
from app.models.choice import Choice

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_engine():
    """テスト用 DB エンジン。テスト終了時にテーブルを削除する。

    StaticPool を使う理由:
    sqlite:///:memory: はコネクションごとに別の空 DB が作成される。
    StaticPool で単一コネクションを強制することで、テーブル作成とクエリ実行が
    同じ DB を参照することを保証する。
    """
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """テスト用 DB セッション。テスト終了時にクローズする。"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """FastAPI の TestClient。Depends(get_db) をテスト用 DB セッションで差し替える。"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def seeded_db(db_session):
    """テスト用DBにサンプル問題を投入する。

    投入内容:
    - q1: 単一選択問題（VIEW, choices: 正解1 + 不正解2）
    - q2: 2つ選べ問題（INDEX, choices: 正解2 + 不正解2）
    - q3: 3つ選べ問題（CONSTRAINT, choices: 正解3 + 不正解1）

    返り値には各問題・選択肢の ID を含む dict を返す。
    commit 後に ID へアクセスすると SQLAlchemy が再クエリを発行するため、
    flush 直後に ID を変数に退避してから commit する。
    """
    # --- 単一選択問題 ---
    q1 = Question(
        category="VIEW", difficulty=1, question_text="単一選択テスト問題",
        multi_select_count=1, explanation="解説1", trap_reason="罠の理由1",
    )
    db_session.add(q1)
    db_session.flush()
    q1_id = q1.id

    q1_c1 = Choice(question_id=q1_id, choice_text="正解",    is_correct=True,  display_order=0)
    q1_c2 = Choice(question_id=q1_id, choice_text="不正解A", is_correct=False, display_order=1)
    q1_c3 = Choice(question_id=q1_id, choice_text="不正解B", is_correct=False, display_order=2)
    db_session.add_all([q1_c1, q1_c2, q1_c3])
    db_session.flush()
    q1_c1_id, q1_c2_id = q1_c1.id, q1_c2.id

    # --- 2つ選べ問題 ---
    q2 = Question(
        category="INDEX", difficulty=2, question_text="2つ選択テスト問題",
        multi_select_count=2, explanation="解説2", trap_reason=None,
    )
    db_session.add(q2)
    db_session.flush()
    q2_id = q2.id

    q2_c1 = Choice(question_id=q2_id, choice_text="正解A",   is_correct=True,  display_order=0)
    q2_c2 = Choice(question_id=q2_id, choice_text="正解B",   is_correct=True,  display_order=1)
    q2_c3 = Choice(question_id=q2_id, choice_text="不正解A", is_correct=False, display_order=2)
    q2_c4 = Choice(question_id=q2_id, choice_text="不正解B", is_correct=False, display_order=3)
    db_session.add_all([q2_c1, q2_c2, q2_c3, q2_c4])
    db_session.flush()
    q2_c1_id, q2_c2_id, q2_c3_id = q2_c1.id, q2_c2.id, q2_c3.id

    # --- 3つ選べ問題 ---
    q3 = Question(
        category="CONSTRAINT", difficulty=3, question_text="3つ選択テスト問題",
        multi_select_count=3, explanation="解説3", trap_reason="罠の理由3",
    )
    db_session.add(q3)
    db_session.flush()
    q3_id = q3.id

    q3_c1 = Choice(question_id=q3_id, choice_text="正解A",  is_correct=True,  display_order=0)
    q3_c2 = Choice(question_id=q3_id, choice_text="正解B",  is_correct=True,  display_order=1)
    q3_c3 = Choice(question_id=q3_id, choice_text="正解C",  is_correct=True,  display_order=2)
    q3_c4 = Choice(question_id=q3_id, choice_text="不正解", is_correct=False, display_order=3)
    db_session.add_all([q3_c1, q3_c2, q3_c3, q3_c4])
    db_session.flush()
    q3_c1_id, q3_c2_id, q3_c3_id, q3_c4_id = q3_c1.id, q3_c2.id, q3_c3.id, q3_c4.id

    db_session.commit()

    return {
        # 単一選択問題
        "q1_id": q1_id,
        "q1_correct_choice_id": q1_c1_id,
        "q1_incorrect_choice_id": q1_c2_id,
        # 2つ選べ問題
        "q2_id": q2_id,
        "q2_correct_choice_ids": [q2_c1_id, q2_c2_id],
        "q2_incorrect_choice_id": q2_c3_id,
        # 3つ選べ問題（選択数不一致テストに使用）
        "q3_id": q3_id,
        "q3_correct_choice_ids": [q3_c1_id, q3_c2_id, q3_c3_id],
        "q3_incorrect_choice_id": q3_c4_id,
        # 別問題の choice_id（問題に属さない choice_id テスト用: q2 の選択肢を q1 に送る）
        "q2_choice_id_for_cross_question_test": q2_c1_id,
    }
