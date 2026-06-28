# Solicitação de Configuração de Laboratório - T.I.

**Disciplina:** Estágio II em Desenvolvimento Web
**Professor:** Ronildo
**Semestre/Ano:** 2026.2

Prezados(as) membros da equipe de Tecnologia da Informação,

Para o bom andamento das aulas práticas da disciplina de Estágio II, solicito a instalação e configuração dos seguintes softwares e ferramentas nos computadores do laboratório designado. O ambiente de desenvolvimento baseia-se em ecossistema Python (FastAPI), bancos de dados relacionais e sistemas de mensageria.

---

## 1. Ferramentas Essenciais de Desenvolvimento

| Software | Versão Mínima | Descrição / Justificativa |
| :--- | :--- | :--- |
| **Python** | 3.10 ou superior | Linguagem base para o framework backend. **Importante:** Marcar a opção "Add Python to PATH" durante a instalação. |
| **Node.js** | 20.x (LTS) ou superior | Ambiente de execução JavaScript/TypeScript necessário para compilar e executar o frontend (React + Vite). |
| **Poetry** | Mais recente | Gerenciador de dependências oficial do projeto (instalado via pip ou instalador próprio). Necessário para gerenciar os pacotes virtuais do Python. |
| **Git** | Mais recente | Sistema de controle de versão. Essencial para o fluxo de repositórios e entrega de trabalhos. |
| **Visual Studio Code (VS Code)** | Mais recente | Editor de código padrão da disciplina. |

### 1.1 Extensões Recomendadas no VS Code
Para agilizar as aulas e padronizar o ambiente, caso seja possível a pré-configuração, solicitamos a inclusão das seguintes extensões no VS Code:
- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **GitLens** (GitKraken)
- **Tailwind CSS IntelliSense** (Tailwind Labs)
- **ESLint** (Dirk Baeumer)

---

## 2. Bancos de Dados, Mensageria e Virtualização

Temos duas opções para a arquitetura de dados (PostgreSQL, MongoDB e RabbitMQ). A **Opção A** (via Docker) é a mais recomendada pelo padrão de mercado atual. Caso haja restrições de permissão nos laboratórios, a **Opção B** (instalações nativas) pode ser adotada.

### Opção A: Ambiente conteinerizado (Recomendada)
| Software | Descrição |
| :--- | :--- |
| **Docker Desktop** (ou Docker Engine no Linux) | Permite que os alunos subam os bancos de dados (PostgreSQL, MongoDB) e a fila de mensageria via `docker-compose`, sem a necessidade de instalar os serviços nativamente na máquina. |
| **DBeaver Community** ou **pgAdmin 4** | Interface gráfica para conectar e inspecionar o banco de dados relacional rodando no contêiner. |
| **MongoDB Compass** | Interface gráfica oficial para inspecionar e consultar documentos do MongoDB rodando no contêiner. |

### Opção B: Instalações nativas (Alternativa)
| Software | Versão Mínima | Descrição |
| :--- | :--- | :--- |
| **PostgreSQL** | 14 ou superior | Banco de dados principal relacional. Os alunos devem ter credenciais conhecidas (ex: usuário `postgres`, senha `postgres`) para desenvolvimento local. |
| **DBeaver Community** | Mais recente | Interface gráfica universal para gerenciamento do banco de dados (preferencial ao pgAdmin). |
| **MongoDB Community Server** | 6.0 ou superior | Banco de dados NoSQL de documentos para histórico e auditorias de transação. |
| **MongoDB Compass** | Mais recente | Interface gráfica oficial para conexão com o banco MongoDB. |
| **Erlang + RabbitMQ** | Mais recente | Broker de mensageria (necessário apenas se o Docker não for instalado). |

---

## 3. Testes de API

| Software | Descrição |
| :--- | :--- |
| **Postman** ou **Insomnia** | Aplicativo cliente para realizar requisições HTTP e testar as rotas da API REST. |

---

## 4. Requisitos de Rede, Portas e Permissões

Para garantir que os alunos consigam desenvolver e testar sem bloqueios, os computadores precisam atender às seguintes políticas de rede e execução:

1. **Acesso à Internet:**
   - Liberação para clonagem e push no domínio `github.com` (via HTTPS e SSH).
   - Liberação para download de dependências Python via gerenciadores `pip` e `poetry` (acesso aos domínios do `pypi.org` e `python-poetry.org`).
   - Liberação para download de dependências JavaScript/Node via `npm` (acesso aos domínios `registry.npmjs.org`).
2. **Portas Locais (Localhost):**
   - Os alunos precisam ter permissão para rodar processos locais (abrir portas). As portas frequentemente utilizadas serão: `5173` (Vite Frontend), `8000` (FastAPI Backend), `5432` (PostgreSQL), `27017` (MongoDB) e `5672`/`15672` (RabbitMQ).
3. **Privilégios de Execução:**
   - Permissão para abrir e executar terminais (Prompt de Comando, PowerShell ou Bash) integrados no VS Code.

---

Agradeço antecipadamente o suporte da equipe. Fico à disposição para validar o ambiente em uma máquina de teste antes do início das aulas.

Atenciosamente,

**Me. Ronildo Silva**
*Professor - Estágio II em Desenvolvimento Web*
