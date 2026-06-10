# API Reference - MCP ERPNext Plugin

Documentação completa das ferramentas disponíveis no plugin MCP para integração com Claude.

## Ferramentas Disponíveis

### 1. `configure_erpnext`

**Descrição:** Configura a conexão com o servidor ERPNext.

**Parâmetros:**
```json
{
  "url": "string (required) - URL da instância ERPNext",
  "api_key": "string (required) - Chave API do ERPNext",
  "api_secret": "string (required) - Segredo API do ERPNext"
}
```

**Resposta Bem-sucedida:**
```json
{
  "success": true,
  "message": "ERPNext configuration saved successfully"
}
```

**Resposta de Erro:**
```json
{
  "error": "Configuration failed: [motivo do erro]"
}
```

**Exemplo:**
```json
{
  "url": "https://sua-instancia.erpnext.com",
  "api_key": "sua_api_key",
  "api_secret": "seu_api_secret"
}
```

---

### 2. `test_connection`

**Descrição:** Testa a conexão com o servidor ERPNext.

**Parâmetros:** (nenhum)

**Resposta Bem-sucedida:**
```json
{
  "success": true,
  "message": "Connection successful"
}
```

**Resposta de Erro:**
```json
{
  "success": false,
  "message": "[motivo do erro]"
}
```

---

### 3. `get_document`

**Descrição:** Obtém um documento específico do ERPNext.

**Parâmetros:**
```json
{
  "doctype": "string (required) - Tipo de documento",
  "name": "string (required) - Nome/ID do documento"
}
```

**Resposta Bem-sucedida:**
```json
{
  "data": {
    "name": "CUST-001",
    "doctype": "Customer",
    "customer_name": "Acme Corporation",
    ...
  }
}
```

**Exemplo:**
```json
{
  "doctype": "Customer",
  "name": "CUST-001"
}
```

---

### 4. `get_list`

**Descrição:** Obtém uma lista de documentos com filtros opcionais.

**Parâmetros:**
```json
{
  "doctype": "string (required) - Tipo de documento",
  "filters": "object (optional) - Condições de filtro",
  "fields": "array (optional) - Campos a retornar",
  "limit": "integer (optional) - Limitar resultados (padrão: 20)"
}
```

**Resposta Bem-sucedida:**
```json
{
  "data": [
    {
      "name": "CUST-001",
      "customer_name": "Acme Corp"
    },
    {
      "name": "CUST-002",
      "customer_name": "Globex Corp"
    }
  ]
}
```

**Exemplo 1: Lista simples**
```json
{
  "doctype": "Customer",
  "limit": 10
}
```

**Exemplo 2: Com filtros**
```json
{
  "doctype": "Invoice",
  "filters": {
    "docstatus": 0,
    "customer": "CUST-001"
  },
  "fields": ["name", "customer", "total_amount"],
  "limit": 20
}
```

**Sintaxe de Filtros:**
- Igualdade: `{"field": "value"}`
- Comparação: `{"field": ["!=", "value"]}`
- Intervalo: `{"field": [">=", "100"]}`
- Operadores: `["=", "!=", ">", "<", ">=", "<=", "like", "in"]`

---

### 5. `create_document`

**Descrição:** Cria um novo documento no ERPNext.

**Parâmetros:**
```json
{
  "doctype": "string (required) - Tipo de documento",
  "data": "object (required) - Dados do novo documento"
}
```

**Resposta Bem-sucedida:**
```json
{
  "data": {
    "name": "CUST-NEW-001",
    "doctype": "Customer",
    "customer_name": "Nova Empresa",
    ...
  }
}
```

**Exemplo: Criar Cliente**
```json
{
  "doctype": "Customer",
  "data": {
    "customer_name": "Nova Empresa Ltda",
    "customer_type": "Company",
    "country": "Brazil",
    "customer_group": "All Customer Groups"
  }
}
```

**Exemplo: Criar Nota Fiscal**
```json
{
  "doctype": "Sales Invoice",
  "data": {
    "customer": "CUST-001",
    "posting_date": "2024-01-15",
    "due_date": "2024-02-15",
    "items": [
      {
        "item_code": "ITEM-001",
        "qty": 5,
        "rate": 100
      }
    ]
  }
}
```

---

### 6. `update_document`

**Descrição:** Atualiza um documento existente no ERPNext.

**Parâmetros:**
```json
{
  "doctype": "string (required) - Tipo de documento",
  "name": "string (required) - Nome/ID do documento",
  "data": "object (required) - Campos a atualizar"
}
```

**Resposta Bem-sucedida:**
```json
{
  "data": {
    "name": "CUST-001",
    "doctype": "Customer",
    "customer_name": "Nome Atualizado",
    ...
  }
}
```

**Exemplo 1: Atualizar Cliente**
```json
{
  "doctype": "Customer",
  "name": "CUST-001",
  "data": {
    "customer_name": "Nova Denominação Social",
    "email": "novo@example.com"
  }
}
```

**Exemplo 2: Atualizar Status**
```json
{
  "doctype": "Sales Order",
  "name": "SO-001",
  "data": {
    "status": "To Deliver and Bill"
  }
}
```

---

### 7. `delete_document`

**Descrição:** Deleta um documento do ERPNext.

**Parâmetros:**
```json
{
  "doctype": "string (required) - Tipo de documento",
  "name": "string (required) - Nome/ID do documento"
}
```

**Resposta Bem-sucedida:**
```json
{
  "success": true,
  "message": "Customer CUST-001 deleted"
}
```

**Exemplo:**
```json
{
  "doctype": "Customer",
  "name": "CUST-TEMP-001"
}
```

---

### 8. `call_method`

**Descrição:** Chama um método Frappe/ERPNext personalizado.

**Parâmetros:**
```json
{
  "method": "string (required) - Nome do método",
  "params": "object (optional) - Parâmetros do método"
}
```

**Resposta:**
```json
{
  "message": "[resultado do método]"
}
```

**Exemplos Comuns:**

**Exemplo 1: Contar Documentos**
```json
{
  "method": "frappe.client.get_count",
  "params": {
    "doctype": "Customer"
  }
}
```

**Exemplo 2: Obter Valor Sequencial**
```json
{
  "method": "frappe.client.get_next_name",
  "params": {
    "doctype": "Sales Invoice"
  }
}
```

**Exemplo 3: Executar Ação**
```json
{
  "method": "frappe.client.set_value",
  "params": {
    "doctype": "Invoice",
    "name": "INV-001",
    "fieldname": "status",
    "value": "Submitted"
  }
}
```

---

### 9. `get_config`

**Descrição:** Obtém o status da configuração atual (sem expor dados sensíveis).

**Parâmetros:** (nenhum)

**Resposta:**
```json
{
  "erpnext": {
    "url": "https://sua-instancia.erpnext.com",
    "configured": true
  },
  "claude": {
    "configured": true
  }
}
```

---

## Tipos de Documentos Comuns

### Vendas
- `Sales Order` - Pedido de Venda
- `Sales Invoice` - Nota Fiscal
- `Sales Return` - Devolução de Venda
- `Quotation` - Orçamento
- `Customer` - Cliente

### Compras
- `Purchase Order` - Pedido de Compra
- `Purchase Invoice` - Fatura de Compra
- `Purchase Return` - Devolução de Compra
- `Supplier` - Fornecedor

### Estoque
- `Item` - Produto/Serviço
- `Stock Ledger Entry` - Movimento de Estoque
- `Warehouse` - Armazém
- `Stock Transfer` - Transferência de Estoque

### Contábil
- `Journal Entry` - Lançamento Contábil
- `Payment Entry` - Recebimento/Pagamento
- `Expense Claim` - Reembolso de Despesa

### Recursos Humanos
- `Employee` - Funcionário
- `Attendance` - Presença
- `Leave Application` - Solicitação de Licença
- `Salary Structure` - Estrutura de Salário

---

## Códigos de Status HTTP

| Código | Significado |
|--------|------------|
| 200 | Sucesso |
| 400 | Requisição Inválida |
| 401 | Não Autorizado (credenciais inválidas) |
| 403 | Acesso Negado (sem permissão) |
| 404 | Documento não encontrado |
| 500 | Erro no Servidor |

---

## Filtros Avançados

### Operadores de Comparação
```python
# Igual
{"field": "value"}

# Não igual
{"field": ["!=", "value"]}

# Maior que
{"field": [">", 100]}

# Menor que
{"field": ["<", 100]}

# Maior ou igual
{"field": [">=", 100]}

# Menor ou igual
{"field": ["<=", 100]}

# Contém (LIKE)
{"field": ["like", "%text%"]}

# Em lista
{"field": ["in", ["value1", "value2"]]}

# Entre (BETWEEN)
{"field": ["between", [100, 200]]}

# É NULL
{"field": ["is", "null"]}

# Não é NULL
{"field": ["is", "not null"]}
```

### Filtros Compostos
```json
{
  "doctype": "Invoice",
  "filters": {
    "status": "Draft",
    "customer": "CUST-001",
    "total_amount": [">", 1000],
    "posting_date": [">=", "2024-01-01"]
  }
}
```

---

## Melhorias de Performance

### Limitar Campos
```json
{
  "doctype": "Customer",
  "fields": ["name", "customer_name", "email"],
  "limit": 100
}
```

### Usar Filtros Eficientes
```json
{
  "doctype": "Invoice",
  "filters": {
    "docstatus": 1,
    "posting_date": [">=", "2024-01-01"]
  }
}
```

---

## Tratamento de Erros

Sempre verifique se há `error` na resposta:

```python
if "error" in response:
    print(f"Erro: {response['error']}")
else:
    # Processar dados com sucesso
    data = response.get("data")
```

---

## Segurança

- ✅ Use HTTPS sempre
- ✅ Mantenha API Key e Secret seguros
- ✅ Revoke chaves não utilizadas
- ✅ Use permissões restritivas
- ✅ Implemente rate limiting em produção

---

## Mais Informações

- [Documentação Frappe](https://frappe.io/docs)
- [API do ERPNext](https://docs.frappe.io/erpnext/introduction)
- [Exemplos de Uso](example.py)
