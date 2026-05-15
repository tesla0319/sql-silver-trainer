"""
サンプル問題データ（sample_questions.py）の品質テスト。
DB 不要。Python リストを直接検証する。

SPEC 10.1 の要件:
  - 全10カテゴリ最低1問ずつ
  - うち複数選択5問以上（2つ選べ×3、3つ選べ×2）
  - うち長文問題3問以上（200文字超）
  - 各問題に explanation と trap_reason がある
"""

import pytest

from app.config import CATEGORIES
from app.seed.sample_questions import SAMPLE_QUESTIONS


class TestSeedCoverage:

    def test_total_question_count(self):
        """Phase 1e 目標: 15問以上。"""
        assert len(SAMPLE_QUESTIONS) >= 15, (
            f"問題数: {len(SAMPLE_QUESTIONS)} (最低15問必要)"
        )

    def test_all_categories_covered(self):
        """全10カテゴリが最低1問ずつカバーされている。"""
        covered = {q["category"] for q in SAMPLE_QUESTIONS}
        missing = set(CATEGORIES) - covered
        assert missing == set(), f"未カバーカテゴリ: {sorted(missing)}"

    def test_category_in_config(self):
        """全問題のカテゴリが config.CATEGORIES に含まれる（typo 検出）。"""
        invalid = {q["category"] for q in SAMPLE_QUESTIONS} - set(CATEGORIES)
        assert invalid == set(), f"未定義カテゴリ: {invalid}"

    def test_multi_select_count_gte_5(self):
        """複数選択問題が5問以上ある（SPEC 10.1）。"""
        multi = [q for q in SAMPLE_QUESTIONS if q["multi_select_count"] > 1]
        assert len(multi) >= 5, (
            f"複数選択問題数: {len(multi)} (最低5問必要)"
        )

    def test_two_select_count_gte_3(self):
        """「2つ選べ」問題が3問以上ある（SPEC 10.1）。"""
        two = [q for q in SAMPLE_QUESTIONS if q["multi_select_count"] == 2]
        assert len(two) >= 3, f"2つ選べ問題数: {len(two)} (最低3問必要)"

    def test_three_select_count_gte_2(self):
        """「3つ選べ」問題が2問以上ある（SPEC 10.1）。"""
        three = [q for q in SAMPLE_QUESTIONS if q["multi_select_count"] == 3]
        assert len(three) >= 2, f"3つ選べ問題数: {len(three)} (最低2問必要)"

    def test_long_questions_count(self):
        """長文問題（200文字超）が3問以上ある（SPEC 10.1）。"""
        long_qs = [q for q in SAMPLE_QUESTIONS if len(q["question_text"]) > 200]
        assert len(long_qs) >= 3, (
            f"長文問題数: {len(long_qs)} (最低3問必要)\n"
            f"現在の文字数: {[len(q['question_text']) for q in SAMPLE_QUESTIONS]}"
        )

    def test_all_questions_have_explanation(self):
        """全問題に explanation がある（空文字・None 不可）。"""
        missing = [
            f"Q{i} ({q['category']})"
            for i, q in enumerate(SAMPLE_QUESTIONS)
            if not q.get("explanation")
        ]
        assert missing == [], f"explanation がない問題: {missing}"

    def test_all_questions_have_trap_reason(self):
        """全問題に trap_reason がある（Ping-t 誤答パターン記述の品質要件）。"""
        no_trap = [
            f"Q{i} ({q['category']})"
            for i, q in enumerate(SAMPLE_QUESTIONS)
            if not q.get("trap_reason")
        ]
        assert no_trap == [], f"trap_reason がない問題: {no_trap}"

    def test_correct_choice_count_matches_multi_select_count(self):
        """正解数が multi_select_count と一致する（不整合検出）。"""
        errors = []
        for i, q in enumerate(SAMPLE_QUESTIONS):
            correct_count = sum(1 for c in q["choices"] if c["is_correct"])
            if correct_count != q["multi_select_count"]:
                errors.append(
                    f"Q{i} ({q['category']}): "
                    f"multi_select_count={q['multi_select_count']} "
                    f"vs 正解数={correct_count}"
                )
        assert errors == [], "\n".join(errors)

    def test_each_question_has_at_least_one_correct_choice(self):
        """各問題に正解が最低1つある。"""
        errors = [
            f"Q{i} ({q['category']})"
            for i, q in enumerate(SAMPLE_QUESTIONS)
            if not any(c["is_correct"] for c in q["choices"])
        ]
        assert errors == [], f"正解選択肢がない問題: {errors}"

    def test_display_order_unique_per_question(self):
        """各問題内で display_order が重複しない。"""
        errors = []
        for i, q in enumerate(SAMPLE_QUESTIONS):
            orders = [c["display_order"] for c in q["choices"]]
            if len(orders) != len(set(orders)):
                errors.append(f"Q{i} ({q['category']}): display_order 重複")
        assert errors == [], "\n".join(errors)

    def test_difficulty_range(self):
        """difficulty が 1〜3 の範囲内。"""
        errors = [
            f"Q{i} ({q['category']}): difficulty={q['difficulty']}"
            for i, q in enumerate(SAMPLE_QUESTIONS)
            if q["difficulty"] not in (1, 2, 3)
        ]
        assert errors == [], f"difficulty 範囲外: {errors}"
