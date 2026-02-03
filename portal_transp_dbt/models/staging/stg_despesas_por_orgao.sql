{{ config(materialized='table') }}

SELECT
    ano,
    codigo_orgao,
    orgao,
    codigo_orgao_superior,
    orgao_superior,
    valor_empenhado,
    valor_liquidado,
    valor_pago,
    carga_timestamp
FROM {{ source('raw', 'staging_despesas_por_orgao') }}
WHERE valor_empenhado >= 0
  AND valor_liquidado >= 0
  AND valor_pago >= 0