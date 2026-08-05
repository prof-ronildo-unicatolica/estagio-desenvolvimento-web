# Primeiros Passos — Do Zero ao Projeto Rodando

Este guia leva você do **repositório recém-clonado** até a **stack completa rodando**
na sua máquina, e explica o que fazer em seguida. É o primeiro documento que todo
integrante de equipe deve seguir, antes de escrever qualquer linha de código.

> **Pré-requisito:** ambiente já instalado (Docker, Git, Python e Node).
> Se ainda não instalou, faça primeiro o [Guia de Instalação](./guia_instalacao.md).
> Se ainda não configurou sua chave SSH no GitHub, veja a seção de SSH no
> [Guia de Git e GitHub](../02_engenharia_software/git_github_basico.md).

---

## 1. O que já vem pronto no repositório da sua equipe

O repositório da equipe **não está vazio**. O professor já subiu um **projeto-base
funcional** — o mesmo código que está no [repositório da
disciplina](https://github.com/prof-ronildo-unicatolica/estagio-desenvolvimento-web).
Você **não precisa criar a estrutura do zero**; seu trabalho é evoluí-la sprint a sprint.

```text
/ (raiz do repositório da equipe)
├── apps/
│   ├── frontend/                  # Cliente Web (React + Vite + Bootstrap)
│   └── services/core-service/     # Backend (FastAPI + SQLAlchemy + Alembic)
├── docker-compose.yml             # Sobe toda a stack com um comando
├── .gitignore
└── README.md
```

O que esse projeto-base já entrega:

- **Backend** em FastAPI com arquitetura em camadas (`api / schemas / services / repositories / models`), rota `GET /health`, migração inicial do Alembic e suíte de testes com pytest.
- **Frontend** em React + Vite já configurado, com componentes de exemplo e layout base.
- **Infraestrutura** completa em Docker: PostgreSQL, MongoDB e RabbitMQ.

> ⚠️ **Atenção — o que é exemplo e o que é o projeto:** os componentes de tela que vêm
> no frontend (perfil, mapa, carrossel, tabela de stacks) são **material de
> demonstração** das aulas, e **não** fazem parte do Sistema de Hotelaria. Eles servem
> como referência de código React. Ao longo das sprints vocês vão substituí-los pelas
> telas reais do sistema. O mesmo vale para a autenticação: ela é **propositalmente
> insegura** (veja a Seção 5).

---

## 2. Clonando o repositório

Pegue a URL na página do repositório da sua equipe, em **Code → SSH**:

```bash
# Clone o repositório da SUA equipe (troque a URL pela da sua equipe)
git clone git@github.com:prof-ronildo-unicatolica/est_web_2026_2_turma_a_alpha.git
cd est_web_2026_2_turma_a_alpha
```

Confirme que você caiu na branch de trabalho:

```bash
git branch --show-current
# deve imprimir: develop
```

A branch padrão do repositório é a `develop`, então o clone já traz você nela.
Se aparecer `main`, rode `git fetch origin && git checkout develop`.

---

## 3. Subindo a stack com Docker

Um único comando sobe banco de dados, mensageria, backend e frontend:

```bash
docker compose up -d --build
```

A primeira execução baixa as imagens e compila o projeto — pode levar alguns minutos.
Acompanhe o progresso com `docker compose logs -f`.

Verifique se todos os containers subiram:

```bash
docker compose ps
```

### Endereços do ambiente

| Serviço | Endereço | Observação |
| :--- | :--- | :--- |
| Frontend | http://localhost:5173 | Interface web |
| API (backend) | http://localhost:8000 | |
| Documentação da API | http://localhost:8000/docs | Swagger interativo — teste as rotas por aqui |
| Health check | http://localhost:8000/health | Deve responder `200` |
| Painel do RabbitMQ | http://localhost:15672 | |
| PostgreSQL | `localhost:5432` | |
| MongoDB | `localhost:27017` | |

**Teste rápido de que está tudo no ar:**

```bash
curl http://localhost:8000/health
```

Se responder `200`, seu ambiente está pronto. Para derrubar tudo: `docker compose down`
(acrescente `-v` para também apagar os dados dos bancos e recomeçar limpo).

---

## 4. Rodando o backend fora do Docker (opcional)

O Docker é suficiente para o dia a dia. Rodar o backend direto na máquina é útil quando
você quer usar o **debugger** ou o *hot reload* do Python:

```bash
cd apps/services/core-service
cp env_example .env          # ajuste as variáveis se necessário
python -m venv .venv
source .venv/bin/activate    # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head         # aplica as migrações no banco
uvicorn app.main:app --reload
```

> Os bancos precisam estar no ar. Suba só a infraestrutura com
> `docker compose up -d postgres mongodb rabbitmq`.

Para rodar a suíte de testes:

```bash
pytest
```

Detalhes sobre a organização dos testes no [Guia de Testes](./guia_testes.md).

---

## 5. Antes de começar a codar: leia isto

A autenticação que vem no projeto-base é um **placeholder proposital** —
usuários em memória, sem hash de senha e sem token real. **Não é um bug**, e
**não deve ser usada como referência de código seguro**. Substituí-la por JWT +
bcrypt é justamente a [Atividade da Sprint
2](../02_engenharia_software/atividade_auth_sprint2.md).

Leia também, nesta ordem:

1. [Contexto e Problematização](../02_engenharia_software/contexto_problematica_hotelaria.md) — o problema que o sistema resolve.
2. [Requisitos e Casos de Uso](../02_engenharia_software/requisitos_casos_uso.md) — o escopo mínimo obrigatório.
3. [Roadmap das Sprints](../01_planejamento_metodologia/roadmap_sprints.md) — o que entregar em cada sprint.
4. [Padrão de Arquitetura do FastAPI](../03_arquitetura_tecnica/arquitetura_backend_fastapi.md) — onde cada arquivo deve morar.

---

## 6. Seu primeiro Pull Request

O fluxo de trabalho completo está no
[Guia de Git e GitHub](../02_engenharia_software/git_github_basico.md). O resumo:

```bash
# 1. Atualize a develop local
git checkout develop
git pull origin develop

# 2. Crie sua branch a partir da develop
git checkout -b feature/minha-tarefa

# 3. Codifique, comite e envie
git add .
git commit -m "feat: descreve o que foi feito"
git push -u origin feature/minha-tarefa

# 4. Abra o Pull Request no GitHub, com destino à branch develop
```

Regras que o GitHub vai cobrar de você automaticamente:

- A `develop` é **protegida**: não aceita `git push` direto. Todo código entra por Pull Request.
- Todo PR precisa de **pelo menos uma aprovação** de um colega de equipe.
- Você **não pode aprovar o seu próprio PR** — revisar o código dos colegas faz parte do trabalho avaliado.
- Comentários de revisão precisam ser **resolvidos** antes do merge.

---

## 7. Problemas comuns

| Sintoma | Causa provável | O que fazer |
| :--- | :--- | :--- |
| `port is already allocated` | Você já tem PostgreSQL/Mongo instalado ocupando a porta | Pare o serviço local ou altere a porta no `docker-compose.yml` |
| `permission denied` ao rodar `docker` | Usuário fora do grupo `docker` (Linux) | `sudo usermod -aG docker $USER` e reinicie a sessão |
| `Permission denied (publickey)` no clone | Chave SSH não configurada no GitHub | Siga a seção de SSH do [Guia de Git](../02_engenharia_software/git_github_basico.md) |
| Backend sobe mas responde erro de conexão | Bancos ainda inicializando | Aguarde e veja `docker compose logs -f postgres` |
| Frontend abre em branco | Build antigo em cache | `docker compose up -d --build frontend` |
| Alterei o código e nada mudou | Imagem não foi reconstruída | `docker compose up -d --build` |
| `protected branch hook declined` no push | Tentou dar push direto na `develop` | Crie uma branch e abra um Pull Request (Seção 6) |

Se o problema persistir, abra uma **issue** no repositório da sua equipe descrevendo o
sintoma, o comando executado e a mensagem de erro completa.
