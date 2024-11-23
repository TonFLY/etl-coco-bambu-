import boto3
import json

s3 = boto3.client('s3')
bucket_name = "coco-bambu-data-lake2"

def create_s3_structure():
    folders = [
        "raw/api1/",
        "raw/api2/",
        "raw/erp/",
        "processed/api1/",
        "processed/api2/",
        "processed/erp/"
    ]
    for folder in folders:
        s3.put_object(Bucket=bucket_name, Key=(folder + "/"))

def upload_sample_files():
    # Simulação para API 1 (Pedidos)
    api1_data = {
        "orderId": 12345,
        "timestamp": "2024-01-01T12:00:00Z",
        "items": [
            {"itemId": 1, "quantity": 2, "price": 10.5},
            {"itemId": 2, "quantity": 1, "price": 5.0}
        ],
        "total": 26.0
    }
    s3.put_object(Bucket=bucket_name, Key="raw/api1/order1.json", Body=json.dumps(api1_data))

    # Simulação para API 2 (Feedbacks)
    api2_data = {
        "feedbackId": 54321,
        "timestamp": "2024-01-01T15:00:00Z",
        "customerId": 9876,
        "rating": 4.5,
        "comments": "Ótimo serviço!"
    }
    s3.put_object(Bucket=bucket_name, Key="raw/api2/feedback1.json", Body=json.dumps(api2_data))

if __name__ == "__main__":
    create_s3_structure()
    upload_sample_files()
    print("Estrutura e arquivos simulados criados no S3 com sucesso!")
