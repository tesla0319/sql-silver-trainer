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

    # ──────────────────────────────────────────────────────────────────
    # 16. VIEW（1つ選べ・難易度1）CREATE OR REPLACE VIEW
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 1,
        "question_text": "CREATE OR REPLACE VIEW 構文に関する説明として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "CREATE OR REPLACE VIEW は、同名のビューが既に存在する場合でも DROP せずにビュー定義を置き換えます。\n\n"
            "OR REPLACE の主なメリット:\n"
            "・DROP → CREATE の2ステップが不要\n"
            "・既存ビューに付与されたオブジェクト権限（GRANT）が引き継がれる\n"
            "  （DROP → CREATE にすると権限が消えてしまう）\n"
            "・依存するオブジェクトが意図せず INVALID になるリスクを減らせる\n\n"
            "ビューが存在しない場合は通常の CREATE VIEW と同じ動作をします。"
        ),
        "trap_reason": "「OR REPLACEはDROPしてから再作成するため権限が失われる」という誤解が頻出。実際はオブジェクト権限が引き継がれる点が DROP→CREATE との最大の違い。",
        "choices": [
            {"choice_text": "OR REPLACEを指定すると既存ビューをDROPしてから再作成するため、付与済みの権限は失われる",   "is_correct": False, "display_order": 0},
            {"choice_text": "OR REPLACEを指定すると既存ビューの権限を引き継いだままビュー定義を置き換えられる",         "is_correct": True,  "display_order": 1},
            {"choice_text": "OR REPLACEは同名ビューが存在する場合にのみ有効で、存在しない場合はエラーになる",           "is_correct": False, "display_order": 2},
            {"choice_text": "OR REPLACEを使うと、そのビューを参照する全オブジェクトが自動再コンパイルされVALIDになる",  "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 17. VIEW（1つ選べ・難易度2）FORCE オプション
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "次のSQL文を実行した時点では、テーブル future_data が存在しないとします。\n\n"
            "CREATE FORCE VIEW v_future AS\n"
            "  SELECT id, name FROM future_data;\n\n"
            "この文の実行結果として正しいものを1つ選んでください。"
        ),
        "multi_select_count": 1,
        "explanation": (
            "FORCE オプションを指定すると、ベーステーブルが存在しなくてもビューを作成できます。\n"
            "ただし、ビューは INVALID（無効）状態として登録されます。\n\n"
            "その後の挙動:\n"
            "・future_data テーブルを作成後にビューにアクセスすると、自動的に再コンパイルされ VALID になる\n"
            "・FORCE なし（デフォルトは NOFORCE）の場合は、ベーステーブル不在でエラーになる\n\n"
            "FORCE の用途:\n"
            "・テーブルより先にビューを定義する必要があるスクリプト作成時\n"
            "・開発中にオブジェクトの依存関係に関わらずビューを先に作成したい場合"
        ),
        "trap_reason": "FORCEを指定するとビューが正常に使えると誤解しやすいが、実際はINVALID状態で登録される。ベーステーブルを作成した後、初回アクセス時に初めてVALIDになる。",
        "choices": [
            {"choice_text": "future_data が存在しないためエラーになり、ビューは作成されない",              "is_correct": False, "display_order": 0},
            {"choice_text": "ビューは INVALID 状態で作成され、future_data 作成後に初めて使用可能になる",   "is_correct": True,  "display_order": 1},
            {"choice_text": "ビューは VALID 状態で作成され、future_data がなくてもSELECTが実行できる",    "is_correct": False, "display_order": 2},
            {"choice_text": "FORCE は読み取り専用ビューを作成するオプションであり、テーブルの有無とは関係ない", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 18. VIEW（2つ選べ・難易度2）更新不可になる条件
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "次のVIEW定義のうち、DML操作（INSERT/UPDATE/DELETE）が実行できないものを2つ選んでください。\n\n"
            "A: CREATE VIEW v_a AS SELECT DISTINCT department_id FROM employees;\n"
            "B: CREATE VIEW v_b AS SELECT employee_id, salary FROM employees WHERE salary > 3000;\n"
            "C: CREATE VIEW v_c AS SELECT employee_id, ROWNUM AS rn FROM employees;\n"
            "D: CREATE VIEW v_d AS SELECT employee_id, last_name FROM employees ORDER BY last_name;"
        ),
        "multi_select_count": 2,
        "explanation": (
            "正解は A（DISTINCT を含む）と C（ROWNUM を含む）です。\n\n"
            "更新不可となるVIEWの主な条件:\n"
            "・DISTINCT を含む\n"
            "・GROUP BY / HAVING 句を含む\n"
            "・集合演算子（UNION, INTERSECT, MINUS）を含む\n"
            "・集計関数（SUM, AVG, COUNT 等）を含む\n"
            "・ROWNUM 疑似列を含む\n\n"
            "B（WHERE 句のみ）: 単純なSELECTであり更新可能\n"
            "D（ORDER BY のみ）: ORDER BY 単独は更新不可の条件に含まれない"
        ),
        "trap_reason": "ORDER BY を含むビューは更新不可と誤解するパターンが多い。ORDER BY 単独は更新可能条件を満たす。一方、ROWNUM は更新不可条件に含まれるため見落としやすい。",
        "choices": [
            {"choice_text": "A（DISTINCT を含むビュー）", "is_correct": True,  "display_order": 0},
            {"choice_text": "B（WHERE 句のみのビュー）",  "is_correct": False, "display_order": 1},
            {"choice_text": "C（ROWNUM を含むビュー）",   "is_correct": True,  "display_order": 2},
            {"choice_text": "D（ORDER BY のみのビュー）", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 19. VIEW（1つ選べ・難易度1）WITH READ ONLY
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 1,
        "question_text": (
            "以下のビュー定義に関する説明として正しいものを1つ選んでください。\n\n"
            "CREATE VIEW v_readonly AS\n"
            "  SELECT employee_id, first_name, salary\n"
            "  FROM employees\n"
            "WITH READ ONLY;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "WITH READ ONLY を指定したビューに対して INSERT / UPDATE / DELETE を実行しようとすると、\n"
            "ORA-42399 エラーが発生し、DML 操作はすべて禁止されます。\n\n"
            "SELECT（読み取り）は WITH READ ONLY でも通常どおり実行できます。\n\n"
            "WITH READ ONLY と WITH CHECK OPTION の違い:\n"
            "・WITH READ ONLY:    DML 操作を完全に禁止\n"
            "・WITH CHECK OPTION: DML 操作は許可するが、ビューの WHERE 条件を満たさなくなる変更を禁止"
        ),
        "trap_reason": "WITH READ ONLYをWITH CHECK OPTIONと混同するパターン。READ ONLYはDMLを「完全禁止」、CHECK OPTIONはDML自体は許可して「条件違反だけを禁止」という違いを押さえること。",
        "choices": [
            {"choice_text": "ビューのWHERE条件を満たさない行のINSERTのみが禁止される",         "is_correct": False, "display_order": 0},
            {"choice_text": "SELECTを含むすべての操作が禁止される",                            "is_correct": False, "display_order": 1},
            {"choice_text": "INSERT / UPDATE / DELETE がすべて禁止され、SELECTは実行できる",   "is_correct": True,  "display_order": 2},
            {"choice_text": "UPDATEのみが禁止され、INSERTとDELETEは実行できる",               "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 20. VIEW（2つ選べ・難易度2）WITH CHECK OPTION と WITH READ ONLY の違い
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "WITH CHECK OPTION と WITH READ ONLY に関する説明として正しいものを2つ選んでください。\n\n"
            "-- ビュー定義例\n"
            "CREATE VIEW v_check AS\n"
            "  SELECT * FROM employees WHERE salary > 5000\n"
            "WITH CHECK OPTION;\n\n"
            "CREATE VIEW v_read AS\n"
            "  SELECT * FROM employees WHERE salary > 5000\n"
            "WITH READ ONLY;"
        ),
        "multi_select_count": 2,
        "explanation": (
            "WITH READ ONLY:\n"
            "・INSERT / UPDATE / DELETE がすべて禁止される（ORA-42399）\n"
            "・SELECT は通常どおり実行可能\n\n"
            "WITH CHECK OPTION:\n"
            "・INSERT / UPDATE / DELETE は実行可能\n"
            "・ただし、操作後にビューの WHERE 条件を満たさなくなる INSERT / UPDATE はエラーになる\n"
            "・DELETE はビューから行を取り除くだけで「条件を満たさない行を生成しない」ため常に許可\n\n"
            "まとめ:\n"
            "・v_check: DELETE は実行できる。salary=4000 の INSERT はエラー\n"
            "・v_read:  DELETE はエラー。SELECT は可能"
        ),
        "trap_reason": "WITH CHECK OPTIONでDELETEが禁止されると誤解するパターンが多い。DELETEは行を消すだけでWHERE条件に違反する行を「作らない」ため、CHECK OPTIONの対象外。WITH READ ONLYがDMLを完全禁止する唯一のオプション。",
        "choices": [
            {"choice_text": "WITH READ ONLY ではSELECTは実行できる",                                "is_correct": True,  "display_order": 0},
            {"choice_text": "WITH CHECK OPTION ではDELETEも禁止される",                            "is_correct": False, "display_order": 1},
            {"choice_text": "WITH CHECK OPTION ではビューのWHERE条件を満たす行のDELETEは実行できる", "is_correct": True,  "display_order": 2},
            {"choice_text": "WITH READ ONLY と WITH CHECK OPTION は同一の動作をする",               "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 21. VIEW（1つ選べ・難易度2・長文）NOT NULL列がビューに含まれない場合のINSERT
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "以下のテーブルとビューが存在するとき、ビュー経由のINSERTの動作として正しいものを1つ選んでください。\n\n"
            "-- テーブル定義\n"
            "CREATE TABLE products (\n"
            "  product_id   NUMBER       PRIMARY KEY,\n"
            "  product_name VARCHAR2(50) NOT NULL,\n"
            "  price        NUMBER\n"
            ");\n\n"
            "-- ビュー定義（product_name 列を含まない）\n"
            "CREATE VIEW v_products AS\n"
            "  SELECT product_id, price FROM products;\n\n"
            "-- INSERT文\n"
            "INSERT INTO v_products (product_id, price) VALUES (1, 500);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "ビューを通じたINSERTでは、ビューに含まれていない列にNULLが設定されます。\n"
            "product_name は NOT NULL 制約があり DEFAULT も定義されていないため、\n"
            "NULL を設定しようとしてエラーになります（ORA-01400）。\n\n"
            "成功 / 失敗の判断基準:\n"
            "・ビュー外の列が NULL 許容             → NULL が設定されINSERT成功\n"
            "・ビュー外の列が NOT NULL かつ DEFAULT なし → NULL設定でエラー\n"
            "・ビュー外の列が NOT NULL かつ DEFAULT あり → DEFAULT値が設定されINSERT成功\n\n"
            "この例では price 列は NULL 許容のため問題なく、product_name の NOT NULL 制約がエラーの原因です。"
        ),
        "trap_reason": "「ビューに含まれない列はスキップされる」と思い込み成功すると誤解するパターン。実際はNULLが設定されようとし、NOT NULL制約があるとエラーになる。DEFAULTが設定されていれば成功する点が試験で問われやすい。",
        "choices": [
            {"choice_text": "product_name に NULL が設定され、INSERTが成功する",                     "is_correct": False, "display_order": 0},
            {"choice_text": "product_name の NOT NULL 制約によりエラーになる",                      "is_correct": True,  "display_order": 1},
            {"choice_text": "ビュー経由のINSERTは全列が揃っていない場合は常にエラーになる",          "is_correct": False, "display_order": 2},
            {"choice_text": "price が NULL 許容のためINSERTは成功し、product_name は空文字列になる", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 22. VIEW（1つ選べ・難易度3・長文）SELECT * 後の ALTER TABLE ADD
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 3,
        "question_text": (
            "次の操作を順番に実行しました。最後のSELECT文の結果として正しいものを1つ選んでください。\n\n"
            "① CREATE TABLE t (col1 NUMBER, col2 VARCHAR2(10));\n"
            "② CREATE VIEW v AS SELECT * FROM t;\n"
            "③ INSERT INTO t VALUES (1, 'A');\n"
            "④ ALTER TABLE t ADD (col3 DATE);\n"
            "⑤ SELECT * FROM v;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "⑤の SELECT * FROM v; は col1 と col2 の2列のみを返します。col3 は含まれません。\n\n"
            "理由:\n"
            "Oracle では CREATE VIEW 時に SELECT * の「*」がその時点の列リストに展開されてビュー定義に保存されます。\n"
            "ビュー v は「SELECT col1, col2 FROM t」として登録されており、\n"
            "④の ALTER TABLE で col3 を追加してもビュー定義は更新されません。\n\n"
            "col3 をビューに含めるには:\n"
            "  CREATE OR REPLACE VIEW v AS SELECT * FROM t;\n"
            "とビューを再定義する必要があります。\n\n"
            "なお、ALTER TABLE で既存列が削除・型変更された場合はビューが INVALID になることがあります。"
        ),
        "trap_reason": "SELECT * は「テーブルの現在の全列」を常に返すと思い込むパターン。ビューのSELECT *はビュー作成時点の列定義に固定される。これを「ビューは静的な列リストを持つ」と覚えると正確。",
        "choices": [
            {"choice_text": "col1, col2, col3 の3列が返される（ALTER TABLEの変更がビューに自動反映される）", "is_correct": False, "display_order": 0},
            {"choice_text": "col1, col2 の2列のみ返される（ビュー作成時点の列定義に固定されている）",        "is_correct": True,  "display_order": 1},
            {"choice_text": "ビューが INVALID になるためエラーが発生し、SELECTは失敗する",                  "is_correct": False, "display_order": 2},
            {"choice_text": "col3 のみが返される（最後に追加された列だけがSELECT *の対象になる）",          "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 23. VIEW（1つ選べ・難易度1）DROP VIEW の影響
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 1,
        "question_text": "DROP VIEW 文を実行した場合の動作として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "DROP VIEW はビューオブジェクト（ビュー定義）のみを削除します。\n"
            "ベーステーブルのデータや構造には一切影響しません。\n\n"
            "DROP VIEW の影響範囲:\n"
            "・ビュー定義がデータディクショナリから削除される\n"
            "・そのビューに付与されていたオブジェクト権限（GRANT）も削除される\n"
            "・そのビューを参照する他のビューは INVALID 状態になる\n\n"
            "影響を受けないもの:\n"
            "・ベーステーブルの行データ\n"
            "・ベーステーブルのスキーマ（列・制約・インデックス）\n"
            "・ベーステーブルに付与された権限"
        ),
        "trap_reason": "DROP VIEWでベーステーブルのデータも消えると誤解するパターン。ビューは「データを持たない仮想テーブル」であり、DROP VIEWはビュー定義（メタデータ）を削除するだけ。また、参照ビューが自動削除されない点も見落としやすい。",
        "choices": [
            {"choice_text": "ビュー定義とベーステーブルの行データが両方削除される",                  "is_correct": False, "display_order": 0},
            {"choice_text": "ビュー定義のみが削除され、ベーステーブルのデータは影響を受けない",      "is_correct": True,  "display_order": 1},
            {"choice_text": "ベーステーブルのデータのみが削除され、ビュー定義は残る",                "is_correct": False, "display_order": 2},
            {"choice_text": "ビューを参照するすべてのビューも自動的に削除される（カスケード削除）",  "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 24. VIEW（2つ選べ・難易度3・長文）JOINビューのDML制限
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 3,
        "question_text": (
            "以下のJOINビューに関する説明として正しいものを2つ選んでください。\n\n"
            "CREATE TABLE dept (\n"
            "  dept_id   NUMBER PRIMARY KEY,\n"
            "  dept_name VARCHAR2(50)\n"
            ");\n"
            "CREATE TABLE emp (\n"
            "  emp_id   NUMBER PRIMARY KEY,\n"
            "  emp_name VARCHAR2(50),\n"
            "  dept_id  NUMBER,\n"
            "  salary   NUMBER\n"
            ");\n"
            "CREATE VIEW v_emp_dept AS\n"
            "  SELECT e.emp_id, e.emp_name, e.salary, d.dept_name\n"
            "  FROM emp e JOIN dept d ON e.dept_id = d.dept_id;"
        ),
        "multi_select_count": 2,
        "explanation": (
            "JOINビューのDML可否は「key-preserved テーブル」の概念で判断します。\n\n"
            "key-preserved テーブル:\n"
            "結合後も各行が元テーブルの一意な行に対応し、主キーの一意性が保たれるテーブル。\n\n"
            "このビューでの判定:\n"
            "・emp:  結合後も emp_id は一意 → key-preserved ✓\n"
            "・dept: 複数の emp が同一 dept に属するため dept_id が結合結果で重複 → key-preserved でない\n\n"
            "DML可否:\n"
            "・emp.salary の UPDATE → 可（emp は key-preserved）\n"
            "・dept.dept_name の UPDATE → 不可（dept は key-preserved でない）\n"
            "・DELETE → emp が唯一の key-preserved テーブルのため実行可\n\n"
            "「JOINビューはDML不可」という思い込みが最大のトラップです。"
        ),
        "trap_reason": "「JOINビューに対してはDML操作が一切できない」という誤解が多い。実際はkey-preservedテーブルの列に限りUPDATE/DELETEが可能。key-preservedかどうかは「結合後も主キーの一意性が保たれるか」で判断する。",
        "choices": [
            {"choice_text": "key-preserved テーブルの列はJOINビューを通じてUPDATEできる",                      "is_correct": True,  "display_order": 0},
            {"choice_text": "JOINビューに対してはいかなるDML操作（UPDATE/DELETE）も実行できない",            "is_correct": False, "display_order": 1},
            {"choice_text": "key-preserved テーブルとは結合後も各行が元テーブルの1行に対応するテーブルのこと",  "is_correct": True,  "display_order": 2},
            {"choice_text": "dept テーブルの dept_name はこのビューを通じてUPDATEできる",                     "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 25. VIEW（2つ選べ・難易度2・長文）ビューを参照するビューの挙動
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "VIEW",
        "difficulty": 2,
        "question_text": (
            "以下のビュー定義が存在するとき、DROP VIEW v_base を実行した後の動作として正しいものを2つ選んでください。\n\n"
            "CREATE VIEW v_base AS\n"
            "  SELECT employee_id, salary FROM employees WHERE department_id = 10;\n\n"
            "CREATE VIEW v_top AS\n"
            "  SELECT employee_id, salary FROM v_base WHERE salary > 5000;"
        ),
        "multi_select_count": 2,
        "explanation": (
            "DROP VIEW v_base を実行すると:\n\n"
            "・v_top は INVALID 状態になるが、自動的に削除はされない\n"
            "・v_top に対してSELECTを実行しようとすると、コンパイルエラーが発生する\n\n"
            "その後 v_base を再作成（CREATE VIEW v_base ...）すると:\n"
            "・v_top への初回アクセス時にOracleが自動再コンパイルを試みる\n"
            "・再コンパイルが成功すれば v_top は再び VALID になる\n\n"
            "ビューのカスケード削除はデフォルトでは行われません。\n"
            "（DROP TABLE に CASCADE CONSTRAINTS オプションがある点と混同しないこと）"
        ),
        "trap_reason": "「ベースビューを削除すると参照ビューも自動削除される（カスケード）」という誤解が頻出。ビューの場合はINVALIDになるだけで削除されない。また、v_baseを再作成すれば v_top も再コンパイルで復活できる点を知らないケースも多い。",
        "choices": [
            {"choice_text": "v_top は INVALID 状態になるが削除はされない",                             "is_correct": True,  "display_order": 0},
            {"choice_text": "v_top も自動的に削除される（カスケード削除）",                            "is_correct": False, "display_order": 1},
            {"choice_text": "v_base を再作成すれば、v_top への初回アクセス時に自動再コンパイルされる",   "is_correct": True,  "display_order": 2},
            {"choice_text": "v_top は v_base 削除後もVALID状態を維持し、SELECTを正常に実行できる",      "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 26. JOIN（1つ選べ・難易度1・長文）INNER JOIN と等価結合
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 1,
        "question_text": (
            "以下の2つのSQL文の動作として正しいものを1つ選んでください。\n\n"
            "-- SQL①\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e INNER JOIN departments d ON e.dept_id = d.dept_id;\n\n"
            "-- SQL②\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e, departments d\n"
            "WHERE e.dept_id = d.dept_id;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "SQL①（ANSI JOIN構文）とSQL②（Oracleの伝統的なカンマ結合）はどちらも内部結合を行い、\n"
            "同一の結果を返します。\n\n"
            "・INNER JOIN ... ON: ISO/ANSI標準の結合構文（Oracle 9i以降で推奨）\n"
            "・カンマ結合 + WHERE: Oracleの伝統的な構文。現在も正常に動作する\n\n"
            "どちらの構文もオプティマイザは同様に処理します。\n"
            "可読性・保守性の観点からANSI構文が推奨されますが、結果は同一です。"
        ),
        "trap_reason": "「ANSI JOINはカンマ結合より高速」「カンマ結合はOUTER JOINになる」という誤解が頻出。どちらも内部結合であり同じ結果を返す。OUTER JOINにはならない点に注意。",
        "choices": [
            {"choice_text": "SQL①はANSI準拠のため最適化されるが、SQL②は最適化されず遅くなる",         "is_correct": False, "display_order": 0},
            {"choice_text": "SQL①はINNER JOIN、SQL②はOUTER JOINを行うため結果が異なる場合がある",    "is_correct": False, "display_order": 1},
            {"choice_text": "SQL①とSQL②は同一の内部結合を行い、同じ結果を返す",                     "is_correct": True,  "display_order": 2},
            {"choice_text": "SQL②のカンマ結合構文はOracleでは非推奨であり、エラーになる場合がある",   "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 27. JOIN（1つ選べ・難易度1・長文）LEFT OUTER JOIN のNULL行
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 1,
        "question_text": (
            "以下のSQL文の実行結果として正しいものを1つ選んでください。\n\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e LEFT OUTER JOIN departments d\n"
            "  ON e.dept_id = d.dept_id;\n\n"
            "一部の従業員は dept_id が departments テーブルに存在しない（未配属）とします。"
        ),
        "multi_select_count": 1,
        "explanation": (
            "LEFT OUTER JOIN は左表（employees）のすべての行を結果に保持します。\n"
            "右表（departments）に一致する行がない場合は、右表の列に NULL が設定されます。\n\n"
            "・一致する部署がある従業員: emp_name と dept_name が両方設定される\n"
            "・一致する部署がない従業員: emp_name は設定され、dept_name は NULL になる\n\n"
            "「未配属の従業員を含めて全従業員を抽出したい」といった場面でよく使います。\n"
            "OUTER は省略可能で LEFT JOIN と書いても同じ意味です。"
        ),
        "trap_reason": "LEFT JOINで一致しない行が「除外される」と誤解するパターン。除外するのはINNER JOIN。LEFT JOINは左表のすべての行を保持し、一致しない右表の列にNULLを設定する。",
        "choices": [
            {"choice_text": "対応する部署が存在しない従業員は結果から除外される",                      "is_correct": False, "display_order": 0},
            {"choice_text": "対応する部署が存在しない従業員も含まれ、dept_name にはNULLが設定される",  "is_correct": True,  "display_order": 1},
            {"choice_text": "対応する部署が存在しない従業員の行には、すべての部署の情報が結合される",   "is_correct": False, "display_order": 2},
            {"choice_text": "LEFT OUTER JOINでは departments 側のすべての行が保持される",             "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 28. JOIN（1つ選べ・難易度2）NATURAL JOIN の結合キー
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 2,
        "question_text": (
            "以下のテーブル定義で NATURAL JOIN を実行するとき、結合キーとして使用される列を1つ選んでください。\n\n"
            "employees テーブルの列: emp_id, emp_name, dept_id, manager_id\n"
            "departments テーブルの列: dept_id, dept_name, manager_id\n\n"
            "SELECT * FROM employees NATURAL JOIN departments;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "NATURAL JOIN は、2つのテーブルで名前が同じすべての列を自動的に結合キーとして使用します。\n\n"
            "この例では dept_id と manager_id が両テーブルに存在するため、\n"
            "両方を AND 条件で結合キーとして使用します。\n\n"
            "以下の ON 句と同等です:\n"
            "ON employees.dept_id = departments.dept_id\n"
            "AND employees.manager_id = departments.manager_id\n\n"
            "注意: 意図せず複数列が結合キーになり予期しない結果になることがあるため、\n"
            "実務では NATURAL JOIN より明示的な JOIN ... ON が推奨されます。"
        ),
        "trap_reason": "NATURAL JOINは「最初に見つかった同名列1つだけを結合キーにする」と思い込むパターン。実際はすべての同名列が結合キーになるため、意図しない絞り込みが発生することがある。",
        "choices": [
            {"choice_text": "dept_id のみを結合キーとして使用する",                     "is_correct": False, "display_order": 0},
            {"choice_text": "dept_id と manager_id の両方を結合キーとして使用する",      "is_correct": True,  "display_order": 1},
            {"choice_text": "主キー列（emp_id）を自動的に検出して結合キーとして使用する", "is_correct": False, "display_order": 2},
            {"choice_text": "NATURAL JOINはOracleではサポートされていない",              "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 29. JOIN（1つ選べ・難易度2）USING 句でのテーブル別名使用
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文のSELECT句を「e.dept_id, e.emp_name, d.dept_name」に変更した場合の動作として\n"
            "正しいものを1つ選んでください。\n\n"
            "SELECT dept_id, e.emp_name, d.dept_name\n"
            "FROM employees e JOIN departments d USING (dept_id);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "USING 句で指定した結合列（dept_id）にはテーブル別名を付けられません。\n"
            "e.dept_id と書くと ORA-25154 エラーが発生します。\n\n"
            "USING句の結合列の参照ルール:\n"
            "・SELECT dept_id    → OK（テーブル別名なし）\n"
            "・SELECT e.dept_id  → NG（ORA-25154）\n"
            "・SELECT d.dept_id  → NG（ORA-25154）\n\n"
            "ON 句を使った場合は e.dept_id / d.dept_id のどちらも参照可能です。\n"
            "USING句の結合列は「どちらのテーブルにも属さない共有列」として扱われるためです。"
        ),
        "trap_reason": "JOINの結合列には常にテーブル別名を付けられると思い込むパターン。USING句の列はどちらのテーブルにも属さない「共有列」として扱われるため、テーブル別名を付けるとORA-25154エラーになる。",
        "choices": [
            {"choice_text": "e.dept_id は employees 側の列を明示するため曖昧さが排除でき、問題なく実行できる", "is_correct": False, "display_order": 0},
            {"choice_text": "USING句の結合列にテーブル別名は付けられないため ORA-25154 エラーになる",       "is_correct": True,  "display_order": 1},
            {"choice_text": "USING句の列はSELECT句では参照できないためエラーになる",                     "is_correct": False, "display_order": 2},
            {"choice_text": "e.dept_id と d.dept_id が両方存在するため曖昧さエラー（ORA-00918）になる",    "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 30. JOIN（1つ選べ・難易度2）Oracle固有の (+) 外部結合
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文（Oracle固有構文）の動作として正しいものを1つ選んでください。\n\n"
            "SELECT e.emp_name, d.dept_name\n"
            "FROM employees e, departments d\n"
            "WHERE e.dept_id = d.dept_id(+);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "Oracle固有の (+) 演算子は外部結合を表します。(+) を付けた側が「省略可能（NULL許容）」な側です。\n\n"
            "・d.dept_id(+) → departments 側が省略可能\n"
            "・employees 側のすべての行が保持される（= LEFT OUTER JOIN 相当）\n\n"
            "ANSI構文に直すと以下と同等です:\n"
            "FROM employees e LEFT OUTER JOIN departments d ON e.dept_id = d.dept_id\n\n"
            "注意: (+) を WHERE 句の両辺に付けることはできません。\n"
            "FULL OUTER JOIN を (+) で表現することはできないため、ANSI構文を使う必要があります。"
        ),
        "trap_reason": "(+)を付けた側が「保持される（重要な）側」と逆に覚えるパターンが多い。(+)は「穴埋め側（NULLが入る可能性がある側）」を示す。(+)がない側のテーブルがすべての行を保持する。",
        "choices": [
            {"choice_text": "departments 側のすべての行が保持される（RIGHT OUTER JOIN 相当）",        "is_correct": False, "display_order": 0},
            {"choice_text": "employees 側のすべての行が保持される（LEFT OUTER JOIN 相当）",          "is_correct": True,  "display_order": 1},
            {"choice_text": "両側のすべての行が保持される（FULL OUTER JOIN 相当）",                  "is_correct": False, "display_order": 2},
            {"choice_text": "(+) を WHERE 句の両辺に付けることでFULL OUTER JOINが実現できる",        "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 31. JOIN（1つ選べ・難易度1）CROSS JOIN の結果行数
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 1,
        "question_text": (
            "以下のSQL文の結果として返される行数を1つ選んでください。\n\n"
            "SELECT * FROM table_a CROSS JOIN table_b;\n\n"
            "table_a: 4行、table_b: 5行"
        ),
        "multi_select_count": 1,
        "explanation": (
            "CROSS JOIN（直積・デカルト積）は、2つのテーブルのすべての行の組み合わせを返します。\n\n"
            "結果行数 = 左テーブルの行数 × 右テーブルの行数 = 4 × 5 = 20行\n\n"
            "CROSS JOIN の特徴:\n"
            "・ON 句や結合条件を持たない\n"
            "・テーブルが大きいほど結果が爆発的に増える\n"
            "・Oracleではカンマ結合でWHERE条件なしにすると意図せず同じ結果になる（デカルト積バグ）"
        ),
        "trap_reason": "CROSS JOINの行数を「左+右」の加算（9行）と誤解するパターン。正しくは「左×右」の乗算（20行）。結合条件なしのデカルト積を意図せず作ってしまうSQLバグの代表例。",
        "choices": [
            {"choice_text": "4行（table_a の行数）", "is_correct": False, "display_order": 0},
            {"choice_text": "5行（table_b の行数）", "is_correct": False, "display_order": 1},
            {"choice_text": "9行（4 + 5）",          "is_correct": False, "display_order": 2},
            {"choice_text": "20行（4 × 5）",         "is_correct": True,  "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 32. JOIN（2つ選べ・難易度2）FULL OUTER JOIN の動作
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文とデータに関する説明として正しいものを2つ選んでください。\n\n"
            "SELECT a.id AS a_id, b.id AS b_id\n"
            "FROM tbl_a a FULL OUTER JOIN tbl_b b ON a.id = b.id;\n\n"
            "tbl_a の id 列の値: 1, 2, 3\n"
            "tbl_b の id 列の値: 2, 3, 4"
        ),
        "multi_select_count": 2,
        "explanation": (
            "FULL OUTER JOIN は LEFT OUTER JOIN と RIGHT OUTER JOIN を合わせた結果を返します。\n\n"
            "このクエリの結果（4行）:\n"
            "・id=1（tbl_aのみ）: a_id=1, b_id=NULL\n"
            "・id=2（両方一致）:  a_id=2, b_id=2\n"
            "・id=3（両方一致）:  a_id=3, b_id=3\n"
            "・id=4（tbl_bのみ）: a_id=NULL, b_id=4\n\n"
            "FULL OUTER JOIN はどちらのテーブルにしか存在しない行も保持し、\n"
            "もう一方のテーブルの列には NULL を設定します。\n\n"
            "OracleではFULL OUTER JOINはANSI構文でのみ記述可能です。\n"
            "(+) 演算子ではFULL OUTER JOINを表現できません。"
        ),
        "trap_reason": "FULL OUTER JOINの結果が「両方に存在する行のみ」（= INNER JOIN）と誤解するパターン。FULL JOINはどちらか一方にしかない行も保持しNULLを設定する。また(+)でFULL JOINが書けると思い込むパターンも頻出。",
        "choices": [
            {"choice_text": "id=1（tbl_aのみ）の行は結果に含まれ、b_id はNULLになる",             "is_correct": True,  "display_order": 0},
            {"choice_text": "結果に含まれる行は id=2 と id=3 の2行のみである",                    "is_correct": False, "display_order": 1},
            {"choice_text": "id=4（tbl_bのみ）の行は結果に含まれ、a_id はNULLになる",             "is_correct": True,  "display_order": 2},
            {"choice_text": "OracleではFULL OUTER JOINを (+) 演算子を使って記述できる",            "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 33. JOIN（1つ選べ・難易度2）NULLを含む列のJOIN
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文において、tbl_a に code = NULL の行が存在する場合の動作として\n"
            "正しいものを1つ選んでください。\n\n"
            "SELECT a.col1, b.col2\n"
            "FROM tbl_a a JOIN tbl_b b ON a.code = b.code;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "INNER JOIN の結合条件 ON a.code = b.code で NULL を比較した場合、\n"
            "NULL = NULL は TRUE ではなく UNKNOWN（不明）として評価されます。\n\n"
            "SQLでは条件が UNKNOWN の行は結果から除外されるため、\n"
            "a.code = NULL の行は結合条件を満たさず、結果に含まれません。\n\n"
            "NULL同士を一致させたい場合は明示的な IS NULL チェックが必要です:\n"
            "ON (a.code = b.code OR (a.code IS NULL AND b.code IS NULL))"
        ),
        "trap_reason": "「NULL = NULLはTRUEになりNULL同士で結合される」という誤解が非常に多い。SQLの3値論理ではNULL = NULLはUNKNOWNであり、JOIN条件を満たさないため行は除外される。LEFT JOINとは異なる動作なので混同しないこと。",
        "choices": [
            {"choice_text": "NULL = NULL はTRUEとして扱われ、tbl_b のNULL行と結合されて結果に含まれる",  "is_correct": False, "display_order": 0},
            {"choice_text": "NULL = NULL はUNKNOWNとして扱われ、code=NULLの行は結果に含まれない",       "is_correct": True,  "display_order": 1},
            {"choice_text": "NULLを含む列でJOINを実行するとORA-01427エラーが発生する",                 "is_correct": False, "display_order": 2},
            {"choice_text": "code=NULLの行はLEFT JOINと同様に結果に含まれ、b.col2にはNULLが設定される", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 34. JOIN（2つ選べ・難易度2・長文）3テーブルJOIN
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文の実行結果に関する説明として正しいものを2つ選んでください。\n\n"
            "SELECT e.emp_name, d.dept_name, l.city\n"
            "FROM employees e\n"
            "  JOIN departments d ON e.department_id = d.department_id\n"
            "  JOIN locations l ON d.location_id = l.location_id;"
        ),
        "multi_select_count": 2,
        "explanation": (
            "このSQL文は employees・departments・locations の3テーブルを INNER JOIN で結合しています。\n\n"
            "INNER JOIN の特性:\n"
            "・departments に一致しない従業員は結果に含まれない\n"
            "・locations に一致しない部署に属する従業員も結果に含まれない\n"
            "・ANSI INNER JOIN は記述順序を変えても最終的な結果は変わらない\n\n"
            "このSQL文は以下のWHERE結合でも同じ結果が得られます:\n"
            "FROM employees e, departments d, locations l\n"
            "WHERE e.department_id = d.department_id\n"
            "  AND d.location_id = l.location_id;"
        ),
        "trap_reason": "「INNER JOINの順序を変えると結果が変わる」という誤解がある。ANSI INNER JOINは結合順序によって最終結果は変わらない。また、WHERE句のカンマ結合で同じ3テーブル結合が書けることを知らないケースも多い。",
        "choices": [
            {"choice_text": "いずれかの結合条件に一致しない従業員は結果に含まれない",                        "is_correct": True,  "display_order": 0},
            {"choice_text": "JOIN句の記述順序を入れ替えると結果の行数が変わる場合がある",                     "is_correct": False, "display_order": 1},
            {"choice_text": "FROM句にカンマ区切りで3テーブルを並べWHERE句に結合条件を書いても同じ結果になる", "is_correct": True,  "display_order": 2},
            {"choice_text": "3テーブルを結合する場合、ON句は最後のJOINにのみ書けるという制約がある",          "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 35. JOIN（2つ選べ・難易度3・長文）USING 句と ON 句の違い
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "JOIN",
        "difficulty": 3,
        "question_text": (
            "JOIN構文における USING 句と ON 句の違いとして正しいものを2つ選んでください。\n\n"
            "-- 書き方A: ON句\n"
            "SELECT e.dept_id, e.emp_name, d.dept_name\n"
            "FROM employees e JOIN departments d ON e.dept_id = d.dept_id;\n\n"
            "-- 書き方B: USING句\n"
            "SELECT dept_id, e.emp_name, d.dept_name\n"
            "FROM employees e JOIN departments d USING (dept_id);"
        ),
        "multi_select_count": 2,
        "explanation": (
            "USING 句と ON 句の主な違い:\n\n"
            "① 結合列の重複:\n"
            "・ON 句: SELECT * を実行すると e.dept_id と d.dept_id が別々の2列として返される\n"
            "・USING 句: SELECT * を実行すると dept_id は1列だけ返される（重複なし）\n\n"
            "② テーブル別名の使用:\n"
            "・ON 句: e.dept_id / d.dept_id どちらも使用可能\n"
            "・USING 句: dept_id のみ使用可。e.dept_id と書くと ORA-25154 エラー\n\n"
            "③ 条件の柔軟性:\n"
            "・ON 句: 等号以外（>、<、BETWEEN 等）も使用可能\n"
            "・USING 句: 等価結合（=）のみ使用可能"
        ),
        "trap_reason": "USINGとONが「完全に同じ動作をする別の書き方」と思い込むパターン。SELECT *での列数の違い（USING=1列、ON=2列）と、テーブル別名の使用可否が試験頻出の差異。特にUSINGでテーブル別名を付けるとエラーになる点を押さえること。",
        "choices": [
            {"choice_text": "USING句ではSELECT *を実行すると結合列（dept_id）は1列のみ返される",              "is_correct": True,  "display_order": 0},
            {"choice_text": "ON句ではSELECT *を実行するとe.dept_idとd.dept_idが別々の2列として返される",     "is_correct": True,  "display_order": 1},
            {"choice_text": "USING句はON句より常に高速に実行される",                                         "is_correct": False, "display_order": 2},
            {"choice_text": "USING句でもe.dept_idのようにテーブル別名を付けて結合列を参照できる",             "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 36. INDEX（1つ選べ・難易度2）UNIQUE INDEXとNULL値
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "以下のUNIQUE INDEXが定義されているとき、email 列が NULL の行を複数行INSERTした場合の\n"
            "動作として正しいものを1つ選んでください。\n\n"
            "CREATE UNIQUE INDEX idx_email ON users(email);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "OracleのB-treeインデックスはNULL値を格納しません。\n"
            "UNIQUE INDEXの一意性チェックはインデックスを通して行われるため、\n"
            "インデックスに存在しないNULL値は「一意性違反」とみなされません。\n\n"
            "結果として、UNIQUE INDEXが設定された列でも複数行のNULLをINSERTできます。\n\n"
            "これはSQL標準の仕様（NULL同士の比較はUNKNOWN）とも一致しています。\n"
            "UNIQUE制約でも同様の動作をします（既存Q3の制約問題も参照）。\n\n"
            "NULL値を1行だけに制限したい場合は、アプリケーション側の制御や\n"
            "NOT NULL + UNIQUE 制約の組み合わせが必要です。"
        ),
        "trap_reason": "「UNIQUE INDEXはすべての値の一意性を保証するため、NULLも1行しか持てない」という誤解が頻出。B-treeインデックスはNULLを格納しないためNULL値はUNIQUEチェックの対象外になる。",
        "choices": [
            {"choice_text": "UNIQUE INDEXは一意性を保証するためemail=NULLの行は1行しかINSERTできない",       "is_correct": False, "display_order": 0},
            {"choice_text": "B-treeインデックスはNULLを格納しないためUNIQUE INDEXでも複数のNULLを許容する",  "is_correct": True,  "display_order": 1},
            {"choice_text": "NULL値はUNIQUE INDEXで重複エラー（ORA-00001）として扱われる",                  "is_correct": False, "display_order": 2},
            {"choice_text": "2行目のNULLは自動的に別の値（シーケンス番号等）に変換されてINSERTされる",        "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 37. INDEX（1つ選べ・難易度2）複合INDEXの先頭列ルール
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "以下の複合インデックスが定義されているとき、インデックスが使用されない可能性が最も高い\n"
            "WHERE句を1つ選んでください。\n\n"
            "CREATE INDEX idx_orders ON orders(status, order_date);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "複合インデックスは先頭列（status）を条件に含む場合に有効に使われます。\n\n"
            "各WHERE句の評価:\n"
            "・WHERE status = 'PENDING'                        → status が先頭列 → インデックス使用可\n"
            "・WHERE status = 'PENDING' AND order_date > ...   → 両列指定 → インデックス使用可\n"
            "・WHERE order_date > SYSDATE - 7                  → status なし → 通常インデックス不使用\n"
            "・WHERE status IS NOT NULL AND order_date IS NOT NULL → statusが先頭列 → インデックス使用可\n\n"
            "先頭列を含まない条件（order_date のみ）では複合インデックスは一般に使用されません。\n"
            "（オプティマイザがIndex Skip Scanを選択する場合もありますが、基本ルールは先頭列が必要）"
        ),
        "trap_reason": "「複合インデックスに含まれる列ならどれでもインデックスが使える」という誤解が多い。先頭列（第1列）を含まないWHERE句では通常インデックスは使われない。インデックス設計で先頭列の選択が重要な理由でもある。",
        "choices": [
            {"choice_text": "WHERE status = 'PENDING'",                              "is_correct": False, "display_order": 0},
            {"choice_text": "WHERE status = 'PENDING' AND order_date > SYSDATE - 7", "is_correct": False, "display_order": 1},
            {"choice_text": "WHERE order_date > SYSDATE - 7",                        "is_correct": True,  "display_order": 2},
            {"choice_text": "WHERE status IS NOT NULL AND order_date IS NOT NULL",    "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 38. INDEX（1つ選べ・難易度2）関数適用によるINDEX無効化
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "last_name 列にB-treeインデックスが定義されているとき、\n"
            "そのインデックスを使用できないWHERE句を1つ選んでください。\n\n"
            "CREATE INDEX idx_name ON employees(last_name);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "インデックスが定義された列に関数を適用すると、通常のB-treeインデックスは使用できません。\n\n"
            "各WHERE句の評価:\n"
            "・WHERE last_name = 'Smith'        → 直接比較 → インデックス使用可\n"
            "・WHERE last_name LIKE 'Sm%'       → 後方ワイルドカード → インデックス使用可\n"
            "・WHERE UPPER(last_name) = 'SMITH' → 列に関数適用 → インデックス不使用 ✗\n"
            "・WHERE last_name > 'S'            → 範囲検索 → インデックス使用可\n\n"
            "UPPER(last_name)でインデックスを使いたい場合は関数ベースインデックスが必要です:\n"
            "CREATE INDEX idx_upper ON employees(UPPER(last_name));"
        ),
        "trap_reason": "「列名がWHERE句に含まれているからインデックスが使える」という誤解が多い。UPPER()などの関数を列に適用すると、その列のインデックスは使用できなくなる。これは入門者が最も見落としやすい落とし穴のひとつ。",
        "choices": [
            {"choice_text": "WHERE last_name = 'Smith'",        "is_correct": False, "display_order": 0},
            {"choice_text": "WHERE last_name LIKE 'Sm%'",       "is_correct": False, "display_order": 1},
            {"choice_text": "WHERE UPPER(last_name) = 'SMITH'", "is_correct": True,  "display_order": 2},
            {"choice_text": "WHERE last_name > 'S'",            "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 39. INDEX（1つ選べ・難易度2）B-tree INDEXとNULL
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": "OracleのB-treeインデックスのNULL値の扱いに関する説明として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "OracleのB-treeインデックスはNULL値をインデックスエントリとして格納しません。\n\n"
            "この仕様による影響:\n"
            "・IS NULL 条件:     インデックスを使用できない（NULL値がインデックスに存在しないため）\n"
            "                    → フルテーブルスキャンが実行される\n"
            "・IS NOT NULL 条件: インデックスを使用できる（非NULL値はインデックスに存在するため）\n\n"
            "NULLを多く含む列のインデックスは、NULL分だけエントリが少なくなりサイズが小さくなります。\n\n"
            "IS NULL条件で高速検索したい場合の対策:\n"
            "・ビットマップインデックスの使用（データウェアハウス環境向け）\n"
            "・NULLの代わりにデフォルト値を設定してインデックスを作成する"
        ),
        "trap_reason": "「インデックスはNULL値も含めてすべての値を格納する」という誤解が多い。B-treeインデックスはNULLを格納しないため、IS NULL条件ではインデックスが使われない。またNULLが多い列はインデックスサイズが小さくなる（大きくなるではない）点も注意。",
        "choices": [
            {"choice_text": "B-treeインデックスはNULL値も格納するため、IS NULL条件でもインデックスが使われる",  "is_correct": False, "display_order": 0},
            {"choice_text": "B-treeインデックスはNULL値を格納しないため、IS NULL条件ではフルスキャンになる",   "is_correct": True,  "display_order": 1},
            {"choice_text": "B-treeインデックスはNULL値を最小値として格納し、昇順ソートで先頭に現れる",        "is_correct": False, "display_order": 2},
            {"choice_text": "NULL値が多い列はB-treeインデックスのサイズが通常より大きくなる",                 "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 40. INDEX（1つ選べ・難易度2）制約で自動作成されたINDEXのDROP制限
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "PRIMARY KEY制約によって自動作成されたインデックスを、直接DROP INDEXで削除しようとした場合の\n"
            "動作として正しいものを1つ選んでください。"
        ),
        "multi_select_count": 1,
        "explanation": (
            "PRIMARY KEY制約（またはUNIQUE制約）によって自動作成されたインデックスは、\n"
            "DROP INDEX で直接削除しようとすると ORA-02429 エラーが発生します。\n\n"
            "ORA-02429: 主キー/一意キーの強制に使用されているインデックスは削除できません\n\n"
            "正しい削除手順:\n"
            "① 制約ごとインデックスを削除する:\n"
            "   ALTER TABLE t DROP PRIMARY KEY;\n\n"
            "② インデックスを残して制約のみ削除する:\n"
            "   ALTER TABLE t DROP PRIMARY KEY KEEP INDEX;\n"
            "   → その後 DROP INDEX が実行可能になる\n\n"
            "この仕様は、制約の強制に使われているインデックスを誤って削除しないためのOracle安全機構です。"
        ),
        "trap_reason": "「インデックスは制約とは独立したオブジェクトなので自由にDROPできる」と思い込むパターン。PK/UNIQUE制約が有効な間は、その制約が使用しているインデックスをDROP INDEXで削除することはできない（ORA-02429）。",
        "choices": [
            {"choice_text": "DROP INDEXを実行するとPRIMARY KEY制約も同時に削除される",               "is_correct": False, "display_order": 0},
            {"choice_text": "PRIMARY KEY制約が有効な間はDROP INDEXでは削除できずORA-02429エラーになる", "is_correct": True,  "display_order": 1},
            {"choice_text": "DROP INDEXを実行してもPRIMARY KEY制約は維持されたまま削除できる",         "is_correct": False, "display_order": 2},
            {"choice_text": "システム管理インデックスのため削除できないが、エラーではなく無視される",    "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 41. INDEX（1つ選べ・難易度1）LIKEのワイルドカードとINDEX
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 1,
        "question_text": (
            "product_name 列にB-treeインデックスが定義されているとき、\n"
            "インデックスを使用できないWHERE句を1つ選んでください。\n\n"
            "CREATE INDEX idx_product ON products(product_name);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "B-treeインデックスはデータを「前方から」ソートして格納しています。\n\n"
            "・LIKE 'Widget%'（後方ワイルドカード）: 前方一致 → インデックス使用可\n"
            "・LIKE '%Widget'（前方ワイルドカード）: 先頭文字が不明 → インデックス不使用\n"
            "・= 'Widget': 直接等値比較 → インデックス使用可\n"
            "・> 'A': 範囲検索 → インデックス使用可\n\n"
            "先頭にワイルドカード（%）を付けた LIKE は、インデックスの前方一致検索が\n"
            "利用できないためフルテーブルスキャンになります。"
        ),
        "trap_reason": "LIKE '%Widget' もLIKE 'Widget%' もどちらも同じようにインデックスが使えると思い込むパターン。前方ワイルドカード（%で始まる）は先頭文字が不明なためインデックスが使えない。後方ワイルドカード（%で終わる）は前方一致として使える。",
        "choices": [
            {"choice_text": "WHERE product_name = 'Widget'",     "is_correct": False, "display_order": 0},
            {"choice_text": "WHERE product_name LIKE 'Widget%'", "is_correct": False, "display_order": 1},
            {"choice_text": "WHERE product_name LIKE '%Widget'", "is_correct": True,  "display_order": 2},
            {"choice_text": "WHERE product_name > 'A'",          "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 42. INDEX（1つ選べ・難易度2）低選択性とフルテーブルスキャン
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "Oracleのオプティマイザがインデックスを使用せずに\n"
            "フルテーブルスキャン（FTS）を選択する可能性が最も高い状況として正しいものを1つ選んでください。"
        ),
        "multi_select_count": 1,
        "explanation": (
            "Oracleのコストベースオプティマイザ（CBO）は、インデックス使用とFTSのコストを比較して\n"
            "実行計画を選択します。\n\n"
            "FTSが選ばれやすい条件:\n"
            "・列の値の種類が少ない（低カーディナリティ）場合\n"
            "  例: 性別列（M/F）、フラグ列（0/1）、ステータス列（数種類のみ）\n"
            "  → 多くの行が返されるため、インデックス経由よりFTSが効率的\n\n"
            "インデックスが有効に使われる条件:\n"
            "・列の値の種類が多い（高カーディナリティ）: 氏名・メールアドレス・注文番号など\n"
            "・WHERE条件で返される行が全体の少数にとどまる場合\n\n"
            "「インデックスを作れば必ず使われる」わけではなく、\n"
            "オプティマイザが費用対効果を判断して実行計画を決定します。"
        ),
        "trap_reason": "「インデックスを作成すれば必ずそのインデックスが使われる」という誤解が多い。オプティマイザは列の選択性（カーディナリティ）を評価し、低選択性の列ではFTSを選ぶ場合がある。性別やフラグ列へのインデックスが効果的でないのはこのため。",
        "choices": [
            {"choice_text": "PRIMARY KEY列に対してINSERTとSELECTを繰り返す場合",                       "is_correct": False, "display_order": 0},
            {"choice_text": "性別（M/F）のように値の種類が少ない列を条件にして多くの行が返される場合",   "is_correct": True,  "display_order": 1},
            {"choice_text": "10万行のテーブルからメールアドレスで1件を検索する場合",                    "is_correct": False, "display_order": 2},
            {"choice_text": "インデックス作成直後の初回SELECTを実行する場合",                          "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 43. INDEX（2つ選べ・難易度3）複合INDEXの使用可否
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 3,
        "question_text": (
            "以下の複合インデックスが定義されているとき、このインデックスを使用できる可能性があるものを\n"
            "2つ選んでください。\n\n"
            "CREATE INDEX idx_emp ON employees(department_id, salary);"
        ),
        "multi_select_count": 2,
        "explanation": (
            "複合インデックス(department_id, salary) の使用可否:\n\n"
            "A: WHERE department_id = 10\n"
            "   → 先頭列のみ指定 → インデックス使用可 ✓\n\n"
            "B: WHERE salary > 50000\n"
            "   → 先頭列(department_id)なし → 通常インデックス不使用\n\n"
            "C: WHERE department_id = 10 AND salary > 50000\n"
            "   → 先頭列 + 第2列の範囲検索 → インデックス使用可 ✓\n\n"
            "D: WHERE department_id IS NULL\n"
            "   → B-treeインデックスはNULLを格納しないため → インデックス不使用\n\n"
            "先頭列を含み、かつNULL以外の条件（等値・範囲・LIKE前方一致等）であればインデックスが使われます。"
        ),
        "trap_reason": "複合インデックスはすべての組み合わせで使えると思いがちだが、先頭列なしのWHERE句やNULL検索（IS NULL）では使えない。第2列だけ指定したWHERE salary > 50000 が典型的なトラップ。IS NULLも見落としやすい。",
        "choices": [
            {"choice_text": "WHERE department_id = 10",                    "is_correct": True,  "display_order": 0},
            {"choice_text": "WHERE salary > 50000",                        "is_correct": False, "display_order": 1},
            {"choice_text": "WHERE department_id = 10 AND salary > 50000", "is_correct": True,  "display_order": 2},
            {"choice_text": "WHERE department_id IS NULL",                 "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 44. INDEX（1つ選べ・難易度2）関数ベースインデックス
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文の検索性能をインデックスで改善したい場合、有効なインデックス定義を1つ選んでください。\n\n"
            "SELECT * FROM employees WHERE UPPER(last_name) = 'SMITH';"
        ),
        "multi_select_count": 1,
        "explanation": (
            "列に関数（UPPER等）を適用した条件では、通常のB-treeインデックスは使用できません。\n\n"
            "解決策: 関数ベースインデックス（Function-Based Index）を作成する\n"
            "CREATE INDEX idx_upper_name ON employees(UPPER(last_name));\n\n"
            "このインデックスは UPPER(last_name) の計算結果を格納するため、\n"
            "WHERE UPPER(last_name) = 'SMITH' の条件でインデックスが使用されます。\n\n"
            "関数ベースインデックスの利点:\n"
            "・大文字小文字を区別しない検索に有効\n"
            "・変換関数を使った検索をインデックスで高速化できる\n"
            "・アプリケーション側の修正が不要"
        ),
        "trap_reason": "「同じ列のインデックスがあればUPPER()の条件でも使える」という誤解が多い。関数を適用すると通常インデックスは使えず、関数ベースインデックスを別途作成する必要がある。",
        "choices": [
            {"choice_text": "CREATE INDEX idx ON employees(last_name)",                   "is_correct": False, "display_order": 0},
            {"choice_text": "CREATE INDEX idx ON employees(UPPER(last_name))",            "is_correct": True,  "display_order": 1},
            {"choice_text": "CREATE UNIQUE INDEX idx ON employees(last_name)",            "is_correct": False, "display_order": 2},
            {"choice_text": "CREATE INDEX idx ON employees(last_name, UPPER(last_name))", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 45. INDEX（2つ選べ・難易度2）INDEXが使用されない条件
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INDEX",
        "difficulty": 2,
        "question_text": (
            "salary 列にB-treeインデックスが定義されているとき、\n"
            "インデックスが使用されない（または有効に使えない）条件として正しいものを2つ選んでください。\n\n"
            "CREATE INDEX idx_salary ON employees(salary);"
        ),
        "multi_select_count": 2,
        "explanation": (
            "各条件の評価:\n\n"
            "A: WHERE NVL(salary, 0) > 50000\n"
            "   → salary列にNVL関数を適用 → インデックス不使用 ✓\n\n"
            "B: WHERE salary > 50000\n"
            "   → 直接の範囲比較 → インデックス使用可\n\n"
            "C: WHERE TO_CHAR(salary) = '50000'\n"
            "   → salary列にTO_CHAR関数を適用 → インデックス不使用 ✓\n\n"
            "D: WHERE salary = 50000\n"
            "   → 直接の等値比較 → インデックス使用可\n\n"
            "NVL・TO_CHAR・UPPER等の関数を列に適用するとインデックスが無効化されます。\n"
            "これらの条件でインデックスを使いたい場合は関数ベースインデックスが必要です。"
        ),
        "trap_reason": "「NVL(salary, 0)のようなNULL対策の関数でもインデックスが無効になる」点を見落とすパターン。NVLをはじめとした関数の適用はすべてインデックスを無効化する。「salary列のインデックスがある=salary関連は全部速い」という誤解に注意。",
        "choices": [
            {"choice_text": "WHERE NVL(salary, 0) > 50000",     "is_correct": True,  "display_order": 0},
            {"choice_text": "WHERE salary > 50000",              "is_correct": False, "display_order": 1},
            {"choice_text": "WHERE TO_CHAR(salary) = '50000'",  "is_correct": True,  "display_order": 2},
            {"choice_text": "WHERE salary = 50000",              "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 46. CONSTRAINT（1つ選べ・難易度2）FOREIGN KEY列のNULL値
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": (
            "以下のテーブル定義において、orders.customer_id 列に NULL をINSERTした場合の\n"
            "動作として正しいものを1つ選んでください。\n\n"
            "CREATE TABLE customers (customer_id NUMBER PRIMARY KEY, name VARCHAR2(50));\n"
            "CREATE TABLE orders (\n"
            "  order_id    NUMBER PRIMARY KEY,\n"
            "  customer_id NUMBER REFERENCES customers(customer_id)\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "FOREIGN KEY制約が設定された列にNULL値を格納することは許可されています。\n\n"
            "FKの制約チェックは「NULLでない値が参照先テーブルに存在するか」を検証します。\n"
            "NULLは「不明な値」として扱われ、FK制約のチェック対象外になります。\n\n"
            "・customer_id = NULL のINSERT → FK制約をパス → 成功\n"
            "・customer_id = 999 で customers に 999 が存在しない → FK制約違反 → エラー\n\n"
            "NULL値を持つFKは「所属先不明」の行（例:未確定の注文）を表現するときに使われます。\n"
            "NULLを禁止したい場合はFKに加えてNOT NULL制約も設定します。"
        ),
        "trap_reason": "「FK制約がある列にはNULL以外の参照先が必要」という誤解が多い。実際はNULLはFK制約の対象外であり格納可能。NULLを禁止するにはNOT NULLを別途設定する必要がある。",
        "choices": [
            {"choice_text": "customers にNULLのcustomer_idが存在しないためFK違反でエラーになる",   "is_correct": False, "display_order": 0},
            {"choice_text": "NULLはFK制約の対象外のためエラーにならず、INSERTが成功する",          "is_correct": True,  "display_order": 1},
            {"choice_text": "NULLは自動的に0に変換されてINSERTされる",                           "is_correct": False, "display_order": 2},
            {"choice_text": "FK制約のある列はNOT NULLが暗黙的に設定されるためエラーになる",        "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 47. CONSTRAINT（1つ選べ・難易度2）ON DELETE CASCADE
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": (
            "以下の定義のテーブルで、departments から dept_id=10 の行をDELETEした場合の\n"
            "動作として正しいものを1つ選んでください。\n\n"
            "CREATE TABLE departments (dept_id NUMBER PRIMARY KEY, dept_name VARCHAR2(50));\n"
            "CREATE TABLE employees (\n"
            "  emp_id  NUMBER PRIMARY KEY,\n"
            "  dept_id NUMBER REFERENCES departments(dept_id) ON DELETE CASCADE\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "ON DELETE CASCADE を指定すると、親テーブルの行を削除したときに\n"
            "子テーブルの参照行も自動的に削除されます。\n\n"
            "・departments の dept_id=10 を DELETE\n"
            "→ employees の dept_id=10 を参照しているすべての行も自動DELETE\n\n"
            "ON DELETE オプションの比較:\n"
            "・ON DELETE CASCADE:  親削除 → 子行も削除\n"
            "・ON DELETE SET NULL: 親削除 → 子のFK列をNULLに更新\n"
            "・指定なし（デフォルト）: 子行が存在する場合は親の削除がエラーになる"
        ),
        "trap_reason": "「FK制約があると親行の削除は常にエラーになる」という誤解が多い。ON DELETE CASCADEを指定すれば子行ごと削除される。ON DELETE SET NULLとCASCADEの動作の違いも頻出の比較ポイント。",
        "choices": [
            {"choice_text": "FK制約違反のエラーになりDELETEが拒否される",                            "is_correct": False, "display_order": 0},
            {"choice_text": "departmentsの行のみが削除され、employeesのdept_id=10の行はNULLになる",  "is_correct": False, "display_order": 1},
            {"choice_text": "departmentsの行が削除され、dept_id=10を参照するemployeesの行も自動削除される", "is_correct": True, "display_order": 2},
            {"choice_text": "CASCADEはDROP TABLE等のDDLにのみ適用され、DELETEでは動作しない",         "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 48. CONSTRAINT（2つ選べ・難易度2）CHECK制約とNULL値
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": (
            "以下の定義において、price = NULL の行をINSERTするときのCHECK制約の動作として\n"
            "正しいものを2つ選んでください。\n\n"
            "CREATE TABLE products (\n"
            "  product_id NUMBER PRIMARY KEY,\n"
            "  price      NUMBER CHECK (price > 0)\n"
            ");\n\n"
            "INSERT INTO products VALUES (1, NULL);"
        ),
        "multi_select_count": 2,
        "explanation": (
            "CHECK制約はその条件がFALSEのときにのみ違反になります。\n"
            "NULL > 0 を評価すると結果は NULL（UNKNOWN）になります。\n\n"
            "OracleのCHECK制約:\n"
            "・条件が TRUE → 制約をパス（挿入成功）\n"
            "・条件が NULL（UNKNOWN）→ 制約をパス（挿入成功）\n"
            "・条件が FALSE → 制約違反（ORA-02290 エラー）\n\n"
            "したがって price = NULL の場合:\n"
            "NULL > 0 → NULL（UNKNOWN）→ CHECK制約をパス → INSERTが成功します。\n\n"
            "NULLを拒否したい場合はCHECK制約に加えてNOT NULL制約も必要です:\n"
            "price NUMBER NOT NULL CHECK (price > 0)"
        ),
        "trap_reason": "「NULL > 0 はFALSEとなりCHECK制約違反になる」という誤解が非常に多い。SQLの3値論理ではNULLを含む比較結果はNULL（UNKNOWN）となり、CHECKのFALSE判定に当たらない。NOT NULLとCHECKを組み合わせて初めてNULLを完全に拒否できる。",
        "choices": [
            {"choice_text": "NULL > 0 はNULL（UNKNOWN）と評価されCHECK制約をパスしINSERTが成功する",    "is_correct": True,  "display_order": 0},
            {"choice_text": "NULL > 0 はFALSEと評価されCHECK制約違反（ORA-02290）でエラーになる",       "is_correct": False, "display_order": 1},
            {"choice_text": "NULL値を拒否するにはCHECK制約だけでなくNOT NULL制約も別途追加する必要がある", "is_correct": True,  "display_order": 2},
            {"choice_text": "CHECK制約があるとNULL値は自動的に0に変換されてINSERTされる",               "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 49. CONSTRAINT（1つ選べ・難易度3）DEFERRABLE制約
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 3,
        "question_text": (
            "以下の制約定義の動作として正しいものを1つ選んでください。\n\n"
            "ALTER TABLE orders ADD CONSTRAINT fk_customer\n"
            "  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)\n"
            "  DEFERRABLE INITIALLY DEFERRED;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "DEFERRABLE INITIALLY DEFERRED の意味:\n\n"
            "・DEFERRABLE: トランザクション内で制約チェックのタイミングを遅延できる\n"
            "・INITIALLY DEFERRED: デフォルトで「COMMIT時にチェック」する動作\n\n"
            "この設定では:\n"
            "① INSERT/UPDATE の実行時点では制約チェックが行われない\n"
            "② COMMIT 時に制約チェックが実行される\n"
            "③ COMMIT 時に違反が検出されると、トランザクション全体がロールバックされる\n\n"
            "DEFERRABLE の主な用途:\n"
            "・親テーブルと子テーブルへの挿入順序を気にせずに1トランザクションで処理したいとき\n"
            "・循環参照がある制約の一時的な回避\n\n"
            "SET CONSTRAINT fk_customer IMMEDIATE; で特定トランザクションだけ即時チェックに変更可能。"
        ),
        "trap_reason": "「DEFERRABLEにすると制約が永遠にチェックされない」という誤解が多い。COMMIT時には必ず制約チェックが行われる。チェックを「毎文の直後」から「COMMIT時」に先送りするだけであり、制約そのものが無効化されるわけではない。",
        "choices": [
            {"choice_text": "INSERTとUPDATE時は制約チェックが行われず、ROLLBACKのみ制約が検証される",  "is_correct": False, "display_order": 0},
            {"choice_text": "各DML実行時の制約チェックが省略され、COMMIT時にまとめて制約チェックが行われる", "is_correct": True, "display_order": 1},
            {"choice_text": "DEFERRABLE制約は一切チェックされないため、FK違反のデータを恒久的に保存できる", "is_correct": False, "display_order": 2},
            {"choice_text": "INITIALLY DEFERREDにより、このFK制約は最初から無効（DISABLE）状態で定義される", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 50. CONSTRAINT（1つ選べ・難易度1）既存データと制約追加
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 1,
        "question_text": (
            "email 列に重複データが既に存在するテーブルに、以下のSQL文を実行した場合の\n"
            "動作として正しいものを1つ選んでください。\n\n"
            "ALTER TABLE employees ADD CONSTRAINT uq_email UNIQUE (email);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "ALTER TABLE ADD CONSTRAINT でUNIQUE制約を追加するとき、\n"
            "Oracleは既存のすべてのデータに対して制約チェックを実行します。\n\n"
            "・既存データに重複がある → ORA-02299 エラー（制約の追加が失敗）\n"
            "・制約は追加されない（テーブル定義は変更されない）\n\n"
            "既存データが制約を満たさない場合の対処法:\n"
            "① 重複データをクリーニングしてから制約を追加する\n"
            "② ENABLE NOVALIDATE オプションで既存データをチェックせずに有効化する:\n"
            "   ALTER TABLE employees ADD CONSTRAINT uq_email UNIQUE (email)\n"
            "   ENABLE NOVALIDATE;\n"
            "   （既存データは保証されないが新規DMLには制約が適用される）"
        ),
        "trap_reason": "「ALTER TABLE ADD CONSTRAINTは制約定義だけで既存データはチェックしない」という誤解が多い。実際はデフォルトでENABLE VALIDATEで追加されるため既存データがチェックされ、違反があれば追加自体が失敗する。",
        "choices": [
            {"choice_text": "重複データがあってもUNIQUE制約は定義されるが、新規INSERTのみに適用される",  "is_correct": False, "display_order": 0},
            {"choice_text": "既存データの重複がORA-02299エラーを引き起こし、制約の追加が失敗する",       "is_correct": True,  "display_order": 1},
            {"choice_text": "重複データは自動的に削除されてから制約が追加される",                       "is_correct": False, "display_order": 2},
            {"choice_text": "制約はDISABLE状態で追加されるため、既存データはチェックされない",          "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 51. CONSTRAINT（1つ選べ・難易度2）ENABLE NOVALIDATE
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文で制約を有効化した場合の動作として正しいものを1つ選んでください。\n\n"
            "ALTER TABLE employees ENABLE NOVALIDATE CONSTRAINT chk_salary;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "ENABLE NOVALIDATE は、制約を有効化しつつ既存データのチェックをスキップする設定です。\n\n"
            "有効化オプションの比較:\n"
            "・ENABLE VALIDATE（デフォルト）:\n"
            "  既存データすべてを検証してから制約を有効化\n"
            "  → 既存データに違反があればエラー\n\n"
            "・ENABLE NOVALIDATE:\n"
            "  既存データはチェックせず、今後のDML操作（INSERT/UPDATE）に対してのみ制約を適用\n"
            "  → 既存の違反データはそのまま残る\n\n"
            "用途: 大量の既存データがある場合に検証コストを回避しつつ、\n"
            "新規データの品質を保証したいときに使用します。"
        ),
        "trap_reason": "「ENABLEにすれば必ず既存データも検証される」という誤解が多い。NOVALIDATEを付けると既存データをチェックせずに制約が有効化される。既存の違反データはそのまま残り、新規DMLにのみ制約が適用される点に注意。",
        "choices": [
            {"choice_text": "既存のすべてのデータに対して制約チェックが実行され、違反があればエラーになる", "is_correct": False, "display_order": 0},
            {"choice_text": "既存データはチェックせず、今後のINSERT/UPDATEのみに制約が適用される",      "is_correct": True,  "display_order": 1},
            {"choice_text": "NOVALIDATE はDEFERRABLE制約にのみ指定できるため、非DEFERRABLE制約ではエラーになる", "is_correct": False, "display_order": 2},
            {"choice_text": "制約は有効化されるが、INSERTのみが対象でUPDATEには制約が適用されない",      "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 52. CONSTRAINT（1つ選べ・難易度2）複合PRIMARY KEY
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": (
            "以下のテーブル定義の複合PRIMARY KEYに関する説明として正しいものを1つ選んでください。\n\n"
            "CREATE TABLE enrollment (\n"
            "  student_id NUMBER,\n"
            "  course_id  NUMBER,\n"
            "  grade      VARCHAR2(2),\n"
            "  CONSTRAINT pk_enroll PRIMARY KEY (student_id, course_id)\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "複合PRIMARY KEYは、指定した複数列の組み合わせが一意であることを保証します。\n\n"
            "このテーブルでの挙動:\n"
            "・(student_id=1, course_id=101) の後に (student_id=1, course_id=102) はINSERT可能\n"
            "  → student_id が同じでも course_id が異なれば組み合わせが一意\n"
            "・(student_id=1, course_id=101) の重複はエラー\n"
            "・(student_id=NULL, course_id=101) はエラー\n"
            "  → PRIMARY KEY の構成列はすべてNOT NULLが強制される\n\n"
            "つまり「個別列の一意性」ではなく「列の組み合わせの一意性」が保証されます。"
        ),
        "trap_reason": "「複合PK内の各列が個別に一意でなければならない」という誤解が多い。実際は「組み合わせ」が一意であればよく、同じstudent_idやcourse_idを持つ行が複数存在してもよい。また、複合PK内の列はNULL不可という点も見落としやすい。",
        "choices": [
            {"choice_text": "student_idが同じ行は複数存在できない（student_id単独でも一意でなければならない）",       "is_correct": False, "display_order": 0},
            {"choice_text": "student_idが同じでもcourse_idが異なれば複数の行をINSERTできる（組み合わせの一意性）",    "is_correct": True,  "display_order": 1},
            {"choice_text": "course_idが同じ行は複数存在できない（course_id単独でも一意でなければならない）",         "is_correct": False, "display_order": 2},
            {"choice_text": "複合PK内のいずれかの列にNULL値を格納すれば複合値の一意性チェックが免除される",           "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 53. CONSTRAINT（2つ選べ・難易度2）PK と UNIQUE の違い
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": "PRIMARY KEY制約とUNIQUE制約の違いとして正しいものを2つ選んでください。",
        "multi_select_count": 2,
        "explanation": (
            "PRIMARY KEY と UNIQUE の主な違い:\n\n"
            "① NULL の扱い:\n"
            "・PRIMARY KEY: 構成列はすべて NOT NULL が強制（NULL 不可）\n"
            "・UNIQUE:       NULL 値は許容される（複数行の NULL も可）\n\n"
            "② テーブルあたりの定義数:\n"
            "・PRIMARY KEY: テーブルにつき1つのみ定義可能\n"
            "・UNIQUE:       複数定義可能\n\n"
            "③ インデックス（共通）:\n"
            "・どちらもOracleが自動的にUNIQUEインデックスを作成する\n\n"
            "④ 目的:\n"
            "・PRIMARY KEY: テーブルの主識別子（行を一意に特定する主要な列）\n"
            "・UNIQUE:       ビジネスキーなど補助的な一意性の保証"
        ),
        "trap_reason": "「UNIQUE制約もNULLを許可しない」「PRIMARY KEYとUNIQUEはほぼ同じ」という誤解が多い。NULLの扱いとテーブルあたりの定義数が主要な違い。どちらも自動でインデックスを作成する点は共通。",
        "choices": [
            {"choice_text": "PRIMARY KEY列はNULL不可だが、UNIQUE列はNULL値を許容する",                          "is_correct": True,  "display_order": 0},
            {"choice_text": "1つのテーブルにPRIMARY KEYは1つのみ定義できるが、UNIQUEは複数定義できる",          "is_correct": True,  "display_order": 1},
            {"choice_text": "PRIMARY KEY制約は自動でインデックスを作成するが、UNIQUE制約は作成しない",           "is_correct": False, "display_order": 2},
            {"choice_text": "UNIQUE制約はNOT NULL制約が暗黙的に付与されるためNULL値を格納できない",             "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 54. CONSTRAINT（1つ選べ・難易度1）USER_CONSTRAINTSのCONSTRAINT_TYPE
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 1,
        "question_text": (
            "データディクショナリビュー USER_CONSTRAINTS の CONSTRAINT_TYPE 列において、\n"
            "FOREIGN KEY制約に対応する値として正しいものを1つ選んでください。"
        ),
        "multi_select_count": 1,
        "explanation": (
            "USER_CONSTRAINTS の CONSTRAINT_TYPE 列の値:\n\n"
            "・P: PRIMARY KEY\n"
            "・U: UNIQUE\n"
            "・C: CHECK（NOT NULL 制約も内部的には CHECK として格納される）\n"
            "・R: REFERENTIAL（FOREIGN KEY）\n\n"
            "確認クエリの例:\n"
            "SELECT constraint_name, constraint_type\n"
            "FROM user_constraints\n"
            "WHERE table_name = 'EMPLOYEES';\n\n"
            "注意: NOT NULL は独自の制約タイプではなく、\n"
            "CHECK制約（type='C'）として USER_CONSTRAINTS に格納されます。"
        ),
        "trap_reason": "FK制約のCONSTRAINT_TYPEが 'F' や 'FK' と思い込むパターン。正しくは 'R'（Referential integrity の略）。また、NOT NULL が 'N' ではなく 'C' (CHECK) として格納される点も試験頻出の落とし穴。",
        "choices": [
            {"choice_text": "F",  "is_correct": False, "display_order": 0},
            {"choice_text": "R",  "is_correct": True,  "display_order": 1},
            {"choice_text": "K",  "is_correct": False, "display_order": 2},
            {"choice_text": "FK", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 55. CONSTRAINT（1つ選べ・難易度2）ON DELETE SET NULL
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CONSTRAINT",
        "difficulty": 2,
        "question_text": (
            "以下の定義において、employees テーブルの manager_id=5 の行（上司）をDELETEした場合の\n"
            "動作として正しいものを1つ選んでください。\n\n"
            "CREATE TABLE employees (\n"
            "  emp_id     NUMBER PRIMARY KEY,\n"
            "  emp_name   VARCHAR2(50),\n"
            "  manager_id NUMBER REFERENCES employees(emp_id) ON DELETE SET NULL\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "ON DELETE SET NULL を指定すると、親行を削除したときに\n"
            "子テーブルの参照列（FK列）が NULL に更新されます。\n\n"
            "この例での動作:\n"
            "① employees の emp_id=5（上司）の行を DELETE\n"
            "② その上司を参照していた部下の manager_id が NULL に自動更新される\n"
            "③ 部下の行は削除されずに残る\n\n"
            "ON DELETE オプションの比較:\n"
            "・CASCADE:      親削除 → 子行も削除される\n"
            "・SET NULL:     親削除 → 子のFK列がNULLになる（子行は残る）\n"
            "・指定なし:     子行が存在する場合は親の削除がエラーになる\n\n"
            "SET NULLを使うには、FK列がNOT NULL制約を持たないことが前提です。"
        ),
        "trap_reason": "ON DELETE SET NULLをON DELETE CASCADEと混同するパターン。CASCADEは子行を「削除」するが、SET NULLは子行を「残してFK列をNULLにする」。部下が消えるか残るかが最大の違い。",
        "choices": [
            {"choice_text": "manager_id=5を参照するすべての部下の行も自動的に削除される（CASCADE相当）",   "is_correct": False, "display_order": 0},
            {"choice_text": "FK制約違反のエラーになりDELETEが拒否される",                               "is_correct": False, "display_order": 1},
            {"choice_text": "上司の行が削除され、その上司を参照していた部下のmanager_idがNULLになる",     "is_correct": True,  "display_order": 2},
            {"choice_text": "上司の行が削除され、部下のmanager_idは0（ゼロ）に更新される",               "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 56. CORRELATED_SUBQUERY（1つ選べ・難易度1）相関副問い合わせの基本概念
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 1,
        "question_text": "相関副問い合わせ（Correlated Subquery）と通常の副問い合わせの違いとして正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "相関副問い合わせは「外側クエリの列を内側クエリが参照している」副問い合わせです。\n\n"
            "通常の副問い合わせ:\n"
            "・外側クエリから独立して1回だけ実行される\n"
            "・結果はキャッシュされて外側クエリ全体で再利用される\n"
            "例: WHERE salary = (SELECT MAX(salary) FROM employees)\n\n"
            "相関副問い合わせ:\n"
            "・外側クエリの各行を処理するたびに1回ずつ実行される\n"
            "・外側クエリの現在の行の列値を参照する\n"
            "例: WHERE salary > (SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = e1.dept_id)\n"
            "  → dept_id が e1（外側）の現在行に依存するため相関副問い合わせ"
        ),
        "trap_reason": "「副問い合わせはすべて先に1回実行される」という誤解が多い。相関副問い合わせは外側クエリの列を参照するため、外側の行ごとに毎回実行される。通常の副問い合わせとは実行タイミングが根本的に異なる。",
        "choices": [
            {"choice_text": "相関副問い合わせはSELECT句にのみ使用でき、WHERE句では使用できない",                  "is_correct": False, "display_order": 0},
            {"choice_text": "相関副問い合わせは外側クエリの列を参照し、外側の各行ごとに1回ずつ評価される",         "is_correct": True,  "display_order": 1},
            {"choice_text": "相関副問い合わせは通常の副問い合わせと同様に1回だけ実行されて結果が再利用される",      "is_correct": False, "display_order": 2},
            {"choice_text": "相関副問い合わせは集計関数（SUM, AVG等）と組み合わせて使用することができない",         "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 57. CORRELATED_SUBQUERY（1つ選べ・難易度1）EXISTSの動作
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 1,
        "question_text": (
            "以下のSQL文の動作として正しいものを1つ選んでください。\n\n"
            "SELECT e.emp_name\n"
            "FROM employees e\n"
            "WHERE EXISTS (\n"
            "  SELECT 1 FROM orders o WHERE o.emp_id = e.emp_id\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "EXISTS は、サブクエリが1行以上の行を返す場合に TRUE となります。\n\n"
            "このクエリの動作:\n"
            "・外側クエリの各 employee に対してサブクエリを実行\n"
            "・その employee の emp_id が orders に1件でも存在すれば EXISTS → TRUE\n"
            "・結果: orders テーブルに少なくとも1件の注文がある従業員の emp_name が返される\n\n"
            "重要なポイント:\n"
            "・EXISTS はサブクエリが返す値（SELECT 1 でも SELECT * でも）に関係なく、\n"
            "  行が存在するかどうかだけを判定する\n"
            "・最初の一致行が見つかった時点でサブクエリの評価を中断する（効率的）"
        ),
        "trap_reason": "「SELECT 1 は値1を返すだけでフィルタリングに使えない」と思い込むパターン。EXISTSはサブクエリが返す値の中身には関心がなく、行が1行でも存在するかどうかのみを判定する。",
        "choices": [
            {"choice_text": "サブクエリが正確に1行を返すemployeeのemp_nameが返される",              "is_correct": False, "display_order": 0},
            {"choice_text": "ordersテーブルに少なくとも1件の注文があるemployeeのemp_nameが返される", "is_correct": True,  "display_order": 1},
            {"choice_text": "SELECT 1は値1を返すため、emp_idが1のemployeeのemp_nameが返される",    "is_correct": False, "display_order": 2},
            {"choice_text": "EXISTSはINと同等の動作をするため、orders.emp_idに等しいemployeeが返される", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 58. CORRELATED_SUBQUERY（1つ選べ・難易度2）NOT EXISTSの動作
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文が返す部署として正しいものを1つ選んでください。\n\n"
            "SELECT d.dept_name\n"
            "FROM departments d\n"
            "WHERE NOT EXISTS (\n"
            "  SELECT 1 FROM employees e WHERE e.dept_id = d.dept_id\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "NOT EXISTS は、サブクエリが1行も返さない場合に TRUE となります。\n\n"
            "このクエリの動作:\n"
            "・各 department に対して、その部署に所属する employee を検索\n"
            "・1人も employee が存在しない場合 → NOT EXISTS → TRUE\n"
            "・結果: 従業員が1人も所属していない部署の dept_name が返される\n\n"
            "用途: 「片方のテーブルに存在しないデータを取得する」パターンで頻繁に使用されます。\n"
            "NOT IN と違い、NULLが混在しても正しく動作する点がメリットです。"
        ),
        "trap_reason": "NOT EXISTSをEXISTSと逆に理解するパターン。NOT EXISTSは「サブクエリが0行」のときTRUE。つまり「対応するデータが存在しない行」を取得するときに使う。EXISTSとNOT EXISTSの返す行の集合は正反対になる。",
        "choices": [
            {"choice_text": "少なくとも1人の従業員が所属している部署",                  "is_correct": False, "display_order": 0},
            {"choice_text": "1人も従業員が所属していない部署",                          "is_correct": True,  "display_order": 1},
            {"choice_text": "すべての部署（NOT EXISTSは常にTRUEになる）",               "is_correct": False, "display_order": 2},
            {"choice_text": "employeesテーブルとdepartmentsテーブルの両方に存在する部署", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 59. CORRELATED_SUBQUERY（2つ選べ・難易度2）IN と EXISTS の違い
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": "WHERE句で使う IN と EXISTS の違いとして正しいものを2つ選んでください。",
        "multi_select_count": 2,
        "explanation": (
            "IN と EXISTS の主な違い:\n\n"
            "① 評価の仕組み:\n"
            "・IN:     サブクエリの全結果を取得してリストを作成し、外側の値がリストに含まれるか比較する\n"
            "・EXISTS: サブクエリが1行でも返せばTRUE。最初の一致で評価を中断する\n\n"
            "② NULL値の扱い:\n"
            "・IN:     サブクエリにNULLが含まれると NOT IN が空の結果を返すことがある（重大な落とし穴）\n"
            "・EXISTS: サブクエリの結果に関わらず行の存在/非存在だけを判定するためNULLの影響を受けない\n\n"
            "③ パフォーマンス:\n"
            "・一般的にEXISTSは大きなサブクエリに対して効率的だが、\n"
            "  Oracleのオプティマイザが自動的に最適化するため常にEXISTSが速いとは限らない"
        ),
        "trap_reason": "「INとEXISTSは同じ結果を返す代替構文」という誤解が多い。NULL値が絡む NOT IN は特に危険で、サブクエリに1件でもNULLがあると0行が返ってしまう。NOT EXISTSならNULLがあっても正しく動作する。",
        "choices": [
            {"choice_text": "EXISTSはサブクエリが1行でも返せばTRUEとなり、INはすべての値とリスト比較を行う",     "is_correct": True,  "display_order": 0},
            {"choice_text": "NOT INはサブクエリにNULL値が含まれると空の結果を返す場合があるが、NOT EXISTSはNULLの影響を受けない", "is_correct": True, "display_order": 1},
            {"choice_text": "EXISTSはINより常に高速に実行されるため、INは使うべきではない",                    "is_correct": False, "display_order": 2},
            {"choice_text": "INはWHERE句のみで使用できるが、EXISTSはHAVING句でのみ使用できる",               "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 60. CORRELATED_SUBQUERY（1つ選べ・難易度2）NOT IN と NULL
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "departments.dept_id 列に NULL を含む行が存在するとき、以下のSQL文の実行結果として\n"
            "正しいものを1つ選んでください。\n\n"
            "SELECT emp_name FROM employees\n"
            "WHERE dept_id NOT IN (SELECT dept_id FROM departments);"
        ),
        "multi_select_count": 1,
        "explanation": (
            "NOT IN のサブクエリにNULLが含まれると、結果は0行（空の結果）になります。\n\n"
            "理由:\n"
            "SELECT dept_id FROM departments が (10, 20, NULL) を返すとすると:\n"
            "dept_id NOT IN (10, 20, NULL)\n"
            "→ dept_id != 10 AND dept_id != 20 AND dept_id != NULL\n"
            "→ dept_id != NULL は NULL（UNKNOWN）と評価される\n"
            "→ TRUE AND TRUE AND UNKNOWN → UNKNOWN → 行は除外される\n\n"
            "全行でUNKNOWNが発生するため、どの行も返されません。\n\n"
            "対策: NOT EXISTS を使うか、サブクエリにWHERE dept_id IS NOT NULL を追加する:\n"
            "WHERE dept_id NOT IN (SELECT dept_id FROM departments WHERE dept_id IS NOT NULL)"
        ),
        "trap_reason": "「NULLはNOT INで自動的に除外される」という誤解が非常に多い。SQLの3値論理では値とNULLの比較はUNKNOWNになり、NOT INの条件がUNKNOWNになった行はすべて除外される。結果として0行が返る。これは最もよくある副問い合わせのバグのひとつ。",
        "choices": [
            {"choice_text": "NULLの行は自動的に除外されて、一致しないemp_nameが返される",                     "is_correct": False, "display_order": 0},
            {"choice_text": "サブクエリにNULLが含まれるため、0行（空の結果）が返される",                       "is_correct": True,  "display_order": 1},
            {"choice_text": "ORA-01427: 単一行副問い合わせが複数行を返しましたというエラーが発生する",          "is_correct": False, "display_order": 2},
            {"choice_text": "NULLはINの比較で無視されるため、NULLを除いたdept_idと不一致の行が返される",        "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 61. CORRELATED_SUBQUERY（1つ選べ・難易度2・長文）相関副問い合わせの評価順序
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文のサブクエリの評価に関する正しい記述を1つ選んでください。\n\n"
            "SELECT e.emp_name, e.salary\n"
            "FROM employees e\n"
            "WHERE e.salary > (\n"
            "  SELECT AVG(salary)\n"
            "  FROM employees\n"
            "  WHERE dept_id = e.dept_id\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "このサブクエリは e.dept_id（外側クエリの列）を参照しているため相関副問い合わせです。\n\n"
            "評価の流れ:\n"
            "① 外側クエリが employees の1行目を取得（例: dept_id=10 の従業員）\n"
            "② サブクエリが実行される: SELECT AVG(salary) FROM employees WHERE dept_id = 10\n"
            "③ 外側クエリで salary > (dept_id=10の平均) を判定\n"
            "④ 次の行（例: dept_id=20）に移り、再びサブクエリが実行される\n"
            "⑤ これを全行に対して繰り返す\n\n"
            "つまり、サブクエリは外側クエリの行数分だけ実行されます。\n"
            "（通常の副問い合わせは1回しか実行されない点が大きな違い）"
        ),
        "trap_reason": "「副問い合わせは先に1回だけ実行される」という誤解が多い。このSQL文のサブクエリはe.dept_idという外側列を参照しているため相関副問い合わせであり、外側クエリの各行に対して毎回実行される。全社平均ではなく部署ごとの平均が計算されている点も重要。",
        "choices": [
            {"choice_text": "サブクエリは一度だけ実行され、全社の平均給与が計算されて外側クエリで再利用される",   "is_correct": False, "display_order": 0},
            {"choice_text": "サブクエリはemployeesの各行に対して1回ずつ実行され、その行の部署の平均給与が計算される", "is_correct": True, "display_order": 1},
            {"choice_text": "サブクエリはemployeesの全行のAVGを先に計算してから、外側クエリが実行される",        "is_correct": False, "display_order": 2},
            {"choice_text": "相関副問い合わせはWHERE句では使用できないためエラーになる",                       "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 62. CORRELATED_SUBQUERY（1つ選べ・難易度2・長文）UPDATE + 相関副問い合わせ
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "以下のUPDATE文の動作として正しいものを1つ選んでください。\n\n"
            "UPDATE employees e\n"
            "SET e.salary = e.salary * 1.1\n"
            "WHERE EXISTS (\n"
            "  SELECT 1 FROM dept_bonuses db\n"
            "  WHERE db.dept_id = e.dept_id\n"
            "  AND db.bonus_year = 2024\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "このUPDATE文は、相関副問い合わせのEXISTSを使って更新対象を絞り込んでいます。\n\n"
            "動作:\n"
            "① employees の各行に対してサブクエリを実行\n"
            "② その従業員の dept_id が dept_bonuses に bonus_year=2024 で存在すれば\n"
            "   EXISTS → TRUE → salary を10%増加\n"
            "③ 一致しない従業員は更新されない\n\n"
            "この書き方のポイント:\n"
            "・EXISTS は1件でも一致すれば更新対象になる\n"
            "・dept_bonuses に同じ dept_id で複数行あっても、EXISTS は最初の一致で止まるため\n"
            "  同じ従業員が複数回更新されることはない"
        ),
        "trap_reason": "「EXISTSに一致するのがdept_bonusesの行なのでdept_bonusesのsalaryが更新される」という誤解が多い。UPDATEの対象はあくまでFROM句（ここではemployees）の行。EXISTSは更新対象行を絞り込む条件として機能する。",
        "choices": [
            {"choice_text": "dept_bonusesテーブルのすべての行のsalaryが10%増加する",                          "is_correct": False, "display_order": 0},
            {"choice_text": "2024年のボーナス対象部署に所属するemployeesの給与が10%増加する",                  "is_correct": True,  "display_order": 1},
            {"choice_text": "dept_bonusesに複数の一致行がある場合、同じ従業員のsalaryが複数回増加する",         "is_correct": False, "display_order": 2},
            {"choice_text": "SELECT 1をサブクエリで使用しているため、更新する値が1になる",                     "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 63. CORRELATED_SUBQUERY（1つ選べ・難易度2・長文）DELETE + 相関副問い合わせ
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "以下のDELETE文が削除する行を正しく説明したものを1つ選んでください。\n\n"
            "DELETE FROM orders o\n"
            "WHERE NOT EXISTS (\n"
            "  SELECT 1 FROM customers c\n"
            "  WHERE c.customer_id = o.customer_id\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "NOT EXISTS は「サブクエリが0行を返す場合」にTRUEとなります。\n\n"
            "このDELETEの動作:\n"
            "① orders の各行に対してサブクエリを実行\n"
            "② その orders.customer_id が customers テーブルに存在しない場合\n"
            "   → NOT EXISTS → TRUE → その orders 行を削除\n"
            "③ customers に対応するレコードがある orders 行は削除されない\n\n"
            "この処理の用途:\n"
            "「孤立したデータ（参照先が存在しない行）の削除」によく使われます。\n"
            "例: 顧客が削除されたが、その顧客の注文が残っている場合のクリーニング"
        ),
        "trap_reason": "「NOT EXISTSはEXISTSの逆なので、customersに存在する注文が削除される」という逆の解釈をするパターン。NOT EXISTSは「対応するデータが存在しない（孤立した）行」を対象にする。削除されるのはcustomersに対応がない注文行。",
        "choices": [
            {"choice_text": "customersテーブルに存在するcustomer_idを持つordersの行が削除される",           "is_correct": False, "display_order": 0},
            {"choice_text": "customersテーブルに対応するcustomer_idが存在しない孤立したordersの行が削除される", "is_correct": True,  "display_order": 1},
            {"choice_text": "customersテーブルのすべての行が削除される",                                    "is_correct": False, "display_order": 2},
            {"choice_text": "ordersテーブルのcustomer_id列がNULLの行のみが削除される",                      "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 64. CORRELATED_SUBQUERY（1つ選べ・難易度2・長文）部署平均との比較
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文が返す従業員の説明として正しいものを1つ選んでください。\n\n"
            "SELECT e.emp_name, e.salary, e.dept_id\n"
            "FROM employees e\n"
            "WHERE e.salary > (\n"
            "  SELECT AVG(e2.salary)\n"
            "  FROM employees e2\n"
            "  WHERE e2.dept_id = e.dept_id\n"
            ");"
        ),
        "multi_select_count": 1,
        "explanation": (
            "このクエリは相関副問い合わせを使って「自分の部署の平均より高い給与の従業員」を取得します。\n\n"
            "動作:\n"
            "① employees e の各行を処理\n"
            "② その行の dept_id を使ってサブクエリを実行:\n"
            "   SELECT AVG(salary) FROM employees e2 WHERE e2.dept_id = （現在の行のdept_id）\n"
            "③ 現在の行の salary > そのdept_idの平均 なら結果に含める\n\n"
            "もし通常の副問い合わせ（相関なし）にすると:\n"
            "WHERE salary > (SELECT AVG(salary) FROM employees)\n"
            "→ 全社の平均と比較になる（別のクエリ）\n\n"
            "外側の e.dept_id を参照することで「部署ごとの」平均を計算できるのが相関副問い合わせの強み。"
        ),
        "trap_reason": "「e2.dept_id = e.dept_idの右辺にe（外側別名）が使われているのに気づかず、全社平均と比較していると誤解するパターン」が多い。e.dept_idは外側クエリの行の部署IDを指しており、行ごとに異なる値になる。",
        "choices": [
            {"choice_text": "会社全体の平均給与より高い給与の従業員",                  "is_correct": False, "display_order": 0},
            {"choice_text": "自分が所属する部署の平均給与より高い給与の従業員",         "is_correct": True,  "display_order": 1},
            {"choice_text": "全部署の中で平均給与が最も高い部署に所属する従業員",       "is_correct": False, "display_order": 2},
            {"choice_text": "全従業員の中で給与が上位50%に入る従業員",                "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 65. CORRELATED_SUBQUERY（2つ選べ・難易度3・長文）相関副問い合わせの識別
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "CORRELATED_SUBQUERY",
        "difficulty": 3,
        "question_text": (
            "次のSQL文のうち、相関副問い合わせが使用されているものを2つ選んでください。\n\n"
            "A: SELECT * FROM employees\n"
            "   WHERE salary = (SELECT MAX(salary) FROM employees)\n\n"
            "B: SELECT * FROM employees e1\n"
            "   WHERE salary > (SELECT AVG(salary) FROM employees e2\n"
            "                   WHERE e2.dept_id = e1.dept_id)\n\n"
            "C: SELECT * FROM departments\n"
            "   WHERE dept_id IN (SELECT dept_id FROM employees\n"
            "                     GROUP BY dept_id HAVING COUNT(*) > 5)\n\n"
            "D: SELECT * FROM employees e\n"
            "   WHERE EXISTS (SELECT 1 FROM orders o\n"
            "                 WHERE o.emp_id = e.emp_id AND o.amount > 1000)"
        ),
        "multi_select_count": 2,
        "explanation": (
            "相関副問い合わせの判別基準: サブクエリが外側クエリの列を参照しているか\n\n"
            "A: SELECT MAX(salary) FROM employees\n"
            "   → 外側クエリの列を参照していない → 通常の副問い合わせ\n\n"
            "B: WHERE e2.dept_id = e1.dept_id\n"
            "   → e1.dept_id は外側クエリ（e1）の列を参照 → 相関副問い合わせ ✓\n\n"
            "C: SELECT dept_id FROM employees GROUP BY dept_id HAVING COUNT(*) > 5\n"
            "   → 外側の departments 列を参照していない → 通常の副問い合わせ\n\n"
            "D: WHERE o.emp_id = e.emp_id\n"
            "   → e.emp_id は外側クエリ（e）の列を参照 → 相関副問い合わせ ✓\n\n"
            "BとDが相関副問い合わせです。"
        ),
        "trap_reason": "「EXISTSを使っていれば相関副問い合わせ」「INを使っていれば通常の副問い合わせ」という思い込みが多い。相関かどうかはEXISTSやINの種類ではなく、サブクエリが外側クエリの列（テーブル別名）を参照しているかどうかで判断する。",
        "choices": [
            {"choice_text": "A（WHERE salary = (SELECT MAX(salary) FROM employees)）",                "is_correct": False, "display_order": 0},
            {"choice_text": "B（WHERE salary > (SELECT AVG(salary) ... WHERE e2.dept_id = e1.dept_id)）", "is_correct": True, "display_order": 1},
            {"choice_text": "C（WHERE dept_id IN (SELECT dept_id FROM employees GROUP BY ...)）",      "is_correct": False, "display_order": 2},
            {"choice_text": "D（WHERE EXISTS (SELECT 1 FROM orders WHERE o.emp_id = e.emp_id)）",     "is_correct": True,  "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 66. INTERSECT（1つ選べ・難易度1）列数不一致エラー
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 1,
        "question_text": (
            "以下のSQL文の実行結果として正しいものを1つ選んでください。\n\n"
            "SELECT employee_id, first_name, salary\n"
            "FROM employees\n"
            "UNION\n"
            "SELECT department_id, department_name\n"
            "FROM departments;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "集合演算子（UNION/UNION ALL/INTERSECT/MINUS）を使用するとき、\n"
            "結合するすべてのSELECT文の選択列数は完全に一致している必要があります。\n\n"
            "このSQL文:\n"
            "・1つ目のSELECT: employee_id, first_name, salary → 3列\n"
            "・2つ目のSELECT: department_id, department_name → 2列\n\n"
            "列数が異なるため ORA-01789 エラーが発生します:\n"
            "ORA-01789: クエリ・ブロックの結果列数が不正です\n\n"
            "修正するには列数を合わせる必要があります（例: NULLを追加して列数を揃える）。"
        ),
        "trap_reason": "「列数が違っても少ない方に合わせて自動調整される」という誤解が多い。Oracleは列数の不一致を自動補完せず、必ずORA-01789エラーになる。NULLを明示的に追加して列数を合わせる必要がある。",
        "choices": [
            {"choice_text": "列数が異なるため少ない方（2列）に自動的に合わせてUNIONが実行される",      "is_correct": False, "display_order": 0},
            {"choice_text": "列数が異なるためORA-01789エラーが発生し実行されない",                    "is_correct": True,  "display_order": 1},
            {"choice_text": "1つ目のSELECTの最初の2列だけが2つ目とUNIONされる",                    "is_correct": False, "display_order": 2},
            {"choice_text": "不足する列にNULLが自動補完されて3列の結果が返される",                   "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 67. INTERSECT（1つ選べ・難易度1）結果列名の決定ルール
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 1,
        "question_text": (
            "以下のSQL文の結果セットの列名として正しいものを1つ選んでください。\n\n"
            "SELECT dept_id AS a_dept, dept_name AS a_name FROM dept_a\n"
            "UNION\n"
            "SELECT dept_id AS b_dept, dept_name AS b_name FROM dept_b;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "集合演算子を含む複合クエリの結果列名は、最初のSELECT文の列名（列別名）が使われます。\n\n"
            "このSQL文では:\n"
            "・最初のSELECT: AS a_dept, AS a_name\n"
            "・2番目のSELECT: AS b_dept, AS b_name\n\n"
            "結果列名 → a_dept, a_name（最初のSELECTの別名）\n\n"
            "この仕様により、ORDER BY 句でも最初のSELECTの列名を使ってソートできます:\n"
            "ORDER BY a_name DESC → 有効\n"
            "ORDER BY b_name DESC → エラー（2番目のSELECTの列名は使えない）"
        ),
        "trap_reason": "「最後のSELECTの列名が使われる」「両方のSELECTの列名が使える」という誤解が多い。集合演算子の結果列名は常に最初のSELECT文の列名・列別名が採用される。",
        "choices": [
            {"choice_text": "a_dept と a_name（最初のSELECT文の列別名）", "is_correct": True,  "display_order": 0},
            {"choice_text": "b_dept と b_name（最後のSELECT文の列別名）", "is_correct": False, "display_order": 1},
            {"choice_text": "dept_id と dept_name（元の列名）",           "is_correct": False, "display_order": 2},
            {"choice_text": "列名は定義されず位置番号（1, 2）のみで参照できる", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 68. INTERSECT（1つ選べ・難易度2）ORDER BYの位置制限
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文の実行結果として正しいものを1つ選んでください。\n\n"
            "SELECT dept_id FROM dept_a ORDER BY dept_id\n"
            "UNION\n"
            "SELECT dept_id FROM dept_b;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "集合演算子を含む複合クエリでは、ORDER BY は最後に一度だけ書く必要があります。\n"
            "個々のSELECT文の中にORDER BYを書くことはできません。\n\n"
            "このSQL文は ORDER BY が UNION の前にあるためエラーになります:\n"
            "ORA-00933: SQLコマンドが正しく終了されていません\n\n"
            "正しい書き方:\n"
            "SELECT dept_id FROM dept_a\n"
            "UNION\n"
            "SELECT dept_id FROM dept_b\n"
            "ORDER BY dept_id;  ← 最後にまとめて指定\n\n"
            "最後のORDER BYはUNION全体の結果に適用されます。"
        ),
        "trap_reason": "「最初のSELECTにORDER BYを書けばその部分だけソートされてUNIONされる」という誤解が多い。集合演算子とORDER BYを組み合わせる場合、ORDER BYは必ず最後のSELECTの後（全体の末尾）に1つだけ書く必要がある。",
        "choices": [
            {"choice_text": "最初のSELECTのORDER BYがUNION全体に適用されて実行される",            "is_correct": False, "display_order": 0},
            {"choice_text": "ORA-00933エラーが発生し、集合演算子の前にORDER BYは書けない",         "is_correct": True,  "display_order": 1},
            {"choice_text": "dept_aの結果のみORDER BYでソートされてからUNIONが実行される",         "is_correct": False, "display_order": 2},
            {"choice_text": "ORDER BYは自動的にUNIONの後ろに移動して全体の結果がソートされる",     "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 69. INTERSECT（1つ選べ・難易度2）NULL値の扱い
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": (
            "以下のデータでINTERSECTを実行した場合の結果として正しいものを1つ選んでください。\n\n"
            "table_a の col1 の値: 1, NULL\n"
            "table_b の col1 の値: NULL, 2\n\n"
            "SELECT col1 FROM table_a\n"
            "INTERSECT\n"
            "SELECT col1 FROM table_b;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "集合演算子（UNION/INTERSECT/MINUS）では、NULLは「同じNULL」として扱われます。\n\n"
            "通常の比較（WHERE句）では NULL = NULL はUNKNOWN（偽として扱われる）ですが、\n"
            "集合演算子の重複判定では NULL同士が一致するとみなされます。\n\n"
            "このINTERSECTの処理:\n"
            "・col1 = 1: table_b に 1 は存在しない → 共通行なし\n"
            "・col1 = NULL: table_b にも NULL が存在する → 共通行あり ✓\n\n"
            "結果: NULL が1行返される\n\n"
            "UNION の場合も同様に NULL の重複が除去されます（NULL が2つあっても1行になる）。"
        ),
        "trap_reason": "「NULL = NULLはUNKNOWNなので、INTERSECTでNULL同士は一致しない」という誤解が多い。集合演算子での重複判定はDISTINCTと同じ基準でNULL同士を等しいとみなす。通常のWHERE句での比較とは動作が異なる点が試験頻出のポイント。",
        "choices": [
            {"choice_text": "NULL = NULL はUNKNOWNのため一致行なし、0行が返される",  "is_correct": False, "display_order": 0},
            {"choice_text": "集合演算子はNULL同士を等しいとみなすためNULLが1行返される", "is_correct": True,  "display_order": 1},
            {"choice_text": "1とNULLの2行が返される",                                "is_correct": False, "display_order": 2},
            {"choice_text": "NULLを含む行はINTERSECTの対象外となり自動的に除外される", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 70. INTERSECT（1つ選べ・難易度2）集合演算子の優先順位
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": (
            "以下のSQL文の評価順序として正しいものを1つ選んでください。\n\n"
            "SELECT a FROM t1\n"
            "UNION\n"
            "SELECT a FROM t2\n"
            "INTERSECT\n"
            "SELECT a FROM t3;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "Oracle SQL では INTERSECT は UNION / UNION ALL / MINUS より優先度が高いです。\n\n"
            "このSQL文の評価順序:\n"
            "1. まず INTERSECT が評価される:\n"
            "   (t2 INTERSECT t3)\n"
            "2. 次に UNION が評価される:\n"
            "   t1 UNION (t2 INTERSECT t3)\n\n"
            "もし優先順位を変えたい場合は括弧を使います:\n"
            "  (SELECT a FROM t1 UNION SELECT a FROM t2)\n"
            "  INTERSECT SELECT a FROM t3;\n\n"
            "UNION / UNION ALL / MINUS は同じ優先順位で、左から右に評価されます。"
        ),
        "trap_reason": "「集合演算子はすべて同じ優先順位で左から右に評価される」という誤解が多い。INTERSECTはUNION/MINUS/UNION ALLより優先度が高い。括弧なしで混在させると、意図しない順序で評価される可能性がある。",
        "choices": [
            {"choice_text": "左から右に評価され、(t1 UNION t2) INTERSECT t3 となる",      "is_correct": False, "display_order": 0},
            {"choice_text": "INTERSECTが先に評価され、t1 UNION (t2 INTERSECT t3) となる", "is_correct": True,  "display_order": 1},
            {"choice_text": "UNIONが先に評価され、(t1 UNION t2) INTERSECT t3 となる",     "is_correct": False, "display_order": 2},
            {"choice_text": "すべての集合演算子は同じ優先順位のため括弧なしでは実行できない", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 71. INTERSECT（1つ選べ・難易度2）UNION ALLとUNIONの性能差
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": "UNION と UNION ALL のパフォーマンスに関する説明として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "UNION と UNION ALL のパフォーマンスの違い:\n\n"
            "UNION:\n"
            "・両方のSELECT結果を結合した後、重複行を除去する処理が必要\n"
            "・重複除去にはソートまたはハッシュ処理が発生するためコストが高い\n\n"
            "UNION ALL:\n"
            "・重複除去なしに結果を単純に結合するだけ\n"
            "・ソート/ハッシュ処理が不要なため一般的に高速\n"
            "・ただし重複行がそのまま残る\n\n"
            "重複が確実に存在しない場合（または重複を含めたい場合）は\n"
            "UNION ALL を使うと性能向上が期待できます。"
        ),
        "trap_reason": "「UNIONは重複を除去してくれるため処理が複雑になるが、UNION ALLは単純なので同じ速度」という誤解が多い。UNIONはソート/ハッシュによる重複除去が発生するためUNION ALLより遅い。重複が不要な場合はUNION ALLを意識的に選択する。",
        "choices": [
            {"choice_text": "UNIONはUNION ALLより常に高速に実行される",                                       "is_correct": False, "display_order": 0},
            {"choice_text": "UNION ALLは重複除去の処理が不要なためUNIONより一般的に高速だが重複行が含まれる",   "is_correct": True,  "display_order": 1},
            {"choice_text": "UNIONとUNION ALLの実行速度は常に同一である",                                    "is_correct": False, "display_order": 2},
            {"choice_text": "UNION ALLはNULL値を含む行を除外するため高速になる",                              "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 72. INTERSECT（1つ選べ・難易度2）MINUSの非対称性
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": (
            "以下のデータで2つの問い合わせを実行した場合の結果として正しいものを1つ選んでください。\n\n"
            "テーブルA の id 列の値: 1, 2, 3\n"
            "テーブルB の id 列の値: 2, 3, 4\n\n"
            "問い合わせ1: SELECT id FROM A MINUS SELECT id FROM B\n"
            "問い合わせ2: SELECT id FROM B MINUS SELECT id FROM A"
        ),
        "multi_select_count": 1,
        "explanation": (
            "MINUS は差集合演算子です。「左のSELECT結果から右のSELECT結果に含まれる行を除いたもの」を返します。\n\n"
            "問い合わせ1（A MINUS B）:\n"
            "A = {1, 2, 3}、B = {2, 3, 4}\n"
            "A にあってB にない行 = {1} → 1行\n\n"
            "問い合わせ2（B MINUS A）:\n"
            "B = {2, 3, 4}、A = {1, 2, 3}\n"
            "B にあってA にない行 = {4} → 1行\n\n"
            "MINUS は演算の順序（左右の入れ替え）で結果が変わります（非可換）。\n"
            "UNION や INTERSECT は順序を入れ替えても同じ結果になります（可換）。"
        ),
        "trap_reason": "「MINUSはどちらを左右に書いても同じ結果になる（交換法則が成立する）」という誤解が多い。MINUSは左側にしか存在しない行を返すため、左右を入れ替えると結果が変わる非可換な演算子。UNIONやINTERSECTとは異なる点に注意。",
        "choices": [
            {"choice_text": "両方とも {2, 3} の2行を返す（どちらも共通行を除いた結果）",      "is_correct": False, "display_order": 0},
            {"choice_text": "問い合わせ1は {1}、問い合わせ2は {4} を返す",                    "is_correct": True,  "display_order": 1},
            {"choice_text": "問い合わせ1は {1, 2, 3}、問い合わせ2は {2, 3, 4} を返す",        "is_correct": False, "display_order": 2},
            {"choice_text": "MINUSは演算順序に関わらず同じ結果を返す（交換法則が成立する）",   "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 73. INTERSECT（2つ選べ・難易度2）集合演算子の共通ルール
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": "集合演算子（UNION/UNION ALL/INTERSECT/MINUS）を使用するときの制約として正しいものを2つ選んでください。",
        "multi_select_count": 2,
        "explanation": (
            "集合演算子の共通ルール:\n\n"
            "① 列数の一致:\n"
            "  各SELECT文の選択列数は同じでなければならない（ORA-01789）\n\n"
            "② データ型の互換性:\n"
            "  対応する位置の列は同じデータ型か互換性のあるデータ型でなければならない（ORA-01790）\n\n"
            "③ 結果列名:\n"
            "  最初のSELECT文の列名・列別名が結果セットの列名として使用される\n\n"
            "④ ORDER BY の位置:\n"
            "  ORDER BYは複合クエリ全体の末尾に一度だけ記述できる\n"
            "  個々のSELECT文内には書けない（ORA-00933）\n\n"
            "⑤ 参照テーブルの制限:\n"
            "  各SELECT文は異なるテーブルを参照しても構わない"
        ),
        "trap_reason": "「集合演算子は同じテーブルしか参照できない」「列名が違っていてもよい」という誤解が多い。実際は異なるテーブルを自由に組み合わせられるが、列数と対応位置のデータ型の互換性は必須条件。",
        "choices": [
            {"choice_text": "各SELECT文の選択列数は同じでなければならない",                         "is_correct": True,  "display_order": 0},
            {"choice_text": "ORDER BYは各SELECT文に個別に指定することができる",                    "is_correct": False, "display_order": 1},
            {"choice_text": "結果セットの列名は最初のSELECT文の列名（列別名）が使用される",          "is_correct": True,  "display_order": 2},
            {"choice_text": "集合演算子を使うすべてのSELECT文は同じテーブルを参照しなければならない", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 74. INTERSECT（2つ選べ・難易度2）UNION vs UNION ALL の行数
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 2,
        "question_text": (
            "以下のデータで2つの問い合わせを実行した場合の説明として正しいものを2つ選んでください。\n\n"
            "テーブルA の id 列の値: 1, 2, 2, 3\n"
            "テーブルB の id 列の値: 2, 3, 4\n\n"
            "問い合わせ1: SELECT id FROM A UNION     SELECT id FROM B\n"
            "問い合わせ2: SELECT id FROM A UNION ALL SELECT id FROM B"
        ),
        "multi_select_count": 2,
        "explanation": (
            "問い合わせ1（UNION）:\n"
            "A = {1, 2, 2, 3}、B = {2, 3, 4}\n"
            "すべてを合わせて重複除去: {1, 2, 3, 4} → 4行\n\n"
            "問い合わせ2（UNION ALL）:\n"
            "A(4行) + B(3行) = 7行（重複保持）\n"
            "結果: {1, 2, 2, 3, 2, 3, 4} の7行\n\n"
            "UNION: A の重複 {2, 2} も除去対象になる点に注意\n"
            "UNION ALL: A・B をそのまま縦結合するため A 内の重複もそのまま残る"
        ),
        "trap_reason": "「UNIONはAとBの間の重複のみを除去し、A内の重複は残る」という誤解が多い。UNIONは全体の結果セットから重複を除去するため、A内の重複行（この例ではid=2の2行）も1行に縮約される。結果は4行になる。",
        "choices": [
            {"choice_text": "問い合わせ1（UNION）は重複除去後 {1, 2, 3, 4} の4行を返す",               "is_correct": True,  "display_order": 0},
            {"choice_text": "問い合わせ2（UNION ALL）は重複除去後 {1, 2, 3, 4} の4行を返す",           "is_correct": False, "display_order": 1},
            {"choice_text": "問い合わせ2（UNION ALL）はAの4行とBの3行を合わせた7行を返す",              "is_correct": True,  "display_order": 2},
            {"choice_text": "問い合わせ1（UNION）はAとBの間の重複のみ除去するため5行を返す",            "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 75. INTERSECT（1つ選べ・難易度3）複合クエリの優先順位
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "INTERSECT",
        "difficulty": 3,
        "question_text": (
            "以下のSQL文が内部的に評価される順序として正しいものを1つ選んでください。\n\n"
            "SELECT a FROM t1\n"
            "UNION\n"
            "SELECT a FROM t2\n"
            "INTERSECT\n"
            "SELECT a FROM t3\n"
            "UNION\n"
            "SELECT a FROM t4;"
        ),
        "multi_select_count": 1,
        "explanation": (
            "集合演算子の優先順位:\n"
            "・INTERSECT は UNION / UNION ALL / MINUS より優先度が高い\n"
            "・UNION / UNION ALL / MINUS は同じ優先順位で左から右に評価される\n\n"
            "このSQL文の評価順序:\n"
            "① まず INTERSECT を評価:\n"
            "   (t2 INTERSECT t3) を計算\n\n"
            "② 次に UNION を左から右に評価:\n"
            "   (t1 UNION (t2 INTERSECT t3)) UNION t4\n\n"
            "最終的な形: (t1 UNION (t2 INTERSECT t3)) UNION t4\n\n"
            "意図した順序と異なる可能性があるため、\n"
            "集合演算子を混在させる場合は括弧で優先順位を明示することを推奨します。"
        ),
        "trap_reason": "「集合演算子はすべて同じ優先順位で左から右に評価される」という誤解が多い。INTERSECTが最優先で評価されるため、括弧なしでは意図しない評価順序になる可能性がある。複数の集合演算子を混在させる場合は必ず括弧で明示すべき。",
        "choices": [
            {"choice_text": "左から右に評価: ((t1 UNION t2) INTERSECT t3) UNION t4",      "is_correct": False, "display_order": 0},
            {"choice_text": "INTERSECTが最優先: (t1 UNION (t2 INTERSECT t3)) UNION t4",   "is_correct": True,  "display_order": 1},
            {"choice_text": "UNION が最優先: (t1 UNION t2 UNION t4) INTERSECT t3",        "is_correct": False, "display_order": 2},
            {"choice_text": "右から左に評価: t1 UNION (t2 INTERSECT (t3 UNION t4))",      "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 76. DATA_DICTIONARY（1つ選べ・難易度1）USER_TAB_COLUMNS の用途
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 1,
        "question_text": "テーブルを構成する列の名前・データ型・NULL可否などの詳細情報を確認するためのデータディクショナリビューとして正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "各ディクショナリビューの役割:\n\n"
            "・USER_TABLES:      テーブル自体の情報（テーブル名・テーブルスペース等）\n"
            "・USER_TAB_COLUMNS: テーブルの列情報（列名・データ型・桁数・NULL可否・デフォルト値等）\n"
            "・USER_OBJECTS:     スキーマ内のオブジェクト一覧（テーブル・ビュー・プロシージャ等）\n"
            "・USER_CONSTRAINTS: テーブルに設定された制約情報\n\n"
            "列情報を調べるクエリ例:\n"
            "SELECT column_name, data_type, nullable\n"
            "FROM user_tab_columns\n"
            "WHERE table_name = 'EMPLOYEES';"
        ),
        "trap_reason": "「USER_TABLESでテーブルの全情報が確認できる」と思い込むパターン。USER_TABLESはテーブル単位の情報のみで列詳細は含まない。列の情報を得るにはUSER_TAB_COLUMNSを使う。",
        "choices": [
            {"choice_text": "USER_TABLES",      "is_correct": False, "display_order": 0},
            {"choice_text": "USER_TAB_COLUMNS", "is_correct": True,  "display_order": 1},
            {"choice_text": "USER_OBJECTS",     "is_correct": False, "display_order": 2},
            {"choice_text": "USER_COLUMNS",     "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 77. DATA_DICTIONARY（1つ選べ・難易度1）DUAL 表
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 1,
        "question_text": "Oracle の DUAL 表に関する説明として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "DUAL はSYSが所有する特別な1行1列のテーブルです。\n\n"
            "DUAL の特徴:\n"
            "・列名は DUMMY（VARCHAR2(1)、値は 'X'）\n"
            "・常に1行だけ返す\n"
            "・テーブルを参照しない式や関数の結果を取得したいときに使う\n\n"
            "主な用途例:\n"
            "  SELECT SYSDATE FROM DUAL;         → 現在日時の取得\n"
            "  SELECT 1 + 1 FROM DUAL;           → 算術計算\n"
            "  SELECT USER FROM DUAL;            → 接続ユーザー名の確認\n"
            "  SELECT seq.NEXTVAL FROM DUAL;     → シーケンス番号の取得\n\n"
            "Oracle 10g 以降は FROM DUAL を省略できる場合がありますが、\n"
            "互換性のため FROM DUAL を明示するのが一般的です。"
        ),
        "trap_reason": "「DUALは一時テーブルで各セッションで初期化される」「DUALは各ユーザーが持つ専用テーブル」という誤解が多い。DUALはSYSが所有する共有の特別テーブルであり、永続的に1行だけ存在する。",
        "choices": [
            {"choice_text": "DUAL は各ユーザーが自分のスキーマに作成した一時テーブルである",         "is_correct": False, "display_order": 0},
            {"choice_text": "DUAL はSYSが所有する1行1列の特別なテーブルで、式・関数の実行に使われる", "is_correct": True,  "display_order": 1},
            {"choice_text": "DUAL はNULL値のみを返すため算術計算の結果取得には使えない",             "is_correct": False, "display_order": 2},
            {"choice_text": "DUAL はFROM句なしのSELECT文でのみ参照できる特殊な構文である",          "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 78. DATA_DICTIONARY（1つ選べ・難易度2）USER_OBJECTS の STATUS
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 2,
        "question_text": "USER_OBJECTS ビューの STATUS 列が「INVALID」になる状況として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "USER_OBJECTS の STATUS 列には VALID / INVALID の2つの値が入ります。\n\n"
            "INVALID になる主なケース:\n"
            "・ビューが参照するテーブルが削除・変更された\n"
            "・プロシージャ/ファンクションが呼び出す別のオブジェクトが削除・変更された\n"
            "・ビューを DROP して再作成した場合、それを参照する別のビューが INVALID になる\n\n"
            "INVALID の挙動:\n"
            "・INVALIDなオブジェクトを使おうとするとOracleが自動再コンパイルを試みる\n"
            "・再コンパイルが成功すれば VALID に戻る\n"
            "・再コンパイルが失敗するとエラーになる\n\n"
            "確認クエリ: SELECT object_name, object_type, status FROM user_objects\n"
            "            WHERE status = 'INVALID';"
        ),
        "trap_reason": "「INVALIDはDML操作の失敗によって発生する」という誤解が多い。INVALIDはあくまで依存するオブジェクト（テーブル・プロシージャ等）の変更・削除によって発生する。INSERTの失敗やNULL値の存在とは無関係。",
        "choices": [
            {"choice_text": "そのテーブルへのINSERT操作が一度でも失敗した場合",                   "is_correct": False, "display_order": 0},
            {"choice_text": "そのビューやプロシージャが参照するオブジェクトが削除・変更された場合",  "is_correct": True,  "display_order": 1},
            {"choice_text": "そのテーブルの行数が0件になった場合",                                "is_correct": False, "display_order": 2},
            {"choice_text": "DBA権限を持つユーザーのオブジェクトに限りINVALIDになる",              "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 79. DATA_DICTIONARY（1つ選べ・難易度1）USER_SEQUENCES
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 1,
        "question_text": "USER_SEQUENCES ビューで確認できる情報として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "USER_SEQUENCES の主要な列:\n\n"
            "・SEQUENCE_NAME:  シーケンス名\n"
            "・MIN_VALUE:      最小値\n"
            "・MAX_VALUE:      最大値\n"
            "・INCREMENT_BY:   増分値\n"
            "・CYCLE_FLAG:     最大値超過時に最小値に戻るか（Y/N）\n"
            "・ORDER_FLAG:     順序保証（Y/N）\n"
            "・CACHE_SIZE:     キャッシュ件数（デフォルト20）\n"
            "・LAST_NUMBER:    次にキャッシュされる番号\n\n"
            "注意: LAST_NUMBER はキャッシュ済みの次番号であり、\n"
            "NEXTVAL で払い出した正確な最終値とは異なる場合があります。"
        ),
        "trap_reason": "「USER_SEQUENCESでNEXTVALを呼び出した回数が確認できる」「シーケンスの現在値がCURRVAL相当で確認できる」という誤解が多い。INCREMENT_BYやCYCLE_FLAGなどのシーケンス属性は確認できるが、使用回数や正確な現在値の取得は別手段が必要。",
        "choices": [
            {"choice_text": "NEXTVAL を呼び出した累計回数（シーケンスの使用履歴）",                   "is_correct": False, "display_order": 0},
            {"choice_text": "INCREMENT_BY（増分値）や CYCLE_FLAG（循環設定）などのシーケンス属性",    "is_correct": True,  "display_order": 1},
            {"choice_text": "シーケンスの現在の正確な使用値（CURRVAL と同等の情報）",                 "is_correct": False, "display_order": 2},
            {"choice_text": "シーケンスを参照しているテーブルと列の一覧",                            "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 80. DATA_DICTIONARY（1つ選べ・難易度2）USER_VIEWS の TEXT 列
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 2,
        "question_text": "Oracle でビューの定義SQL（CREATE VIEW 文で指定した SELECT 文）を確認するとき、USER_VIEWS の中で参照すべき列として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "USER_VIEWS の主要な列:\n\n"
            "・VIEW_NAME:    ビュー名\n"
            "・TEXT_LENGTH:  TEXTの文字数\n"
            "・TEXT:         ビューの定義SQL（SELECT文）が格納される（LONG型）\n\n"
            "確認クエリ例:\n"
            "SELECT text FROM user_views WHERE view_name = 'V_EMP';\n\n"
            "注意: TEXT列はLONG型なので、SQLクライアントによっては切り捨てられる場合があります。\n"
            "フルテキストを取得したい場合は DBMS_METADATA.GET_DDL() を使う方法もあります。"
        ),
        "trap_reason": "「USER_VIEWSにVIEW_TEXT列やSQL_TEXT列がある」という誤解が多い。正しい列名はTEXTのみ。また、USER_SOURCEと混同するパターンもある（USER_SOURCEはプロシージャ等のPL/SQL用で、ビューのSQLはUSER_VIEWS.TEXTに格納）。",
        "choices": [
            {"choice_text": "VIEW_TEXT",  "is_correct": False, "display_order": 0},
            {"choice_text": "TEXT",       "is_correct": True,  "display_order": 1},
            {"choice_text": "SQL_TEXT",   "is_correct": False, "display_order": 2},
            {"choice_text": "DEFINITION", "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 81. DATA_DICTIONARY（1つ選べ・難易度2）ディクショナリビューの読み取り専用
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 2,
        "question_text": "USER_TABLES や USER_CONSTRAINTS などのデータディクショナリビューに対して直接 UPDATE や DELETE を実行した場合の動作として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "データディクショナリビューは読み取り専用です。\n"
            "直接 UPDATE / DELETE / INSERT を実行することはできません。\n\n"
            "データディクショナリの変更はDDL文（CREATE / ALTER / DROP）を通じて行います:\n"
            "・テーブルを作成 → Oracle が USER_TABLES に自動的に行を追加\n"
            "・カラムを追加 → Oracle が USER_TAB_COLUMNS に自動的に行を追加\n"
            "・制約を削除 → Oracle が USER_CONSTRAINTS から自動的に行を削除\n\n"
            "ユーザーが直接ディクショナリビューを更新しようとすると:\n"
            "ORA-01031: 権限が不足しています\n"
            "または ORA-01751: 表は更新不可です　のエラーが発生します。"
        ),
        "trap_reason": "「DBA権限があればデータディクショナリを直接更新できる」という誤解が多い。DBA権限があってもディクショナリビューへの直接DMLは禁止されている。DBの構造変更はDDL文を介してOracleが自動的にディクショナリを更新する。",
        "choices": [
            {"choice_text": "DBA権限があれば直接UPDATE/DELETEが可能",                                     "is_correct": False, "display_order": 0},
            {"choice_text": "データディクショナリビューは読み取り専用のため直接の更新はできない",           "is_correct": True,  "display_order": 1},
            {"choice_text": "USER_プレフィックスのビューのみ所有者が直接更新できる",                       "is_correct": False, "display_order": 2},
            {"choice_text": "SELECT は可能だが INSERT のみ不可で UPDATE と DELETE は実行できる",           "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 82. DATA_DICTIONARY（1つ選べ・難易度2）USER_INDEXES で確認できない情報
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 2,
        "question_text": "USER_INDEXES ビューを参照しても確認できない情報として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "USER_INDEXES で確認できる主な情報:\n"
            "・INDEX_NAME:    インデックス名\n"
            "・TABLE_NAME:    インデックスが設定されているテーブル名\n"
            "・INDEX_TYPE:    インデックスの種類（NORMAL / BITMAP / FUNCTION-BASED NORMAL 等）\n"
            "・UNIQUENESS:    一意か否か（UNIQUE / NONUNIQUE）\n"
            "・STATUS:        インデックスの状態（VALID / UNUSABLE 等）\n"
            "・TABLESPACE_NAME: 格納先テーブルスペース名\n\n"
            "USER_INDEXES で確認できない情報:\n"
            "・インデックスを構成する列名と順序 → USER_IND_COLUMNS で確認\n\n"
            "SELECT index_name, column_name, column_position\n"
            "FROM user_ind_columns WHERE table_name = 'EMPLOYEES';"
        ),
        "trap_reason": "「USER_INDEXESでインデックスを構成する列の詳細も確認できる」という誤解が多い。USER_INDEXESはインデックス単位の情報のみ。列の詳細（どの列が何番目の構成列か）はUSER_IND_COLUMNSで確認する必要がある。",
        "choices": [
            {"choice_text": "インデックスが設定されているテーブル名（TABLE_NAME）",             "is_correct": False, "display_order": 0},
            {"choice_text": "インデックスを構成する各列の名前と定義順（列の詳細情報）",           "is_correct": True,  "display_order": 1},
            {"choice_text": "インデックスが一意か非一意かの区別（UNIQUENESS）",                  "is_correct": False, "display_order": 2},
            {"choice_text": "インデックスの種類（INDEX_TYPE: NORMAL / BITMAP 等）",             "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 83. DATA_DICTIONARY（2つ選べ・難易度2）USER_TABLES で確認できる情報
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 2,
        "question_text": "USER_TABLES ビューで確認できる情報として正しいものを2つ選んでください。",
        "multi_select_count": 2,
        "explanation": (
            "USER_TABLES の主要な列:\n\n"
            "確認できるもの:\n"
            "・TABLE_NAME:      テーブル名\n"
            "・TABLESPACE_NAME: テーブルスペース名\n"
            "・NUM_ROWS:        統計情報として記録された行数\n"
            "・STATUS:          テーブルの状態（VALID 等）\n"
            "・AVG_ROW_LEN:     平均行長\n"
            "・ROW_MOVEMENT:    行移動設定\n\n"
            "確認できないもの（別のビューが必要）:\n"
            "・列の詳細情報      → USER_TAB_COLUMNS\n"
            "・制約の情報        → USER_CONSTRAINTS\n"
            "・インデックスの情報 → USER_INDEXES"
        ),
        "trap_reason": "「USER_TABLESでテーブルの全情報（列・制約・インデックス等）が確認できる」という誤解が多い。USER_TABLESはテーブル単位のメタ情報のみを持ち、列や制約の詳細は別のディクショナリビューで確認する必要がある。",
        "choices": [
            {"choice_text": "TABLE_NAME（テーブル名）",                        "is_correct": True,  "display_order": 0},
            {"choice_text": "そのテーブルを構成する列の名前とデータ型",         "is_correct": False, "display_order": 1},
            {"choice_text": "TABLESPACE_NAME（テーブルスペース名）",            "is_correct": True,  "display_order": 2},
            {"choice_text": "そのテーブルに定義された制約名と制約タイプ",        "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 84. DATA_DICTIONARY（1つ選べ・難易度2）USER_SYNONYMS とスコープ
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 2,
        "question_text": "Oracle のシノニムとデータディクショナリビューの関係として正しいものを1つ選んでください。",
        "multi_select_count": 1,
        "explanation": (
            "シノニムには2種類あります:\n\n"
            "プライベートシノニム（CREATE SYNONYM）:\n"
            "・作成したユーザーのスキーマに所属する\n"
            "・USER_SYNONYMS で確認できる\n\n"
            "パブリックシノニム（CREATE PUBLIC SYNONYM）:\n"
            "・全ユーザーからアクセス可能なシノニム\n"
            "・USER_SYNONYMS では確認できない\n"
            "・ALL_SYNONYMS または DBA_SYNONYMS で確認できる\n\n"
            "USER_SYNONYMS の主要な列:\n"
            "・SYNONYM_NAME:  シノニム名\n"
            "・TABLE_OWNER:   参照先オブジェクトの所有者\n"
            "・TABLE_NAME:    参照先の実際のオブジェクト名\n"
            "・DB_LINK:       リモートDBへのリンク名（あれば）"
        ),
        "trap_reason": "「USER_SYNONYMSはパブリックシノニムを確認するためのビュー」という誤解が多い。USER_SYNONYMSは現在ユーザーが所有するプライベートシノニムのみ表示する。パブリックシノニムはALL_SYNONYMS等で確認できる。",
        "choices": [
            {"choice_text": "USER_SYNONYMSには現在ユーザーが所有するプライベートシノニムの情報が格納される",    "is_correct": True,  "display_order": 0},
            {"choice_text": "USER_SYNONYMSはパブリックシノニム専用のビューで、プライベートシノニムはALL_SYNONYMSで確認できる", "is_correct": False, "display_order": 1},
            {"choice_text": "USER_SYNONYMSはSYSスキーマのシノニムのみを表示する",                           "is_correct": False, "display_order": 2},
            {"choice_text": "シノニムはデータディクショナリに記録されず、セッション変数として管理される",        "is_correct": False, "display_order": 3},
        ],
    },

    # ──────────────────────────────────────────────────────────────────
    # 85. DATA_DICTIONARY（2つ選べ・難易度3）USER_SOURCE の対象オブジェクト
    # ──────────────────────────────────────────────────────────────────
    {
        "category": "DATA_DICTIONARY",
        "difficulty": 3,
        "question_text": "次のオブジェクトのうち、USER_SOURCE ビューでソースコードを確認できるものを2つ選んでください。",
        "multi_select_count": 2,
        "explanation": (
            "USER_SOURCE はPL/SQLオブジェクトのソースコードを格納するビューです。\n\n"
            "USER_SOURCE で確認できるオブジェクト:\n"
            "・PROCEDURE（ストアドプロシージャ）\n"
            "・FUNCTION（ストアドファンクション）\n"
            "・PACKAGE / PACKAGE BODY\n"
            "・TRIGGER（トリガー）\n"
            "・TYPE / TYPE BODY\n\n"
            "USER_SOURCE では確認できないもの（別ビューが必要）:\n"
            "・ビューの定義SQL → USER_VIEWS.TEXT\n"
            "・テーブルのDDL文 → DBMS_METADATA.GET_DDL() を使用\n"
            "・シーケンスの属性 → USER_SEQUENCES\n\n"
            "USER_SOURCE の主要列: NAME（オブジェクト名）、TYPE（種類）、LINE（行番号）、TEXT（ソース行）"
        ),
        "trap_reason": "「USER_SOURCEでビューのSELECT文も確認できる」という誤解が多い。ビューの定義SQLはUSER_VIEWS.TEXTに格納されており、USER_SOURCEにはない。USER_SOURCEはPL/SQLコードを持つオブジェクト（プロシージャ・トリガー等）専用。",
        "choices": [
            {"choice_text": "CREATE VIEW で作成したビューのSELECT定義文",                   "is_correct": False, "display_order": 0},
            {"choice_text": "CREATE PROCEDURE で作成したPL/SQLプロシージャのコード",         "is_correct": True,  "display_order": 1},
            {"choice_text": "CREATE TABLE で作成したテーブルのDDL文",                       "is_correct": False, "display_order": 2},
            {"choice_text": "CREATE TRIGGER で作成したトリガーのPL/SQLコード",              "is_correct": True,  "display_order": 3},
        ],
    },

]
