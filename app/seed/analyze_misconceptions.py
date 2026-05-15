"""
誤解パターン分析 CLI ツール。

使用方法:
    python -m app.seed.analyze_misconceptions

DB の user_answers テーブルを集計し、各問題で最もよく誤選択された
選択肢と誤答率をコンソールに出力する。
開発者が trap_reason の内容改善に活用することを目的とする。

出力例:
    [VIEW] Q1: 次のVIEW定義のうち...
      回答数: 12 / 誤答率: 58%
      誤選択 5/12回 (42%): A（SELECT * FROM employees）
      誤選択 2/12回 (17%): C（WHERE 句のみのビュー）
"""

import json

from app.database import SessionLocal
from app.models.choice import Choice
from app.models.question import Question
from app.models.user_answer import UserAnswer


def _build_choice_map(question: Question) -> dict[int, str]:
    """choice_id → choice_text の辞書を返す。"""
    return {c.id: c.choice_text for c in question.choices}


def _build_correct_ids(question: Question) -> set[int]:
    """正解の choice_id セットを返す。"""
    return {c.id for c in question.choices if c.is_correct}


def analyze(db) -> None:
    total_answers = db.query(UserAnswer).count()
    if total_answers == 0:
        print("回答データがありません。問題を解いてから実行してください。")
        return

    questions = db.query(Question).order_by(Question.category, Question.id).all()
    has_output = False

    for q in questions:
        answers = db.query(UserAnswer).filter(UserAnswer.question_id == q.id).all()
        if not answers:
            continue

        correct_ids = _build_correct_ids(q)
        choice_map  = _build_choice_map(q)
        total       = len(answers)
        wrong_count = sum(1 for a in answers if not a.is_correct)

        # 誤選択カウント: 各回答の selected_choices JSON をパースして集計
        wrong_choice_counts: dict[int, int] = {}
        for answer in answers:
            try:
                selected = json.loads(answer.selected_choices)
            except (json.JSONDecodeError, TypeError):
                continue
            for cid in selected:
                if cid not in correct_ids:
                    wrong_choice_counts[cid] = wrong_choice_counts.get(cid, 0) + 1

        if not wrong_choice_counts:
            continue

        has_output = True
        preview = q.question_text[:50].replace("\n", " ")
        print(f"[{q.category}] Q{q.id}: {preview}...")
        print(f"  回答数: {total} / 誤答率: {wrong_count / total:.0%}")

        # 誤選択が多い順に表示
        for cid, count in sorted(wrong_choice_counts.items(), key=lambda x: -x[1]):
            text = choice_map.get(cid, f"(choice_id={cid})")
            short_text = text[:60] + ("..." if len(text) > 60 else "")
            print(f"  誤選択 {count}/{total}回 ({count / total:.0%}): {short_text}")
        print()

    if not has_output:
        print("誤答データがありません（全問正解中）。")

    print(f"=== 集計完了 (総回答数: {total_answers}) ===")


def main() -> None:
    db = SessionLocal()
    try:
        analyze(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
