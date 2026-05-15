"""サンプル問題データ。

Phase 3 で全10カテゴリ・15問に拡充。
SPEC 10.1 の要件:
  - 全10カテゴリ最低1問
  - 複数選択5問以上（2つ選べ×3以上、3つ選べ×2以上）
  - 長文問題3問以上（200文字超）
  - 全問題に explanation と trap_reason を記述

内容の正確性はユーザー側で最終レビューすること（SPEC 10.2）。
"""

SAMPLE_QUESTIONS = [

    # ──────────────────────────────────────────────────────────────────
    # 1. VIEW（単一選択・難易度2・長文）
    # ──────────────────────────────────────────────────────────────────
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
            {"choice_text": "A（SELECT * FROM employees）",  "is_correct": False, "display_order": 0},
            {"choice_text": "B（GROUP BY を含むビュー）",     "is_correct": True,  "display_order": 1},
            {"choice_text": "C（WHERE 句のみのビュー）",      "is_correct": False, "display_order": 2},
            {"choice_text": "D（列を絞ったシンプルなビュー）", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 2. INDEX（単一選択・難易度1）
    # ──────────────────────────────────────────────────────────────────
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
            {"choice_text": "インデックスを作成すると INSERT/UPDATE/DELETE も必ず高速化される",      "is_correct": False, "display_order": 0},
            {"choice_text": "PRIMARY KEY制約を定義すると、自動的にインデックスが作成される",         "is_correct": True,  "display_order": 1},
            {"choice_text": "1つのテーブルに作成できるインデックスは最大1つまでである",              "is_correct": False, "display_order": 2},
            {"choice_text": "インデックスを削除すると、そのインデックスの元になった表データも削除される", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 3. CONSTRAINT（単一選択・難易度1）
    # ──────────────────────────────────────────────────────────────────
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
            {"choice_text": "UNIQUE制約が設定された列には NULL 値を1行しか持てない",        "is_correct": False, "display_order": 0},
            {"choice_text": "NOT NULL制約は列レベルでのみ定義でき、表レベルでは定義できない", "is_correct": True,  "display_order": 1},
            {"choice_text": "PRIMARY KEY制約が設定された列には NULL 値を1行だけ持てる",      "is_correct": False, "display_order": 2},
            {"choice_text": "FOREIGN KEY制約は参照先テーブルに存在しない値も格納できる",     "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 4. SUBQUERY（2つ選べ・難易度2・長文）
    # ──────────────────────────────────────────────────────────────────
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
            {"choice_text": "A（WHERE句に MAX を使ったSELECT）",      "is_correct": True,  "display_order": 0},
            {"choice_text": "B（GROUP BY + AVG の集計クエリ）",        "is_correct": False, "display_order": 1},
            {"choice_text": "C（INSERT...SELECT 構文）",               "is_correct": False, "display_order": 2},
            {"choice_text": "D（FROM句にインラインビューを含むクエリ）", "is_correct": True,  "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 5. ORACLE_TERM（単一選択・難易度1）
    # ──────────────────────────────────────────────────────────────────
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
            {"choice_text": "データベース全体の論理的な構造のこと",                          "is_correct": False, "display_order": 0},
            {"choice_text": "特定のユーザーが所有するデータベースオブジェクトの集合",        "is_correct": True,  "display_order": 1},
            {"choice_text": "表領域（テーブルスペース）と同義のもの",                        "is_correct": False, "display_order": 2},
            {"choice_text": "Oracleインスタンスのメモリ構造（SGA）のこと",                  "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 6. MERGE（単一選択・難易度2）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "MERGE",
        "difficulty": 2,
        "question_text": (
            "以下のMERGE文に関する説明として正しいものを1つ選んでください。\n\n"
            "MERGE INTO target t\n"
            "USING source s ON (t.id = s.id)\n"
            "WHEN MATCHED     THEN UPDATE SET t.name = s.name\n"
            "WHEN NOT MATCHED THEN INSERT (id, name) VALUES (s.id, s.name);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "MERGE文は、条件に一致する行と一致しない行に対して別々のDML操作を実行します。\n\n"
            "・WHEN MATCHED: ターゲットに ON 条件で一致する行が存在する → UPDATE を実行\n"
            "・WHEN NOT MATCHED: ターゲットに一致する行が存在しない → INSERT を実行\n\n"
            "どちらの句も省略可能です（片方だけでも動作します）。\n"
            "MERGEは1文でUPSERT（UPDATE + INSERT）を実現できる点が特徴です。"
        ),
        "trap_reason": "WHEN MATCHEDの主語を「ソース側に一致があるか」と誤解しやすい。正しくは「ターゲット側に一致する行があるか」で判断する。また、WHEN MATCHED句でDELETEも記述可能な点が試験に出やすい。",
        "choices": [
            {"choice_text": "WHEN MATCHED句は、ソーステーブルに一致する行がある場合にINSERTを実行する",       "is_correct": False, "display_order": 0},
            {"choice_text": "WHEN NOT MATCHED句は、ターゲットに一致する行がない場合にINSERTを実行する",    "is_correct": True,  "display_order": 1},
            {"choice_text": "MERGE文ではWHEN MATCHEDとWHEN NOT MATCHEDの両方を必ず記述しなければならない", "is_correct": False, "display_order": 2},
            {"choice_text": "WHEN MATCHED句でDELETEを実行することはできない",                              "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 7. INTERSECT（単一選択・難易度1）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 1,
        "question_text": "Oracle SQL の集合演算子に関する説明として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "INTERSECT（積集合）は、2つのSELECT文の結果から共通する行のみを返します。\n\n"
            "集合演算子の基本:\n"
            "・UNION:     両方の結果を合わせ、重複を除去する\n"
            "・UNION ALL: 両方の結果を合わせ、重複を除去しない\n"
            "・INTERSECT: 共通する行のみ（重複除去あり）\n"
            "・MINUS:     1つ目の結果から2つ目に含まれる行を除いたもの\n\n"
            "INTERSECT・UNION・MINUSはいずれも重複行を自動的に除去します。"
        ),
        "trap_reason": "「INTERSECTは重複を除去しない」と思い込むパターン。重複を除去しないのはUNION ALLのみ。INTERSECT・UNION・MINUSはすべて重複除去が行われる。",
        "choices": [
            {"choice_text": "INTERSECTは2つのSELECTの結果をすべて合わせて返す",                        "is_correct": False, "display_order": 0},
            {"choice_text": "INTERSECTは2つのSELECTの共通する行を返す（重複行は除去される）",           "is_correct": True,  "display_order": 1},
            {"choice_text": "INTERSECTは2つのSELECTの共通する行を返すが、重複行はすべて残る",           "is_correct": False, "display_order": 2},
            {"choice_text": "INTERSECTはWHERE句の条件と同じ動作をするため、JOINで代替できない",         "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 8. DICTIONARY_VIEW（単一選択・難易度2）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DICTIONARY_VIEW",
        "difficulty": 2,
        "question_text": "Oracleのデータディクショナリビューのプレフィックスとアクセス範囲の組み合わせとして正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "Oracleのデータディクショナリビューには3種類のプレフィックスがあります。\n\n"
            "・USER_: 現在のユーザーが所有するオブジェクトのみ表示\n"
            "・ALL_:  現在のユーザーがアクセス権を持つすべてのオブジェクトを表示\n"
            "・DBA_:  データベース内のすべてのオブジェクトを表示（DBA権限が必要）\n\n"
            "使用例:\n"
            "・SELECT table_name FROM USER_TABLES; → 自分のテーブル一覧\n"
            "・SELECT table_name FROM ALL_TABLES;  → アクセス可能な全テーブル\n"
            "・SELECT table_name FROM DBA_TABLES;  → DB全体のテーブル（DBA権限必要）"
        ),
        "trap_reason": "USER_（所有者基準）とALL_（アクセス権基準）の区別を逆に覚えるパターンが頻出。また、DBA_は特権が必要な点を見落としやすい。",
        "choices": [
            {"choice_text": "USER_: アクセス権のある全オブジェクト / ALL_: 自分が所有するオブジェクトのみ", "is_correct": False, "display_order": 0},
            {"choice_text": "USER_: 自分が所有するオブジェクトのみ / ALL_: アクセス権のある全オブジェクト", "is_correct": True,  "display_order": 1},
            {"choice_text": "ALL_: データベース全体 / DBA_: アクセス権のある全オブジェクト",               "is_correct": False, "display_order": 2},
            {"choice_text": "DBA_は一般ユーザーでもアクセス可能な全オブジェクトを表示する",               "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 9. FUNCTION_NEST（単一選択・難易度1）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "FUNCTION_NEST",
        "difficulty": 1,
        "question_text": (
            "次のSQL文を実行したとき、commission_pct が NULL である行に対して返される値を1つ選んでください。\n\n"
            "SELECT NVL(commission_pct, 0) FROM employees;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "NVL(expr1, expr2) は、expr1 が NULL の場合に expr2 を返し、NULL でない場合は expr1 をそのまま返します。\n\n"
            "この例では:\n"
            "・commission_pct が NULL     → 0 を返す\n"
            "・commission_pct が 0.1 の場合 → 0.1 をそのまま返す\n\n"
            "NVL は NULL を別の値に置き換えたい場合に最もよく使われる関数です。\n"
            "引数順: NVL(NULL判定対象, NULLの場合に返す値)"
        ),
        "trap_reason": "NVL(A, B)の引数順序を逆に覚えてしまうパターン。「NULLの場合にBを返す」という順序で覚えること。NVL2との引数順の違いにも注意が必要。",
        "choices": [
            {"choice_text": "NULL",                             "is_correct": False, "display_order": 0},
            {"choice_text": "0",                               "is_correct": True,  "display_order": 1},
            {"choice_text": "commission_pct 列のデフォルト値",  "is_correct": False, "display_order": 2},
            {"choice_text": "エラーが発生する",                 "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 10. DB_THEORY（単一選択・難易度1）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DB_THEORY",
        "difficulty": 1,
        "question_text": "トランザクションのACID特性のうち、「一度コミットされたトランザクションの結果は、障害が発生しても失われない」という特性はどれですか？",
        "multi_select_count": 1,
        "explanation": (
            "ACID特性とは:\n\n"
            "・A（Atomicity: 原子性）:   トランザクション内の操作はすべて成功するか、すべて取り消されるか\n"
            "・C（Consistency: 一貫性）: トランザクション前後でデータの整合性が保たれる\n"
            "・I（Isolation: 独立性）:   複数のトランザクションは互いに干渉しない\n"
            "・D（Durability: 永続性）:  コミット済みの変更は障害後も失われない\n\n"
            "「一度コミットされた結果が失われない」は Durability（永続性）の説明です。"
        ),
        "trap_reason": "AtomicityとDurabilityが混同されやすい。Atomicityは「全部か無か（中途半端な状態を残さない）」、Durabilityは「コミット後の永続化保証」という違いを押さえること。",
        "choices": [
            {"choice_text": "Atomicity（原子性）",    "is_correct": False, "display_order": 0},
            {"choice_text": "Consistency（一貫性）",  "is_correct": False, "display_order": 1},
            {"choice_text": "Isolation（独立性）",    "is_correct": False, "display_order": 2},
            {"choice_text": "Durability（永続性）",   "is_correct": True,  "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 11. INTERSECT（2つ選べ・難易度2・長文）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": (
            "次のテーブルと問い合わせ結果に関する説明として正しいものを2つ選んでください。\n\n"
            "テーブルA の dept_id 列の値: 10, 20, 20, 30\n"
            "テーブルB の dept_id 列の値: 20, 30, 40\n\n"
            "問い合わせ1: SELECT dept_id FROM A  UNION      SELECT dept_id FROM B\n"
            "問い合わせ2: SELECT dept_id FROM A  INTERSECT  SELECT dept_id FROM B\n"
            "問い合わせ3: SELECT dept_id FROM A  MINUS      SELECT dept_id FROM B\n"
            "問い合わせ4: SELECT dept_id FROM A  UNION ALL  SELECT dept_id FROM B"
        ),
        "multi_select_count": 2,
        "explanation": (
            "各問い合わせの結果:\n\n"
            "問い合わせ1 UNION     → {10, 20, 30, 40} の4行（重複除去）\n"
            "問い合わせ2 INTERSECT → {20, 30} の2行（共通部分のみ、重複除去）\n"
            "問い合わせ3 MINUS     → {10} の1行（Aにあり、Bにない行、重複除去）\n"
            "問い合わせ4 UNION ALL → A(4行) + B(3行) = 7行（重複保持）\n\n"
            "【選択肢の正誤】\n"
            "・問い合わせ2の結果が {20, 30} の2行 → 正\n"
            "・問い合わせ4の結果が7行 → 正\n"
            "・問い合わせ1の結果は4行（{10,20,30,40}）であり3行ではない → 誤\n"
            "・問い合わせ3の結果は {10} の1行のみ → 誤"
        ),
        "trap_reason": "UNION ALLの行数はそれぞれのSELECT結果の合計行数になる点を忘れがち。またMINUSはAとBの差集合だが、A側の重複も除去される（AのMINUS結果は {10}、{10,20,20}ではない）。",
        "choices": [
            {"choice_text": "問い合わせ1（UNION）の結果は3行である",          "is_correct": False, "display_order": 0},
            {"choice_text": "問い合わせ2（INTERSECT）の結果は {20, 30} の2行", "is_correct": True,  "display_order": 1},
            {"choice_text": "問い合わせ3（MINUS）の結果は {10, 20} の2行",     "is_correct": False, "display_order": 2},
            {"choice_text": "問い合わせ4（UNION ALL）の結果は7行である",       "is_correct": True,  "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 12. VIEW（2つ選べ・難易度2）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "次のVIEW定義に WITH CHECK OPTION を付けた場合の動作として正しいものを2つ選んでください。\n\n"
            "CREATE VIEW v_high_sal AS\n"
            "  SELECT * FROM employees WHERE salary > 5000\n"
            "WITH CHECK OPTION;"
        ),
        "multi_select_count": 2,
        "explanation": (
            "WITH CHECK OPTION は、ビューを通じてDML操作を行う際に、ビューの WHERE 条件を満たさなくなる変更を禁止する制約です。\n\n"
            "このビュー（salary > 5000 が条件）での動作:\n"
            "・salary = 6000 の行をINSERT → 許可（WHERE条件を満たす）\n"
            "・salary = 4000 の行をINSERT → エラー（WHERE条件を満たさない）\n"
            "・既存行の salary を 3000 に UPDATE → エラー（更新後にWHERE条件を満たさなくなる）\n"
            "・WHERE条件を満たす行をDELETE → 許可\n\n"
            "WITH CHECK OPTION がない場合は条件を満たさない行もINSERT/UPDATEできてしまい、ビューから見えなくなる問題が生じます。"
        ),
        "trap_reason": "WITH CHECK OPTIONがない場合は salary=4000 の行をINSERTしても成功する（ただしビューからは見えなくなる）。この「見えないINSERT」を防ぐのがWITH CHECK OPTIONの目的だと理解すると覚えやすい。DELETEは許可される点も見落としやすい。",
        "choices": [
            {"choice_text": "salary = 4000 の行をINSERTしようとするとエラーになる",        "is_correct": True,  "display_order": 0},
            {"choice_text": "salary = 6000 の行をINSERTしようとするとエラーになる",        "is_correct": False, "display_order": 1},
            {"choice_text": "既存行の salary を 3000 に UPDATEしようとするとエラーになる", "is_correct": True,  "display_order": 2},
            {"choice_text": "WITH CHECK OPTIONがあるビューに対してDELETEは実行できない",   "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 13. CONSTRAINT（3つ選べ・難易度3・長文）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 3,
        "question_text": (
            "以下のテーブル定義と INSERT 文について、実行するとエラーになるものを3つ選んでください。\n\n"
            "CREATE TABLE orders (\n"
            "  order_id    NUMBER       PRIMARY KEY,\n"
            "  customer_id NUMBER       NOT NULL,\n"
            "  amount      NUMBER       CHECK (amount > 0),\n"
            "  status      VARCHAR2(10) DEFAULT 'PENDING' NOT NULL\n"
            ");\n\n"
            "A: INSERT INTO orders VALUES (1, NULL, 100, 'NEW');\n"
            "B: INSERT INTO orders VALUES (2, 101, -50, 'NEW');\n"
            "C: INSERT INTO orders (order_id, customer_id, amount) VALUES (3, 102, 200);\n"
            "D: INSERT INTO orders VALUES (4, 103, 0, 'NEW');"
        ),
        "multi_select_count": 3,
        "explanation": (
            "各INSERT文の分析:\n\n"
            "A: customer_id = NULL → NOT NULL 制約違反 → エラー\n"
            "B: amount = -50 → CHECK (amount > 0) 違反（負の値は不可）→ エラー\n"
            "C: status を省略 → DEFAULT 値 'PENDING' が自動設定される → 成功\n"
            "   DEFAULT が定義された NOT NULL 列は INSERT で省略可能。\n"
            "D: amount = 0 → CHECK (amount > 0) 違反（ゼロも不可）→ エラー\n\n"
            "正解: A（NOT NULL違反）・B（CHECK違反 負数）・D（CHECK違反 ゼロ）"
        ),
        "trap_reason": "CHECK制約の境界値を見落としやすい。amount > 0 はゼロを含まない（ゼロもエラー）。また、DEFAULT が設定された NOT NULL 列は省略可能（C が成功する）という点を「NOT NULLなら省略できないはず」と誤解するパターンが非常に多い。",
        "choices": [
            {"choice_text": "A（customer_id = NULL によるNOT NULL違反）",  "is_correct": True,  "display_order": 0},
            {"choice_text": "B（amount = -50 によるCHECK制約違反）",       "is_correct": True,  "display_order": 1},
            {"choice_text": "C（status を省略したINSERT）",                "is_correct": False, "display_order": 2},
            {"choice_text": "D（amount = 0 によるCHECK制約違反）",         "is_correct": True,  "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 14. FUNCTION_NEST（2つ選べ・難易度2）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "FUNCTION_NEST",
        "difficulty": 2,
        "question_text": "Oracle SQL の NVL2 関数と NULLIF 関数に関する説明として正しいものを2つ選んでください。",
        "multi_select_count": 2,
        "explanation": (
            "NVL2(expr1, expr2, expr3):\n"
            "・expr1 が NULL でない場合 → expr2 を返す\n"
            "・expr1 が NULL の場合     → expr3 を返す\n"
            "（NVL と引数順が異なる: NVL2 は3引数）\n\n"
            "NULLIF(expr1, expr2):\n"
            "・expr1 = expr2 の場合 → NULL を返す\n"
            "・expr1 ≠ expr2 の場合 → expr1 をそのまま返す\n"
            "（ゼロ除算回避などに使われる: NULLIF(分母, 0) とすれば分母が0のとき NULL を返す）\n\n"
            "NVL2(commission_pct, salary*1.1, salary):\n"
            "・commission_pct が NULL でない → salary*1.1 を返す\n"
            "・commission_pct が NULL       → salary を返す"
        ),
        "trap_reason": "NVLとNVL2の引数順を混同しやすい。NVLは2引数(元の値, NULLの場合)。NVL2は3引数で(チェック対象, NULLでない場合の値, NULLの場合の値)の順序。NULLIFはゼロ除算回避によく使われるが、「等しいときにNULLを返す」という点を逆に覚えがち。",
        "choices": [
            {"choice_text": "NVL2(commission_pct, salary*1.1, salary) は commission_pct が NULL の場合に salary を返す",       "is_correct": True,  "display_order": 0},
            {"choice_text": "NVL2(commission_pct, salary*1.1, salary) は commission_pct が NULL でない場合に salary を返す",    "is_correct": False, "display_order": 1},
            {"choice_text": "NULLIF(a, b) は a と b が等しい場合に NULL を返す",                                               "is_correct": True,  "display_order": 2},
            {"choice_text": "NULLIF(a, b) は a と b が等しい場合に 0 を返す",                                                  "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 15. DB_THEORY（3つ選べ・難易度3・長文）
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DB_THEORY",
        "difficulty": 3,
        "question_text": (
            "Oracle SQL における NULL の扱いについて、正しい記述を3つ選んでください。\n\n"
            "A: NULL と任意の値の算術演算（+、-、×、÷）の結果はすべて NULL になる\n"
            "B: WHERE 条件で NULL を検索するには「列名 = NULL」ではなく「列名 IS NULL」を使う必要がある\n"
            "C: ORDER BY を昇順（ASC）で指定した場合、NULL 値を持つ行はデフォルトで先頭（最も前）に並ぶ\n"
            "D: COUNT(*) は NULL を含む行もカウントするが、COUNT(列名) はその列が NULL の行をカウントしない"
        ),
        "multi_select_count": 3,
        "explanation": (
            "A: 正。NULL は「未知の値」のため、算術演算の結果も「不明」(NULL) になります。\n\n"
            "B: 正。NULL は = 演算子では比較できません。「列名 = NULL」は常に偽として扱われます。\n"
            "   IS NULL または IS NOT NULL を使う必要があります。\n\n"
            "C: 誤。Oracle の昇順ソートでは、NULL は最大値として扱われ末尾に表示されます。\n"
            "   （NULLS FIRST / NULLS LAST オプションで順序を明示的に指定可能）\n\n"
            "D: 正。COUNT(*) は全行数を返しますが、COUNT(列名) は指定列が NULL でない行のみカウントします。\n"
            "   AVG等の集計関数も同様に、NULL は集計の計算から除外されます。"
        ),
        "trap_reason": "Oracleの ORDER BY での NULL の位置（昇順ソートで末尾）を誤解するケースが多い。他のDBMS（MySQLなど）では昇順で先頭になる場合があり混同しやすい。また COUNT(*) と COUNT(列名) の違いは毎回試験に出る頻出ポイント。",
        "choices": [
            {"choice_text": "A（NULL を含む算術演算の結果は NULL）",             "is_correct": True,  "display_order": 0},
            {"choice_text": "B（NULL の検索には IS NULL を使う）",               "is_correct": True,  "display_order": 1},
            {"choice_text": "C（昇順 ORDER BY で NULL は先頭に表示される）",     "is_correct": False, "display_order": 2},
            {"choice_text": "D（COUNT(*) と COUNT(列名) の動作が異なる）",       "is_correct": True,  "display_order": 3},
        ],
    },
]
