# Guia de Testes Automatizados — Core Service

Este guia explica como os testes estão organizados no **core-service**, como executá-los e como os alunos devem escrever novos testes para as suas rotas e repositórios.

---

## Estrutura de Testes

```text
tests/
├── conftest.py          # Fixtures compartilhadas (client, db_session)
├── test_api.py          # Testes de integração das rotas HTTP (status codes)
└── test_repository.py   # Testes unitários do repositório (camada de dados)
```

---

## Como Executar

```bash
# Dentro do diretório core-service, com o venv ativo
cd apps/services/core-service

poetry run pytest -v
```

Saída esperada:

```
collected 8 items

tests/test_api.py::test_get_sobre_returns_200            PASSED
tests/test_api.py::test_get_professor_inexistente_returns_404  PASSED
tests/test_api.py::test_criar_professor_sem_autorizacao_returns_401  PASSED
tests/test_api.py::test_criar_professor_com_autorizacao_invalida_returns_403 PASSED
tests/test_api.py::test_criar_professor_com_dados_invalidos_returns_422 PASSED
tests/test_api.py::test_trigger_server_error_returns_500  PASSED
tests/test_repository.py::test_create_professor_in_repository PASSED
tests/test_repository.py::test_get_professor_by_id_in_repository PASSED

8 passed in ~40s
```

> **Nota**: Os testes de API usam um banco de dados **SQLite em memória** (`test.db`), separado completamente do banco de desenvolvimento. Não é necessário ter o PostgreSQL ou MongoDB rodando para executar os testes.

---

## Tipos de Testes Implementados

### 1. Testes de API (Integração) — `test_api.py`

Cada teste verifica um **código de status HTTP** diferente, cobrindo os principais cenários de uma API REST:

| Teste | Status Code | O que verifica |
| :--- | :---: | :--- |
| `test_get_sobre_returns_200` | **200 OK** | A rota `/api/v1/sobre` retorna os dados corretos do professor |
| `test_get_professor_inexistente_returns_404` | **404 Not Found** | Busca por um UUID inexistente retorna erro correto |
| `test_criar_professor_sem_autorizacao_returns_401` | **401 Unauthorized** | Tentativa sem token retorna erro de autenticação |
| `test_criar_professor_com_autorizacao_invalida_returns_403` | **403 Forbidden** | Token inválido/sem permissão retorna acesso proibido |
| `test_criar_professor_com_dados_invalidos_returns_422` | **422 Unprocessable** | Payload incompleto falha na validação do Pydantic |
| `test_trigger_server_error_returns_500` | **500 Internal Server Error** | Rota de debug força um erro não tratado |

**Exemplo de teste de API:**

```python
# tests/test_api.py
def test_get_sobre_returns_200(client, db_session):
    repo = TutorialRepository(db_session)
    repo.create_professor(
        nome="Ronildo Silva",
        email="ronildo@ufc.br",
        sala="Sala 07",
        biografia="Professor",
    )

    response = client.get("/api/v1/sobre")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["equipe"] == "Alpha"
    assert json_data["professor"]["nome"] == "Ronildo Silva"
```

---

### 2. Testes de Repositório (Unitários) — `test_repository.py`

Verificam a camada de acesso ao banco diretamente, sem passar pelo HTTP:

| Teste | O que verifica |
| :--- | :--- |
| `test_create_professor_in_repository` | `create_professor()` persiste corretamente os dados no banco |
| `test_get_professor_by_id_in_repository` | `get_professor_by_id()` recupera o registro correto |

**Exemplo de teste de repositório:**

```python
# tests/test_repository.py
def test_create_professor_in_repository(db_session):
    repo = TutorialRepository(db_session)
    prof = repo.create_professor(
        nome="Professor de Teste",
        email="teste@unicatolica.edu.br",
        sala="Sala Teste, Bloco T",
        biografia="Uma biografia de teste.",
    )

    assert prof.id is not None
    assert prof.nome == "Professor de Teste"
    assert prof.detalhe is not None
    assert prof.detalhe.sala == "Sala Teste, Bloco T"
```

---

## Fixtures (conftest.py)

As **fixtures** são funções que preparam o ambiente antes de cada teste e o limpam depois. Elas ficam em `conftest.py` e são compartilhadas entre todos os arquivos de teste.

```python
# tests/conftest.py (simplificado)
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.models.tutorial import Base

# Banco de dados de teste separado (SQLite em memória)
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})

@pytest.fixture
def db_session():
    """Cria e destrói o banco a cada teste."""
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Cliente HTTP que usa o banco de testes."""
    # ... injeta o db_session na app
    with TestClient(app) as c:
        yield c
```

---

## Como Escrever Novos Testes

### Para uma nova rota (`test_api.py`)

```python
def test_minha_nova_rota_returns_201(client, db_session):
    payload = {
        "campo1": "valor1",
        "campo2": "valor2",
    }
    headers = {"Authorization": "Bearer token-admin-master"}
    
    response = client.post("/api/v1/minha-rota", json=payload, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["campo1"] == "valor1"
```

### Para um novo método de repositório (`test_repository.py`)

```python
def test_meu_novo_metodo_repository(db_session):
    from app.repositories.meu_repository import MeuRepository
    
    repo = MeuRepository(db_session)
    resultado = repo.meu_metodo(parametro="valor")
    
    assert resultado is not None
    assert resultado.campo == "valor"
```

---

## Boas Práticas para os Alunos

> [!TIP]
> Cada teste deve verificar **uma única coisa**. Evite fazer múltiplas asserções não relacionadas em um mesmo teste.

> [!IMPORTANT]
> Sempre use o `db_session` da fixture para operações de banco nos testes. Nunca acesse o banco de desenvolvimento diretamente nos testes.

> [!NOTE]
> O nome do teste deve descrever o que está sendo testado. Use o padrão `test_<acao>_<condicao>_returns_<resultado>`.
