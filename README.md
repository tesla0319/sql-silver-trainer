# SQL Silver 学習支援アプリ

SQL Silver 試験の「ルール・制約・用語の理解」を強化するための学習支援 Web アプリ。

- **10問1セット**のチャレンジ形式で学習リズムを作る
- **normal / weak / review** の3モードで学習スタイルを切り替え
- **ニックネーム別**に苦手分析を管理（複数ユーザー対応）
- **正答率連動の背景テーマ**（normal training モードのみ）

> 詳細仕様は `SPEC_rev4.md` を参照してください。

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

現在 **92 テスト** が定義されています。

---

## 主な機能

| 機能 | 説明 |
|---|---|
| **10問セッション** | 10問回答後に正答率・苦手カテゴリ上位3件を表示。リトライ or 終了を選択 |
| **通常モード** | 全カテゴリからランダム出題。同カテゴリ最大2問・3連続禁止の分散制御あり |
| **苦手克服モード** | 正答率 50% 未満かつ 3問以上回答済みのカテゴリを優先出題 |
| **復習モード** | 直近の回答が不正解だった問題を優先出題 |
| **苦手分析** | カテゴリ別正答率・プログレスバーを表示 |
| **ニックネーム対応** | localStorage で保存。苦手分析・weak/review はユーザー別に管理 |
| **背景テーマ** | normal training モードのセッション正答率に連動（40% 未満: dark、70% 以上: normal） |

---

## API 一覧

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック |
| GET | `/api/questions/random` | ランダム問題取得 |
| POST | `/api/answers` | 回答送信・正誤判定・履歴記録 |
| GET | `/api/stats/categories` | カテゴリ別正答率取得 |
| DELETE | `/api/answers` | 回答履歴リセット（テスト用） |

### GET `/api/questions/random` クエリパラメータ

| パラメータ | デフォルト | 説明 |
|---|---|---|
| `mode` | `normal` | `normal` / `weak` / `review` |
| `user_name` | `guest` | ニックネーム（苦手・復習判定に使用） |
| `exclude_ids` | `[]` | 除外する question_id（重複出題防止） |
| `excluded_categories` | `[]` | 除外するカテゴリ（normal モードの偏り抑制用） |
| `category` | なし | カテゴリ絞り込み（normal モードのみ有効） |

### POST `/api/answers` リクエスト Body

```json
{
  "question_id": 1,
  "selected_choice_ids": [3, 5],
  "user_name": "alice"
}
```

### GET `/api/stats/categories` クエリパラメータ

| パラメータ | デフォルト | 説明 |
|---|---|---|
| `user_name` | `guest` | ニックネーム（ユーザー別に集計） |

レスポンス例:

```json
{
  "stats": [
    {"category": "VIEW",     "answered_count": 10, "correct_count": 4, "accuracy": 0.4},
    {"category": "INTERVAL", "answered_count": 5,  "correct_count": 1, "accuracy": 0.2}
  ]
}
```

- `answered_count` が 0 のカテゴリは含まれない（未着手と区別するため）
- `accuracy` は 0.0〜1.0。フロント側で % 変換する

### 苦手判定の閾値（`config.py` で変更可能）

| 設定値 | デフォルト | 説明 |
|---|---|---|
| `WEAK_THRESHOLD` | `0.5` | 正答率がこの値**未満**のカテゴリを苦手とみなす |
| `MIN_ANSWERS` | `3` | 苦手判定に必要な最低回答数 |

---

## 問題データ管理

問題データは `app/seed/sample_questions.py` の Python リストで管理します。
現在 **125問 / 13カテゴリ**。

### カテゴリ一覧

`VIEW` / `INDEX` / `MERGE` / `INTERSECT` / `SUBQUERY` / `CONSTRAINT` /
`FUNCTION_NEST` / `ORACLE_TERM` / `JOIN` / `CORRELATED_SUBQUERY` /
`DATA_DICTIONARY` / `INTERVAL` / `RDB_THEORY`

### 問題を追加する

1. `app/seed/sample_questions.py` に辞書を追記する
2. 既存 DB を削除して再初期化する

```bash
# Mac/Linux
rm app.db
# Windows
del app.db

python -m app.seed.init_db
```

> **注意**: `init_db` は問題が 0 件のときのみ投入します。
> 問題を追加した場合は `app.db` を削除して再実行してください。

### 誤解パターン分析（開発者向け）

ユーザーの誤答データを集計して `trap_reason` 改善のヒントを出力します。

```bash
python -m app.seed.analyze_misconceptions
```

---

## ディレクトリ構成

```
sql-silver-app/
├── app/
│   ├── main.py               # FastAPI エントリポイント
│   ├── config.py             # 設定値（カテゴリ定数・閾値等）
│   ├── database.py           # DB 接続・セッション管理
│   ├── models/               # SQLAlchemy モデル
│   ├── schemas/              # Pydantic スキーマ
│   ├── crud/                 # DB 操作層
│   ├── routers/              # API エンドポイント
│   ├── services/             # ビジネスロジック（判定・苦手分析）
│   └── seed/                 # DB 初期化・問題データ
├── static/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   └── images/               # 背景画像（background-normal.png / background-dark.png）
├── tests/
│   ├── conftest.py
│   ├── test_questions_api.py
│   ├── test_answers_api.py
│   ├── test_stats_api.py
│   ├── test_grading.py
│   ├── test_stats_service.py
│   ├── test_seed_coverage.py
│   └── test_config.py        # カテゴリ整合性の再発防止テスト
├── requirements.txt
└── pytest.ini
```

---

## Render へのデプロイ

本アプリは [Render](https://render.com) で公開可能な構成です。

- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt && python -m app.seed.init_db`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **DB**: SQLite ファイル（`app.db`）はデプロイのたびに再生成されます

> 回答履歴の永続化が必要な場合は PostgreSQL への移行を検討してください。
