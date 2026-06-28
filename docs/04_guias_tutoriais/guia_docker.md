# Guia de Containerização com Docker

Este guia explica como subir todo o ambiente de desenvolvimento (frontend, backend e bancos de dados) com um único comando usando **Docker Compose**.

---

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando
- Nenhuma outra instalação é necessária (Python, Node, etc. ficam dentro dos containers)

---

## Arquivos de Containerização

| Arquivo | Localização | Descrição |
| :--- | :--- | :--- |
| `docker-compose.yml` | Raiz do projeto | Orquestra todos os serviços juntos |
| `Dockerfile` | `apps/services/core-service/` | Build do backend FastAPI com Poetry |
| `Dockerfile` | `apps/frontend/` | Build multi-stage do frontend (Node → Nginx) |
| `nginx.conf` | `apps/frontend/` | Configuração do servidor Nginx para SPA |

---

## Como Subir o Ambiente

### Opção 1: Tudo de uma vez (recomendado)

```bash
# Na raiz do projeto
docker compose up --build
```

Isso vai:
1. Subir o **PostgreSQL** e esperar ele ficar saudável
2. Subir o **MongoDB** e esperar ele ficar saudável
3. Fazer o build da imagem do **backend** (core-service)
4. Executar `alembic upgrade head` para criar as tabelas e injetar os seeds
5. Subir o servidor **uvicorn** na porta 8000
6. Fazer o build multi-stage da imagem do **frontend** (React → Nginx)
7. Servir o frontend na porta 5173

### Opção 2: Somente os bancos de dados

Para desenvolvimento local (backend e frontend rodando fora do Docker):

```bash
docker compose up postgres mongodb
```

### Opção 3: Em background (detached)

```bash
docker compose up --build -d
```

---

## Serviços e Portas

| Serviço | URL Local | Usuário/Senha |
| :--- | :--- | :--- |
| **Frontend** | http://localhost:5173 | — |
| **Backend API** | http://localhost:8000 | — |
| **Swagger UI** | http://localhost:8000/docs | — |
| **PostgreSQL** | `localhost:5432` | `postgres` / `postgres` |
| **MongoDB** | `localhost:27017` | `admin` / `admin123` |

---

## Comandos Úteis

```bash
# Ver o status dos containers
docker compose ps

# Ver os logs de um serviço específico
docker compose logs core-service -f
docker compose logs frontend -f

# Parar e remover todos os containers (mantém os volumes/dados)
docker compose down

# Parar e remover TUDO incluindo os dados do banco
docker compose down -v

# Recriar somente um serviço
docker compose up --build core-service
```

---

## Variáveis de Ambiente

As variáveis de ambiente do backend são configuradas no `docker-compose.yml`. Para desenvolvimento local fora do Docker, edite o arquivo `.env` na pasta `apps/services/core-service/`:

```env
# apps/services/core-service/.env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=hotel_db_dev
POSTGRES_PORT=5432

MONGODB_URL=mongodb://admin:admin123@localhost:27017
MONGODB_DB=hotel_mongo_dev
```

> [!WARNING]
> Nunca faça commit do arquivo `.env` com credenciais reais no Git. O arquivo `.gitignore` já ignora o `.env` por padrão. Use o `.env.example` como modelo documentado.

---

## Healthchecks

O `docker-compose.yml` configura **healthchecks** nos bancos de dados. O backend (`core-service`) só inicia **depois que os bancos estiverem prontos para aceitar conexões**. Isso evita erros de conexão durante o boot.

```yaml
# Exemplo do healthcheck do PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres -d hotel_db_dev"]
  interval: 10s
  timeout: 5s
  retries: 5
```
