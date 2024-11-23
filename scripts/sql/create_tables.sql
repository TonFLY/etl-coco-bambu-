-- Tabela principal das transações
CREATE TABLE guest_checks (
    guest_check_id BIGINT PRIMARY KEY,  -- ID único para o check
    chk_num INTEGER,                    -- Número do check
    opn_bus_dt DATE,                    -- Data de abertura
    clsd_bus_dt DATE,                   -- Data de fechamento
    sub_ttl NUMERIC(10, 2),             -- Subtotal
    chk_ttl NUMERIC(10, 2),             -- Total do check
    emp_num INTEGER,                    -- ID do funcionário
    num_srvc_rd INTEGER,                -- Número de rodadas de serviço
    num_chk_prntd INTEGER               -- Número de vezes que o check foi impresso
);

-- Tabela de impostos
CREATE TABLE taxes (
    tax_id BIGSERIAL PRIMARY KEY,       -- ID único do imposto
    guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),  -- Relacionamento com guest_checks
    tax_num INTEGER,                    -- Número do imposto
    txbl_sls_ttl NUMERIC(10, 2),        -- Total de vendas tributáveis
    tax_coll_ttl NUMERIC(10, 2),        -- Total arrecadado de imposto
    tax_rate NUMERIC(5, 2)              -- Taxa de imposto
);

-- Tabela de detalhes das linhas (itens consumidos)
CREATE TABLE detail_lines (
    detail_line_id BIGSERIAL PRIMARY KEY,   -- ID único da linha
    guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),  -- Relacionamento com guest_checks
    line_num INTEGER,                       -- Número da linha
    detail_utc TIMESTAMP,                   -- Data/hora da linha
    dsp_ttl NUMERIC(10, 2),                 -- Valor total
    dsp_qty INTEGER,                        -- Quantidade
    menu_item_id BIGINT REFERENCES menu_items(menu_item_id)  -- Relacionamento com menu_items
);

-- Tabela de itens do menu
CREATE TABLE menu_items (
    menu_item_id BIGSERIAL PRIMARY KEY, -- ID único do item
    mi_num INTEGER,                    -- Número do item do menu
    mod_flag BOOLEAN,                  -- Indica se houve modificação
    incl_tax NUMERIC(10, 2),           -- Taxa incluída
    prc_lvl INTEGER                    -- Nível de preço
);

-- Tabela genérica para instâncias adicionais (discount, serviceCharge, tenderMedia, etc.)
CREATE TABLE additional_instances (
    instance_id BIGSERIAL PRIMARY KEY,     -- ID único da instância
    detail_line_id BIGINT REFERENCES detail_lines(detail_line_id),  -- Relacionamento com detail_lines
    instance_type VARCHAR(50),            -- Tipo de instância (discount, serviceCharge, etc.)
    instance_data JSONB                    -- Dados completos da instância
);
