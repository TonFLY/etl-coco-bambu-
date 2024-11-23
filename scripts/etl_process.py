import boto3
import psycopg2
import json
import os
from dotenv import load_dotenv
from jsonschema import validate, ValidationError

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
RAW_FILE_PATH = os.getenv("RAW_FILE_PATH")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Schemas para validação de JSON
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

# Função para validar o JSON
def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        print(f"Erro na validação do JSON: {e}")
        return False

# Função principal do ETL
def process_guest_check():
    s3 = boto3.client('s3')

    try:
        # Baixar o arquivo JSON do S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=RAW_FILE_PATH)
        data = json.loads(response['Body'].read())
        print(f"Arquivo {RAW_FILE_PATH} carregado do S3 com sucesso!")

        # Conexão com o banco RDS
        conn = connect_to_rds()
        cursor = conn.cursor()

        # Processar guest_checks
        for guest_check in data["guestChecks"]:
            if not validate_json(guest_check, schemas["guest_checks"]):
                print(f"Registro inválido no guest_checks: {guest_check}")
                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key="logs/invalid_guest_checks.json",
                    Body=json.dumps(guest_check)
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

            # Identificar campos possíveis para taxes (taxes ou taxation)
            taxes_field = next(
                (field for field in ["taxes", "taxation"] if field in guest_check), 
                None
            )

            # Processar taxes
            if taxes_field:
                for tax in guest_check.get(taxes_field, []):
                    if not validate_json(tax, schemas["taxes"]):
                        print(f"Registro inválido no taxes: {tax}")
                        s3.put_object(
                            Bucket=BUCKET_NAME,
                            Key="logs/invalid_taxes.json",
                            Body=json.dumps(tax)
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

            # Processar detailLines
            for detail in guest_check.get("detailLines", []):
                if not validate_json(detail, schemas["detail_lines"]):
                    print(f"Registro inválido no detailLines: {detail}")
                    s3.put_object(
                        Bucket=BUCKET_NAME,
                        Key="logs/invalid_detail_lines.json",
                        Body=json.dumps(detail)
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

                # Processar menuItems
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
                    print(f"Registro inválido no menuItems: {menu_item}")
                    s3.put_object(
                        Bucket=BUCKET_NAME,
                        Key="logs/invalid_menu_items.json",
                        Body=json.dumps(menu_item)
                    )

        conn.commit()
        cursor.close()
        conn.close()
        print("Processamento concluído!")
    except Exception as e:
        print("Erro ao processar os dados:", e)
        raise

# Executar o ETL
if __name__ == "__main__":
    process_guest_check()
