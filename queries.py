import time
import redis
import psycopg2

r = redis.Redis(host='localhost', port=6379, db=0)

pg_conn = psycopg2.connect(
    host='localhost',
    port=5432,
    dbname='dw',
    user='user',
    password='senhaForte2025'
)

## Alternativas Mais Votadas: Alternativas que receberam mais votos por questão;
query1 = """
WITH votos AS (
    SELECT 
        a.question_id, 
        a.alternativa_escolhida, 
        COUNT(*) AS total_votos,
        ROW_NUMBER() OVER (PARTITION BY a.question_id ORDER BY COUNT(*) DESC) AS ranking
    FROM tb_answers a
    GROUP BY a.question_id, a.alternativa_escolhida
)

SELECT 
    question_id, 
    alternativa_escolhida, 
    total_votos
FROM votos
WHERE ranking = 1
ORDER BY total_votos desc;
"""

## Questões mais acertadas: Questões com maior índice de acerto;
query2 = """
SELECT 
    q.question_id,
    SUM(CASE WHEN a.alternativa_escolhida = q.alternativa_correta THEN 1 ELSE 0 END) AS total_acertos,
    COUNT(*) AS total_respostas,
    ROUND(100 * SUM(CASE WHEN a.alternativa_escolhida = q.alternativa_correta THEN 1 ELSE 0 END) / COUNT(*), 2) AS percentual_acerto
FROM (
	SELECT key as question_id, alternativa_correta FROM tb_questions) q
LEFT JOIN (
 SELECT question_id, alternativa_escolhida FROM tb_answers
) a 
ON q.question_id = a.question_id
GROUP BY q.question_id
ORDER BY percentual_acerto DESC;
"""

## Questões com mais abstenções: Ou seja, que tiveram menos votos válidos;
query3 = """
SELECT
    q.key,
    q.question_text,
    COUNT(a.question_id) AS total_respostas
FROM
    tb_questions q
LEFT JOIN
    tb_answers a ON q.key = a.question_id
GROUP BY
    q.key, q.question_text
ORDER BY
    total_respostas ASC;
"""

## Tempo médio de resposta por questão: Tempo médio que os alunos responderam cada questão;
query4 = """
WITH answers_time AS (
    SELECT 
        question_id, 
        AVG(EXTRACT(EPOCH FROM TO_TIMESTAMP(datahora, 'DD/MM/YYYY HH24:MI'))) as media_segundos
    FROM tb_answers
    GROUP BY question_id
)
SELECT 
    *
FROM answers_time
ORDER BY media_segundos ASC;
"""


## Alunos com maior acerto e mais rápidos: rank final dos alunos;
query5 = """
WITH RespostasCorretas AS (
    SELECT
        a.usuario,
        a.question_id,
        a.alternativa_escolhida,
        q.alternativa_correta,
        a.nro_tentativa,
        a.datahora,
        ROW_NUMBER() OVER (PARTITION BY a.usuario, a.question_id ORDER BY a.nro_tentativa, a.datahora) as rn
    FROM
        tb_answers a
    JOIN
        tb_questions q ON a.question_id = q.key
    WHERE
        a.alternativa_escolhida = q.alternativa_correta
)
SELECT
    rc.usuario,
    COUNT(DISTINCT rc.question_id) AS total_acertos,
    AVG(rc.nro_tentativa) AS media_tentativas_corretas,
    RANK() OVER (ORDER BY COUNT(DISTINCT rc.question_id) DESC, AVG(rc.nro_tentativa) ASC) AS rank_final
FROM
    RespostasCorretas rc
WHERE
    rc.rn = 1
GROUP BY
    rc.usuario
ORDER BY
    rank_final ASC;
"""

## Alunos com maior acerto: Independente do tempo que levaram para responder cada pergunta;
query6 = """
SELECT 
    a.usuario, 
    COUNT(*) AS total_respostas,
    SUM(CASE WHEN a.alternativa_escolhida = q.alternativa_correta THEN 1 ELSE 0 END) AS total_acertos
FROM tb_answers a
JOIN tb_questions q ON a.question_id = q.key
GROUP BY a.usuario
ORDER BY total_acertos DESC;

"""

## Alunos mais rápidos: Independente do número de acertos; (Ranking baseado na quantidade de vezes que um aluno foi mais rápido em responder uma questão)
query7 = """
WITH rank_questao AS (
SELECT 
    question_id,
    usuario,
    ROW_NUMBER() OVER (PARTITION BY question_id ORDER BY TO_TIMESTAMP(datahora, 'DD/MM/YYYY HH24:MI') ASC) AS mais_rapido_questao
  FROM tb_answers
),

contagem_mais_rapidos AS (
    SELECT 
        usuario,
        COUNT(*) AS total_vezes_mais_rapido
    FROM rank_questao
    WHERE mais_rapido_questao = 1
    GROUP BY usuario
)
SELECT * 
FROM contagem_mais_rapidos
ORDER BY total_vezes_mais_rapido DESC;
"""

cursor = pg_conn.cursor()

## Executar as queries
cursor.execute(query1)
for row in cursor.fetchall():
    print(row)