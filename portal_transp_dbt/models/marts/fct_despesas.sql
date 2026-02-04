{{ config(materialized='table') }}

SELECT
    d.sk_orgao,
    s.ano,
    s.valor_empenhado,
    s.valor_liquidado,
    s.valor_pago,
    s.carga_timestamp
FROM {{ ref('stg_despesas_por_orgao') }} s
INNER JOIN {{ ref('dim_orgaos') }} d
    ON s.codigo_orgao = d.codigo_orgao