import duckdb
from pathlib import Path

# Caminhos
db_path = Path("data/warehouse/portal_transparencia.duckdb")
parquet_path = Path("data/staging/stg_despesas_por_orgao.parquet")

# Conexão com DuckDB
con = duckdb.connect(str(db_path))

# Criação da tabela a partir do Parquet
con.execute("""
            CREATE OR REPLACE TABLE staging_despesas_por_orgao AS
            SELECT *
            FROM read_parquet(?)
            """, [str(parquet_path)])

print("Tabela staging_despesas_por_orgao criada com sucesso em DuckDB!")