# Quick Start Guide

## 🚀 Instalação em 5 Minutos

### 1. Clonar e Instalar
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mcp-erpnext.git
cd mcp-erpnext

# Instale as dependências
pip install -r requirements.txt
```

### 2. Obter Credenciais do ERPNext
1. Acesse sua instância do ERPNext
2. Clique no seu **Avatar** (canto superior direito) → **Set User Password**
3. Vá para **API** e clique em **Generate a new API secret** (se não tiver uma)
4. Copie:
   - **API Key** (ex: `user@example.com`)
   - **API Secret** (ex: `abc123xyz...`)

### 3. Configurar o Plugin
```bash
# Modo interativo (recomendado)
python src/cli.py configure --interactive

# Ou com argumentos
python src/cli.py configure \
  --url https://seu-instance.erpnext.com \
  --api-key SUA_API_KEY \
  --api-secret SEU_API_SECRET
```

### 4. Testar Conexão
```bash
python src/cli.py test
```

Você deverá ver:
```
✓ Connection successful!
  Message: Connection successful
```

### 5. Iniciar Servidor MCP
```bash
python src/server.py
```

O servidor está pronto para receber comandos do Claude!

## 📋 Verificação Rápida

```bash
# Ver configurações (sem dados sensíveis)
python src/cli.py status

# Ver caminho do arquivo de configuração
python src/cli.py show

# Rodar exemplo de uso
python example.py
```

## 🔧 Usando com Claude

Quando o servidor MCP estiver rodando, Claude terá acesso às seguintes operações:

- **Consultar dados** → `get_list('Customer')`
- **Criar documento** → `create_document('Invoice', {...})`
- **Atualizar documento** → `update_document('Invoice', 'INV-001', {...})`
- **Deletar documento** → `delete_document('Customer', 'CUST-001')`
- **Executar métodos** → `call_method('frappe.client.get_count', {...})`

## ⚠️ Dicas de Segurança

1. **Nunca compartilhe** suas API Key e Secret
2. **Use permissões restritivas** - Crie uma API key específica para este plugin
3. **Não faça commit** do arquivo `.mcp-erpnext/config.json`
4. **Em produção**, considere usar variáveis de ambiente

## 🆘 Problemas Comuns

### "Connection refused"
- Verifique se a URL está correta (ex: `https://seu-instance.erpnext.com`)
- Verifique se o servidor ERPNext está rodando
- Teste a URL no navegador

### "Unauthorized (401)"
- Verifique se API Key e API Secret estão corretos
- Gere uma nova API Secret no ERPNext
- Copie/Cole com cuidado (sem espaços)

### "Forbidden (403)"
- A chave de API não tem permissões
- Verifique permissões no ERPNext
- Considere usar uma chave de API com mais permissões

## 📚 Próximos Passos

- Leia a [documentação completa](README.md)
- Veja [exemplos de uso](example.py)
- Consulte [documentação do Frappe](https://frappe.io/docs)

## 💬 Precisa de Ajuda?

- Abra uma issue no GitHub
- Consulte a documentação do ERPNext
- Verifique logs de erro do servidor

---

**Pronto para usar!** 🎉
