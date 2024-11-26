import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
# Justificativa: O uso do dotenv melhora a segurança ao manter credenciais fora do código fonte.
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def create_tables():
    try:
        # Conectar ao banco
        # Justificativa: O uso de uma conexão centralizada facilita a reutilização e o controle de erros.
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
        # Justificativa: Esta tabela contém informações principais sobre as transações dos clientes.
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
        # Justificativa: Esta tabela armazena detalhes das transações, como itens comprados.
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
        # Justificativa: Esta tabela armazena informações sobre impostos associados às transações.
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
        # Justificativa: Esta tabela armazena detalhes sobre itens do menu associados às transações.
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

        # Criar tabelas no banco de dados
        cursor.execute(create_guest_checks_table)
        print("Tabela guest_checks criada com sucesso!")

        cursor.execute(create_detail_lines_table)
        print("Tabela detail_lines criada com sucesso!")

        cursor.execute(create_taxes_table)
        print("Tabela taxes criada com sucesso!")

        cursor.execute(create_menu_items_table)
        print("Tabela menu_items criada com sucesso!")

        # SQL para criar índices nas tabelas
        # Justificativa: Índices melhoram o desempenho das consultas frequentes, como aquelas baseadas em chaves primárias ou estrangeiras.
        create_indices = [
            "CREATE INDEX IF NOT EXISTS idx_guest_checks_guest_check_id ON guest_checks (guest_check_id);",
            "CREATE INDEX IF NOT EXISTS idx_detail_lines_guest_check_id ON detail_lines (guest_check_id);",
            "CREATE INDEX IF NOT EXISTS idx_taxes_guest_check_id ON taxes (guest_check_id);",
            "CREATE INDEX IF NOT EXISTS idx_menu_items_menu_item_id ON menu_items (menu_item_id);"
        ]

        # Criar índices no banco de dados
        for index_query in create_indices:
            cursor.execute(index_query)
        print("Índices criados com sucesso!")

        # Confirmar alterações no banco de dados
        conn.commit()

    except Exception as e:
        print("Erro ao criar tabelas e índices:", str(e))
    finally:
        # Fechar conexão com o banco de dados
        cursor.close()
        conn.close()
        print("Conexão com o banco encerrada.")

# Executar a função principal
if __name__ == "__main__":
    create_tables()
