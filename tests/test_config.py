"""
config.py の整合性テスト。

カテゴリ整理(統合・追加・削除)の作業ミスを機械的に検出する。
rev.4 のカテゴリ整理で追加された再発防止テスト。
"""

from app.config import CATEGORIES

# rev.4 で廃止されたカテゴリ
DEPRECATED_CATEGORIES = {"DICTIONARY_VIEW", "DB_THEORY"}


def test_no_deprecated_categories():
    """廃止されたカテゴリが config.CATEGORIES に残っていないこと。"""
    leftover = DEPRECATED_CATEGORIES & set(CATEGORIES)
    assert not leftover, f"廃止カテゴリが残存しています: {leftover}"


def test_categories_unique():
    """CATEGORIES に重複がないこと。"""
    assert len(CATEGORIES) == len(set(CATEGORIES)), \
        f"CATEGORIES に重複があります: {CATEGORIES}"


def test_sample_questions_use_valid_categories():
    """全サンプル問題のカテゴリが config.CATEGORIES に含まれること。"""
    from app.seed.sample_questions import SAMPLE_QUESTIONS

    invalid = [
        q for q in SAMPLE_QUESTIONS
        if q["category"] not in CATEGORIES
    ]
    assert not invalid, (
        f"未定義カテゴリを使う問題があります: "
        f"{[(q.get('id', '?'), q['category']) for q in invalid]}"
    )
