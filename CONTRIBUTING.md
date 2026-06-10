# Contribuindo para MCP ERPNext

Obrigado por considerar contribuir para o MCP ERPNext! Este documento fornece diretrizes e instruções para contribuir.

## Código de Conduta

Esperamos que todos os contribuidores tratarem uns aos outros com respeito. Comportamentos agressivos ou discriminatórios não são tolerados.

## Como Contribuir

### Reportando Bugs

Antes de criar um relatório de bug, verifique se o problema já não foi reportado. Ao criar um relatório de bug, inclua:

- **Um título claro e descritivo**
- **Uma descrição detalhada do comportamento observado**
- **Exemplo específico para demonstrar os passos**
- **O comportamento esperado vs. comportamento atual**
- **Screenshots ou logs** (se aplicável)
- **Sua configuração** (versão Python, SO, versão ERPNext)

### Sugerindo Melhorias

Ao sugerir uma melhoria, inclua:

- **Um título claro e descritivo**
- **Uma descrição detalhada da sugestão**
- **Exemplos de uso**
- **Explicação de por que essa melhoria seria útil**

### Pull Requests

- Siga o estilo de código do projeto
- Inclua testes apropriados
- Atualize a documentação conforme necessário
- Termine todos os arquivos com uma nova linha

## Guia de Desenvolvimento

### Setup do Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/mcp-erpnext.git
cd mcp-erpnext

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # ou no Windows: venv\Scripts\activate

# Instale em modo desenvolvedor
pip install -e ".[dev]"

# Instale pre-commit hooks (opcional)
pre-commit install
```

### Rodando Testes

```bash
# Rode todos os testes
pytest

# Com cobertura
pytest --cov=src

# Teste específico
pytest tests/test_config.py::TestPluginConfig::test_set_and_get_erpnext_credentials
```

### Verificação de Código

```bash
# Formatar código
black src tests

# Verificar estilo
flake8 src tests

# Verificar tipos (opcional)
mypy src

# Organizar imports
isort src tests
```

### Estrutura do Código

```
src/
  ├── __init__.py          # Exports públicos
  ├── config.py            # Gerenciamento de configuração
  ├── erpnext_client.py    # Cliente HTTP/API
  ├── server.py            # Servidor MCP
  └── cli.py               # Interface CLI

tests/
  ├── __init__.py
  └── test_*.py            # Testes unitários

example.py                 # Exemplos de uso
```

## Convenções de Código

### Python

- Use **Python 3.8+**
- Siga **PEP 8** para estilo
- Use **type hints** quando possível
- Documente funções públicas

### Commits

```
<tipo>(<escopo>): <assunto>

<corpo>

<rodapé>
```

Tipos:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudança de documentação
- `style`: Formatação (sem mudança de lógica)
- `refactor`: Refatoração sem mudança de comportamento
- `test`: Adição ou atualização de testes
- `chore`: Atualizações de dependências, etc.

Exemplo:
```
feat(erpnext_client): add support for batch operations

Added get_batch and create_batch methods to support bulk
operations on ERPNext documents.

Fixes #123
```

## Processo de Review

1. Um mantenedor irá revisar seu PR
2. Mudanças podem ser solicitadas
3. Uma vez aprovado, será merged

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT do projeto.

## Dúvidas?

- Abra uma issue com a tag `question`
- Consulte a documentação existente
- Entre em contato com os mantenedores

Obrigado por contribuir! 🎉
