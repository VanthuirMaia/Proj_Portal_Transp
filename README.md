# Portal da Transparência - Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![dbt](https://img.shields.io/badge/dbt-1.11-FF694B?style=flat&logo=dbt&logoColor=white)](https://getdbt.com)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.4-FEF000?style=flat&logo=duckdb&logoColor=black)](https://duckdb.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.53-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Pipeline completo de Engenharia de Dados que consome, transforma e analisa dados reais de despesas públicas do **Portal da Transparência do Governo Federal Brasileiro**.

![Pipeline Architecture](<https://img.shields.io/badge/Architecture-Medallion_(Bronze→Silver→Gold)-blue?style=for-the-badge>)

---

## Sobre o Projeto

Este projeto implementa um **pipeline de dados end-to-end** utilizando dados reais da API do Portal da Transparência. O objetivo é demonstrar habilidades práticas em Engenharia de Dados através de um caso de uso real, enfrentando desafios genuínos de qualidade, padronização e integração de dados.

### Destaques

- **Dados Reais**: Consumo de APIs públicas com autenticação e paginação
- **Arquitetura Medallion**: Camadas Bronze (Raw), Silver (Staging) e Gold (Analytics)
- **Modelagem Dimensional**: Star Schema com dbt (dimensões e fatos)
- **Qualidade de Dados**: Validações automatizadas em múltiplas camadas
- **Dashboard Interativo**: Visualizações em tempo real com Streamlit

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PIPELINE DE DADOS                                  │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │   API REST   │   Portal da Transparência
    │   (Fonte)    │   api.portaldatransparencia.gov.br
    └──────┬───────┘
           │
           ▼
┌─────────────────────┐
│   1. INGESTÃO       │   Python + Requests
│   ─────────────     │   • Autenticação por API Key
│   src/ingestion/    │   • Paginação automática
│                     │   • Rate limiting (0.3s)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   2. RAW (Bronze)   │   CSV com timestamp
│   ─────────────     │   • Dados brutos
│   data/raw/         │   • Audit trail
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   3. STAGING        │   Parquet + Validações
│   (Silver)          │   • Tipagem explícita
│   ─────────────     │   • Normalização monetária
│   data/staging/     │   • Quality checks
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   4. WAREHOUSE      │   DuckDB
│   ─────────────     │   • OLAP columnar
│   data/warehouse/   │   • SQL analytics
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   5. TRANSFORM      │   dbt + Star Schema
│   (Gold)            │   ├── stg_despesas_por_orgao
│   ─────────────     │   ├── dim_orgaos
│   portal_transp_dbt │   └── fct_despesas
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   6. DASHBOARD      │   Streamlit + Plotly
│   ─────────────     │   • KPIs interativos
│   dashboard/        │   • Visualizações
└─────────────────────┘
```

---

## Stack Tecnológica

| Camada            | Tecnologia                  | Propósito                         |
| ----------------- | --------------------------- | --------------------------------- |
| **Ingestão**      | Python, Requests            | Consumo de API REST com paginação |
| **Armazenamento** | Parquet, DuckDB             | Formatos colunares otimizados     |
| **Transformação** | dbt, Pandas                 | Modelagem dimensional e ETL       |
| **Qualidade**     | dbt tests, Python           | Validações e contratos de dados   |
| **Orquestração**  | Apache Airflow 2.10.4       | Orquestração de workflows         |
| **Containers**    | Docker & Docker Compose     | Containerização                   |
| **Visualização**  | Streamlit, Plotly           | Dashboard interativo              |
| **Versionamento** | Git                         | Controle de versão                |

---

## Estrutura do Projeto

```
PROJ_PORTAL_TRANSP/
│
├── docker/
│   ├── Dockerfile.ingestion
│   ├── Dockerfile.transformation
│   ├── Dockerfile.load
│   └── Dockerfile.dbt
│
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── plugins/
│
├── docker-compose.yml
│
├── data/
│   ├── raw/                    # Bronze: CSVs brutos da API
│   ├── staging/                # Silver: Parquet tratados
│   ├── warehouse/              # DuckDB database
│   └── analytics/              # Gold: Dados agregados
│
├── src/
│   ├── ingestion/              # Scripts de ingestão
│   │   ├── fetch_orgaos_siafi.py
│   │   └── fetch_despesas_por_orgao.py
│   │
│   ├── transformation/         # ETL: Raw → Staging
│   │   └── stage_despesas_por_orgao.py
│   │
│   └── quality/                # Validações de qualidade
│       └── check_despesas_por_orgao.py
│
├── portal_transp_dbt/          # Projeto dbt
│   ├── models/
│   │   ├── staging/
│   │   │   └── stg_despesas_por_orgao.sql
│   │   └── marts/
│   │       ├── dim_orgaos.sql
│   │       └── fct_despesas.sql
│   └── tests/
│
├── scripts/                    # Utilitários DuckDB
│   ├── init_duckdb.py
│   └── load_staging_to_duckdb.py
│
├── dashboard/
│   └── app.py                  # Streamlit dashboard
│
├── run_pipeline.py             # Orquestrador principal
├── requirements.txt
└── .env.exemplo
```

---

## Modelo de Dados

### Star Schema

```
                    ┌─────────────────┐
                    │   dim_orgaos    │
                    ├─────────────────┤
                    │ sk_orgao (PK)   │
                    │ codigo_orgao    │
                    │ nome_orgao      │
                    │ codigo_superior │
                    │ nome_superior   │
                    └────────┬────────┘
                             │
                             │ 1:N
                             │
                    ┌────────▼────────┐
                    │  fct_despesas   │
                    ├─────────────────┤
                    │ sk_orgao (FK)   │
                    │ ano             │
                    │ valor_empenhado │
                    │ valor_liquidado │
                    │ valor_pago      │
                    │ carga_timestamp │
                    └─────────────────┘
```

### Dicionário de Dados

| Campo             | Tipo    | Descrição                    |
| ----------------- | ------- | ---------------------------- |
| `ano`             | INTEGER | Ano fiscal (2020-2024)       |
| `codigo_orgao`    | VARCHAR | Código SIAFI do órgão        |
| `orgao`           | VARCHAR | Nome do órgão                |
| `valor_empenhado` | DOUBLE  | Valor comprometido (R$)      |
| `valor_liquidado` | DOUBLE  | Valor verificado (R$)        |
| `valor_pago`      | DOUBLE  | Valor efetivamente pago (R$) |

---

## Qualidade de Dados

O pipeline implementa validações em múltiplas camadas:

### Regras de Negócio

| Regra                     | Descrição                             | Camada  |
| ------------------------- | ------------------------------------- | ------- |
| **Valores não negativos** | Todos os campos monetários ≥ 0        | Staging |
| **Coerência financeira**  | empenhado ≥ liquidado ≥ pago          | Staging |
| **Unicidade lógica**      | Sem duplicatas em (ano, codigo_orgao) | Staging |

### Testes dbt

```yaml
# schema.yml
models:
  - name: stg_despesas_por_orgao
    columns:
      - name: ano
        tests: [not_null]
      - name: codigo_orgao
        tests: [not_null]
      - name: valor_empenhado
        tests: [not_null]

  - name: fct_despesas
    columns:
      - name: sk_orgao
        tests:
          - relationships:
              to: ref('dim_orgaos')
              field: sk_orgao
```

---

## Como Executar

### Pré-requisitos

- Python 3.12+
- Chave de API do Portal da Transparência ([solicitar aqui](https://portaldatransparencia.gov.br/api-de-dados))

### Instalação

```bash
# Clonar repositório
git clone https://github.com/seu-usuario/portal-transparencia-pipeline.git
cd portal-transparencia-pipeline

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.exemplo .env
# Editar .env com sua API_KEY
```

### Executar Pipeline Completo

```bash
# Rodar todo o pipeline
python run_pipeline.py
```

### Executar Etapas Individuais

```bash
# 1. Ingestão (API → Raw)
python src/ingestion/fetch_despesas_por_orgao.py

# 2. Transformação (Raw → Staging)
python src/transformation/stage_despesas_por_orgao.py

# 3. Carregar no DuckDB
python scripts/load_staging_to_duckdb.py

# 4. Executar modelos dbt
cd portal_transp_dbt
dbt run
dbt test

# 5. Iniciar dashboard
streamlit run dashboard/app.py
```

---

## Dashboard

O dashboard interativo exibe:

- **KPIs**: Total empenhado, liquidado e pago
- **Top 10 Órgãos**: Ranking por valor pago
- **Evolução Temporal**: Série histórica 2020-2024
- **Filtros**: Por ano e órgão

```bash
# Iniciar dashboard
streamlit run dashboard/app.py
```

Acesse: `http://localhost:8501`

---

## API de Dados

### Endpoints Utilizados

| Endpoint                               | Descrição                    |
| -------------------------------------- | ---------------------------- |
| `GET /api-de-dados/orgaos-siafi`       | Lista de órgãos SIAFI        |
| `GET /api-de-dados/despesas/por-orgao` | Despesas agregadas por órgão |

### Autenticação

```python
headers = {
    "chave-api-dados": os.getenv("API_KEY"),
    "User-Agent": "data-engineering-study"
}
```

---

## Roadmap

| #  | Etapa                        | Status        |
|----|------------------------------|---------------|
| 1  | Ingestão de dados via API    | ✅ Concluído  |
| 2  | Camada Raw (Bronze)          | ✅ Concluído  |
| 3  | Camada Staging (Silver)      | ✅ Concluído  |
| 4  | Validações de qualidade      | ✅ Concluído  |
| 5  | Warehouse DuckDB             | ✅ Concluído  |
| 6  | Modelagem dimensional (dbt)  | ✅ Concluído  |
| 7  | Testes automatizados         | ✅ Concluído  |
| 8  | Dashboard Streamlit          | ✅ Concluído  |
| 9  | CI/CD pipeline               | 🔲 Pendente   |
| 10 | Orquestração com Airflow     | ✅ Concluído  |
| 11 | Documentação dbt Docs        | 🔲 Pendente   |

---

## O que já foi implementado

### Orquestração com Airflow (`airflow/`, `docker/`)
- Airflow configurado via Docker Compose (webserver + scheduler + postgres)
- Dockerfiles isolados para cada etapa do pipeline:
  - `Dockerfile.ingestion`: Container para ingestão via API
  - `Dockerfile.transformation`: Container para transformação CSV → Parquet
  - `Dockerfile.load`: Container para carga no DuckDB
  - `Dockerfile.dbt`: Container para modelagem e testes dbt
- DAG `portal_transparencia_pipeline` implementada com DockerOperator
- Cada task executa em container isolado (sem conflitos de dependências)
- Retry automático configurado (2 tentativas, 5 minutos de delay)
- Logs estruturados e rastreabilidade completa de execuções
- Schedule semanal (`@weekly`) com possibilidade de execução manual
- Arquitetura production-ready e cross-platform

---

## Próximos Passos

- [ ] Deploy do Airflow em ambiente produtivo (Kubernetes ou cloud managed)
- [ ] Implementar alertas via email/Slack em caso de falhas
- [ ] Expandir ingestão para outros órgãos e categorias de despesas
- [ ] Adicionar testes de integração end-to-end
- [ ] Criar dashboard executivo com métricas de pipeline (SLA, data freshness)

---

## 🐳 Como Executar o Projeto

### Pré-requisitos
- Docker Desktop instalado
- Git

### Executar Pipeline Completo com Airflow

1. Clone o repositório
2. Navegue até a pasta do projeto
3. Suba os containers: `docker-compose up -d`
4. Acesse o Airflow: http://localhost:8080 (usuário: admin, senha: admin1234)
5. Ative e execute a DAG `portal_transparencia_pipeline`

### Visualizar Dashboard
```bash
cd dashboard
streamlit run app.py
```

Acesse: http://localhost:8501

### Parar os serviços
```bash
docker-compose down
```

---

## Aprendizados

Este projeto demonstra competências práticas em:

- **Data Engineering**: Construção de pipelines ETL/ELT robustos
- **Data Modeling**: Modelagem dimensional (Star Schema)
- **Data Quality**: Implementação de validações e contratos
- **Modern Data Stack**: dbt, DuckDB, Streamlit
- **API Integration**: Consumo de APIs REST com autenticação
- **Best Practices**: Código limpo, versionamento, documentação

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Autor

Desenvolvido como projeto de portfólio em **Engenharia de Dados**.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/vanthuir-maia-47767810b/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/VanthuirMaia)
[![Email](https://img.shields.io/badge/Email-vanmaiasf@gmail.com-red?style=flat&logo=gmail&logoColor=white)](mailto:vanmaiasf@gmail.com)
[![Email](https://img.shields.io/badge/Dev-vanthuir.dev@gmail.com-orange?style=flat&logo=gmail&logoColor=white)](mailto:vanthuir.dev@gmail.com)

---

<p align="center">
  <i>Dados reais. Problemas reais. Soluções profissionais.</i>
</p>
