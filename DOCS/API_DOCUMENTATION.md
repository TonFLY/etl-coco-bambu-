# Documentação das APIs Simuladas

## Endpoints

---

### 1. `/bi/getFiscalInvoice`
**Método:** POST  
**Descrição:** Retorna notas fiscais emitidas de uma loja em uma data específica.  

**Exemplo de Payload:**
```json
{
  "busDt": "2024-01-01",
  "storeId": "store123"
}
```
**Exemplo de Resposta:**
```json
{
  "storeId": "store123",
  "busDt": "2024-01-01",
  "fiscalInvoices": [
    {"invoiceId": 1, "amount": 100.0, "tax": 10.0},
    {"invoiceId": 2, "amount": 200.0, "tax": 20.0}
  ]
}
```
### 2. `/res/getGuestChecks`
**Método:** POST
**Descrição:** Retorna os dados de Guest Checks de uma loja em uma data específica.

**Exemplo de Payload:**
````json
{
  "busDt": "2024-01-01",
  "storeId": "store123"
}
```
**Exemplo de Resposta:**
```json
{
  "storeId": "store123",
  "busDt": "2024-01-01",
  "guestChecks": [
    {"guestCheckId": 1, "subTtl": 100.0, "chkTtl": 110.0},
    {"guestCheckId": 2, "subTtl": 200.0, "chkTtl": 220.0}
  ]
}
```
---
### 3. `/org/getChargeBack`
**Método:** POST
**Descrição:** Retorna os chargebacks (reembolsos ou disputas) de uma loja em uma data específica.

**Exemplo de Payload:**
```json
{
  "busDt": "2024-01-01",
  "storeId": "store123"
}
```
**Exemplo de Resposta:**

```json
{
  "storeId": "store123",
  "busDt": "2024-01-01",
  "chargeBacks": [
    {"chargeId": 1, "amount": 50.0, "reason": "Dispute"},
    {"chargeId": 2, "amount": 70.0, "reason": "Refund"}
  ]
}
```
---

### 4. `/trans/getTransactions`
**Método:** POST
**Descrição:** Retorna as transações realizadas em uma loja em uma data específica.

**Exemplo de Payload:**

```json
{
  "busDt": "2024-01-01",
  "storeId": "store123"
}
```
**Exemplo de Resposta:**
```json
{
  "storeId": "store123",
  "busDt": "2024-01-01",
  "transactions": [
    {"transactionId": 1, "type": "Credit", "amount": 150.0},
    {"transactionId": 2, "type": "Cash", "amount": 200.0}
  ]
}
```
---

### 5. `/inv/getCashManagementDetails` 
**Método:** POST
**Descrição:** Retorna os detalhes de gestão de caixa de uma loja em uma data específica.

**Exemplo de Payload:**
```json
{
  "busDt": "2024-01-01",
  "storeId": "store123"
}
```
**Exemplo de Resposta:**
```json 
{
  "storeId": "store123",
  "busDt": "2024-01-01",
  "cashManagement": [
    {"cashBoxId": 1, "openingBalance": 500.0, "closingBalance": 450.0},
    {"cashBoxId": 2, "openingBalance": 300.0, "closingBalance": 280.0}
  ]
}
```
--- 

## Observação

Esses endpoints foram simulados no **AWS API Gateway** e representam uma estrutura que pode ser utilizada para desenvolvimento e testes.  
Cada endpoint retorna dados pré-configurados, e suas respostas seguem o formato JSON demonstrado acima.
