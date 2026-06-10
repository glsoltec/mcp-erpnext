# Guia de Desenvolvimento

Instruções para configurar o ambiente de desenvolvimento e trabalhar no plugin MCP ERPNext.

## 🛠️ Setup Inicial

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes)
- Git
- GitHub Desktop (opcional, mas recomendado)

### 1. Clonar Repositório
```bash
cd C:\Users\Pascoal\Documents\GitHub
git clone https://github.com/glsoltec/mcp-erpnext.git
cd mcp-erpnext
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
pip install -e ".[dev]"
```

### 4. Configurar ERPNext
```bash
python src\cli.py configure --interactive
```

## 🚀 Rodar o Servidor

### Desenvolvimento Local
```bash
python src\server.py
```

O servidor estará disponível na porta 9000.

### Com Docker Compose (ERPNext Completo)
```bash
docker-compose up -d
```

Acesse em: http://localhost:8000

## ✅ Testes

### Rodar Testes Unitários
```bash
pytest
```

### Com Cobertura
```bash
pytest --cov=src --cov-report=html
```

### Teste Específico
```bash
pytest tests/test_config.py::TestPluginConfig::test_set_and_get_erpnext_credentials
```

## 📝 Código

### Verificação de Estilo
```bash
# Formatar código
black src tests

# Verificar estilo
flake8 src tests

# Organizar imports
isort src tests

# Verificar tipos
mypy src
```

### Estrutura de Arquivos
```
src/
  ├── __init__.py          # Exports
  ├── config.py            # Configuração
  ├── erpnext_client.py    # Cliente REST
  ├── server.py            # Servidor MCP
  └── cli.py               # CLI
tests/
  └── test_*.py            # Testes
```

## 🔄 Git Workflow

### 1. Criar Branch de Feature
```bash
git checkout -b feature/sua-feature
```

### 2. Fazer Alterações
- Edite os arquivos
- Rode testes: `pytest`
- Verifique estilo: `black` e `flake8`

### 3. Commit
```bash
git add .
git commit -m "feat(modulo): descrição da mudança"
```

**Tipos de Commit:**
- `feat`: Nova feature
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

### 4. Push e Pull Request
```bash
git push origin feature/sua-feature
```

Abra um Pull Request no GitHub.

## 📚 Documentação

Ao adicionar features:
1. Atualize `API.md` com novos endpoints
2. Atualize `README.md` se necessário
3. Adicione docstrings nas funções

## 🔐 Variáveis de Ambiente

Para desenvolvimento, copie `.env.example` para `.env`:
```bash
cp .env.example .env
```

Edite com seus valores:
```
ERPNEXT_URL=https://erpnext.glsoltec.com.br
ERPNEXT_API_KEY=sua_chave
ERPNEXT_API_SECRET=seu_secret
```

⚠️ Nunca commite `.env` com dados reais!

## 🐛 Debug

### Logs do Servidor
```bash
python src\server.py 2>&1 | tee server.log
```

### Teste de Conexão
```bash
python src\cli.py test
```

### Ver Configuração
```bash
python src\cli.py status
python src\cli.py show
```

## 📦 Release

### Versionamento
Versão segue [Semantic Versioning](https://semver.org/):
- MAJOR: mudanças incompatíveis
- MINOR: novas features compatíveis
- PATCH: correções de bugs

### Publicar Nova Versão

1. Atualize `setup.py`:
   ```python
   version='1.1.0'
   ```

2. Atualize `pyproject.toml`:
   ```toml
   version = "1.1.0"
   ```

3. Commit e Tag:
   ```bash
   git add setup.py pyproject.toml
   git commit -m "chore: version 1.1.0"
   git tag v1.1.0
   git push origin main --tags
   ```

## 🆘 Problemas Comuns

**Erro ao instalar dependencies**
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Servidor não inicia**
```bash
python -m pip install -e .
python src\cli.py test
```

**Testes falhando**
```bash
pytest -v --tb=short
```

## 📞 Suporte

- Issues: GitHub Issues
- Docs: Veja [README.md](README.md)
- API: Veja [API.md](API.md)

---

**Happy coding!** 🎉
