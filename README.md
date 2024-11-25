# Desafio de Engenharia de Dados - Coco Bambu

Este repositório contém a solução completa para o Desafio de Engenharia de Dados, que inclui a ingestão, processamento e armazenamento de dados JSON em um Data Lake utilizando AWS S3, além de integração com APIs simuladas via AWS API Gateway e Lambda para fornecer dados de restaurantes.

---

## Estrutura do Repositório

```plaintext
desafio-coco-bambu/
│
├── scripts/
│   ├── create_folders_s3.py          # Script para criar a estrutura inicial no S3
│   ├── create_tables.sql             # Script SQL para criar as tabelas no banco de dados
│   ├── etl_process.py                # Script principal para processar os dados do S3
│   ├── api_fetch.py                  # Script para consumir APIs e salvar os dados no S3
│
├── data/
│   ├── exemplos/
│   │   ├── ERP.json                  # Exemplo original do JSON de ERP
│   │   ├── ERP_ADICIONAL.json        # JSON com novos campos para teste
│   │   ├── ERP_TAXATION.json         # JSON com mudanças no campo "taxes"
│
├── .env                              # Arquivo de variáveis de ambiente
├── requirements.txt                  # Dependências do projeto
├── README.md                         # Documentação do projeto
├── CHALLENGE_DETAILS.md              # Detalhes e respostas ao desafio
├── KANBAN.md                         # Controle de tarefas e progresso do projeto
```
## 1. Configuração do Ambiente

### Pré-requisitos

- **Python 3.12**
- **AWS CLI configurado**
- Permissões para:
  - Criar buckets e objetos no **AWS S3**
  - Criar recursos no **AWS API Gateway**
  - Acessar um banco de dados **PostgreSQL** no **AWS RDS**
- Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

### Arquivo `.env`

Preencha o arquivo `.env` com as variáveis necessárias:

```plaintext
BUCKET_NAME=coco-bambu-data-lake2
API_BASE_URL=https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/default
DB_HOST=coco-bambu-rds.chqcsweg0oqw.us-east-1.rds.amazonaws.com
DB_NAME=coco_bambu_db
DB_USER=postgre
DB_PASSWORD=YourSecurePassword
DB_PORT=5432
```

## 2. Estrutura do Data Lake

### Estrutura Atual do Bucket S3

```plaintext
raw/
├── erp/
├── api_responses/
│   ├── getFiscalInvoice/
│   ├── getGuestChecks/
│   ├── getChargeBack/
│   ├── getTransactions/
│   ├── getCashManagementDetails/
processed/
logs/
```
A estrutura foi projetada para facilitar a organização e o acesso aos dados brutos, processados e logs.

---

## 3. Scripts Implementados

### **3.1. Criação de Tabelas no Banco de Dados**

O script SQL `create_tables.sql` cria as seguintes tabelas no RDS:

- `guest_checks`
- `taxes`
- `detail_lines`
- `menu_items`

Execute no **pgAdmin** ou qualquer ferramenta PostgreSQL.

---

### **3.2. Ingestão de APIs (`api_fetch.py`)**

Este script faz a requisição dos endpoints das APIs e armazena as respostas no S3. Exemplo:

```bash
python scripts/api_fetch.py
```

Cada resposta é salva em uma pasta específica na estrutura `raw/api_responses`.

---

### **3.3. ETL Process (`etl_process.py`)**

O script `etl_process.py` lê os arquivos do S3, valida os dados contra schemas JSON e insere os registros no banco RDS.

Execução:

```bash
python scripts/etl_process.py
```

Logs de validação são armazenados no S3 na pasta `logs`.

---

## 4. APIs Criadas

### Endpoints

Os endpoints simulam a geração de dados para análise de receitas:

- `/bi/getFiscalInvoice`
- `/res/getGuestChecks`
- `/org/getChargeBack`
- `/trans/getTransactions`
- `/inv/getCashManagementDetails`

Cada um retorna dados JSON que representam informações de restaurantes.

---

## 5. Respostas ao Desafio

### 5.1. Esquema JSON

Exemplo de schema de `ERP.json`:

```json
{
    "curUTC": "2024-05-05T06:06:06",
    "locRef": "99 CB CB",
    "guestChecks": [
        {
            "guestCheckId": 1122334455,
            "chkNum": 1234,
            "opnBusDt": "2024-01-01",
            "opnUTC": "2024-01-01T09:09:09",
            "opnLcl": "2024-01-01T06:09:09",
            "clsdBusDt": "2024-01-01",
            "clsdUTC": "2024-01-01T12:12:12",
            "clsdLcl": "2024-01-01T09:12:12",
            "lastTransUTC": "2024-01-01T12:12:12",
            "lastTransLcl": "2024-01-01T09:12:12",
            "lastUpdatedUTC": "2024-01-01T13:13:13",
            "lastUpdatedLcl": "2024-01-01T10:13:13",
            "clsdFlag": true,
            "gstCnt": 1,
            "subTtl": 109.9,
            "nonTxblSlsTtl": null,
            "chkTtl": 109.9,
            "dscTtl": -10,
            "payTtl": 109.9,
            "balDueTtl": null,
            "rvcNum": 101,
            "otNum": 1,
            "ocNum": null,
            "tblNum": 1,
            "tblName": "90",
            "empNum": 55555,
            "numSrvcRd": 3,
            "numChkPrntd": 2,
            "taxes": [
                {
                    "taxNum": 28,
                    "txblSlsTtl": 119.9,
                    "taxCollTtl": 20.81,
                    "taxRate": 21,
                    "type": 3
                }
            ],
            "detailLines": [
                {
                    "guestCheckLineItemId": 9988776655,
                    "rvcNum": 123,
                    "dtlOtNum": 1,
                    "dtlOcNum": null,
                    "lineNum": 1,
                    "dtlId": 1,
                    "detailUTC": "2024-01-01T09:09:09",
                    "detailLcl": "2024-01-01T06:09:09",
                    "lastUpdateUTC": "2024-11-01T10:10:10",
                    "lastUpdateLcl": "2024-01-01T07:10:10",
                    "busDt": "2024-01-01",
                    "wsNum": 7,
                    "dspTtl": 119.9,
                    "dspQty": 1,
                    "aggTtl": 119.9,
                    "aggQty": 1,
                    "chkEmpId": 10454318,
                    "chkEmpNum": 81001,
                    "svcRndNum": 1,
                    "seatNum": 1,
                    "menuItem": {
                        "miNum": 6042,
                        "modFlag": false,
                        "inclTax": 20.809091,
                        "activeTaxes": "28",
                        "prcLvl": 3
                    }
                }
            ]
        }
    ]
}
```
### 5.2. Armazenamento de Respostas da API

As respostas são salvas no S3 com a estrutura:

```plaintext
raw/api_responses/{endpoint}/{data}/{storeId}.json
```
### 5.3. Alterações em `guestChecks.taxes`

O pipeline foi projetado para ser resiliente a mudanças no nome do campo. Ele identifica automaticamente se o campo é `taxes` ou `taxation`.

---

## 6. Kanban

Veja o progresso completo em `KANBAN.md`. Todas as etapas foram documentadas.

---

## 7. Considerações Finais

Este projeto demonstrou o uso de:

1. **AWS Services**:
   - **S3** para armazenamento de dados.
   - **API Gateway** para endpoints.
   - **Lambda** para automação de APIs.

2. **Python Scripts**:
   - ETL robusto e validado.
   - Estrutura modular e escalável.

3. **PostgreSQL**:
   - Banco de dados relacional para armazenar dados processados.

Esta solução é flexível para adaptações futuras, como a adição de novos endpoints ou alterações no esquema JSON.
