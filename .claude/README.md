# Claude MCP Server Configuration

Este diretório contém configurações para executar o servidor MCP ERPNext com Claude.

## 📋 Configurações Disponíveis

### `launch.json`

Define como iniciar o servidor MCP para Claude.

**Servidor Configurado:**
- **MCP ERPNext Server** (Python)
  - Comando: `python src\server.py`
  - Porta: 9000
  - Status: Pronto para usar com Claude

## ▶️ Como Iniciar o Servidor

### Opção 1: Claude Desktop
1. Abra `claude_desktop_config.json` em:
   - Windows: `C:\Users\SEU_USUARIO\AppData\Roaming\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. Adicione esta configuração:
```json
{
  "mcpServers": {
    "erpnext": {
      "command": "python",
      "args": [
        "C:\\Users\\Pascoal\\Documents\\GitHub\\mcp-erpnext\\src\\server.py"
      ]
    }
  }
}
```

3. Salve e reinicie Claude Desktop

### Opção 2: Via Terminal
```bash
cd C:\Users\Pascoal\Documents\GitHub\mcp-erpnext
python src\server.py
```

## 🔐 Configurar Credenciais ERPNext

Antes de usar o servidor, configure suas credenciais:

```bash
python src\cli.py configure --interactive
```

Será solicitado:
- **URL ERPNext:** https://erpnext.glsoltec.com.br
- **API Key:** (sua chave do ERPNext)
- **API Secret:** (seu secret do ERPNext)

### Obter Credenciais
1. Acesse: https://erpnext.glsoltec.com.br
2. Menu → Seu Usuário → Configurações
3. Role até "API" e clique em "Gerar Chave API"
4. Copie API Key e API Secret

## ✅ Verificar Configuração

```bash
python src\cli.py test
```

Você deverá ver:
```
✓ Connection successful!
  Message: Connection successful
```

## 📚 Documentação

- [README Principal](../README.md)
- [Guia Rápido](../QUICKSTART.md)
- [Referência de API](../API.md)
- [Integração com Claude](../CLAUDE_INTEGRATION.md)

## 🆘 Troubleshooting

**Erro: "Module not found"**
```bash
pip install -r requirements.txt
```

**Erro: "ERPNext not configured"**
```bash
python src\cli.py configure --interactive
```

**Erro: "Connection refused"**
- Verifique se a URL está correta
- Teste em navegador: https://erpnext.glsoltec.com.br
- Verifique API Key e API Secret

---

**Pronto para usar com Claude!** 🚀
