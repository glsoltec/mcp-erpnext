# 📦 Guia Completo de Instalação

Instruções passo a passo para instalar e configurar o plugin MCP ERPNext no Claude Desktop.

---

## 🎯 O que você vai instalar

Um plugin que conecta Claude diretamente ao seu ERPNext, permitindo:
- Consultar dados (clientes, notas fiscais, etc)
- Criar documentos
- Atualizar informações
- Executar operações em massa
- Tudo através de conversas naturais com Claude

---

## ✅ Pré-requisitos

### Obrigatório
- ✅ **Windows, Mac ou Linux**
- ✅ **Python 3.8+** instalado (https://python.org)
- ✅ **Claude Desktop** instalado (https://claude.ai/download)
- ✅ **Acesso ao ERPNext** em https://erpnext.glsoltec.com.br
- ✅ **Permissão para gerar API Key** no seu ERPNext

### Opcional
- GitHub Desktop (mais fácil para atualizações)
- VS Code ou editor de texto

---

## 🚀 Passo 1: Instalar Python

### Windows
1. Acesse https://python.org/downloads
2. Clique em **Download Python 3.12** (ou versão mais recente)
3. Execute o instalador
4. ⚠️ **IMPORTANTE:** Marque ☑️ **"Add Python to PATH"**
5. Clique em **Install Now**

### Verificar Instalação
Abra PowerShell/Terminal e execute:
```bash
python --version
pip --version
```

Você deverá ver algo como:
```
Python 3.12.x
pip 24.x.x
```

---

## 🔑 Passo 2: Obter Credenciais do ERPNext

### No seu ERPNext (https://erpnext.glsoltec.com.br)

1. **Faça login** com seu usuário
2. Clique no **Avatar** (canto superior direito)
3. Vá para **Meu Perfil** ou **Configurações**
4. Procure por uma seção chamada **"API"** ou **"API Keys"**
5. Clique em **"Gerar Chave API"** (se não tiver uma)

### Salve em local seguro:
```
URL: https://erpnext.glsoltec.com.br
API Key: [sua_api_key]
API Secret: [seu_api_secret]
```

⚠️ **Segurança:** Nunca compartilhe essas credenciais!

---

## 💻 Passo 3: Baixar o Código

### Opção A: Com GitHub Desktop (Recomendado)

1. Abra https://github.com/glsoltec/mcp-erpnext
2. Clique em **Code** (botão verde)
3. Clique em **Open with GitHub Desktop**
4. Escolha local para salvar (recomenda-se `C:\Users\SeuUsuario\Documents\GitHub`)
5. Clique em **Clone**

### Opção B: Via Terminal

```bash
cd Documents
git clone https://github.com/glsoltec/mcp-erpnext.git
cd mcp-erpnext
```

### Opção C: Download Manual

1. Acesse https://github.com/glsoltec/mcp-erpnext
2. Clique em **Code** → **Download ZIP**
3. Extraia em `C:\Users\SeuUsuario\Documents\GitHub\mcp-erpnext`

---

## 📦 Passo 4: Instalar Dependências

Abra **PowerShell** ou **Terminal** na pasta do projeto:

```bash
# Windows
cd C:\Users\SeuUsuario\Documents\GitHub\mcp-erpnext

# Mac/Linux
cd ~/Documents/GitHub/mcp-erpnext
```

Execute:
```bash
pip install -r requirements.txt
```

Aguarde a instalação (pode levar 1-2 minutos).

---

## ⚙️ Passo 5: Configurar as Credenciais

No mesmo terminal, execute:

```bash
python src/cli.py configure --interactive
```

Será solicitado:

```
=== ERPNext Configuration Setup ===

Enter ERPNext URL: https://erpnext.glsoltec.com.br
Enter API Key: [cole aqui]
Enter API Secret: [cole aqui]
```

Se vir:
```
✓ Configuration saved successfully!
  URL: https://erpnext.glsoltec.com.br
  Config file: C:\Users\...\.mcp-erpnext\config.json
```

**Perfeito!** ✅

---

## ✔️ Passo 6: Testar a Conexão

Execute:

```bash
python src/cli.py test
```

Você deve ver:
```
✓ Connection successful!
  Message: Connection successful
```

Se vir um erro:
- Verifique se a URL está correta
- Verifique se API Key e Secret estão corretos (sem espaços)
- Tente novamente

---

## 🖥️ Passo 7: Instalar no Claude Desktop

### Localizar Arquivo de Configuração

**Windows:**
```
C:\Users\SeuUsuario\AppData\Roaming\Claude\claude_desktop_config.json
```

**Mac:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Se o arquivo NÃO existir:

1. Abra um editor de texto (Notepad, VS Code)
2. Cole isto:

```json
{
  "mcpServers": {
    "erpnext": {
      "command": "python",
      "args": [
        "C:\\Users\\SeuUsuario\\Documents\\GitHub\\mcp-erpnext\\src\\server.py"
      ]
    }
  }
}
```

3. **Substitua `SeuUsuario` pelo seu nome real**
4. Salve como `claude_desktop_config.json` na pasta apropriada

### Se o arquivo JÁ existir:

1. Abra em editor de texto
2. Procure por `"mcpServers"` (deve ter um `{`)
3. Dentro de `mcpServers`, adicione:

```json
"erpnext": {
  "command": "python",
  "args": [
    "C:\\Users\\SeuUsuario\\Documents\\GitHub\\mcp-erpnext\\src\\server.py"
  ]
}
```

**Exemplo completo:**
```json
{
  "mcpServers": {
    "erpnext": {
      "command": "python",
      "args": [
        "C:\\Users\\Pascoal\\Documents\\GitHub\\mcp-erpnext\\src\\server.py"
      ]
    },
    "outro-servidor": {
      "command": "...",
      "args": [...]
    }
  }
}
```

4. Salve o arquivo

---

## 🔄 Passo 8: Reiniciar Claude Desktop

1. **Feche completamente** o Claude Desktop (não apenas minimize)
2. Abra novamente
3. Aguarde ~10 segundos para carregar

---

## ✨ Passo 9: Verificar Instalação

No Claude Desktop:

1. Procure pelo **ícone de ferramentas** (⚙️ ou 🔧) - geralmente no canto inferior
2. Procure por uma seção chamada "Connected Servers" ou similar
3. Você deve ver: ✅ **erpnext - Connected**

Se vir ❌ ou ⚠️:
- Verifique o caminho em `claude_desktop_config.json`
- Verifique se Python está instalado (`python --version`)
- Reinicie Claude Desktop
- Veja a seção [Troubleshooting](#troubleshooting) abaixo

---

## 🎉 Pronto para Usar!

Agora no Claude Desktop, converse normalmente:

```
Você: "Quantos clientes temos cadastrados?"
Claude: [conecta ao ERPNext e responde]

Você: "Liste os 10 últimos clientes"
Claude: [mostra lista]

Você: "Crie um novo cliente chamado 'Acme Corporation'"
Claude: [cria o cliente]
```

---

## 🆘 Troubleshooting

### ❌ Python não encontrado

```bash
python --version
```

Se não funcionar, instale Python:
https://python.org/downloads

### ❌ "Module not found: pydantic"

Reinstale dependências:
```bash
pip install -r requirements.txt
```

### ❌ "ERPNext not configured"

Configure novamente:
```bash
python src/cli.py configure --interactive
```

### ❌ "Connection refused"

Verifique:
1. URL está correta? (https://erpnext.glsoltec.com.br)
2. Seu internet está funcionando?
3. ERPNext está online?
4. Teste a URL no navegador

### ❌ "Unauthorized (401)"

Suas credenciais estão erradas:
```bash
python src/cli.py configure --interactive
```

Gere uma nova API Key no ERPNext

### ❌ Claude Desktop não encontra o servidor

Verifique o arquivo `claude_desktop_config.json`:
- Caminho está correto?
- JSON é válido? (sem erros de sintaxe)
- Use https://jsonlint.com/ para validar

Exemplo válido para Windows:
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

### ❌ Ainda não funciona?

1. Abra terminal na pasta do projeto:
```bash
cd C:\Users\SeuUsuario\Documents\GitHub\mcp-erpnext
```

2. Execute o servidor manualmente:
```bash
python src/server.py
```

3. Você deve ver algo como:
```
MCP Server starting...
Listening on port 9000
```

Se vir erros, leia a mensagem - ela indicará o problema.

---

## 📚 Próximos Passos

1. **Leia** [API.md](API.md) para ver todas as operações disponíveis
2. **Customize** suas operações no ERPNext
3. **Explore** os exemplos em [example.py](example.py)
4. **Leia** [CLAUDE_INTEGRATION.md](CLAUDE_INTEGRATION.md) para usos avançados

---

## 🔐 Dicas de Segurança

### ✅ Faça isso
- ✅ Use uma chave de API específica para este plugin
- ✅ Defina permissões restritivas na chave
- ✅ Guarde seus secrets com segurança

### ❌ NÃO faça isso
- ❌ Nunca compartilhe API Key ou Secret
- ❌ Não faça commit de `~/.mcp-erpnext/config.json`
- ❌ Não use chave de administrador do ERPNext

---

## 📞 Suporte

- **Issues:** https://github.com/glsoltec/mcp-erpnext/issues
- **Documentação:** [README.md](README.md)
- **API Reference:** [API.md](API.md)

---

**Sucesso na instalação!** 🚀
