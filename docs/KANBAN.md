# Kanban - Desafio Engenharia de Dados

## Objetivo
Este documento organiza as tarefas do desafio de engenharia de dados utilizando o método Kanban, separando as atividades em **A Fazer**, **Em Progresso**, e **Concluído**.

---

## 🗂️ Colunas do Kanban

### 📋 A Fazer
- [ ] Analisar os requisitos do desafio.
- [ ] Estruturar a modelagem das tabelas no PostgreSQL.
- [ ] Criar scripts para ingestão de dados no banco.
- [ ] Configurar o ambiente (AWS, PostgreSQL e Python).
- [ ] Criar estrutura de pastas no S3 para armazenar os dados das APIs.
- [ ] Documentar toda a abordagem no README.md.
- [ ] Preparar o repositório no GitHub para entrega.

### 🔄 Em Progresso
- [ ] Implementar o pipeline ETL dinâmico e resiliente.
- [ ] Testar com JSONs diferentes para validar robustez do pipeline.
- [ ] Configurar logs para erros no processamento e armazená-los no S3.

### ✅ Concluído
- [x] Configuração do PostgreSQL e criação do banco de dados.
- [x] Desenvolvimento dos scripts SQL para criação das tabelas.
- [x] Implementação inicial do pipeline ETL.
- [x] Configuração do ambiente Python com dependências (`boto3`, `psycopg2`, etc.).
- [x] Configuração do bucket S3 para ingestão e organização dos dados.
- [x] Adição de validações dinâmicas para lidar com mudanças no JSON.
- [x] Teste com múltiplos cenários de JSON (campos ausentes, renomeações, etc.).

---

## 📊 Status Atual
- O pipeline ETL já está implementado e funcionando com JSONs dinâmicos.
- Dados são ingeridos no banco de dados PostgreSQL, e logs de erros são armazenados no S3.
- Testes foram realizados para cenários comuns e edge cases.

---

## 🔄 Próximos Passos
- Finalizar a documentação detalhada no README.md.
- Realizar testes finais com todos os endpoints e cenários fornecidos.
- Subir o repositório no GitHub e compartilhar o link para avaliação.

---

## 💡 Melhorias Futuras
- [ ] Integrar o pipeline com ferramentas de orquestração como Apache Airflow.
- [ ] Implementar geração automática de colunas no banco em caso de mudanças no JSON.
- [ ] Adicionar métricas de performance e monitoramento ao pipeline.
- [ ] Configurar pipelines para outras camadas do data lake (transformadas, analíticas).

---

**Organização e Execução por:** Wellington Marques
