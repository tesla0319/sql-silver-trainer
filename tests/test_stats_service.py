"""services/stats.py の単体テスト。DB 不要。"""

from app.services.stats import CategoryStat, compute_accuracy, get_weak_categories


class TestComputeAccuracy:
    def test_normal(self):
        assert compute_accuracy(10, 4) == 0.4

    def test_all_correct(self):
        assert compute_accuracy(10, 10) == 1.0

    def test_all_wrong(self):
        assert compute_accuracy(10, 0) == 0.0

    def test_zero_answered(self):
        """ゼロ除算を防ぐ。"""
        assert compute_accuracy(0, 0) == 0.0


class TestGetWeakCategories:
    """SPEC 8.2: 苦手判定の閾値境界テスト。"""

    def test_accuracy_49_is_weak(self):
        """正答率 49% → 苦手（WEAK_THRESHOLD=0.5 未満）。"""
        stats = [CategoryStat("VIEW", 100, 49, 49 / 100)]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert "VIEW" in result

    def test_accuracy_50_is_not_weak(self):
        """正答率 50% → 苦手ではない（「未満」なので 50% ちょうどは対象外）。"""
        stats = [CategoryStat("VIEW", 100, 50, 50 / 100)]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert "VIEW" not in result

    def test_min_answers_not_reached_2(self):
        """回答数 2件（MIN_ANSWERS=3）→ 苦手判定対象外。"""
        stats = [CategoryStat("VIEW", 2, 0, 0.0)]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert "VIEW" not in result

    def test_zero_answers_excluded(self):
        """回答数 0件 → 苦手判定対象外。"""
        stats = [CategoryStat("VIEW", 0, 0, 0.0)]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert "VIEW" not in result

    def test_exactly_min_answers_is_included(self):
        """回答数がちょうど MIN_ANSWERS（=3）の場合は判定対象に含む。"""
        stats = [CategoryStat("VIEW", 3, 0, 0.0)]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert "VIEW" in result

    def test_multiple_weak_categories(self):
        """複数の苦手カテゴリが正しく抽出される。"""
        stats = [
            CategoryStat("VIEW",     5, 1, 1 / 5),   # 20% → 苦手
            CategoryStat("INDEX",    5, 4, 4 / 5),   # 80% → 苦手ではない
            CategoryStat("SUBQUERY", 4, 0, 0.0),     # 0%  → 苦手
        ]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert "VIEW" in result
        assert "INDEX" not in result
        assert "SUBQUERY" in result

    def test_no_weak_categories(self):
        """苦手カテゴリが存在しない場合は空リストを返す。"""
        stats = [CategoryStat("VIEW", 10, 8, 0.8)]
        result = get_weak_categories(stats, weak_threshold=0.5, min_answers=3)
        assert result == []

    def test_empty_stats(self):
        """統計が空の場合は空リストを返す。"""
        result = get_weak_categories([], weak_threshold=0.5, min_answers=3)
        assert result == []
