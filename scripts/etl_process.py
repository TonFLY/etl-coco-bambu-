import boto3
import psycopg2
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from jsonschema import validate, ValidationError

# Carregar variáveis de ambiente do arquivo .env
# Utilizamos dotenv para manter as credenciais e configurações fora do código fonte,
# promovendo segurança e facilidade de manutenção.
load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
RAW_FILE_PATH = os.getenv("RAW_FILE_PATH")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Schemas para validação de JSON
# Definimos esquemas JSON usando jsonschema para validar a estrutura dos dados.
# Isso garante que apenas dados válidos sejam processados, reduzindo riscos de erros.
schemas = {
    "guest_checks": {
        "type": "object",
        "properties": {
            "guestCheckId": {"type": "integer"},
            "chkNum": {"type": "integer"},
            "opnBusDt": {"type": "string"},
            "clsdBusDt": {"type": "string"},
            "subTtl": {"type": "number"},
            "chkTtl": {"type": "number"},
            "empNum": {"type": "integer"},
            "numSrvcRd": {"type": "integer"},
            "numChkPrntd": {"type": "integer"},
            "taxes": {"type": "array"},
            "detailLines": {"type": "array"}
        },
        "required": ["guestCheckId", "chkNum", "opnBusDt", "clsdBusDt"]
    },
    "taxes": {
        "type": "object",
        "properties": {
            "taxNum": {"type": "integer"},
            "txblSlsTtl": {"type": "number"},
            "taxCollTtl": {"type": "number"},
            "taxRate": {"type": "number"}
        },
        "required": ["taxNum"]
    },
    "detail_lines": {
        "type": "object",
        "properties": {
            "guestCheckLineItemId": {"type": "integer"},
            "lineNum": {"type": "integer"},
            "detailUTC": {"type": "string"},
            "dspTtl": {"type": "number"},
            "dspQty": {"type": "integer"},
            "menuItem": {"type": "object"}
        },
        "required": ["guestCheckLineItemId", "lineNum", "detailUTC", "dspTtl", "dspQty"]
    },
    "menu_items": {
        "type": "object",
        "properties": {
            "miNum": {"type": "integer"},
            "modFlag": {"type": "boolean"},
            "inclTax": {"type": "number"},
            "prcLvl": {"type": "integer"}
        },
        "required": ["miNum"]
    }
}

# Função para conectar ao RDS
# Justificativa: Conexões diretas ao banco são encapsuladas em uma função para
# facilitar o reuso e centralizar o controle de erros.
def connect_to_rds():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Erro ao conectar ao RDS:", e)
        raise

# Função para salvar logs detalhados no S3
# Justificativa: Armazenar logs no S3 facilita auditorias e depuração, além de criar
# um histórico persistente de eventos.
def log_error_to_s3(s3_client, bucket_name, log_key, error_message, data=None):
    log_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "error_message": error_message,
        "data": data
    }
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=log_key,
            Body=json.dumps(log_entry)
        )
        print(f"Log salvo no S3: {log_key}")
    except Exception as e:
        print(f"Erro ao salvar log no S3: {e}")

# Função para validar o JSON
# Justificativa: A validação de dados garante integridade e minimiza erros em etapas
# subsequentes do pipeline.
def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Erro na validação do JSON: {e}")
        return False

# Função principal do ETL
# Justificativa: Este método segue a abordagem de ETL (Extração, Transformação e Carga),
# extraindo dados do S3, validando e carregando no RDS.
def process_guest_check():
    s3 = boto3.client('s3')

    try:
        # Extração: Baixar o arquivo JSON do S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=RAW_FILE_PATH)
        data = json.loads(response['Body'].read())
        print(f"Arquivo {RAW_FILE_PATH} carregado do S3 com sucesso!")

        # Conexão com o banco RDS
        conn = connect_to_rds()
        cursor = conn.cursor()

        # Transformação e Carga: Processar guest_checks
        for guest_check in data["guestChecks"]:
            if not validate_json(guest_check, schemas["guest_checks"]):
                log_error_to_s3(
                    s3_client=s3,
                    bucket_name=BUCKET_NAME,
                    log_key="logs/invalid_guest_checks.json",
                    error_message="Estrutura inválida no guest_checks.",
                    data=guest_check
                )
                continue

            cursor.execute("""
                INSERT INTO guest_checks (
                    guest_check_id, chk_num, opn_bus_dt, clsd_bus_dt, sub_ttl,
                    chk_ttl, emp_num, num_srvc_rd, num_chk_prntd
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (guest_check_id) DO NOTHING
            """, (
                guest_check.get("guestCheckId"),
                guest_check.get("chkNum"),
                guest_check.get("opnBusDt"),
                guest_check.get("clsdBusDt"),
                guest_check.get("subTtl"),
                guest_check.get("chkTtl"),
                guest_check.get("empNum"),
                guest_check.get("numSrvcRd"),
                guest_check.get("numChkPrntd")
            ))

            # Taxes: Suporte a nomes diferentes (e.g., taxes ou taxation)
            taxes_field = next(
                (field for field in ["taxes", "taxation"] if field in guest_check), 
                None
            )

            if taxes_field:
                for tax in guest_check.get(taxes_field, []):
                    if not validate_json(tax, schemas["taxes"]):
                        log_error_to_s3(
                            s3_client=s3,
                            bucket_name=BUCKET_NAME,
                            log_key="logs/invalid_taxes.json",
                            error_message="Estrutura inválida no taxes.",
                            data=tax
                        )
                        continue

                    cursor.execute("""
                        INSERT INTO taxes (tax_id, guest_check_id, tax_num, txbl_sls_ttl, tax_coll_ttl, tax_rate)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        tax.get("taxNum"),
                        guest_check.get("guestCheckId"),
                        tax.get("taxNum"),
                        tax.get("txblSlsTtl", 0),
                        tax.get("taxCollTtl", 0),
                        tax.get("taxRate", 0)
                    ))

            # Detalhes e Itens do Menu
            for detail in guest_check.get("detailLines", []):
                if not validate_json(detail, schemas["detail_lines"]):
                    log_error_to_s3(
                        s3_client=s3,
                        bucket_name=BUCKET_NAME,
                        log_key="logs/invalid_detail_lines.json",
                        error_message="Estrutura inválida no detailLines.",
                        data=detail
                    )
                    continue

                cursor.execute("""
                    INSERT INTO detail_lines (
                        guest_check_line_item_id, guest_check_id, line_num, detail_utc,
                        dsp_ttl, dsp_qty, menu_item_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    detail.get("guestCheckLineItemId"),
                    guest_check.get("guestCheckId"),
                    detail.get("lineNum"),
                    detail.get("detailUTC"),
                    detail.get("dspTtl"),
                    detail.get("dspQty"),
                    detail.get("menuItem", {}).get("miNum") if detail.get("menuItem") else None
                ))

                # Itens do Menu
                menu_item = detail.get("menuItem", {})
                if menu_item and validate_json(menu_item, schemas["menu_items"]):
                    cursor.execute("""
                        INSERT INTO menu_items (
                            menu_item_id, mi_num, mod_flag, incl_tax, prc_lvl
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING
                    """, (
                        menu_item.get("miNum"),
                        menu_item.get("miNum"),
                        menu_item.get("modFlag", False),
                        menu_item.get("inclTax", 0),
                        menu_item.get("prcLvl", 0)
                    ))
                elif menu_item:
                    log_error_to_s3(
                        s3_client=s3,
                        bucket_name=BUCKET_NAME,
                        log_key="logs/invalid_menu_items.json",
                        error_message="Estrutura inválida no menuItems.",
                        data=menu_item
                    )

        conn.commit()
        cursor.close()
        conn.close()
        print("Processamento concluído com sucesso!")
    except Exception as e:
        log_error_to_s3(
            s3_client=s3,
            bucket_name=BUCKET_NAME,
            log_key="logs/general_errors.json",
            error_message=f"Erro geral no processamento: {e}"
        )
        print("Erro ao processar os dados:", e)

# Executar o ETL
if __name__ == "__main__":
    process_guest_check()
