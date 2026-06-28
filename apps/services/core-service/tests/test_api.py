import uuid

from app.repositories.tutorial_repository import TutorialRepository


# 1. Teste de 200 OK
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


# 2. Teste de 404 Not Found
def test_get_professor_inexistente_returns_404(client):
    id_fake = uuid.uuid4()
    response = client.get(f"/api/v1/sobre/professores/{id_fake}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Professor nao encontrado"


# 3. Teste de 401 Unauthorized
def test_criar_professor_sem_autorizacao_returns_401(client):
    payload = {
        "nome": "Prof Desautorizado",
        "email": "test@ufc.br",
        "sala": "Sala 12",
        "biografia": "Nenhuma",
    }
    response = client.post("/api/v1/sobre/professores", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Nao autorizado: Token ausente"


# 4. Teste de 403 Forbidden
def test_criar_professor_com_autorizacao_invalida_returns_403(client):
    payload = {
        "nome": "Prof Proibido",
        "email": "test@ufc.br",
        "sala": "Sala 12",
        "biografia": "Nenhuma",
    }
    headers = {"Authorization": "Bearer token-errado-aluno"}
    response = client.post("/api/v1/sobre/professores", json=payload, headers=headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Acesso proibido: Permissao insuficiente"


# 5. Teste de 422 Unprocessable Entity
def test_criar_professor_com_dados_invalidos_returns_422(client):
    payload = {
        "nome": "Prof Invalido",
        "email": "email_valido@ufc.br",
    }
    headers = {"Authorization": "Bearer token-admin-master"}
    response = client.post("/api/v1/sobre/professores", json=payload, headers=headers)
    assert response.status_code == 422


# 6. Teste de 500 Internal Server Error
def test_trigger_server_error_returns_500(client):
    response = client.get("/api/v1/debug/error")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
