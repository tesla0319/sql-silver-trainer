"""苦手分析ロジック。DB に依存しない純粋関数として実装する。

grade_answer() と同様に、呼び出し元がパラメータを渡す設計にすることで
単体テストで閾値を自由に変えてテストできる。
"""

from dataclasses import dataclass


@dataclass
class CategoryStat:
    """カテゴリ別統計。crud 層の Row をこの型に変換してから service に渡す。"""

    category: str
    answered_count: int
    correct_count: int
    accuracy: float  # correct_count / answered_count。answered_count=0 の場合は 0.0


def compute_accuracy(answered_count: int, correct_count: int) -> float:
    """正答率を計算する。ゼロ除算を防ぐために answered_count が 0 の場合は 0.0 を返す。"""
    if answered_count == 0:
        return 0.0
    return correct_count / answered_count


def get_weak_categories(
    stats: list[CategoryStat],
    weak_threshold: float,
    min_answers: int,
) -> list[str]:
    """苦手カテゴリの名前リストを返す。

    苦手の条件（AND 条件）:
    - answered_count >= min_answers（回答数が少ないと正答率が安定しないため下限を設ける）
    - accuracy < weak_threshold（閾値「未満」= 閾値ちょうどは苦手ではない）

    Args:
        stats: カテゴリ別統計リスト
        weak_threshold: 苦手判定の正答率閾値（デフォルト 0.5）
        min_answers: 苦手判定に必要な最低回答数（デフォルト 3）

    Returns:
        苦手カテゴリ名のリスト（空リストなら苦手なし）
    """
    return [
        s.category
        for s in stats
        if s.answered_count >= min_answers and s.accuracy < weak_threshold
    ]
