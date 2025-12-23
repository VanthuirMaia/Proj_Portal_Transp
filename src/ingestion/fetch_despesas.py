import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

HEADERS = {
    "accept": "application/json",
    "chave-api-dados": API_KEY
}

def fetch_despesas(pagina=1):
    url = f"{API_BASE_URL}/despesas"
    params = {
        "pagina": pagina
    }

    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def main():
    all_data = []
    pagina = 1

    while True:
        print(f"Buscando página {pagina}")
        data = fetch_despesas(pagina)

        if not data:
            break

        all_data.extend(data)
        pagina += 1

    df = pd.DataFrame(all_data)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/raw/despesas_{timestamp}.csv"

    df.to_csv(output_path, index=False, encoding="utf-8")

    print(f"Arquivo salvo em {output_path}")


if __name__ == "__main__":
    main()
