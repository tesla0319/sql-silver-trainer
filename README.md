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

## API 一覧

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック |
| GET | `/api/questions/random` | ランダム問題取得 |
| POST | `/api/answers` | 回答送信・判定 |
| GET | `/api/stats/categories` | カテゴリ別正答率 |
| DELETE | `/api/answers` | 回答履歴リセット（テスト用） |

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
