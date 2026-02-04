import pandas as pd
import re
from pathlib import Path
from datetime import datetime

RAW_PATH = Path("data/raw")
STAGING_PATH = Path("data/staging")
STAGING_PATH.mkdir(parents=True, exist_ok=True)


def to_decimal(series: pd.Series) -> pd.Series:
    def normalize(value):
        if pd.isna(value):
            return None

        value = str(value)

        # remove tudo que não é número ou ponto
        value = re.sub(r"[^\d.]", "", value)

        # se tiver mais de um ponto, mantém só o último como decimal
        if value.count(".") > 1:
            parts = value.split(".")
            value = "".join(parts[:-1]) + "." + parts[-1]

        return float(value)

    return series.apply(normalize)



def main():
    # Busca TODOS os CSVs
    raw_files = list(RAW_PATH.glob("despesas_*_*.csv"))
    
    if not raw_files:
        print("❌ Nenhum arquivo CSV encontrado em data/raw/")
        return
    
    print(f"📂 Encontrados {len(raw_files)} arquivo(s) CSV")
    
    all_data = []
    
    for raw_file in raw_files:
        print(f"   Processando: {raw_file.name}")
        df = pd.read_csv(raw_file)
        
        df_stg = pd.DataFrame({
            "ano": df["ano"].astype(int),
            "codigo_orgao": df["codigoOrgao"].astype(str),
            "orgao": df["orgao"].astype(str),
            "codigo_orgao_superior": df["codigoOrgaoSuperior"].astype(str),
            "orgao_superior": df["orgaoSuperior"].astype(str),
            "valor_empenhado": to_decimal(df["empenhado"]),
            "valor_liquidado": to_decimal(df["liquidado"]),
            "valor_pago": to_decimal(df["pago"]),
            "carga_timestamp": datetime.now()
        })
        
        all_data.append(df_stg)
    
    # Consolida todos os DataFrames
    df_final = pd.concat(all_data, ignore_index=True)
    
    output_file = STAGING_PATH / "stg_despesas_por_orgao.parquet"
    df_final.to_parquet(output_file, index=False)
    
    print(f"\n✅ Arquivo STAGING consolidado salvo em {output_file}")
    print(f"📊 Total de registros: {len(df_final)}")
    print(f"📅 Anos processados: {sorted(df_final['ano'].unique())}")
    print(f"\n{df_final.dtypes}")

if __name__ == "__main__":
    main()
