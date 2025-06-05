import time
import redis
import psycopg2
from functions_postgres import *

r = redis.Redis(host='localhost', port=6379, db=0)

pg_conn = psycopg2.connect(
    host='localhost',
    port=5432,
    dbname='dw',
    user='user',
    password='senhaForte2025'
)


def main():
    create_table_if_not_exists(pg_conn)
    print("Iniciando processo de ingestão")
    while True:
        value = r.lpop('pilha_answers')
        if value:
            print(f"Processando chave: {value}")
            insert_into_postgres_answers(r, pg_conn, value)
        time.sleep(1)

if __name__ == "__main__":
    main()