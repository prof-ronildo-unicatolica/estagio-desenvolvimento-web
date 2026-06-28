# Guia de Instalação e Configuração do Ambiente

Este guia detalha o passo a passo necessário para configurar o ambiente de desenvolvimento local para o projeto do **Sistema de Reservas de Rede Hoteleira (Monorepo)** no **Linux** e no **Windows**.

---

## 1. Controle de Versão (.gitignore)
Na raiz do monorepo, foi configurado o arquivo **[.gitignore](file:///media/ronildo/DELL_ARCH/Estágio%20II/.gitignore)** para garantir que arquivos temporários e dependências locais pesadas não sejam enviados ao repositório Git. Os principais diretórios ignorados são:
* `.venv/` e `venv/` (ambientes virtuais do Python).
* `node_modules/` (dependências do Node.js).
* `dist/` (build de produção do Frontend).
* `.env` e arquivos locais de variáveis.

---

## 2. Docker e Docker Compose (Orquestração de Bancos)

Utilizamos o **Docker** para rodar localmente as instâncias isoladas do PostgreSQL e MongoDB sem a necessidade de instalar os bancos diretamente na máquina física.

### 2.1. Comandos Básicos do Docker
* **Verificar versão instalada do Docker**:
  ```bash
  docker -v
  ```
* **Listar containers ativos na máquina**:
  ```bash
  docker ps
  ```
* **Listar todos os containers (ativos e inativos)**:
  ```bash
  docker ps -a
  ```

### 2.2. Comandos do Docker Compose
Execute os comandos a seguir na raiz do projeto (onde está o `docker-compose.yml`):
* **Subir os serviços em segundo plano (Modo Detached)**:
  ```bash
  docker compose up -d
  ```
* **Derrubar os containers e remover a rede local do Docker**:
  ```bash
  docker compose down
  ```
* **Derrubar os containers e apagar os volumes persistidos (Reseta os Bancos)**:
  ```bash
  docker compose down -v
  ```
* **Verificar o status dos containers do compose**:
  ```bash
  docker compose ps
  ```
* **Visualizar logs em tempo real dos containers**:
  ```bash
  docker compose logs -f
  ```

---

## 3. Configuração do Backend (`apps/services/core-service`)

Disponibilizamos duas abordagens de gerenciamento: **Poetry** (recomendado para consistência de pacotes) e **Venv + Pip** (alternativa padrão).

### 3.1. Opção A: Utilizando Python Virtualenv (`venv` + `requirements.txt`)
Se preferir a abordagem clássica com `pip`, execute no diretório `apps/services/core-service`:

#### 1. Criar o ambiente virtual (`.venv`):
* **No Linux / macOS**:
  ```bash
  python3 -m venv .venv
  ```
* **No Windows**:
  ```powershell
  python -m venv .venv
  ```

#### 2. Ativar o ambiente virtual:
* **No Linux / macOS**:
  ```bash
  source .venv/bin/activate
  ```
* **No Windows (PowerShell)**:
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **No Windows (Prompt CMD)**:
  ```cmd
  .venv\Scripts\activate.bat
  ```

#### 3. Instalar as dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3.2. Opção B: Utilizando o Poetry (Recomendado)
Se preferir usar o gerenciador **Poetry** conforme especificado na arquitetura:

#### 1. Instalar o Poetry:
* **Linux / macOS**:
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```
* **Windows (PowerShell)**:
  ```powershell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
  ```

#### 2. Inicializar o ambiente virtual e instalar dependências:
```bash
poetry config virtualenvs.in-project true
poetry install
```

#### 3. Ativar o shell virtual:
```bash
poetry shell
```

---

### 3.3. Configuração de Variáveis de Ambiente (.env)
A aplicacao necessita de variaveis de ambiente para conectar aos bancos de dados.

Disponibilizamos o arquivo de modelo **[env_example](file:///media/ronildo/DELL_ARCH/Estágio%20II/apps/services/core-service/env_example)** (ou `.env.example`). O aluno deve criar uma copia deste arquivo com o nome **.env** no mesmo diretorio:

* **No Linux / macOS (Terminal)**:
  ```bash
  cp env_example .env
  ```
* **No Windows (PowerShell)**:
  ```powershell
  copy env_example .env
  ```

O arquivo `.env` criado contem as chaves configuradas para o Docker local e sera carregado automaticamente pela aplicacao. Este arquivo nunca deve ser enviado ao Git (ja configurado no `.gitignore`).

---

## 4. Alembic (Migrações e Seeds do Banco)

O Alembic gerencia o versionamento de esquema no PostgreSQL. 

### 4.1. Comandos de Migração
Com o ambiente virtual ativado (ou prefixando com `poetry run`):

* **Aplicar todas as migrações até a versão mais recente (Cria tabelas e insere seeds)**:
  ```bash
  alembic upgrade head
  ```
* **Desfazer todas as migrações (Remove todas as tabelas e dados)**:
  ```bash
  alembic downgrade base
  ```
* **Desfazer apenas a última migração realizada**:
  ```bash
  alembic downgrade -1
  ```
* **Ver histórico de migrações criadas**:
  ```bash
  alembic history
  ```
* **Ver a migração atualmente ativa no banco de dados**:
  ```bash
  alembic current
  ```
* **Gerar uma nova migração baseada nas alterações dos modelos**:
  ```bash
  alembic revision --autogenerate -m "descricao_da_mudanca"
  ```

---

## 5. Configuração do Frontend Node.js (`apps/frontend`)

O frontend é construído sobre o **Node.js** utilizando a ferramenta **npm** (Node Package Manager).

### 5.1. Instalação e Execução
No diretório `apps/frontend`:
* **Instalar as dependências do package.json**:
  ```bash
  npm install
  ```
* **Iniciar o servidor de desenvolvimento local (Vite)**:
  ```bash
  npm run dev
  ```
  O frontend estará disponível em `http://localhost:5173`.
* **Compilar o projeto para produção (Gera arquivos otimizados em `dist/`)**:
  ```bash
  npm run build
  ```

---

## 6. Bancos de Dados e Drivers de Conexão

### 6.1. Drivers Utilizados no Backend
* **`psycopg2-binary`**: Driver que faz a conexão do Python com o PostgreSQL. A versão `binary` instala pré-compilada, funcionando em Windows e Linux sem necessidade de instalar compiladores C locais.
* **`motor`**: Driver assíncrono oficial para conexões do MongoDB no Python, essencial para que chamadas NoSQL não travem a thread do FastAPI.

### 6.2. MongoDB no Node.js (Mongoose)
Para fins comparativos, caso os alunos trabalhassem o frontend ou microsserviços em JavaScript/Node.js, a biblioteca padrão de conexão seria o **Mongoose** (uma biblioteca ODM - Object Data Modeling). 

Exemplo de modelo estruturado no Mongoose:
```javascript
const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
  username: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password_hash: { type: String, required: true },
  role: { type: String, default: 'cliente' },
  active: { type: Boolean, default: true }
});

module.exports = mongoose.model('User', UserSchema);
```

### 6.3. Extensão "MongoDB for VS Code"
Para visualizar coleções e rodar consultas direto no VS Code:
1. Instale a extensão **MongoDB for VS Code**.
2. Clique no ícone da extensão na barra lateral e escolha **Add Connection**.
3. Use a string de conexão:
   ```text
   mongodb://admin:admin123@localhost:27017
   ```
4. Navegue pelo banco `hotel_mongo_dev` e inspecione a coleção `users` populada no seed.

---

## 7. Padronização e Estilo de Código (Linters)

Para garantir a qualidade do código e o padrão estético de formatação entre as equipes, o projeto possui linters configurados no Backend e no Frontend.

### 7.1. Backend (Ruff)
O backend em Python utiliza o **Ruff**, um linter e formatador de código extremamente rápido (escrito em Rust).
* **Verificar erros e regras de import**:
  ```bash
  poetry run ruff check
  ```
* **Corrigir automaticamente importações desorganizadas ou variáveis não utilizadas**:
  ```bash
  poetry run ruff check --fix
  ```
* **Aplicar formatação de código padrão (estilo Black/PEP8)**:
  ```bash
  poetry run ruff format
  ```

### 7.2. Frontend (ESLint)
O frontend React utiliza o **ESLint** com regras específicas para React e Hooks de acordo com o arquivo `.eslintrc.cjs`.
* **Verificar regras estéticas e erros no Javascript**:
  ```bash
  npm run lint
  ```

---

## 8. Testes Automatizados (Pytest)

Para garantir o correto funcionamento das regras de negócio e simular o comportamento dos endpoints sob diferentes cenários de erro e sucesso, o projeto conta com uma suíte de testes de integração e unitários no Backend.

Os testes utilizam um banco **SQLite temporário em memória** configurado em `tests/conftest.py`, rodando de forma isolada sem afetar as tabelas ou o seed do Docker local.

### 8.1. Como executar a suíte de testes:
Navegue até a pasta do backend (`apps/services/core-service`) e execute:
```bash
poetry run pytest -v
```

### 8.2. Cobertura de Status de Resposta:
Nossos testes cobrem as seguintes regras e status de resposta HTTP do FastAPI:
* **`200 OK`**: Rota `/api/v1/sobre` retornando a estrutura serializada correta do Pydantic.
* **`401 Unauthorized`**: Tentativa de POST em `/sobre/professores` sem enviar o cabeçalho `Authorization`.
* **`403 Forbidden`**: Tentativa de POST com token diferente de `Bearer token-admin-master`.
* **`404 Not Found`**: Busca por ID de professor inexistente (UUID gerado aleatoriamente).
* **`422 Unprocessable Entity`**: Payload incorreto enviado ao FastAPI (ausência do campo obrigatório `sala`).
* **`500 Internal Server Error`**: Erro não tratado lançado na rota `/debug/error`, validando o fallback automático de erro interno da API.
