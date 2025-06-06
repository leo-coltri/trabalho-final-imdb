# Projeto de Ingestão de Dados para Sistema de Quiz

Este projeto desenvolve um mecanismo de ingestão de dados para um sistema de Quiz, utilizando **Redis** como banco de dados intermediário e **PostgreSQL** como Data Warehouse (DW). O foco está na estruturação dos dados e na geração de indicadores para análise.

## Tecnologias Utilizadas

* **Redis**: Banco de dados intermediário para o processo de ingestão.
* **Python**: Linguagem utilizada para o ETL (Extração, Transformação e Carga) dos dados, responsável pela coleta e ingestão no PostgreSQL.
* **PostgreSQL**: Data Warehouse (DW) onde os dados são armazenados e estruturados.
* **FastAPI**: Framework web Python para a API (porta 8000/docs).
* **Docker Compose**: Para orquestração e execução dos serviços.

---

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o projeto em sua máquina:

### 1. Iniciar os Serviços com Docker Compose

Abra o terminal na raiz do projeto e execute o comando:

```bash
docker compose up -d
```

Este comando irá iniciar os containers do Redis, PostgreSQL e da aplicação FastAPI em segundo plano.

### 2. Acessar a Documentação da API

Após os serviços estarem rodando, você pode acessar a documentação interativa da API no seu navegador:

```
http://localhost:8000/docs
```

Aqui você encontrará todos os endpoints disponíveis para interação com o sistema.

### 5. Postar Perguntas e Respostas

Utilize os endpoints da API (`http://localhost:8000/docs`) para postar novas perguntas e suas respectivas respostas. Isso geralmente envolve requisições POST para `/questions` e `/answers` (ou endpoints similares, conforme definidos em sua API).

### 6. Executar os Processos de ETL

Para processar os dados do Redis para o PostgreSQL, você precisará executar os scripts de ETL. Assumindo que você tem endpoints ou scripts para isso, execute-os na seguinte ordem:

#### a. Executar `pool_questions`

Este processo é responsável por extrair as perguntas do Redis e carregá-las no PostgreSQL.

```bash
python pool_questions.py
```

#### b. Executar `pool_answers`

Este processo extrai as respostas do Redis e as relaciona com as perguntas no PostgreSQL.

```bash
python pool_answers.py
```

---

### 7. Executar as Consultas SQL de Indicadores (`queries.py`)

Para gerar e visualizar os indicadores do sistema, você precisará executar as consultas SQL presentes no arquivo `queries.py`.

1.  **Escolha a Consulta**:
    Abra o arquivo `queries.py` em um editor de texto. No final do arquivo, você encontrará uma variável (como `cursor.execute(query7)` no seu exemplo) que define qual consulta será executada.

    Para executar uma das 7 consultas, **modifique o número da query** na linha `cursor.execute(queryX)` para a consulta desejada (por exemplo, `query1`, `query2`, etc.).

2.  **Salve o Arquivo**:
    Após alterar a variável, salve as modificações no arquivo `queries.py`.

3.  **Execute o Script Python**:
    Execute o script `queries.py` dentro do container da sua aplicação. Primeiro, encontre o nome do seu container de aplicação (usando `docker ps` se você não souber).

    ```bash
    python queries.py
    ```

    A saída da consulta será exibida diretamente no seu terminal.

---