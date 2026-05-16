"""POST /api/answers および DELETE /api/answers のAPIテスト。"""

import app.config
from app.models.user_answer import UserAnswer


class TestSubmitAnswer:

    # ---- 正常系 ----

    def test_single_correct(self, client, seeded_db):
        """単一選択・正解 → is_correct=True。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
        })
        assert response.status_code == 200
        assert response.json()["is_correct"] is True

    def test_single_incorrect(self, client, seeded_db):
        """単一選択・不正解 → is_correct=False。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_incorrect_choice_id"]],
        })
        assert response.status_code == 200
        assert response.json()["is_correct"] is False

    def test_multi_all_correct(self, client, seeded_db):
        """複数選択・完全一致 → is_correct=True。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q2_id"],
            "selected_choice_ids": seeded_db["q2_correct_choice_ids"],
        })
        assert response.status_code == 200
        assert response.json()["is_correct"] is True

    def test_multi_partial_correct(self, client, seeded_db):
        """複数選択・部分一致 → is_correct=False（部分点なし）。"""
        correct_ids = seeded_db["q2_correct_choice_ids"]
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q2_id"],
            "selected_choice_ids": [correct_ids[0], seeded_db["q2_incorrect_choice_id"]],
        })
        assert response.status_code == 200
        assert response.json()["is_correct"] is False

    def test_response_contains_explanation(self, client, seeded_db):
        """レスポンスに explanation と correct_choice_ids が含まれる。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
        })
        data = response.json()
        assert "explanation" in data
        assert "correct_choice_ids" in data
        assert "trap_reason" in data

    # ---- 異常系 ----

    def test_nonexistent_question_returns_404(self, client, seeded_db):
        """存在しない question_id → 404。"""
        response = client.post("/api/answers", json={
            "question_id": 99999,
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
        })
        assert response.status_code == 404

    def test_empty_choice_ids_returns_422(self, client, seeded_db):
        """空の selected_choice_ids → 422。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [],
        })
        assert response.status_code == 422

    def test_invalid_choice_id_returns_422(self, client, seeded_db):
        """問題に属さない choice_id → 422。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q2_choice_id_for_cross_question_test"]],
        })
        assert response.status_code == 422

    def test_duplicate_choice_ids_returns_422(self, client, seeded_db):
        """重複した choice_id を含む → 422（仕様確定事項 #1）。"""
        cid = seeded_db["q1_correct_choice_id"]
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [cid, cid],
        })
        assert response.status_code == 422

    def test_insufficient_reject_mode(self, client, seeded_db, monkeypatch):
        """INSUFFICIENT_SELECTION_MODE="reject": 「3つ選べ」で2つ選択 → 不正解として記録(200)。"""
        monkeypatch.setattr(app.config, "INSUFFICIENT_SELECTION_MODE", "reject")
        correct_ids = seeded_db["q3_correct_choice_ids"]
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q3_id"],
            "selected_choice_ids": correct_ids[:2],  # 3つ選べに対して2つだけ送る
        })
        assert response.status_code == 200
        assert response.json()["is_correct"] is False

    def test_insufficient_warn_mode_returns_422(self, client, seeded_db, monkeypatch):
        """INSUFFICIENT_SELECTION_MODE="warn": 「3つ選べ」で2つ選択 → 422。"""
        monkeypatch.setattr(app.config, "INSUFFICIENT_SELECTION_MODE", "warn")
        correct_ids = seeded_db["q3_correct_choice_ids"]
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q3_id"],
            "selected_choice_ids": correct_ids[:2],
        })
        assert response.status_code == 422

    def test_insufficient_warn_mode_no_record(self, client, db_session, seeded_db, monkeypatch):
        """INSUFFICIENT_SELECTION_MODE="warn": 422 時は user_answers に記録しない。"""
        monkeypatch.setattr(app.config, "INSUFFICIENT_SELECTION_MODE", "warn")
        correct_ids = seeded_db["q3_correct_choice_ids"]
        client.post("/api/answers", json={
            "question_id": seeded_db["q3_id"],
            "selected_choice_ids": correct_ids[:2],
        })
        # DB に記録されていないことを確認
        count = db_session.query(UserAnswer).count()
        assert count == 0


class TestResetAnswers:
    def test_delete_all_answers(self, client, seeded_db):
        """DELETE /api/answers: 回答履歴が全件削除される。"""
        # 先に回答を記録
        client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
        })
        # リセット
        response = client.delete("/api/answers")
        assert response.status_code == 200
        assert response.json()["deleted_count"] == 1


class TestUserName:
    """user_name フィールドのバリデーションと保存テスト。"""

    def test_whitespace_only_returns_422(self, client, seeded_db):
        """空白のみの user_name → 422。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
            "user_name": "   ",
        })
        assert response.status_code == 422

    def test_username_is_stripped(self, client, db_session, seeded_db):
        """前後の空白は strip されて保存される。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
            "user_name": "  alice  ",
        })
        assert response.status_code == 200
        saved = db_session.query(UserAnswer).order_by(UserAnswer.id.desc()).first()
        assert saved.user_name == "alice"

    def test_default_username_is_guest(self, client, db_session, seeded_db):
        """user_name 省略時は 'guest' として保存される（後方互換）。"""
        client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
        })
        saved = db_session.query(UserAnswer).order_by(UserAnswer.id.desc()).first()
        assert saved.user_name == "guest"

    def test_username_too_long_returns_422(self, client, seeded_db):
        """51文字以上の user_name → 422。"""
        response = client.post("/api/answers", json={
            "question_id": seeded_db["q1_id"],
            "selected_choice_ids": [seeded_db["q1_correct_choice_id"]],
            "user_name": "a" * 51,
        })
        assert response.status_code == 422
