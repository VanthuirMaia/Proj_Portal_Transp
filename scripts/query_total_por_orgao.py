import duckdb
from pathlib import Path

db_path = Path("data/warehouse/portal_transparencia.duckdb")
con = duckdb.connect(str(db_path))

query = """
SELECT
    orgao,
    SUM(valor_pago) AS total_pago
FROM staging_despesas_por_orgao
GROUP BY orgao
ORDER BY total_pago DESC
"""

result = con.execute(query).fetchall()

print("Total pago por orgão:")
for row in result:
    print(row)
