# Challenge Details

## 1. Descreva o esquema JSON correspondente ao exemplo acima

O esquema JSON fornecido é modelado como segue:

```json
{
  "type": "object",
  "properties": {
    "curUTC": {"type": "string"},
    "locRef": {"type": "string"},
    "guestChecks": {
      "type": "array",
      "items": {
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
          "taxes": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "taxNum": {"type": "integer"},
                "txblSlsTtl": {"type": "number"},
                "taxCollTtl": {"type": "number"},
                "taxRate": {"type": "number"}
              }
            }
          },
          "detailLines": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "guestCheckLineItemId": {"type": "integer"},
                "lineNum": {"type": "integer"},
                "detailUTC": {"type": "string"},
                "dspTtl": {"type": "number"},
                "dspQty": {"type": "integer"},
                "menuItem": {
                  "type": "object",
                  "properties": {
                    "miNum": {"type": "integer"},
                    "modFlag": {"type": "boolean"},
                    "inclTax": {"type": "number"},
                    "prcLvl": {"type": "integer"}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "required": ["curUTC", "locRef", "guestChecks"]
}
```
## 2. Transcreva o JSON para tabelas SQL

O JSON foi transcrito para as seguintes tabelas SQL:

### guest_checks

| Coluna         | Tipo      | Chave     |
|-----------------|-----------|-----------|
| guest_check_id  | INTEGER   | PK        |
| chk_num         | INTEGER   |           |
| opn_bus_dt      | DATE      |           |
| clsd_bus_dt     | DATE      |           |
| sub_ttl         | NUMERIC   |           |
| chk_ttl         | NUMERIC   |           |
| emp_num         | INTEGER   |           |
| num_srvc_rd     | INTEGER   |           |
| num_chk_prntd   | INTEGER   |           |

---

### taxes

| Coluna          | Tipo      | Chave     |
|------------------|-----------|-----------|
| tax_id           | INTEGER   | PK        |
| guest_check_id   | INTEGER   | FK        |
| tax_num          | INTEGER   |           |
| txbl_sls_ttl     | NUMERIC   |           |
| tax_coll_ttl     | NUMERIC   |           |
| tax_rate         | NUMERIC   |           |

---

### detail_lines

| Coluna                | Tipo      | Chave     |
|-----------------------|-----------|-----------|
| detail_line_id        | INTEGER   | PK        |
| guest_check_id        | INTEGER   | FK        |
| guest_check_line_item_id | INTEGER |           |
| line_num              | INTEGER   |           |
| detail_utc            | TIMESTAMP |           |
| dsp_ttl               | NUMERIC   |           |
| dsp_qty               | INTEGER   |           |
| menu_item_id          | INTEGER   |           |

---

### menu_items

| Coluna       | Tipo      | Chave     |
|--------------|-----------|-----------|
| menu_item_id | INTEGER   | PK        |
| mi_num       | INTEGER   |           |
| mod_flag     | BOOLEAN   |           |
| incl_tax     | NUMERIC   |           |
| prc_lvl      | INTEGER   |           |

---

## 3. Descreva a abordagem escolhida em detalhes

### Passos Adotados

1. **Data Lake no AWS S3**
   - A estrutura hierárquica do S3 foi projetada para armazenar dados brutos, processados e logs.
   - Respostas das APIs são salvas no bucket `raw/api_responses` com subpastas organizadas por data e endpoint.

2. **ETL Automatizado**
   - Scripts Python foram desenvolvidos para processar os arquivos do S3 e validá-los antes de serem armazenados no banco de dados.
   - Logs são gerados para dados inválidos ou com campos inesperados, e armazenados na pasta `logs` do S3.

3. **Banco Relacional**
   - PostgreSQL no Amazon RDS foi utilizado para armazenar os dados processados.
   - O esquema foi projetado para suportar consultas otimizadas e relações claras entre entidades.

4. **APIs Simuladas**
   - Criadas no AWS API Gateway para simular os dados de um ambiente real.
   - As APIs são acessíveis e permitem testar a integridade do pipeline de dados.

---

### Justificativa das Escolhas

1. **AWS S3**
   - Escolhido por sua escalabilidade e custo-benefício para armazenamento de grandes volumes de dados.

2. **PostgreSQL**
   - Banco de dados relacional confiável, amplamente utilizado e com suporte robusto para consultas complexas.

3. **Python**
   - Flexibilidade para automação de processos ETL e ampla biblioteca de validação de dados.

4. **AWS API Gateway**
   - Permitiu a simulação de endpoints para integração e validação do pipeline de dados.

---

### Consequências

1. **Resiliência**
   - O pipeline é dinâmico e suporta mudanças nos campos do JSON, como a alteração de `taxes` para `taxation`.

2. **Escalabilidade**
   - A arquitetura modular permite fácil inclusão de novos endpoints e ajustes nos esquemas de dados.

3. **Auditabilidade**
   - Logs detalhados armazenados no S3 garantem transparência sobre erros e dados processados.

4. **Manutenção**
   - Código estruturado e documentado para facilitar a manutenção e adaptação futura.

---

## 4. Considerações Finais

Este projeto demonstrou o uso prático de ferramentas de dados em um ambiente real:

- **Armazenamento Escalável**: S3 para dados brutos e processados.
- **Banco Relacional**: PostgreSQL para garantir integridade e eficiência.
- **APIs Dinâmicas**: AWS API Gateway para simulação de serviços.
- **Automação Completa**: Pipeline ETL validado, modular e preparado para mudanças futuras.

O projeto está pronto para ser ampliado e adaptado conforme a necessidade da empresa. Além disso, demonstra uma abordagem robusta e prática para lidar com desafios de engenharia de dados em larga escala.
