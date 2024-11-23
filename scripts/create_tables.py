import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# Configurações de conexão ao banco
DB_HOST = os.getenv("DB_HOST")  # Substitua pelo endpoint do RDS
DB_PORT = os.getenv("DB_PORT")             # Porta padrão do PostgreSQL
DB_NAME = os.getenv("DB_NAME")    # Nome do banco
DB_USER = os.getenv("DB_USER")            # Nome do usuário
DB_PASSWORD = os.getenv("DB_PASSWORD")      # Senha do banco

def create_tables():
    try:
        # Conectar ao banco
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        print("Conexão com o banco estabelecida!")

        # SQL para criar a tabela guest_checks
        create_guest_checks_table = """
        CREATE TABLE IF NOT EXISTS guest_checks (
            guest_check_id BIGINT PRIMARY KEY,
            chk_num INT,
            opn_bus_dt DATE,
            clsd_bus_dt DATE,
            sub_ttl DECIMAL(10, 2),
            chk_ttl DECIMAL(10, 2),
            emp_num INT,
            num_srvc_rd INT,
            num_chk_prntd INT
        );
        """

        # SQL para criar a tabela detail_lines
        create_detail_lines_table = """
        CREATE TABLE IF NOT EXISTS detail_lines (
            guest_check_line_item_id BIGINT PRIMARY KEY,
            guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),
            line_num INT,
            detail_utc TIMESTAMP,
            dsp_ttl DECIMAL(10, 2),
            dsp_qty INT,
            menu_item_id BIGINT
        );
        """

        # SQL para criar a tabela taxes
        create_taxes_table = """
        CREATE TABLE IF NOT EXISTS taxes (
            tax_id SERIAL PRIMARY KEY,
            guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),
            tax_num INT,
            txbl_sls_ttl DECIMAL(10, 2),
            tax_coll_ttl DECIMAL(10, 2),
            tax_rate DECIMAL(5, 2),
            tax_type INT
        );
        """

        # SQL para criar a tabela menu_items
        create_menu_items_table = """
        CREATE TABLE IF NOT EXISTS menu_items (
            menu_item_id SERIAL PRIMARY KEY,
            mi_num BIGINT,
            mod_flag BOOLEAN,
            incl_tax DECIMAL(10, 2),
            active_taxes TEXT,
            prc_lvl INT
        );
        """

        # Executar as queries
        cursor.execute(create_guest_checks_table)
        print("Tabela guest_checks criada com sucesso!")

        cursor.execute(create_detail_lines_table)
        print("Tabela detail_lines criada com sucesso!")

        cursor.execute(create_taxes_table)
        print("Tabela taxes criada com sucesso!")

        cursor.execute(create_menu_items_table)
        print("Tabela menu_items criada com sucesso!")

        # Confirmar as mudanças
        conn.commit()

    except Exception as e:
        print("Erro ao criar tabelas:", str(e))
    finally:
        # Fechar conexão
        cursor.close()
        conn.close()
        print("Conexão com o banco encerrada.")

# Executar a função
if __name__ == "__main__":
    create_tables()
