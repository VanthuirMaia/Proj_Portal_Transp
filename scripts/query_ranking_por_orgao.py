import duckdb
from pathlib import Path

db_path = Path("data/warehouse/portal_transparencia.duckdb")
con = duckdb.connect(str(db_path))

query = """
SELECT
    orgao,
    SUM(valor_pago) AS total_pago,
    RANK() OVER (ORDER BY SUM(valor_pago) DESC) AS ranking
FROM staging_despesas_por_orgao
GROUP BY orgao
ORDER BY ranking
"""

# RANK, DENSE_RANK OU ROW_NUMBER podem ser usados dependendo do critério desejado

result = con.execute(query).fetchall()

print("Ranking de orgãos por total pago:")
for row in result:
    print(row)

