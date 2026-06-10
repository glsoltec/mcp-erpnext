# Integração com Claude

Guia completo para integrar o plugin MCP ERPNext com Claude em diferentes plataformas.

## 📋 Índice

1. [Claude Desktop App](#claude-desktop-app)
2. [Claude Web (claude.ai)](#claude-web)
3. [Claude API](#claude-api)
4. [Verificar Integração](#verificar-integração)

---

## Claude Desktop App

### Instalação e Configuração

#### Passo 1: Encontrar Arquivo de Configuração

**Windows:**
```
C:\Users\SEU_USUARIO\AppData\Roaming\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

#### Passo 2: Editar Arquivo de Configuração

Abra o arquivo `claude_desktop_config.json` com um editor de texto e adicione:

```json
{
  "mcpServers": {
    "erpnext": {
      "command": "python",
      "args": [
        "C:\\Users\\SEU_USUARIO\\mcp-erpnext\\src\\server.py"
      ]
    }
  }
}
```

**Ajuste o caminho conforme sua instalação:**
- Windows: Use caminho absoluto (ex: `C:\\Users\\Pascoal\\mcp-erpnext\\...`)
- macOS/Linux: Use caminho absoluto (ex: `/Users/seu_usuario/mcp-erpnext/...`)

#### Passo 3: Reiniciar Claude

1. Feche completamente o Claude Desktop
2. Reabra o Claude Desktop
3. Procure pelo ícone de plugin/ferramentas (geralmente no canto inferior da janela)
4. Verifique se "erpnext" aparece na lista de servidores MCP

#### Passo 4: Configurar Credenciais

Dentro do Claude (em uma conversa), solicite:

```
Configure o ERPNext para mim usando:
- URL: https://sua-instancia.erpnext.com
- API Key: sua_api_key
- API Secret: seu_api_secret
```

Ou configure manualmente antes de usar:

```bash
python src/cli.py configure --interactive
```

---

## Claude Web

### Usando via claude.ai (Com Extensão MCP)

Nota: A integração de MCP no web é limitada. Você pode:

1. Usar através da CLI com encaminhamento da porta
2. Integrar via API do Claude

### Solução Alternativa: Usar via API

Crie um script Python que chama Claude API com ferramentas customizadas:

```python
from anthropic import Anthropic

client = Anthropic()

# Sua ferramenta customizada
TOOLS = [
    {
        "name": "query_erpnext",
        "description": "Query ERPNext documents",
        "input_schema": {
            "type": "object",
            "properties": {
                "doctype": {
                    "type": "string",
                    "description": "Document type (e.g., Customer, Invoice)"
                },
                "action": {
                    "type": "string",
                    "enum": ["list", "get", "create", "update", "delete"],
                    "description": "Action to perform"
                },
                "params": {
                    "type": "object",
                    "description": "Parameters for the action"
                }
            },
            "required": ["doctype", "action"]
        }
    }
]

def query_erpnext(doctype, action, params):
    """Your ERPNext query implementation"""
    # Implement calls to your MCP server
    pass

messages = []

while True:
    user_input = input("\nYou: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["quit", "exit"]:
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        tools=TOOLS,
        messages=messages
    )

    # Handle tool calls
    for block in response.content:
        if block.type == "text":
            print(f"\nClaude: {block.text}")
        elif block.type == "tool_use":
            tool_result = query_erpnext(
                block.input["doctype"],
                block.input["action"],
                block.input.get("params", {})
            )
            messages.append({
                "role": "assistant",
                "content": response.content
            })
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(tool_result)
                    }
                ]
            })
```

---

## Claude API

### Integração via SDK Python

#### 1. Instalar SDK Anthropic

```bash
pip install anthropic
```

#### 2. Criar Script de Integração

```python
#!/usr/bin/env python3
from anthropic import Anthropic
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import PluginConfig
from erpnext_client import ERPNextClient

# Inicializar cliente
client = Anthropic()

# Carregar configuração ERPNext
config = PluginConfig()
if not config.has_erpnext_config():
    print("ERPNext não configurado. Execute: python src/cli.py configure --interactive")
    sys.exit(1)

erpnext_config = config.get_erpnext_config()
erpnext = ERPNextClient(erpnext_config)

# Definir ferramentas disponíveis
TOOLS = [
    {
        "name": "query_customers",
        "description": "List customers from ERPNext",
        "input_schema": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of results",
                    "default": 10
                }
            }
        }
    },
    {
        "name": "query_invoices",
        "description": "List sales invoices from ERPNext",
        "input_schema": {
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "enum": ["Draft", "Submitted", "Cancelled"],
                    "description": "Invoice status"
                },
                "limit": {
                    "type": "integer",
                    "default": 10
                }
            }
        }
    },
    {
        "name": "create_customer",
        "description": "Create a new customer in ERPNext",
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_name": {"type": "string"},
                "customer_type": {"type": "string"},
                "country": {"type": "string"}
            },
            "required": ["customer_name"]
        }
    }
]

def execute_tool(name, input):
    """Execute tool and return result"""
    try:
        if name == "query_customers":
            result = erpnext.get_list('Customer', limit=input.get('limit', 10))
            return json.dumps(result)
        elif name == "query_invoices":
            filters = {}
            if 'status' in input:
                filters['status'] = input['status']
            result = erpnext.get_list('Sales Invoice', filters=filters, limit=input.get('limit', 10))
            return json.dumps(result)
        elif name == "create_customer":
            result = erpnext.create_document('Customer', input)
            return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})

def chat_with_claude():
    """Main chat loop"""
    messages = []
    system_prompt = """
You are an assistant that helps users query and manage their ERPNext system.
You have access to tools to:
- Query customers and invoices
- Create new customers

Be helpful and provide clear responses about the data you retrieve.
"""

    print("Chat with Claude + ERPNext (type 'exit' to quit)\n")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit"]:
            break

        messages.append({
            "role": "user",
            "content": user_input
        })

        # Call Claude
        response = client.messages.create(
            model="claude-opus-4-8",
            max_tokens=2048,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )

        # Process response
        assistant_message = []
        for block in response.content:
            if block.type == "text":
                print(f"\nClaude: {block.text}")
                assistant_message.append(block)
            elif block.type == "tool_use":
                tool_result = execute_tool(block.name, block.input)
                print(f"\n[Executando: {block.name}]")
                assistant_message.append(block)

                # Se o modelo quer usar ferramentas, continue o loop
                if response.stop_reason == "tool_use":
                    messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                    # Adicionar resultado da ferramenta
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": tool_result
                            }
                        ]
                    })

                    # Obter resposta final
                    final_response = client.messages.create(
                        model="claude-opus-4-8",
                        max_tokens=2048,
                        system=system_prompt,
                        tools=TOOLS,
                        messages=messages
                    )

                    for final_block in final_response.content:
                        if final_block.type == "text":
                            print(f"\nClaude: {final_block.text}")

                    messages.append({
                        "role": "assistant",
                        "content": final_response.content
                    })

if __name__ == "__main__":
    chat_with_claude()
```

#### 3. Executar Script

```bash
python script_integracao.py
```

---

## Verificar Integração

### 1. Testar Conexão MCP

No Claude Desktop, procure pelo ícone de ferramentas e verifique:

```
✓ erpnext - Conectado
```

### 2. Testar Primeiro Comando

Converse com Claude:

```
"Teste a conexão com o ERPNext"
```

Claude deverá responder com sucesso.

### 3. Verificar Logs

**Claude Desktop:**
1. Clique no menu (⋯)
2. Vá para "Developer" ou "Settings"
3. Procure pela aba de logs

**CLI:**
```bash
python src/server.py  # Ver logs no console
```

---

## Configuração Avançada

### Múltiplas Instâncias ERPNext

Crie diferentes arquivos de configuração:

```bash
# Instância 1
python src/cli.py configure --url https://prod.erpnext.com --api-key KEY1 --api-secret SECRET1

# Instância 2 (criar novo arquivo manualmente)
# ~/.mcp-erpnext/config.json
```

### Permissões por Chave de API

No ERPNext, você pode limitar o que cada chave pode fazer:

1. Vá para Configurações do Usuário
2. Role para "API"
3. Clique em "Permissões de Acesso"
4. Selecione os documentos que a chave pode acessar

---

## Troubleshooting

### Claude não encontra o servidor MCP

**Windows:**
```json
"command": "python",
"args": ["C:\\Users\\SEU_USUARIO\\mcp-erpnext\\src\\server.py"]
```

**macOS/Linux:**
```json
"command": "python3",
"args": ["/Users/seu_usuario/mcp-erpnext/src/server.py"]
```

### Erro: "Module not found"

```bash
# Reinstale dependências
pip install -r requirements.txt

# Ou em modo desenvolvimento
pip install -e .
```

### Conexão ERPNext falha

```bash
# Teste manualmente
python src/cli.py test

# Se falhar, verifique:
# 1. URL está correta?
# 2. API Key é válida?
# 3. Servidor ERPNext está rodando?
```

---

## Exemplo de Conversa

```
You: Quantos clientes temos cadastrados?

Claude: [Usa ferramenta query_customers]
        Você tem 45 clientes cadastrados no seu ERPNext.

You: Me mostre os 5 últimos?

Claude: [Usa ferramenta query_customers com limit=5]
        Aqui estão os 5 últimos clientes:
        1. CUST-045 - Empresa XYZ
        2. CUST-044 - Negócio ABC
        ... (mais resultados)

You: Crie um novo cliente chamado "Novo Negócio"

Claude: [Usa ferramenta create_customer]
        Criei com sucesso o cliente "Novo Negócio" com ID CUST-046.
```

---

## Próximos Passos

- Customize as ferramentas para suas necessidades
- Adicione mais operações (relatórios, automações)
- Integre com outros sistemas
- Implante em produção com segurança

---

## Documentação Adicional

- [Guia de Instalação](QUICKSTART.md)
- [Referência de API](API.md)
- [Documentação do ERPNext](https://docs.frappe.io/erpnext)
- [Documentação do Claude](https://docs.anthropic.com)
