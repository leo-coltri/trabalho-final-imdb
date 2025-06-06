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
    """
    Inicia o processo de ingestão de perguntas do Redis para o PostgreSQL.

    Cria a tabela no PostgreSQL se não existir e inicia um loop infinito
    para processar as perguntas armazenadas na lista Redis 'pilha_questions'.
    Em cada iteração do loop, verifica se existe uma chave na lista, a
    processa e a remove da lista. Caso não exista, o loop vai para a
    próxima iteração. O loop também espera 1 segundo entre cada iteração.
    """
    create_table_if_not_exists(pg_conn)
    print("Iniciando processo de ingestão")
    while True:
        value = r.lpop('pilha_questions')
        if value:
            print(f"Processando chave: {value}")
            insert_into_postgres_questions(r, pg_conn, value)
        time.sleep(1)

if __name__ == "__main__":
    main()