import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

API_BASE_URL = "https://api.portaldatransparencia.gov.br/api-de-dados"
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "chave-api-dados": API_KEY,
    "accept": "application/json",
    "User-Agent": "data-engineering-study"
}

def fetch_page(pagina: int):
    url = f"{API_BASE_URL}/orgaos-siafi"
    params = {
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
    pagina = 1
    all_data = []

    while True:
        print(f"Coletando página {pagina}")
        data = fetch_page(pagina)

        if not data:
            break

        all_data.extend(data)
        pagina += 1
        time.sleep(0.2)  # respeita rate limit

    df = pd.DataFrame(all_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/raw/orgaos_siafi_{timestamp}.csv"

    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Dados salvos em {output_path}")
    print(f"Total de registros: {len(df)}")


if __name__ == "__main__":
    main()
