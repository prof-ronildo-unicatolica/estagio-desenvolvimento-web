# Atividade da Sprint 2 — Autenticação e Autorização (JWT + RBAC)

> **Contexto:** o exemplo base (`core-service`) já vem com uma autenticação
> **propositalmente básica** (apenas `if/else`, sem hash e sem token real),
> localizada em `app/api/deps.py` e `app/api/v1/auth.py`. **Esta atividade
> consiste em substituir esse placeholder por uma implementação real e
> segura.** Ela atende aos requisitos **RFO01, RFO02 e RFO03** do
> [documento de requisitos](./requisitos_casos_uso.md).

---

## 1. Objetivos de aprendizagem
Ao final desta sprint, o aluno deve ser capaz de:
- Explicar **por que senhas nunca são armazenadas em texto plano** e aplicar **hash** (bcrypt).
- Implementar **autenticação stateless** com **JWT** (geração, assinatura e validação).
- Implementar **autorização baseada em papéis (RBAC)** distinguindo cliente × administrador.
- Proteger rotas com **dependências (guards)** do FastAPI.
- Persistir usuários no PostgreSQL via **SQLAlchemy + Alembic**.

## 2. O que já está pronto (placeholder a ser substituído)
| Arquivo | Estado atual |
| :--- | :--- |
| `app/api/deps.py` | Usuários em memória (`USUARIOS_DEMO`), "token" = e-mail, RBAC via `if/else`. |
| `app/api/v1/auth.py` | Rotas `POST /auth/login`, `GET /auth/me`, `GET /auth/admin/verificacao`. |
| `app/schemas/usuario.py` | DTOs `LoginRequest`, `Token`, `UsuarioPublic`. |
| `tests/test_auth_basico.py` | Testes de fumaça do contrato atual. |

> ⚠️ **Não jogue o contrato fora:** mantenha os mesmos endpoints e formatos de
> entrada/saída para não quebrar o frontend. Troque apenas a *implementação*.

## 3. O que deve ser construído (escopo da atividade)

### 3.1. Persistência
- Criar o model `Usuario` (`app/models/usuario.py`): `id` (UUID), `nome`, `email` (único), `senha_hash`, `is_admin` (bool).
- Gerar a **migração Alembic** da tabela `usuarios` e **semear** um usuário admin padrão.

### 3.2. Segurança (`app/core/security.py`)
- `hash_password` / `verify_password` usando **bcrypt** (via `passlib`, já instalado). **RFO03.**
- `create_access_token` / `decode_access_token` usando **JWT** (adicionar a lib `pyjwt`), assinando com uma `SECRET_KEY` de configuração e incluindo, no mínimo, `sub` (id do usuário) e `exp` (expiração).

### 3.3. Regras de negócio (`app/services/auth_service.py`)
- `registrar`: cria cliente novo com senha em hash; recusa e-mail duplicado.
- `autenticar`: valida e-mail + senha; retorna o usuário ou erro de credenciais.
- `gerar_token`: emite o JWT do usuário autenticado.

### 3.4. Guards (`app/api/deps.py` — substituir o placeholder)
- `get_current_user`: extrai o `Bearer` token, **decodifica o JWT**, carrega o `Usuario` no banco. Falha → **401**.
- `get_current_admin`: exige `is_admin=True`. Não-admin → **403**. **RFO02 (RBAC).**

### 3.5. Rotas (`app/api/v1/auth.py`)
- `POST /auth/register` (novo): cadastro de cliente → **201** (ou **409** se e-mail já existe).
- `POST /auth/login`: agora retorna um **JWT real**.
- `GET /auth/me`: protegida por `get_current_user`. **RFO01.**

## 4. Critérios de aceite (Definition of Done)
A entrega só é considerada pronta quando:
1. ✅ Senha é salva **em hash** no banco (nunca em texto plano) e **nunca** aparece em nenhuma resposta da API.
2. ✅ `POST /auth/login` retorna um **JWT assinado** e com expiração válida.
3. ✅ Rota protegida sem token ou com token inválido/expirado retorna **401**.
4. ✅ Cliente autenticado recebe **403** ao acessar rota de admin; admin recebe **200**.
5. ✅ Existe migração Alembic da tabela `usuarios` e seed do admin.
6. ✅ **Suíte pytest de auth passando** (a suíte definitiva substitui `test_auth_basico.py`).
7. ✅ PR aberto, revisado por um colega e integrado via *merge* na `main`.

## 5. Passo a passo sugerido
1. Modelar `Usuario` + migração/seed (rode `alembic upgrade head`).
2. Escrever `security.py` (hash e JWT) com testes unitários das 4 funções.
3. Escrever `auth_service.py` (registrar/autenticar/gerar_token).
4. Substituir os guards em `deps.py` para usar o JWT + banco.
5. Atualizar as rotas em `auth.py` (incluindo `POST /auth/register`).
6. Adaptar/expandir os testes e validar tudo no **Swagger** (`/docs`) e no **Postman**.

## 6. Dicas
- `pip install pyjwt` (ou `poetry add pyjwt`) para o JWT; o `passlib[bcrypt]` já está no projeto.
- O `HTTPBearer` do FastAPI já habilita o botão **Authorize** no Swagger — cole o token retornado no login.
- bcrypt **trunca senhas em 72 bytes** — valide o tamanho no schema de cadastro.
- **Nunca** versione a `SECRET_KEY` real no Git; use variável de ambiente (`.env`).
- Guardar `is_admin` **também** dentro do token é conveniente, mas confie sempre no valor do **banco** ao autorizar (o token pode estar desatualizado).

## 7. Extensões opcionais (bônus)
- *Refresh tokens* e logout.
- Bloqueio após N tentativas de login inválidas.
- Recuperação de senha por e-mail (simulada via fila do RabbitMQ).
