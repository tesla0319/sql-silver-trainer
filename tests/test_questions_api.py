"""GET /api/questions/random のAPIテスト。"""

import json

from app.models.user_answer import UserAnswer


class TestRandomQuestion:
    def test_success(self, client, seeded_db):
        """正常系: 問題が取得できる。"""
        response = client.get("/api/questions/random")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "category" in data
        assert "question_text" in data
        assert "multi_select_count" in data
        assert "choices" in data

    def test_response_excludes_is_correct(self, client, seeded_db):
        """カンニング防止: choices に is_correct が含まれていない。"""
        response = client.get("/api/questions/random")
        assert response.status_code == 200
        for choice in response.json()["choices"]:
            assert "is_correct" not in choice

    def test_response_excludes_explanation(self, client, seeded_db):
        """カンニング防止: レスポンスに explanation が含まれていない。"""
        response = client.get("/api/questions/random")
        assert response.status_code == 200
        assert "explanation" not in response.json()

    def test_no_questions_returns_404(self, client):
        """異常系: 問題が0件のとき 404。"""
        response = client.get("/api/questions/random")
        assert response.status_code == 404

    def test_invalid_mode_returns_422(self, client, seeded_db):
        """異常系: 不正なモード指定で 422。"""
        response = client.get("/api/questions/random?mode=invalid")
        assert response.status_code == 422

    def test_normal_mode_explicit(self, client, seeded_db):
        """正常系: mode=normal を明示しても取得できる。"""
        response = client.get("/api/questions/random?mode=normal")
        assert response.status_code == 200

    def test_weak_mode_fallback(self, client, seeded_db):
        """正常系: mode=weak で苦手カテゴリなし → 通常モードにフォールバック（SPEC 6.2）。"""
        response = client.get("/api/questions/random?mode=weak")
        assert response.status_code == 200

    def test_choices_ordered_by_display_order(self, client, seeded_db):
        """選択肢が display_order 順に並んでいる。"""
        response = client.get("/api/questions/random")
        choices = response.json()["choices"]
        orders = [c["display_order"] for c in choices]
        assert orders == sorted(orders)


class TestExcludeIds:
    """exclude_ids パラメータのテスト。"""

    def test_exclude_ids_removes_specified_question(self, client, seeded_db):
        """指定した question_id は出題されない。"""
        q1 = seeded_db["q1_id"]
        q2 = seeded_db["q2_id"]
        # q1・q2 を除外 → q3 のみ残る
        response = client.get(
            f"/api/questions/random?exclude_ids={q1}&exclude_ids={q2}"
        )
        assert response.status_code == 200
        assert response.json()["id"] == seeded_db["q3_id"]

    def test_exclude_ids_fallback_when_all_excluded(self, client, seeded_db):
        """全問題を exclude_ids に含めた場合もフォールバックして 200 を返す（404にならない）。"""
        q_ids = [seeded_db["q1_id"], seeded_db["q2_id"], seeded_db["q3_id"]]
        params = "&".join(f"exclude_ids={q}" for q in q_ids)
        response = client.get(f"/api/questions/random?{params}")
        assert response.status_code == 200
        # フォールバック後は exclude_ids が無効になり、いずれかの問題が返る
        assert response.json()["id"] in q_ids

    def test_exclude_ids_empty_is_same_as_no_param(self, client, seeded_db):
        """exclude_ids を省略しても動作する（後方互換）。"""
        response = client.get("/api/questions/random")
        assert response.status_code == 200

    def test_exclude_ids_works_with_weak_mode(self, client, db_session, seeded_db):
        """mode=weak でも exclude_ids が機能する。"""
        from app.models.user_answer import UserAnswer

        # q1（VIEW）を苦手にする（4回不正解）
        for _ in range(4):
            db_session.add(UserAnswer(
                question_id=seeded_db["q1_id"],
                selected_choices=json.dumps([]),
                is_correct=False,
            ))
        db_session.commit()

        # q1 を除外して weak mode → フォールバックして q1 が返るか別の問題が返るか
        response = client.get(
            f"/api/questions/random?mode=weak&exclude_ids={seeded_db['q1_id']}"
        )
        assert response.status_code == 200


class TestReviewMode:
    """mode=review のテスト。"""

    def test_review_mode_valid(self, client, seeded_db):
        """mode=review は有効なモード（422にならない）。"""
        response = client.get("/api/questions/random?mode=review")
        assert response.status_code == 200

    def test_review_mode_returns_wrong_question(self, client, db_session, seeded_db):
        """最直近が不正解の問題が返る。"""
        db_session.add(UserAnswer(
            question_id=seeded_db["q1_id"],
            selected_choices=json.dumps([seeded_db["q1_incorrect_choice_id"]]),
            is_correct=False,
        ))
        db_session.commit()

        response = client.get("/api/questions/random?mode=review")
        assert response.status_code == 200
        assert response.json()["id"] == seeded_db["q1_id"]

    def test_review_mode_excludes_corrected_question(self, client, db_session, seeded_db):
        """一度間違えても、最直近が正解なら復習対象外（克服済み）。"""
        # q1: 不正解 → 正解（克服済み）
        db_session.add(UserAnswer(
            question_id=seeded_db["q1_id"], selected_choices="[]", is_correct=False
        ))
        db_session.add(UserAnswer(
            question_id=seeded_db["q1_id"], selected_choices="[]", is_correct=True
        ))
        # q2: 不正解のみ（復習対象）
        db_session.add(UserAnswer(
            question_id=seeded_db["q2_id"], selected_choices="[]", is_correct=False
        ))
        db_session.commit()

        response = client.get("/api/questions/random?mode=review")
        assert response.status_code == 200
        # q1 は克服済みなので返らない、q2 が返る
        assert response.json()["id"] == seeded_db["q2_id"]

    def test_review_mode_fallback_when_no_wrong_answers(self, client, seeded_db):
        """間違い問題が0件 → 通常モードにフォールバックして問題を返す。"""
        # 全問正解
        for q_id in [seeded_db["q1_id"], seeded_db["q2_id"], seeded_db["q3_id"]]:
            db_session_is_not_available = True  # フィクスチャを使わず seeded_db だけ
        # 未回答状態でも 200 が返ることを確認
        response = client.get("/api/questions/random?mode=review")
        assert response.status_code == 200
        assert "id" in response.json()

    def test_review_mode_with_exclude_ids_resets_when_exhausted(
        self, client, db_session, seeded_db
    ):
        """review 候補が全て exclude_ids にある場合、除外無視で候補から返す。"""
        q1 = seeded_db["q1_id"]
        q2 = seeded_db["q2_id"]
        # q1・q2 を間違える
        for qid in [q1, q2]:
            db_session.add(UserAnswer(
                question_id=qid, selected_choices="[]", is_correct=False
            ))
        db_session.commit()

        # 全復習候補を exclude_ids に入れる → フォールバックで候補から選ぶ
        response = client.get(
            f"/api/questions/random?mode=review&exclude_ids={q1}&exclude_ids={q2}"
        )
        assert response.status_code == 200
        assert response.json()["id"] in [q1, q2]

    def test_review_mode_latest_wrong_not_earlier_wrong(
        self, client, db_session, seeded_db
    ):
        """「最直近」判定: 正解→不正解の順なら復習対象になる。"""
        # q1: 正解 → 不正解（最直近が不正解 → 復習対象）
        db_session.add(UserAnswer(
            question_id=seeded_db["q1_id"], selected_choices="[]", is_correct=True
        ))
        db_session.add(UserAnswer(
            question_id=seeded_db["q1_id"], selected_choices="[]", is_correct=False
        ))
        db_session.commit()

        response = client.get("/api/questions/random?mode=review")
        assert response.status_code == 200
        assert response.json()["id"] == seeded_db["q1_id"]


class TestExcludeCategories:
    """excluded_categories パラメータのテスト（10問トレーニング偏り抑制）。"""

    def test_excluded_category_not_returned(self, client, seeded_db):
        """VIEW と INDEX を除外すると CONSTRAINT の問題だけが返る。"""
        # seeded_db: VIEW(q1), INDEX(q2), CONSTRAINT(q3) の3問
        response = client.get(
            "/api/questions/random"
            "?excluded_categories=VIEW&excluded_categories=INDEX"
        )
        assert response.status_code == 200
        assert response.json()["category"] == "CONSTRAINT"

    def test_single_excluded_category(self, client, seeded_db):
        """1カテゴリ除外で残りのカテゴリから返る。"""
        response = client.get("/api/questions/random?excluded_categories=VIEW")
        assert response.status_code == 200
        assert response.json()["category"] != "VIEW"

    def test_all_excluded_fallback(self, client, seeded_db):
        """全カテゴリ除外でもフォールバックして問題を返す（404 にならない）。"""
        response = client.get(
            "/api/questions/random"
            "?excluded_categories=VIEW&excluded_categories=INDEX&excluded_categories=CONSTRAINT"
        )
        assert response.status_code == 200
        assert "id" in response.json()

    def test_excluded_categories_empty_is_normal(self, client, seeded_db):
        """excluded_categories 省略は通常モードと同じ（後方互換）。"""
        response = client.get("/api/questions/random")
        assert response.status_code == 200
        assert "id" in response.json()
