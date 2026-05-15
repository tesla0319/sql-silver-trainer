# モデルをここでまとめてインポートし、Base のメタデータに全テーブルを登録する
# init_db.py や conftest.py でこのモジュールをインポートするだけで
# Base.metadata.create_all() が全テーブルを認識できる
from app.models.question import Question
from app.models.choice import Choice
from app.models.user_answer import UserAnswer

__all__ = ["Question", "Choice", "UserAnswer"]
