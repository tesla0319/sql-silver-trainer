"""判定ロジック。DB に依存しない純粋関数として実装し、単体テストを容易にする。

grade_answer() は mode パラメータを受け取るため、
呼び出し元（router）が config.INSUFFICIENT_SELECTION_MODE を渡す設計にしてある。
これにより、unit test では mode を直接指定でき、monkeypatch 不要で両モードをテストできる。
"""

from dataclasses import dataclass


@dataclass
class GradingResult:
    is_correct: bool
    # True の場合、呼び出し元は 422 を返し DB に記録しない（warn モード専用）
    should_warn: bool


def grade_answer(
    selected_ids: list[int],
    correct_ids: list[int],
    multi_select_count: int,
    mode: str,
) -> GradingResult:
    """選択肢の集合を比較して正誤を判定する。

    Args:
        selected_ids: ユーザーが選択した choice_id のリスト（重複・空は呼び出し元でバリデーション済み）
        correct_ids: 正解の choice_id のリスト
        multi_select_count: 問題が要求する選択数
        mode: "reject" または "warn"
            "reject": 選択数不一致でも不正解として記録（200）
            "warn"  : 選択数不一致なら should_warn=True を返す（呼び出し元が 422 を返す）

    Returns:
        GradingResult(is_correct, should_warn)
    """
    if len(selected_ids) != multi_select_count:
        if mode == "warn":
            return GradingResult(is_correct=False, should_warn=True)
        # "reject" モード: 選択数不一致は不正解として記録する
        return GradingResult(is_correct=False, should_warn=False)

    # 完全一致（集合比較: 順序不問）
    is_correct = set(selected_ids) == set(correct_ids)
    return GradingResult(is_correct=is_correct, should_warn=False)
