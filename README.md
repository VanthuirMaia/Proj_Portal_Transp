# PROJ_PORTAL_TRANSP

Estrutura inicial para estudos de engenharia de dados.

## Estrutura de Pastas

- **data/raw/**: Dados brutos
- **data/staging/**: Dados intermediários
- **data/analytics/**: Dados prontos para análise
- **src/ingestion/**: Scripts de ingestão de dados
- **src/transformation/**: Scripts de transformação de dados
- **src/utils/**: Utilitários
- **dbt/**: Projetos DBT
- **airflow/**: Orquestração (vazio por enquanto)
- **notebooks/**: Jupyter Notebooks

## Requisitos

Ver arquivo `requirements.txt`.

Fonte de dados inicial:
Portal da Transparência - endpoint orgaos-siafi

Endpoint:
GET /api-de-dados/orgaos-siafi

Objetivo:
Construir ingestão paginada de dados institucionais,
tratando inconsistências e versionando dados brutos.
