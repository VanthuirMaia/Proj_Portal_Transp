import pandas as pd

DATA_PATH = "data/staging/stg_despesas_por_orgao.parquet"

def main():
    df = pd.read_parquet(DATA_PATH)

    print("Total de registros:", len(df))

    # Regra 1 — valores negativos
    negativos = (
        (df["valor_empenhado"] < 0) |
        (df["valor_liquidado"] < 0) |
        (df["valor_pago"] < 0)
    )

    print("Registros com valores negativos:", negativos.sum())

    # Regra 2 — coerência financeira
    incoerentes = (
        (df["valor_empenhado"] < df["valor_liquidado"]) |
        (df["valor_liquidado"] < df["valor_pago"])
    )

    print("Registros incoerentes (empenhado < liquidado < pago):", incoerentes.sum())

    # Regra 3 — unicidade
    duplicados = df.duplicated(subset=["ano", "codigo_orgao"])

    print("Registros duplicados (ano, codigo_orgao):", duplicados.sum())

    # Amostras (se existirem)
    if incoerentes.any():
        print("\nExemplo de incoerência:")
        print(df[incoerentes].head())

    print("\nVerificação concluída")

if __name__ == "__main__":
    main()
