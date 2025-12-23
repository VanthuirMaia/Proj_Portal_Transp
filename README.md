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
│   ├── raw/            # Dados brutos extraídos da API (imutáveis)
│   ├── staging/        # Dados tratados e tipados (Silver Layer)
│   └── analytics/      # Dados prontos para análise (Gold Layer)
│
├── src/
│   ├── ingestion/      # Scripts de ingestão (API → RAW)
│   ├── transformation/ # Scripts de transformação (RAW → STAGING)
│   ├── quality/        # Regras e validações de qualidade de dados
│   └── utils/          # Funções utilitárias
│
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
- dotenv
- dbt (planejado)
- PostgreSQL / DuckDB (planejado)
- Airflow (planejado)

---

## ✅ O que já foi implementado

- Estrutura de pastas organizada e versionada
- Configuração segura de variáveis de ambiente (`.env.exemplo`)
- Ingestão paginada de dados via API pública
- Camada **RAW** com versionamento por timestamp
- Transformação para **STAGING (Silver Layer)**:
  - Tipagem explícita
  - Normalização de valores monetários inconsistentes
  - Conversão para formato **Parquet**
- Criação de regras iniciais de **qualidade de dados**
- Validação de coerência financeira:
  - `empenhado ≥ liquidado ≥ pago`
- Separação clara entre **dimensões** e **fatos**

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

1. Consolidar regras de qualidade como contratos formais
2. Criar projeto **dbt**
3. Modelar camadas **staging** e **marts**
4. Implementar testes declarativos no dbt
5. Gerar documentação automática
6. Carregar dados em banco analítico
7. Criar consultas SQL analíticas
8. Explorar visualizações
9. Orquestrar pipeline com Airflow
10. Transformar o projeto em **case de portfólio técnico**

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
