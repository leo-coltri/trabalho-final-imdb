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