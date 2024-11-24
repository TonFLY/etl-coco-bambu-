import requests
import boto3
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do S3
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Base URL da API Gateway
API_BASE_URL = os.getenv("API_BASE_URL")

# Endpoints e payloads
endpoints = {
    "getFiscalInvoice": {
        "url": f"{API_BASE_URL}/bi/getFiscalInvoice",
        "payload": {"busDt": "2024-01-01", "storeId": "store123"}
    },
    "getGuestChecks": {
        "url": f"{API_BASE_URL}/res/getGuestChecks",
        "payload": {"busDt": "2024-01-01", "storeId": "store123"}
    },
    "getChargeBack": {
        "url": f"{API_BASE_URL}/org/getChargeBack",
        "payload": {"busDt": "2024-01-01", "storeId": "store123"}
    },
    "getTransactions": {
        "url": f"{API_BASE_URL}/trans/getTransactions",
        "payload": {"busDt": "2024-01-01", "storeId": "store123"}
    },
    "getCashManagementDetails": {
        "url": f"{API_BASE_URL}/inv/getCashManagementDetails",
        "payload": {"busDt": "2024-01-01", "storeId": "store123"}
    }
}

def fetch_and_save():
    s3 = boto3.client('s3')
    for key, config in endpoints.items():
        try:
            # Fazer a requisição POST
            response = requests.post(config["url"], json=config["payload"])
            if response.status_code == 200:
                # Dados retornados da API
                data = response.json()

                # Caminho no S3 (ajustado para `api_responses`)
                folder_path = f"raw/api_responses/{key}/{datetime.now().strftime('%Y-%m-%d')}/"
                file_name = f"{config['payload']['storeId']}.json"
                file_path = folder_path + file_name

                # Enviar os dados para o S3
                s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=json.dumps(data))
                print(f"Dados salvos no S3: {file_path}")
            else:
                print(f"Erro ao acessar {key}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao processar {key}: {e}")

if __name__ == "__main__":
    fetch_and_save()
