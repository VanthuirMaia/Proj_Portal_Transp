{{ config(materialized='table') }}

WITH orgaos_unicos AS (
    SELECT DISTINCT
        codigo_orgao,
        orgao,
        codigo_orgao_superior,
        orgao_superior
    FROM {{ ref('stg_despesas_por_orgao') }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY codigo_orgao) AS SK_ORGAO,
    codigo_orgao,
    orgao AS nome_orgao,
    codigo_orgao_superior,
    orgao_superior AS nome_orgao_superior
FROM orgaos_unicos