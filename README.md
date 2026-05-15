# SQL Silver 学習支援アプリ

SQL Silver 試験の「ルール・制約・用語の理解」を強化するための学習支援 Web アプリ。

---

## セットアップ

```bash
cd sql-silver-app

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存ライブラリのインストール
pip install -r requirements.txt

# DB 作成 + サンプル問題投入
python -m app.seed.init_db
```

---

## 起動

```bash
uvicorn app.main:app --reload
```

ブラウザで http://localhost:8000 にアクセス。

ヘルスチェック: http://localhost:8000/health

---

## テスト実行

```bash
pytest
```

---

## 問題データの管理

問題データは `app/seed/sample_questions.py` の Python リストで管理します。

### 問題を追加する

1. `app/seed/sample_questions.py` に辞書を追記する
2. 既存 DB を削除して再初期化する

```bash
# Windows
del app.db
# Mac/Linux
rm app.db

python -m app.seed.init_db
```

> **注意**: `init_db` は問題が0件のときのみ投入します。
> 問題を追加した場合は `app.db` を削除して再実行してください。

### 誤解パターン分析（開発者向け）

ユーザーの誤答データを集計して trap_reason 改善のヒントを出力します。

```bash
python -m app.seed.analyze_misconceptions
```

出力例:
```
[VIEW] Q1: 次のVIEW定義のうち...
  回答数: 12 / 誤答率: 58%
  誤選択 5/12回 (42%): A（SELECT * FROM employees）
```

---

## API 一覧

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック |
| GET | `/api/questions/random` | ランダム問題取得 |
| POST | `/api/answers` | 回答送信・判定 |
| GET | `/api/stats/categories` | カテゴリ別正答率 |
| DELETE | `/api/answers` | 回答履歴リセット（テスト用） |

### GET `/api/questions/random` クエリパラメータ

| パラメータ | 値 | 説明 |
|---|---|---|
| `mode` | `normal`（デフォルト） | 全問題からランダム出題 |
| `mode` | `weak` | 苦手カテゴリ（正答率 < 50%、回答数 >= 3）から優先出題。苦手なし時は通常モードにフォールバック |
| `category` | カテゴリ名（省略可） | 指定カテゴリに絞って出題（mode=normal 時のみ有効） |

### GET `/api/stats/categories` レスポンス例

```json
{
  "stats": [
    {"category": "VIEW",  "answered_count": 10, "correct_count": 4, "accuracy": 0.4},
    {"category": "INDEX", "answered_count": 5,  "correct_count": 1, "accuracy": 0.2}
  ]
}
```

- `answered_count` が 0 のカテゴリは含まれない（未着手と区別するため）
- `accuracy` は 0.0〜1.0。フロント側で % 変換する

### 苦手判定の条件（`config.py` で変更可能）

| 設定値 | デフォルト | 説明 |
|---|---|---|
| `WEAK_THRESHOLD` | `0.5` | 正答率がこの値**未満**のカテゴリを苦手とみなす |
| `MIN_ANSWERS` | `3` | 苦手判定に必要な最低回答数（これ未満は判定対象外）|

---

## ディレクトリ構成

```
sql-silver-app/
├── app/
│   ├── main.py          # FastAPI エントリポイント
│   ├── config.py        # 設定値（閾値、カテゴリ定数等）
│   ├── database.py      # DB接続・セッション管理
│   ├── models/          # SQLAlchemy モデル（テーブル定義）
│   ├── schemas/         # Pydantic スキーマ（リクエスト/レスポンス）
│   ├── crud/            # DB操作層（SELECT/INSERT等）
│   ├── routers/         # API エンドポイント定義
│   ├── services/        # ビジネスロジック（判定・苦手分析）
│   └── seed/            # DB初期化・サンプルデータ
├── static/              # フロントエンド（HTML/CSS/JS）
├── tests/               # pytest テスト
├── requirements.txt
└── pytest.ini
```

### 設計の意図

- **routers / services / crud / models / schemas を分離**: 各層を独立してテストできるようにするため
- **services 層**: 判定ロジックや苦手分析を crud から切り離し、DB に依存しない単体テストを書けるようにするため
- **seed をモジュール化**: 問題追加時に `sample_questions.py` だけ編集すればよい構造
