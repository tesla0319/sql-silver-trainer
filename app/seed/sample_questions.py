"""サンプル問題データ。

Phase 1a では動作確認用として5問を定義（VIEW, INDEX, CONSTRAINT, SUBQUERY, ORACLE_TERM）。
Phase 1e で全10カテゴリ・15問程度に拡充予定。

各エントリの構造:
  - category: config.CATEGORIES のいずれか
  - difficulty: 1〜3
  - question_text: 問題文
  - multi_select_count: 選ぶ数（1=単一選択、2=2つ選べ、3=3つ選べ）
  - explanation: 解説（信頼できる入力として innerHTML でレンダリングされる）
  - trap_reason: 間違えやすい理由（省略可）
  - choices: 選択肢リスト（display_order 昇順で表示）
"""

SAMPLE_QUESTIONS = [
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "次のVIEW定義のうち、DML操作（INSERT/UPDATE/DELETE）を実行できないものを1つ選んでください。\n\n"
            "A. CREATE VIEW v_emp AS SELECT * FROM employees;\n"
            "B. CREATE VIEW v_dept_count AS SELECT department_id, COUNT(*) AS cnt FROM employees GROUP BY department_id;\n"
            "C. CREATE VIEW v_sales AS SELECT * FROM employees WHERE department_id = 80;\n"
            "D. CREATE VIEW v_simple AS SELECT employee_id, first_name FROM employees WHERE salary > 5000;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "GROUP BY句を含むVIEWは更新不可です。B が該当します。\n\n"
            "更新不可となるVIEWの主な条件:\n"
            "・GROUP BY / HAVING 句を含む\n"
            "・DISTINCT を含む\n"
            "・集合演算子（UNION, INTERSECT, MINUS）を含む\n"
            "・ROWNUM 疑似列を含む\n"
            "・グループ関数（SUM, AVG, COUNT等）を含む\n\n"
            "A・C・Dはいずれも単一テーブルからの単純なSELECTであり、条件を満たせばDML操作が可能です。"
        ),
        "trap_reason": "「VIEWは更新できない」と一律に覚えてしまうパターン。シンプルなVIEWは更新可能。GROUP BYやDISTINCTが含まれる場合のみ更新不可になる。",
        "choices": [
            {"choice_text": "A（SELECT * FROM employees）", "is_correct": False, "display_order": 0},
            {"choice_text": "B（GROUP BY を含むビュー）", "is_correct": True, "display_order": 1},
            {"choice_text": "C（WHERE 句のみのビュー）", "is_correct": False, "display_order": 2},
            {"choice_text": "D（列を絞ったシンプルなビュー）", "is_correct": False, "display_order": 3},
        ],
    },
    {
        "category": "INDEX",
        "difficulty": 1,
        "question_text": "Oracleデータベースのインデックスに関する記述として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "PRIMARY KEY制約またはUNIQUE制約を定義すると、Oracleは自動的にインデックスを作成します。\n\n"
            "インデックスのトレードオフ:\n"
            "・SELECT の検索は高速化される\n"
            "・INSERT/UPDATE/DELETE 時はインデックスの更新も発生するため書き込みのオーバーヘッドが生じる\n"
            "・1つのテーブルに複数のインデックスを作成することは可能\n"
            "・インデックスを削除しても表データは削除されない（インデックスは独立したオブジェクト）"
        ),
        "trap_reason": "「インデックスを作ると全操作が速くなる」という誤解が多い。書き込み時はオーバーヘッドが発生する。また、PRIMARY KEY制約での自動作成を知らないケースも頻出。",
        "choices": [
            {"choice_text": "インデックスを作成すると INSERT/UPDATE/DELETE も必ず高速化される", "is_correct": False, "display_order": 0},
            {"choice_text": "PRIMARY KEY制約を定義すると、自動的にインデックスが作成される", "is_correct": True, "display_order": 1},
            {"choice_text": "1つのテーブルに作成できるインデックスは最大1つまでである", "is_correct": False, "display_order": 2},
            {"choice_text": "インデックスを削除すると、そのインデックスの元になった表データも削除される", "is_correct": False, "display_order": 3},
        ],
    },
    {
        "category": "CONSTRAINT",
        "difficulty": 1,
        "question_text": "Oracleデータベースの制約に関する記述として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "NOT NULL制約は列レベルでのみ定義可能です（表レベル制約としては定義できません）。\n\n"
            "各制約のポイント:\n"
            "・NOT NULL: 列レベルのみ。NULLを禁止する。\n"
            "・UNIQUE: NULL値は複数行に存在できる（NULLは「未知の値」として互いに等しくないとみなされる）。\n"
            "・PRIMARY KEY: 内部的に NOT NULL + UNIQUE の組み合わせ。NULL不可・重複不可。\n"
            "・FOREIGN KEY: 参照先に存在する値のみを許容する。"
        ),
        "trap_reason": "「UNIQUE制約はNULLを1行しか持てない」という誤解が非常に多い。NULLはUNIQUE制約のもとでも複数行に存在できる点が頻出ポイント。",
        "choices": [
            {"choice_text": "UNIQUE制約が設定された列には NULL 値を1行しか持てない", "is_correct": False, "display_order": 0},
            {"choice_text": "NOT NULL制約は列レベルでのみ定義でき、表レベルでは定義できない", "is_correct": True, "display_order": 1},
            {"choice_text": "PRIMARY KEY制約が設定された列には NULL 値を1行だけ持てる", "is_correct": False, "display_order": 2},
            {"choice_text": "FOREIGN KEY制約は参照先テーブルに存在しない値も格納できる", "is_correct": False, "display_order": 3},
        ],
    },
    {
        "category": "SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "次のSQL文のうち、サブクエリが含まれているものを2つ選んでください。\n\n"
            "A: SELECT * FROM employees WHERE salary = (SELECT MAX(salary) FROM employees)\n"
            "B: SELECT department_id, AVG(salary) FROM employees GROUP BY department_id\n"
            "C: INSERT INTO dept_backup SELECT * FROM departments\n"
            "D: SELECT e.* FROM employees e JOIN (SELECT department_id FROM departments WHERE location_id = 1700) d ON e.department_id = d.department_id"
        ),
        "multi_select_count": 2,
        "explanation": (
            "正解は A と D です。\n\n"
            "A: WHERE句のサブクエリ（スカラーサブクエリ）。MAX(salary)を返す内側のSELECTがサブクエリ。\n"
            "D: FROM句のサブクエリ（インラインビュー）。JOINの右辺にあるSELECTがサブクエリ。\n\n"
            "B: サブクエリなし。GROUP BY を使った集計クエリ。\n"
            "C: INSERT...SELECT 構文。SELECTがメインのSQL文の一部であり、サブクエリではない。"
        ),
        "trap_reason": "INSERT...SELECT のSELECT部分をサブクエリと混同しやすい。また、FROM句のインラインビューを見落とすケースが多い。",
        "choices": [
            {"choice_text": "A（WHERE句に MAX を使ったSELECT）", "is_correct": True, "display_order": 0},
            {"choice_text": "B（GROUP BY + AVG の集計クエリ）", "is_correct": False, "display_order": 1},
            {"choice_text": "C（INSERT...SELECT 構文）", "is_correct": False, "display_order": 2},
            {"choice_text": "D（FROM句にインラインビューを含むクエリ）", "is_correct": True, "display_order": 3},
        ],
    },
    {
        "category": "ORACLE_TERM",
        "difficulty": 1,
        "question_text": "Oracle Databaseにおける「スキーマ」の説明として最も適切なものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "Oracleにおけるスキーマとは、特定のデータベースユーザーが所有するオブジェクト（表・ビュー・索引・シーケンス等）の集合です。\n"
            "スキーマ名はユーザー名と同一になります。\n\n"
            "例: ユーザー HR が作成した表は HR.EMPLOYEES のようにスキーマ名を接頭辞として参照できます。\n\n"
            "混同しやすい用語:\n"
            "・表領域（テーブルスペース）: 物理的なデータ格納領域\n"
            "・インスタンス: メモリ（SGA）とバックグラウンドプロセスの組み合わせ\n"
            "・データベース: 物理ファイル（データファイル・制御ファイル・REDOログ）の集合"
        ),
        "trap_reason": "スキーマをデータベース全体と混同するパターンが頻出。Oracleではスキーマ＝ユーザーが所有するオブジェクトのコレクションであり、他のDBMS（MySQL等）とは意味が異なる点に注意。",
        "choices": [
            {"choice_text": "データベース全体の論理的な構造のこと", "is_correct": False, "display_order": 0},
            {"choice_text": "特定のユーザーが所有するデータベースオブジェクトの集合", "is_correct": True, "display_order": 1},
            {"choice_text": "表領域（テーブルスペース）と同義のもの", "is_correct": False, "display_order": 2},
            {"choice_text": "Oracleインスタンスのメモリ構造（SGA）のこと", "is_correct": False, "display_order": 3},
        ],
    },
]
