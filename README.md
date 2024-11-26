# Desafio de Engenharia de Dados - Coco Bambu

Este repositório contém a solução completa para o Desafio de Engenharia de Dados, que inclui a ingestão, processamento e armazenamento de dados JSON em um Data Lake utilizando AWS S3, integração com APIs simuladas via AWS API Gateway e Lambda, além de um robusto processo de ETL validado e escalável.

---

## Estrutura do Repositório

```plaintext
desafio-coco-bambu/
│
├── scripts/
│   ├── create_folders_s3.py          # Script para criar a estrutura inicial no S3
│   ├── create_tables.py              # Script para criar tabelas e índices no RDS
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
├── API_DOCUMENTATION.md              # Documentação detalhada dos endpoints simulados
```

---

## 1. Configuração do Ambiente

### Pré-requisitos

- **Python 3.12**
- **AWS CLI configurado**
- Permissões para:
  - Criar buckets e objetos no **AWS S3**
  - Criar recursos no **AWS API Gateway**
  - Acessar um banco de dados **PostgreSQL** no **AWS RDS**

### Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```
### Arquivo `.env`

Preencha o arquivo `.env` com as variáveis necessárias para configurar o ambiente:

```plaintext
BUCKET_NAME=coco-bambu-data-lake2
API_BASE_URL=https://<api-gateway-id>.execute-api.us-east-1.amazonaws.com/default
DB_HOST=coco-bambu-rds.chqcsweg0oqw.us-east-1.rds.amazonaws.com
DB_NAME=coco_bambu_db
DB_USER=postgre
DB_PASSWORD=YourSecurePassword
DB_PORT=5432
```
Certifique-se de substituir `<api-gateway-id>` pelo ID do API Gateway e `YourSecurePassword` pela senha correta do banco.

---

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
A estrutura foi projetada para facilitar a organização e o acesso aos dados brutos, processados e logs. Todas as respostas das APIs agora são armazenadas em `raw/api_responses`.

---

## 3. Scripts Implementados

### **3.1. Criação de Tabelas no Banco de Dados**

O script Python `create_tables.py` cria as seguintes tabelas no RDS com índices para otimizar consultas frequentes:

- `guest_checks`: Índice em `guest_check_id`.
- `taxes`: Índice em `guest_check_id`.
- `detail_lines`: Índice em `guest_check_id`.
- `menu_items`: Índice em `menu_item_id`.

Cada tabela e índice foi projetado para atender às necessidades de performance do projeto e garantir integridade relacional.

Execução:

```bash
python scripts/create_tables.py

```

### **3.2. Ingestão de APIs (`api_fetch.py`)**

Este script realiza requisições para os endpoints configurados e salva as respostas no bucket S3, seguindo a estrutura organizada em `raw/api_responses`. 

Alterações recentes:
- Estrutura ajustada para salvar todas as respostas das APIs simuladas dentro de `raw/api_responses`.
- Validação de erros e logs detalhados foram adicionados para rastreabilidade.

Execução:

```bash
python scripts/api_fetch.py
```
--- 

### **3.3. ETL Process (`etl_process.py`)**

O script `etl_process.py` é responsável por processar os dados JSON armazenados no S3, validar suas estruturas e salvar as informações no banco de dados PostgreSQL (RDS). Ele realiza as seguintes etapas principais:

1. **Leitura do S3**:
   - Baixa os arquivos JSON armazenados na estrutura `raw/erp` e `raw/api_responses`.

2. **Validação**:
   - Cada registro é validado contra schemas JSON previamente definidos para garantir a integridade e consistência dos dados.

3. **Inserção no banco**:
   - Os registros são armazenados nas tabelas `guest_checks`, `taxes`, `detail_lines` e `menu_items`.

4. **Logs detalhados**:
   - Logs de erros e falhas de validação são armazenados no S3 em `logs/invalid_<tipo>.json`.
   - Agora os logs incluem:
     - **Timestamps**.
     - **Campos inválidos específicos**.
     - **Detalhes do erro**.

### **Alterações Recentes**

- **Campos Dinâmicos**: O pipeline foi ajustado para lidar automaticamente com mudanças nos nomes dos campos, como `taxes` para `taxation`.
- **Melhorias de Logs**: Logs expandidos para incluir informações detalhadas de cada registro inválido.
- **Mensagens de Sucesso**: Logs no console indicam progresso e completude.

### **Execução**

Para executar o script, utilize o comando:

```bash
python scripts/etl_process.py
```

#### Exemplo de Execução com Sucesso:

```plaintext
Arquivo raw/erp/ERP.json carregado do S3 com sucesso!
Dados de guest_checks inseridos no banco.
Dados de taxes inseridos no banco.
Dados de detail_lines inseridos no banco.
Dados de menu_items inseridos no banco.
Processamento concluído!
```

#### Exemplo de Log de Erros:

Os registros inválidos são armazenados no S3, por exemplo:

- `logs/invalid_guest_checks.json`
- `logs/invalid_taxes.json`
- `logs/invalid_detail_lines.json`
- `logs/invalid_menu_items.json`

Exemplo de log:

```json
{
    "timestamp": "2024-01-01T12:00:00Z",
    "error": "Erro na validação do JSON",
    "details": {
        "schema": "guest_checks",
        "errorField": "chkNum",
        "expectedType": "integer",
        "providedValue": "abc",
        "context": {
            "guestCheckId": 1122334455,
            "opnBusDt": "2024-01-01",
            "subTtl": 109.9
        }
    }
}
```
---

## 4. APIs Criadas

### Endpoints

Os endpoints simulam a geração de dados para análise de receitas:

- `/bi/getFiscalInvoice`
- `/res/getGuestChecks`
- `/org/getChargeBack`
- `/trans/getTransactions`
- `/inv/getCashManagementDetails`

Cada endpoint aceita um payload com `busDt` (data de operação) e `storeId` (identificador da loja), e retorna dados JSON que representam informações de restaurantes.

Para mais detalhes, acesse [`API_DOCUMENTATION.md`](API_DOCUMENTATION.md).

---

## 5. Respostas ao Desafio

### 5.1. Esquema JSON

Exemplo de esquema de `ERP.json`:

```json
{
    "curUTC": "2024-05-05T06:06:06",
    "locRef": "99 CB CB",
    "guestChecks": [
        {
            "guestCheckId": 1122334455,
            "chkNum": 1234,
            "opnBusDt": "2024-01-01",
            "clsdBusDt": "2024-01-01",
            "subTtl": 109.9,
            "chkTtl": 109.9,
            "empNum": 55555,
            "numSrvcRd": 3,
            "numChkPrntd": 2,
            "taxes": [
                {
                    "taxNum": 28,
                    "txblSlsTtl": 119.9,
                    "taxCollTtl": 20.81,
                    "taxRate": 21
                }
            ],
            "detailLines": [
                {
                    "guestCheckLineItemId": 9988776655,
                    "lineNum": 1,
                    "detailUTC": "2024-01-01T09:09:09",
                    "dspTtl": 119.9,
                    "dspQty": 1,
                    "menuItem": {
                        "miNum": 6042,
                        "modFlag": false,
                        "inclTax": 20.81,
                        "prcLvl": 3
                    }
                }
            ]
        }
    ]
}
```

---

### 5.2. Armazenamento de Respostas da API

As respostas das APIs simuladas são salvas no S3 na seguinte estrutura:

```plaintext
raw/
└── api_responses/
    ├── getFiscalInvoice/
    │   ├── 2024-01-01/
    │   │   ├── store123.json
    ├── getGuestChecks/
    │   ├── 2024-01-01/
    │   │   ├── store123.json
    ├── getChargeBack/
    │   ├── 2024-01-01/
    │   │   ├── store123.json
    ├── getTransactions/
    │   ├── 2024-01-01/
    │   │   ├── store123.json
    └── getCashManagementDetails/
        ├── 2024-01-01/
        │   ├── store123.json
```

A estrutura foi projetada para permitir um acesso organizado e rápido aos dados das APIs. Cada endpoint possui sua pasta específica e organiza as respostas por data de operação.

Os dados processados posteriormente são movidos para a pasta `processed`, garantindo a separação clara entre dados brutos e transformados.

### 6. Kanban

Para acompanhar o progresso do projeto, consulte o arquivo `KANBAN.md`. O Kanban foi estruturado em três colunas principais:

- **A Fazer**: Etapas planejadas, mas ainda não iniciadas.
- **Em Progresso**: Tarefas em andamento.
- **Concluído**: Atividades finalizadas.

O controle visual das tarefas ajudou a organizar a entrega incremental e facilitou ajustes rápidos durante o desenvolvimento.

---

### 7. Considerações Finais

Este projeto foi desenvolvido utilizando as melhores práticas em Engenharia de Dados, com destaque para:

1. **Flexibilidade**: 
   - O pipeline é resiliente a mudanças nos esquemas JSON.
   - Adaptação dinâmica para novos campos ou endpoints.

2. **Organização**:
   - Estrutura clara no S3 para dados brutos, processados e logs.
   - Validação rigorosa dos dados com logs detalhados.

3. **Automação**:
   - Utilização de AWS API Gateway e Lambda para automação de ingestão de dados.
   - Scripts modulares para criação de tabelas, ingestão de APIs e processamento ETL.

O projeto está preparado para futuras expansões, como a inclusão de novos endpoints, alterações nos requisitos de validação ou migração para arquiteturas mais escaláveis.

Para mais detalhes técnicos, consulte a documentação das [APIs](API_DOCUMENTATION.md) e os scripts no repositório.


