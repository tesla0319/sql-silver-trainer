"""GET /api/stats/categories と weak mode 出題のAPIテスト。"""

import json

from app.models.question import Question
from app.models.choice import Choice
from app.models.user_answer import UserAnswer


# --- フィクスチャヘルパー ---

def _add_answers(
    db_session,
    question_id: int,
    is_correct: bool,
    count: int,
    user_name: str = "guest",
) -> None:
    """指定数の回答履歴を直接 DB に挿入する。
    API 経由で挿入すると choice_id バリデーションが走るため、
    統計テスト用データはここで直接 INSERT する。
    selected_choices の値は統計クエリでは参照されないためダミー値を使用。
    """
    for _ in range(count):
        db_session.add(UserAnswer(
            question_id=question_id,
            selected_choices=json.dumps([]),  # 統計クエリは参照しない
            is_correct=is_correct,
            user_name=user_name,
        ))
    db_session.commit()


def _make_question(db_session, category: str) -> tuple[int, int]:
    """最小構成の問題と選択肢を作成し (question_id, correct_choice_id) を返す。"""
    q = Question(
        category=category, difficulty=1, question_text=f"{category}テスト問題",
        multi_select_count=1, explanation="解説", trap_reason=None,
    )
    db_session.add(q)
    db_session.flush()
    q_id = q.id

    c = Choice(question_id=q_id, choice_text="正解", is_correct=True, display_order=0)
    db_session.add(c)
    db_session.flush()
    c_id = c.id

    db_session.commit()
    return q_id, c_id


# --- 統計 API テスト ---

class TestCategoryStats:

    def test_empty_when_no_answers(self, client, seeded_db):
        """全カテゴリ未着手 → stats: []（SPEC 8.2 異常系）。"""
        response = client.get("/api/stats/categories")
        assert response.status_code == 200
        assert response.json() == {"stats": []}

    def test_shows_category_after_answer(self, client, seeded_db):
        """回答後はそのカテゴリの統計が現れる。"""
        client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
        })

        response = client.get("/api/stats/categories")
        stats = response.json()["stats"]
        assert len(stats) == 1
        s = stats[0]
        assert s["category"] == "VIEW"
        assert s["answered_count"] == 1
        assert s["correct_count"] == 1
        assert s["accuracy"] == 1.0

    def test_accuracy_calculation(self, client, seeded_db):
        """正答率 = correct_count / answered_count が正しく計算される。"""
        q_id = seeded_db["q1_id"]
        c_correct = seeded_db["q1_correct_choice_id"]
        c_wrong = seeded_db["q1_incorrect_choice_id"]

        # 1正解 + 3不正解 → accuracy = 0.25
        client.post("/api/answers", json={"question_id": q_id, "selected_choice_ids": [c_correct]})
        for _ in range(3):
            client.post("/api/answers", json={"question_id": q_id, "selected_choice_ids": [c_wrong]})

        stats = client.get("/api/stats/categories").json()["stats"]
        s = next(x for x in stats if x["category"] == "VIEW")
        assert s["answered_count"] == 4
        assert s["correct_count"] == 1
        assert abs(s["accuracy"] - 0.25) < 1e-9

    def test_excludes_unanswered_categories(self, client, db_session):
        """回答済みカテゴリのみ返す（answered=0 のカテゴリは含めない）。"""
        # VIEW に問題を作り回答する。INDEX は問題だけ作り回答しない。
        view_id, view_c_id = _make_question(db_session, "VIEW")
        _make_question(db_session, "INDEX")  # 回答しない

        client.post("/api/answers", json={
            "question_id": view_id, "selected_choice_ids": [view_c_id],
        })

        stats = client.get("/api/stats/categories").json()["stats"]
        categories = [s["category"] for s in stats]
        assert "VIEW" in categories
        assert "INDEX" not in categories

    def test_multiple_categories(self, client, db_session):
        """複数カテゴリを回答すると、それぞれの統計が返る。"""
        view_id, view_c_id = _make_question(db_session, "VIEW")
        index_id, index_c_id = _make_question(db_session, "INDEX")

        client.post("/api/answers", json={"question_id": view_id,  "selected_choice_ids": [view_c_id]})
        client.post("/api/answers", json={"question_id": index_id, "selected_choice_ids": [index_c_id]})

        stats = client.get("/api/stats/categories").json()["stats"]
        assert len(stats) == 2


# --- weak mode 出題テスト ---

class TestWeakMode:

    def test_weak_mode_picks_weak_category(self, client, db_session):
        """苦手カテゴリがある場合、weak mode でそのカテゴリの問題が出題される。

        セットアップ:
        - VIEW: 4回全不正解 → accuracy=0.0 (苦手, MIN_ANSWERS=3 以上)
        - INDEX: 3回全正解  → accuracy=1.0 (苦手ではない)
        各カテゴリに問題が1問だけあるため、weak mode は必ず VIEW の問題を返す。
        """
        view_id,  _ = _make_question(db_session, "VIEW")
        index_id, _ = _make_question(db_session, "INDEX")

        _add_answers(db_session, view_id,  is_correct=False, count=4)
        _add_answers(db_session, index_id, is_correct=True,  count=3)

        response = client.get("/api/questions/random?mode=weak")
        assert response.status_code == 200
        assert response.json()["category"] == "VIEW"

    def test_weak_mode_fallback_when_no_weak(self, client, seeded_db):
        """苦手カテゴリがない場合（回答数不足）、通常モードにフォールバックして問題を返す。

        seeded_db は問題データがあるが回答は0件 → MIN_ANSWERS 未達 → 苦手なし。
        """
        response = client.get("/api/questions/random?mode=weak")
        assert response.status_code == 200
        assert "id" in response.json()

    def test_weak_mode_fallback_all_good_accuracy(self, client, db_session):
        """全カテゴリの正答率が閾値以上の場合も通常モードにフォールバックする。"""
        view_id, view_c_id = _make_question(db_session, "VIEW")
        _add_answers(db_session, view_id, is_correct=True, count=3)  # accuracy=1.0

        response = client.get("/api/questions/random?mode=weak")
        assert response.status_code == 200
        assert "id" in response.json()

    def test_weak_mode_multiple_weak_categories(self, client, db_session):
        """複数の苦手カテゴリがある場合、そのいずれかから出題される。"""
        view_id,    _ = _make_question(db_session, "VIEW")
        index_id,   _ = _make_question(db_session, "INDEX")
        subq_id,    _ = _make_question(db_session, "SUBQUERY")

        _add_answers(db_session, view_id,  is_correct=False, count=3)  # 苦手
        _add_answers(db_session, index_id, is_correct=False, count=3)  # 苦手
        _add_answers(db_session, subq_id,  is_correct=True,  count=3)  # 苦手ではない

        response = client.get("/api/questions/random?mode=weak")
        assert response.status_code == 200
        assert response.json()["category"] in ("VIEW", "INDEX")


# --- ユーザー別データ分離テスト ---

class TestUserIsolation:
    """alice と bob のデータが互いに干渉しないことを確認するテスト。"""

    def test_stats_isolated_per_user(self, client, db_session):
        """alice の統計に bob のデータは含まれない（逆も同様）。"""
        view_id,  _ = _make_question(db_session, "VIEW")
        index_id, _ = _make_question(db_session, "INDEX")

        # alice は VIEW を 3回全不正解
        _add_answers(db_session, view_id,  is_correct=False, count=3, user_name="alice")
        # bob は INDEX を 3回全不正解
        _add_answers(db_session, index_id, is_correct=False, count=3, user_name="bob")

        alice_stats = client.get("/api/stats/categories?user_name=alice").json()["stats"]
        bob_stats   = client.get("/api/stats/categories?user_name=bob").json()["stats"]

        assert len(alice_stats) == 1
        assert alice_stats[0]["category"] == "VIEW"

        assert len(bob_stats) == 1
        assert bob_stats[0]["category"] == "INDEX"

    def test_weak_mode_isolated_per_user(self, client, db_session):
        """weak mode で alice と bob がそれぞれ自分の苦手カテゴリから出題される。"""
        view_id,  _ = _make_question(db_session, "VIEW")
        index_id, _ = _make_question(db_session, "INDEX")

        # alice は VIEW が苦手 / INDEX は得意
        _add_answers(db_session, view_id,  is_correct=False, count=4, user_name="alice")
        _add_answers(db_session, index_id, is_correct=True,  count=4, user_name="alice")
        # bob は INDEX が苦手 / VIEW は得意
        _add_answers(db_session, view_id,  is_correct=True,  count=4, user_name="bob")
        _add_answers(db_session, index_id, is_correct=False, count=4, user_name="bob")

        alice_q = client.get("/api/questions/random?mode=weak&user_name=alice").json()
        bob_q   = client.get("/api/questions/random?mode=weak&user_name=bob").json()

        assert alice_q["category"] == "VIEW"
        assert bob_q["category"]   == "INDEX"

    def test_guest_user_isolated_from_named_user(self, client, db_session):
        """user_name 未指定（guest）と named user のデータは分離される。"""
        view_id,  _ = _make_question(db_session, "VIEW")
        index_id, _ = _make_question(db_session, "INDEX")

        # guest は VIEW のみ回答
        _add_answers(db_session, view_id, is_correct=True, count=3, user_name="guest")
        # alice は INDEX のみ回答
        _add_answers(db_session, index_id, is_correct=True, count=3, user_name="alice")

        # user_name 省略（= guest） → VIEW のみ返す
        guest_stats = client.get("/api/stats/categories").json()["stats"]
        assert any(s["category"] == "VIEW"  for s in guest_stats)
        assert not any(s["category"] == "INDEX" for s in guest_stats)

        # user_name=alice → INDEX のみ返す
        alice_stats = client.get("/api/stats/categories?user_name=alice").json()["stats"]
        assert any(s["category"] == "INDEX" for s in alice_stats)
        assert not any(s["category"] == "VIEW"  for s in alice_stats)
