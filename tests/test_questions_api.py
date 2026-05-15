"""GET /api/questions/random のAPIテスト。"""


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
        """正常系: mode=weak で苦手未定義 → 通常モードにフォールバック（SPEC 6.2）。
        Phase 1b では weak モードのロジックが未実装のため、常に通常モードと同じ動作をする。
        """
        response = client.get("/api/questions/random?mode=weak")
        assert response.status_code == 200

    def test_choices_ordered_by_display_order(self, client, seeded_db):
        """選択肢が display_order 順に並んでいる。"""
        response = client.get("/api/questions/random")
        choices = response.json()["choices"]
        orders = [c["display_order"] for c in choices]
        assert orders == sorted(orders)
