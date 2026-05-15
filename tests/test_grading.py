"""services/grading.py の単体テスト。DB不要。"""

from app.services.grading import grade_answer


class TestGradeAnswerCorrectness:
    """集合比較ロジックの単体テスト。"""

    def test_single_correct(self):
        result = grade_answer(
            selected_ids=[1], correct_ids=[1], multi_select_count=1, mode="reject"
        )
        assert result.is_correct is True
        assert result.should_warn is False

    def test_single_incorrect(self):
        result = grade_answer(
            selected_ids=[2], correct_ids=[1], multi_select_count=1, mode="reject"
        )
        assert result.is_correct is False
        assert result.should_warn is False

    def test_multi_all_correct(self):
        result = grade_answer(
            selected_ids=[1, 2], correct_ids=[1, 2], multi_select_count=2, mode="reject"
        )
        assert result.is_correct is True

    def test_multi_all_correct_order_independent(self):
        """順序が逆でも正解（集合比較）。"""
        result = grade_answer(
            selected_ids=[2, 1], correct_ids=[1, 2], multi_select_count=2, mode="reject"
        )
        assert result.is_correct is True

    def test_multi_partial_correct(self):
        """部分一致は不正解（部分点なし）。"""
        result = grade_answer(
            selected_ids=[1, 3], correct_ids=[1, 2], multi_select_count=2, mode="reject"
        )
        assert result.is_correct is False

    def test_multi_all_wrong(self):
        result = grade_answer(
            selected_ids=[3, 4], correct_ids=[1, 2], multi_select_count=2, mode="reject"
        )
        assert result.is_correct is False

    def test_three_select_all_correct(self):
        result = grade_answer(
            selected_ids=[1, 2, 3], correct_ids=[1, 2, 3], multi_select_count=3, mode="reject"
        )
        assert result.is_correct is True

    def test_three_select_partial(self):
        result = grade_answer(
            selected_ids=[1, 2, 4], correct_ids=[1, 2, 3], multi_select_count=3, mode="reject"
        )
        assert result.is_correct is False


class TestGradeAnswerInsufficientSelection:
    """選択数不一致時の挙動テスト（モード切替）。"""

    def test_reject_mode_insufficient_count(self):
        """reject モード: 選択数不一致 → 不正解として記録（should_warn=False）。"""
        result = grade_answer(
            selected_ids=[1, 2], correct_ids=[1, 2, 3], multi_select_count=3, mode="reject"
        )
        assert result.is_correct is False
        assert result.should_warn is False

    def test_reject_mode_excess_count(self):
        """reject モード: 選択数超過 → 不正解として記録。"""
        result = grade_answer(
            selected_ids=[1, 2, 3, 4], correct_ids=[1, 2, 3], multi_select_count=3, mode="reject"
        )
        assert result.is_correct is False
        assert result.should_warn is False

    def test_warn_mode_insufficient_count(self):
        """warn モード: 選択数不一致 → should_warn=True（呼び出し元が 422 を返す）。"""
        result = grade_answer(
            selected_ids=[1, 2], correct_ids=[1, 2, 3], multi_select_count=3, mode="warn"
        )
        assert result.is_correct is False
        assert result.should_warn is True

    def test_warn_mode_correct_count(self):
        """warn モード: 選択数が一致している場合は通常の判定。"""
        result = grade_answer(
            selected_ids=[1, 2, 3], correct_ids=[1, 2, 3], multi_select_count=3, mode="warn"
        )
        assert result.is_correct is True
        assert result.should_warn is False
