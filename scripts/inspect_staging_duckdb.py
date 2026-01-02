import duckdb
from pathlib import Path

db_path = Path("data/warehouse/portal_transparencia.duckdb")

con = duckdb.connect(str(db_path))

# Verificar se a tabela existe
tables = con.execute("SHOW TABLES").fetchall()
print("Tabelas no DuckDB:", tables)

# Visualizar o Schema da tabela
schema = con.execute("DESCRIBE staging_despesas_por_orgao").fetchall()
print("\nSchema da tabela:")
for col in schema:
    print(col)

# Contar o número de registros na tabela
count = con.execute(
    "SELECT COUNT(*) FROM staging_despesas_por_orgao"
).fetchone()

print("\nTotal de registros:", count[0])
