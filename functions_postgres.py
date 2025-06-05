def create_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS questions4 (
                key INT PRIMARY KEY,
                question_text VARCHAR,
                alternativa_a VARCHAR,
                alternativa_b VARCHAR,
                alternativa_c VARCHAR,
                alternativa_d VARCHAR,
                alternativa_correta VARCHAR,
                dificuldade VARCHAR,
                assunto VARCHAR
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS answers4 (
                answer_key VARCHAR PRIMARY KEY,
                question_id INT,
                alternativa_escolhida VARCHAR,
                datahora VARCHAR,
                usuario VARCHAR,
                nro_tentativa INT
            );
        """)
    conn.commit()

def insert_into_postgres_answers(r, conn, answer_key):
    value = r.hgetall(answer_key)
    meu_dict_str = {k.decode(): v.decode() for k, v in value.items()}

    if meu_dict_str:
        #print(meu_dict_str.keys())
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO answers4
                (answer_key, question_id, alternativa_escolhida, datahora, usuario, nro_tentativa)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (answer_key) DO NOTHING;
                """, (
                    answer_key,                      # sua chave única gerada (ex: UUID, hash, etc)
                    meu_dict_str['question_id'],
                    meu_dict_str['alternativa_escolhida'],
                    meu_dict_str['datahora'],
                    meu_dict_str['usuario'],
                    meu_dict_str['nro_tentativa']
                )
            )
            conn.commit()

def insert_into_postgres_questions(r, conn, key):
    value = r.hgetall(key)
    meu_dict_str = {k.decode(): v.decode() for k, v in value.items()}

    key_str = key.decode()
    question_id = int(key_str.split(":")[1])
    # Inserir uma coluna de data/hora de inserção
    if meu_dict_str:
        #print(meu_dict_str.keys())
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO questions3
                (key, question_text, alternativa_a, alternativa_b, alternativa_c, alternativa_d, alternativa_correta, dificuldade, assunto)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (key) DO NOTHING;
                """, (
                    question_id,
                    meu_dict_str['question_text'],
                    meu_dict_str['alternativa_a'],
                    meu_dict_str['alternativa_b'],
                    meu_dict_str['alternativa_c'],
                    meu_dict_str['alternativa_d'],
                    meu_dict_str['alternativa_correta'],
                    meu_dict_str['dificuldade'],
                    meu_dict_str['assunto']
                )
            )
        conn.commit()