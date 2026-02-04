# PROJ_PORTAL_TRANSP

**Projeto prático de Engenharia de Dados com dados públicos reais**

---

## 📌 Visão Geral

Este projeto foi criado com o objetivo de **aprender Engenharia de Dados de forma prática**, utilizando **dados reais do Portal da Transparência do Governo Federal**, enfrentando problemas reais de qualidade, padronização, volume e integração.

O foco não é apenas consumir dados, mas **construir um pipeline completo**, bem estruturado, versionável e evolutivo, seguindo boas práticas utilizadas em ambientes profissionais.

> Aprendizado baseado em **projeto**, não em exemplos artificiais.

---

## 🎯 Objetivos do Projeto

- Consumir APIs públicas reais com autenticação e paginação
- Implementar camadas de dados (**RAW → STAGING → ANALYTICS**)
- Tratar dados inconsistentes e sem contrato
- Aplicar regras de **qualidade de dados**
- Evoluir para modelagem dimensional
- Utilizar **dbt** para transformação, testes e documentação
- Preparar o pipeline para orquestração com **Airflow**
- Consolidar o projeto como **case técnico de portfólio**

---

## 🗂️ Estrutura de Pastas

```
PROJ_PORTAL_TRANSP/
│
├── data/
│   ├── raw/            # Dados brutos extraídos da API (CSV com timestamp)
│   ├── staging/        # Dados tratados e tipados (Parquet)
│   ├── warehouse/      # Banco DuckDB com dados carregados
│   └── analytics/      # Dados prontos para análise (Gold Layer)
│
├── src/
│   ├── ingestion/      # Scripts de ingestão (API → RAW)
│   ├── transformation/ # Scripts de transformação (RAW → STAGING)
│   ├── quality/        # Regras e validações de qualidade de dados
│   └── utils/          # Funções utilitárias
│
├── scripts/            # Scripts DuckDB (queries, views, carga)
├── dbt/                # Projeto dbt (modelagem, testes, docs)
├── airflow/            # Orquestração (planejado)
├── notebooks/          # Análises exploratórias e validações
│
├── requirements.txt
├── .env.exemplo
└── README.md
```

---

## 🔌 Fonte de Dados

**Portal da Transparência – Governo Federal**

### Endpoint inicial (dimensão)

```
GET /api-de-dados/orgaos-siafi
```

### Endpoint principal (fato)

```
GET /api-de-dados/despesas/por-orgao
```

Os dados utilizados são os mesmos disponibilizados publicamente no portal, acessados via API REST.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.12
- Pandas
- Requests
- PyArrow (Parquet)
- DuckDB (warehouse analítico)
- dotenv
- dbt (próxima etapa)
- Airflow (planejado)

---

## 🧭 Roteiro do Projeto (checkpoint)

| Etapa | Descrição | Status |
|-------|-----------|--------|
| 1 | Escolher fonte de dados (API pública) | ✅ Concluído |
| 2 | Ingestão Python: consumir API e salvar CSV | ✅ Concluído |
| 3 | Camada staging: CSV → Parquet | ✅ Concluído |
| 4 | Regras de qualidade de dados | ✅ Concluído |
| 5 | Warehouse DuckDB: inicializar e carregar staging | ✅ Concluído |
| 6 | Queries analíticas SQL (agregações, rankings) | ✅ Concluído |
| 7 | Views analíticas no DuckDB | ✅ Concluído |
| 8 | Projeto dbt com testes e documentação | 🔲 Pendente |
| 9 | Visualização (Power BI / Metabase) | 🔲 Pendente |
| 10 | Orquestração com Airflow | 🔲 Pendente |

---

## ✅ O que já foi implementado

### Infraestrutura
- Estrutura de pastas organizada e versionada
- Configuração segura de variáveis de ambiente (`.env.exemplo`)

### Ingestão (`src/ingestion/`)
- Consumo paginado de APIs públicas
- Scripts: `fetch_orgaos_siafi.py`, `fetch_despesas_por_orgao.py`
- Camada **RAW** com versionamento por timestamp

### Transformação (`src/transformation/`)
- Tipagem explícita e normalização de valores monetários
- Conversão CSV → Parquet
- Saída em `data/staging/`

### Qualidade (`src/quality/`)
- Validação de valores não negativos
- Coerência financeira: `empenhado ≥ liquidado ≥ pago`
- Unicidade lógica por `(ano, codigo_orgao)`

### Warehouse DuckDB (`scripts/`)
- Banco inicializado em `data/warehouse/portal_transparencia.duckdb`
- Staging carregado no DuckDB
- Queries analíticas: totais e rankings por órgão
- View analítica `vw_ranking_orgaos` criada

---

## 📊 Dataset Atual (STAGING)

Tabela: `stg_despesas_por_orgao`

| Campo                 | Tipo      |
| --------------------- | --------- |
| ano                   | int       |
| codigo_orgao          | string    |
| orgao                 | string    |
| codigo_orgao_superior | string    |
| orgao_superior        | string    |
| valor_empenhado       | float     |
| valor_liquidado       | float     |
| valor_pago            | float     |
| carga_timestamp       | timestamp |

---

## 🧪 Qualidade de Dados

Regras implementadas:

- Valores monetários não negativos
- Coerência financeira entre empenhado, liquidado e pago
- Unicidade lógica por `(ano, codigo_orgao)`

Essas regras servem como base para contratos de dados e testes futuros no dbt.

---

## 🚀 Próximos Passos

### Fase 1 — dbt (próximo)

- [ ] Criar projeto dbt em `dbt/` com adapter DuckDB
- [ ] Configurar `profiles.yml` apontando para o warehouse
- [ ] Modelar staging (`stg_despesas_por_orgao`) no dbt
- [ ] Criar marts/dimensões (ex: `dim_orgaos`, `fct_despesas`)
- [ ] Implementar testes declarativos (`unique`, `not_null`, `relationships`)
- [ ] Gerar documentação automática (`dbt docs generate`)

### Fase 2 — Visualização

- [ ] Conectar Power BI ou Metabase ao DuckDB
- [ ] Criar dashboard com métricas de despesas
- [ ] Explorar séries temporais e comparativos

### Fase 3 — Automação

- [ ] Criar DAG no Airflow para orquestrar o pipeline
- [ ] Implementar alertas e retry em caso de falha
- [ ] Documentar o projeto como case de portfólio

---

## 📌 Filosofia do Projeto

Este projeto segue uma abordagem **realista**:

- Dados reais são imperfeitos
- APIs falham
- Ambientes quebram
- Qualidade precisa ser explícita
- Engenharia vem antes de dashboards

> O objetivo não é apenas fazer funcionar,  
> é **entender, justificar e sustentar cada decisão técnica**.

---

## ✍️ Autor

Projeto desenvolvido para estudo e aprofundamento em **Engenharia de Dados**, com foco em aprendizado contínuo baseado em projetos reais.
