# アプリケーション全体の設定値を一元管理する
# 閾値変更時はここだけ編集すればよい

DATABASE_URL = "sqlite:///./app.db"

# カテゴリ一覧: typo防止のため定数として管理し、seedとAPIでこの値を参照する
CATEGORIES = [
    "VIEW",
    "INDEX",
    "MERGE",
    "INTERSECT",
    "SUBQUERY",
    "CONSTRAINT",
    "DICTIONARY_VIEW",
    "FUNCTION_NEST",
    "ORACLE_TERM",
    "DB_THEORY",
    "JOIN",
]

# 苦手判定の正答率閾値: この値未満かつ MIN_ANSWERS 以上回答したカテゴリを苦手とみなす
WEAK_THRESHOLD = 0.5

# 苦手判定に必要な最低回答数: 回答数が少ないと正答率が安定しないため下限を設ける
MIN_ANSWERS = 3

# 選択数不一致時の挙動:
#   "reject": 不正解として記録（MVPデフォルト、本番試験耐性を鍛える）
#   "warn"  : 422 を返し記録しない（Phase2 想定、学習初期の再選択促し）
INSUFFICIENT_SELECTION_MODE = "reject"
