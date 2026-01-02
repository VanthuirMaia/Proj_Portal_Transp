import duckdb
from pathlib import Path

db_path = Path("data/warehouse/portal_transparencia.duckdb")
con = duckdb.connect(str(db_path))

query = """
SELECT
    ranking,
    orgao,
    total_pago
FROM vw_ranking_orgao_valor_pago
ORDER BY ranking
"""

result = con.execute(query).fetchall()

print("Ranking de órgãos (via VIEW):")
for row in result:
    print(row)
