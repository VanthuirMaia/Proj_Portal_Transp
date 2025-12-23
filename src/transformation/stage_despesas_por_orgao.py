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
    raw_file = max(RAW_PATH.glob("despesas_*_*.csv"), key=lambda f: f.stat().st_mtime)
    print(f"Lendo arquivo RAW: {raw_file}")

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

    output_file = STAGING_PATH / "stg_despesas_por_orgao.parquet"
    df_stg.to_parquet(output_file, index=False)

    print(f"Arquivo STAGING salvo em {output_file}")
    print(df_stg.dtypes)


if __name__ == "__main__":
    main()
