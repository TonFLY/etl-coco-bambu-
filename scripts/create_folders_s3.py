import boto3
import json

# Cliente do S3 e nome do bucket
s3 = boto3.client('s3')
bucket_name = "coco-bambu-data-lake2"

def create_s3_structure():
    """
    Cria a estrutura de pastas no bucket S3.
    Justificativa: Organizar os dados em pastas `raw` e `processed` para facilitar a manipulação.
    """
    folders = [
        "raw/api_responses/",  # Pasta para respostas brutas das APIs
        "raw/erp/",            # Pasta para dados ERP brutos
        "processed/api_responses/",  # Pasta para dados processados das APIs
        "processed/erp/"       # Pasta para dados ERP processados
    ]
    for folder in folders:
        s3.put_object(Bucket=bucket_name, Key=(folder))
    print("Estrutura de pastas criada no S3 com sucesso.")

def upload_sample_files():
    """
    Envia arquivos JSON de exemplo para o S3.
    Justificativa: Fornecer exemplos iniciais para validar a estrutura e integração.
    """
    # Exemplo de resposta da API
    api_response_data = {
        "responseId": 1,
        "timestamp": "2024-01-01T12:00:00Z",
        "data": [
            {"key": "value1"},
            {"key": "value2"}
        ]
    }
    s3.put_object(Bucket=bucket_name, Key="raw/api_responses/example_response.json", Body=json.dumps(api_response_data))

    # Exemplo de dados ERP
    erp_data = {
        "transactionId": 1001,
        "timestamp": "2024-01-01T15:00:00Z",
        "amount": 150.0,
        "details": "Example ERP data"
    }
    s3.put_object(Bucket=bucket_name, Key="raw/erp/example_erp.json", Body=json.dumps(erp_data))
    print("Arquivos de exemplo enviados para o S3 com sucesso.")

if __name__ == "__main__":
    # Criação da estrutura e envio dos arquivos simulados
    create_s3_structure()
    upload_sample_files()
