import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "chave-api-dados": API_KEY,
    "accept": "application/json",
    "User-Agent": "data-engineering-study"
}

def fetch_page(ano: int, orgao_superior: str, pagina: int):
    url = f"{API_BASE_URL}/despesas/por-orgao"
    params = {
        "ano": ano,
        "orgaoSuperior": orgao_superior,
        "pagina": pagina
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def main():
    # Lista de anos pra buscar
    anos = [2020, 2021, 2022, 2023, 2024]
    orgao_superior = "26000"
    
    for ano in anos:
        print(f"\n{'='*50}")
        print(f"Buscando dados do ano {ano}")
        print(f"{'='*50}\n")
        
        pagina = 1
        all_data = []

        while True:
            print(f"Ano {ano} | Órgão {orgao_superior} | Página {pagina}")
            try:
                data = fetch_page(ano, orgao_superior, pagina)

                if not data:
                    break

                all_data.extend(data)
                pagina += 1
                time.sleep(0.3)
            except Exception as e:
                print(f"Erro na página {pagina}: {e}")
                break

        if all_data:
            df = pd.DataFrame(all_data)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"data/raw/despesas_{orgao_superior}_{ano}_{timestamp}.csv"
            df.to_csv(output_path, index=False, encoding="utf-8")
            print(f"✅ Arquivo salvo: {output_path} | Registros: {len(df)}")
        else:
            print(f"⚠️  Nenhum dado encontrado para {ano}")

if __name__ == "__main__":
    main()
