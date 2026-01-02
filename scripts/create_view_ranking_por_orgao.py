import duckdb
from pathlib import Path

db_path = Path("data/warehouse/portal_transparencia.duckdb")
con = duckdb.connect(str(db_path))

query = """
CREATE OR REPLACE VIEW vw_ranking_orgao_valor_pago AS
SELECT
    orgao,
    SUM(valor_pago) AS total_pago,
    DENSE_RANK() OVER (ORDER BY SUM(valor_pago) DESC) AS ranking
FROM staging_despesas_por_orgao
GROUP BY orgao
"""

con.execute(query)

print("View vw_ranking_orgao_valor_pago criada com sucesso")
