import duckdb 
from pathlib import Path

db_path = Path("data/warehouse/portal_transparencia.duckdb")
db_path.parent.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(db_path))
con.execute("SELECT 1").fetchall()

print("DuckDB inicializado com sucesso!")