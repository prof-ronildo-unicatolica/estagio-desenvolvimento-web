# Guia de Testes Automatizados — Core Service

Este guia explica como os testes estão organizados no **core-service**, como executá-los e como os alunos devem escrever novos testes para as suas rotas e repositórios.

---

## Estrutura de Testes

```text
tests/
├── __init__.py          # Marca o pacote de testes
├── conftest.py          # Fixtures compartilhadas (client, db_session)
├── test_api.py          # Testes de integração das rotas HTTP (status codes)
├── test_auth_basico.py  # Testes de fumaça do auth placeholder (login e RBAC)
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
collected 13 items

tests/test_api.py::test_get_sobre_returns_200 PASSED
tests/test_api.py::test_get_professor_inexistente_returns_404 PASSED
tests/test_api.py::test_criar_disciplina_returns_201 PASSED
tests/test_api.py::test_criar_disciplina_com_dados_invalidos_returns_422 PASSED
tests/test_api.py::test_trigger_server_error_returns_500 PASSED
tests/test_auth_basico.py::test_login_valido_retorna_token PASSED
tests/test_auth_basico.py::test_login_invalido_retorna_401 PASSED
tests/test_auth_basico.py::test_rota_protegida_sem_token_e_bloqueada PASSED
tests/test_auth_basico.py::test_rota_protegida_com_token_retorna_perfil PASSED
tests/test_auth_basico.py::test_cliente_nao_acessa_rota_admin PASSED
tests/test_auth_basico.py::test_admin_acessa_rota_admin PASSED
tests/test_repository.py::test_create_professor_in_repository PASSED
tests/test_repository.py::test_get_professor_by_id_in_repository PASSED

13 passed in ~90s
```

> **Nota**: Os testes de API usam um banco **SQLite em arquivo temporário** (`test.db`), separado completamente do banco de desenvolvimento e recriado a cada teste. Não é necessário ter o PostgreSQL, o MongoDB ou o RabbitMQ rodando para executar os testes.

---

## Tipos de Testes Implementados

### 1. Testes de API (Integração) — `test_api.py`

Cada teste verifica um **código de status HTTP** diferente, cobrindo os principais cenários de uma API REST:

| Teste | Status Code | O que verifica |
| :--- | :---: | :--- |
| `test_get_sobre_returns_200` | **200 OK** | A rota `/api/v1/sobre` retorna os dados corretos do professor |
| `test_get_professor_inexistente_returns_404` | **404 Not Found** | Busca por um UUID inexistente retorna erro correto |
| `test_criar_disciplina_returns_201` | **201 Created** | `POST /api/v1/sobre/disciplinas` cria o registro e publica o evento na fila |
| `test_criar_disciplina_com_dados_invalidos_returns_422` | **422 Unprocessable** | Payload incompleto falha na validação do Pydantic |
| `test_trigger_server_error_returns_500` | **500 Internal Server Error** | Rota de debug força um erro não tratado |

> **Nota**: `test_criar_disciplina_returns_201` usa `@patch("app.services.tutorial_service.publish_event")` para não depender de um RabbitMQ real, e ainda assim verifica com `mock_publish.assert_called_once()` que o evento *seria* publicado. Esse é o padrão para testar código que fala com serviços externos.

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

### 2. Testes de Autenticação (Fumaça) — `test_auth_basico.py`

Documentam o **contrato atual** da API de autenticação, que hoje é um placeholder (`if/else`, sem hash, sem JWT). O "token" devolvido pelo login é simplesmente o e-mail do usuário.

| Teste | O que verifica |
| :--- | :--- |
| `test_login_valido_retorna_token` | `POST /api/v1/auth/login` com credenciais corretas devolve `access_token` e `token_type: bearer` |
| `test_login_invalido_retorna_401` | Senha errada retorna **401 Unauthorized** |
| `test_rota_protegida_sem_token_e_bloqueada` | `GET /api/v1/auth/me` sem header retorna 401 ou 403 |
| `test_rota_protegida_com_token_retorna_perfil` | Com token válido retorna o perfil, e a senha **nunca** aparece na resposta |
| `test_cliente_nao_acessa_rota_admin` | Usuário comum recebe **403 Forbidden** em rota administrativa |
| `test_admin_acessa_rota_admin` | Usuário admin acessa a rota administrativa com **200 OK** |

> [!IMPORTANT]
> Ao implementar a autenticação real (JWT + bcrypt) na **Sprint 2**, estes testes devem ser adaptados ou substituídos pela suíte definitiva descrita em [`atividade_auth_sprint2.md`](../02_engenharia_software/atividade_auth_sprint2.md). Os cenários (401, 403, vazamento de senha) continuam válidos; o que muda é como o token é gerado e validado.

---

### 3. Testes de Repositório (Unitários) — `test_repository.py`

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
from app.core.database import get_db
from app.main import app
from app.models.tutorial import Base

# Banco SQLite em arquivo temporário, separado do de desenvolvimento
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Cria e destrói o banco a cada teste."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Cliente HTTP que usa o banco de testes no lugar do banco real."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    # raise_server_exceptions=False deixa o 500 virar resposta HTTP,
    # em vez de estourar a exceção dentro do teste.
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()
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
    # Obtenha o token pelo login — não invente um valor fixo.
    token = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@hotel.com", "senha": "admin123"},
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/v1/minha-rota", json=payload, headers=headers)

    assert response.status_code == 201
    assert response.json()["campo1"] == "valor1"
```

> [!TIP]
> Pegar o token pelo endpoint de login mantém o teste válido depois que a Sprint 2 trocar o placeholder por JWT — um token escrito à mão no teste quebraria.

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
