import requests
import boto3
import json
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis de ambiente do arquivo .env
# Justificativa: O uso do dotenv mantém as credenciais e URLs fora do código-fonte, melhorando a segurança.
load_dotenv()

# Configuração do S3
# Justificativa: Centralizar a configuração do bucket simplifica a reutilização e manutenção.
BUCKET_NAME = os.getenv("BUCKET_NAME")

# Base URL da API Gateway
# Justificativa: Ter uma URL base facilita a atualização em caso de mudanças no domínio da API.
API_BASE_URL = os.getenv("API_BASE_URL")

# Configuração dos endpoints da API e seus payloads
# Justificativa: Centralizar os endpoints e os payloads permite maior organização e fácil manutenção.
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
    """
    Função principal para buscar dados de APIs e salvá-los no S3.
    """
    s3 = boto3.client('s3')
    for key, config in endpoints.items():
        try:
            # Fazer a requisição POST
            # Justificativa: O método POST permite enviar dados específicos (como data e loja) para cada endpoint.
            response = requests.post(config["url"], json=config["payload"])
            if response.status_code == 200:
                # Dados retornados da API
                data = response.json()

                # Estrutura de armazenamento no S3
                # Justificativa: A estrutura `api_responses/{endpoint}/{data}` organiza bem os dados para buscas futuras.
                folder_path = f"raw/api_responses/{key}/{datetime.now().strftime('%Y-%m-%d')}/"
                file_name = f"{config['payload']['storeId']}.json"
                file_path = folder_path + file_name

                # Enviar os dados para o S3
                # Justificativa: Salvando no S3, garantimos persistência e acessibilidade para análises posteriores.
                s3.put_object(Bucket=BUCKET_NAME, Key=file_path, Body=json.dumps(data))
                print(f"Dados salvos no S3: {file_path}")
            else:
                # Registrar erros de acesso
                # Justificativa: Rastrear erros ajuda na depuração e monitoramento do serviço.
                print(f"Erro ao acessar {key}: {response.status_code} - {response.text}")
        except Exception as e:
            # Registrar exceções inesperadas
            # Justificativa: Manter a execução mesmo após erros em endpoints individuais.
            print(f"Erro ao processar {key}: {e}")

if __name__ == "__main__":
    fetch_and_save()
