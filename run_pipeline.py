import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Executa um comando e retorna True se sucesso"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode == 0:
        print(f"✅ {description} - SUCESSO")
        return True
    else:
        print(f"❌ {description} - FALHOU")
        return False

def main():
    print("\n🚀 INICIANDO PIPELINE COMPLETO - Portal da Transparência\n")
    
    # Etapa 1: Transformação CSV → Parquet
    if not run_command(
        "python src/transformation/stage_despesas_por_orgao.py",
        "Transformação: CSV → Parquet"
    ):
        sys.exit(1)
    
    # Etapa 2: Carga no DuckDB
    if not run_command(
        "python scripts/load_staging_to_duckdb.py",
        "Carga: Parquet → DuckDB"
    ):
        sys.exit(1)
    
    # Etapa 3: dbt - Modelos + Testes
    if not run_command(
        "cd portal_transp_dbt && dbt run",
        "dbt: Executando modelos"
    ):
        sys.exit(1)
    
    if not run_command(
        "cd portal_transp_dbt && dbt test",
        "dbt: Executando testes"
    ):
        sys.exit(1)
    
    print("\n" + "="*60)
    print("🎉 PIPELINE CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n📊 Para visualizar o dashboard, execute:")
    print("   cd dashboard && streamlit run app.py\n")

if __name__ == "__main__":
    main()