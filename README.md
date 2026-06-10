# MCP ERPNext Plugin

Plugin MCP (Model Context Protocol) para integração entre Claude e ERPNext v16. Permite que Claude se conecte e interaja com instâncias do ERPNext através de uma interface simples e segura.

## Características

- ✅ Configuração segura de credenciais (URL, API Key, API Secret)
- ✅ Testes de conexão com ERPNext
- ✅ CRUD completo (Create, Read, Update, Delete) de documentos
- ✅ Suporte para filtros e consultas avançadas
- ✅ Chamadas de métodos Frappe/ERPNext
- ✅ Recuperação de metadados de documentos
- ✅ Interface CLI para configuração
- ✅ Armazenamento seguro de credenciais

## 📦 Instalação

### Guia Rápido

Para instalação completa e detalhada, veja **[INSTALL.md](INSTALL.md)** (recomendado para primeira instalação).

### Resumo
1. Instale Python 3.8+
2. Baixe o repositório
3. Execute `pip install -r requirements.txt`
4. Configure com `python src/cli.py configure --interactive`
5. Adicione ao Claude Desktop via `claude_desktop_config.json`
6. Reinicie Claude Desktop

### Pré-requisitos
- Python 3.8+
- Claude Desktop
- Acesso ao ERPNext v16 (https://erpnext.glsoltec.com.br)

## Configuração

### Obter Credenciais do ERPNext

1. Acesse sua instância do ERPNext
2. Vá para: Menu → Usuário (seu usuário) → Configurações
3. Gere uma nova chave de API:
   - Clique em "Gerar Chave API"
   - Copie a **API Key** e **API Secret**

### Configurar o Plugin

```bash
# Modo interativo (recomendado)
python src/cli.py configure --interactive

# Exemplo de resposta:
# Enter ERPNext URL: https://seu-instance.erpnext.com
# Enter API Key: sua_api_key
# Enter API Secret: seu_api_secret
```

### Verificar Configuração

```bash
# Ver status
python src/cli.py status

# Testar conexão
python src/cli.py test
```

## Uso

### Iniciar o Servidor MCP

```bash
python src/server.py
```

O servidor será iniciado e estará pronto para receber comandos do Claude.

### Ferramentas Disponíveis para Claude

#### 1. `configure_erpnext`
Configura a conexão com ERPNext.

```json
{
  "url": "https://seu-instance.erpnext.com",
  "api_key": "sua_chave_api",
  "api_secret": "seu_secret"
}
```

#### 2. `test_connection`
Testa a conexão com o servidor ERPNext.

```json
{}
```

#### 3. `get_document`
Obtém um documento específico.

```json
{
  "doctype": "Customer",
  "name": "CUST-001"
}
```

#### 4. `get_list`
Obtém uma lista de documentos com filtros opcionais.

```json
{
  "doctype": "Invoice",
  "filters": {"status": "Draft"},
  "fields": ["name", "customer", "total"],
  "limit": 10
}
```

#### 5. `create_document`
Cria um novo documento.

```json
{
  "doctype": "Customer",
  "data": {
    "customer_name": "Novo Cliente",
    "customer_type": "Individual",
    "country": "Brazil"
  }
}
```

#### 6. `update_document`
Atualiza um documento existente.

```json
{
  "doctype": "Customer",
  "name": "CUST-001",
  "data": {
    "customer_name": "Nome Atualizado"
  }
}
```

#### 7. `delete_document`
Deleta um documento.

```json
{
  "doctype": "Customer",
  "name": "CUST-001"
}
```

#### 8. `call_method`
Chama um método Frappe/ERPNext.

```json
{
  "method": "frappe.client.get_list",
  "params": {
    "doctype": "Customer",
    "limit_page_length": 5
  }
}
```

#### 9. `get_config`
Mostra o status da configuração atual.

```json
{}
```

## Exemplos de Uso com Claude

### Exemplo 1: Consultar Clientes
```
Claude: "Liste os 5 primeiros clientes da minha instância ERPNext"

Claude usará:
- get_list(doctype="Customer", limit=5)
```

### Exemplo 2: Criar Nota Fiscal
```
Claude: "Crie uma nota fiscal para o cliente CUST-001 com total de R$ 1.000"

Claude usará:
- create_document(doctype="Invoice", data={...})
```

### Exemplo 3: Atualizar Pedido
```
Claude: "Atualize o pedido SO-001 para status de processamento"

Claude usará:
- update_document(doctype="Sales Order", name="SO-001", data={...})
```

## Estrutura de Diretórios

```
mcp-erpnext/
├── src/
│   ├── __init__.py           # Inicializador do pacote
│   ├── config.py             # Gerenciamento de configuração
│   ├── erpnext_client.py     # Cliente ERPNext
│   ├── server.py             # Servidor MCP
│   └── cli.py                # Interface de linha de comando
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

## Armazenamento de Credenciais

As credenciais são armazenadas de forma segura em:
- **Linux/Mac:** `~/.mcp-erpnext/config.json`
- **Windows:** `C:\Users\seu_usuario\.mcp-erpnext\config.json`

⚠️ **Segurança:** O arquivo contém credenciais sensíveis. Nunca compartilhe ou faça commit deste arquivo no git.

## Segurança

### Boas Práticas
1. Use API Keys específicas para cada integração
2. Defina permissões apropriadas na chave de API no ERPNext
3. Nunca compartilhe credenciais em repositórios públicos
4. Considere usar variáveis de ambiente em produção

### Permissões Recomendadas no ERPNext
- Leitura (Read) para documentos que Claude pode consultar
- Criação (Create) apenas se necessário
- Edição (Write) apenas se necessário
- Exclusão (Delete) restrita ao necessário

## 📚 Documentação

### 🚀 Comece Aqui
- **[INSTALL.md](INSTALL.md)** - Guia passo a passo de instalação (⭐ Comece aqui!)
- **[QUICKSTART.md](QUICKSTART.md)** - Instalação em 5 minutos

### 💡 Usando o Plugin
- **[.claude/README.md](.claude/README.md)** - Como usar com Claude Desktop
- **[API.md](API.md)** - Referência técnica de todas as ferramentas
- **[CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md)** - Integração avançada com Claude

### 🛠️ Desenvolvimento
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Guia para desenvolvedores
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Como contribuir

### 📖 Referências Externas
- [Documentação ERPNext](https://docs.frappe.io/erpnext/introduction)
- [Frappe REST API](https://frappe.io/docs/user/en/guides/basics/api/rest)
- [Claude Documentation](https://docs.anthropic.com)

## Troubleshooting

### Erro: "ERPNext not configured"
Execute o comando de configuração:
```bash
python src/cli.py configure --interactive
```

### Erro: "Connection refused"
Verifique:
1. A URL do ERPNext está correta
2. O servidor ERPNext está rodando
3. Sua rede permite acesso à instância

### Erro: "Unauthorized (401)"
Verifique:
1. API Key e API Secret estão corretos
2. A chave de API ainda é válida
3. O usuário tem permissões necessárias

### Erro: "Forbidden (403)"
A chave de API não tem permissões para a ação. Configure permissões apropriadas no ERPNext.

## Suporte

Para problemas, sugestões ou contribuições:
1. Abra uma issue no repositório
2. Envie um pull request com melhorias
3. Consulte a documentação do Frappe/ERPNext

## Licença

Este projeto está sob licença MIT. Veja LICENSE para detalhes.

## Changelog

### v1.0.0
- Lançamento inicial
- Suporte completo para CRUD de documentos
- Configuração interativa via CLI
- Suporte a filtros e consultas avançadas
- Integração com MCP para Claude
