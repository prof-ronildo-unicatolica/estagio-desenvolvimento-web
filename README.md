# Documentação Oficial: Estágio II em Desenvolvimento Web

Bem-vindo ao repositório de documentação da disciplina de **Estágio II em Desenvolvimento Web** (Semestre 2026.2). 

Este diretório contém todos os materiais de planejamento, arquitetura técnica e processos metodológicos que guiarão os alunos ao longo do semestre na construção do projeto prático (Sistema de Gestão de Hotelaria).

Para facilitar a navegação, os documentos estão organizados nas categorias abaixo. Clique nos links para acessar o conteúdo completo.

---

## 1. Planejamento e Metodologia da Disciplina

Documentos voltados para a estruturação do semestre, regras de avaliação e divisão de equipes.

* **[Plano de Curso e Metodologia](./docs/01_planejamento_metodologia/plano_curso_estagio_ii.md)**: Visão geral da disciplina, metodologia ágil (Scrum/Sprints), dinâmica das equipes, gerenciamento dos repositórios e critérios de avaliação individual por repositório.
* **[Cronograma de Aulas](./docs/01_planejamento_metodologia/cronograma_aulas_2026_2.md)**: Planejamento semana a semana das 19 aulas do semestre, mapeando o avanço das Sprints de desenvolvimento.
* **[Roadmap das Sprints](./docs/01_planejamento_metodologia/roadmap_sprints.md)**: Detalhamento semanal das 15 sprints, entregáveis de cada uma, marcos de Sprint Review e caminho crítico para equipes menores.
* **[Requisitos do Laboratório (TI)](./docs/01_planejamento_metodologia/requisitos_laboratorio_ti.md)**: Documento formal destinado ao departamento de Infraestrutura/TI com a lista de softwares e configurações de rede necessárias nas máquinas do laboratório.

## 2. Regras de Negócio e Engenharia de Software

Documentos que explicam *o que* vamos construir (o problema real) e as regras que os alunos devem seguir.

* **[Contexto e Problematização (Hotelaria)](./docs/02_engenharia_software/contexto_problematica_hotelaria.md)**: Descrição detalhada do cenário, requisitos funcionais (Épicos e Histórias de Usuário) do sistema de gestão hoteleira que será desenvolvido pelas equipes.
* **[Requisitos Mínimos e Casos de Uso](./docs/02_engenharia_software/requisitos_casos_uso.md)**: Definição do escopo mínimo aceitável para o front-end e back-end, requisitos funcionais (RFO) e não-funcionais (RNFO) obrigatórios.
* **[Guia Básico de Git, GitHub e Gitflow](./docs/02_engenharia_software/git_github_basico.md)**: Manual obrigatório de versionamento. Cobre comandos fundamentais, fluxo de Pull Requests, proteção de branches, exemplos práticos de Code Review e resolução de conflitos.
* **[Atividade de Autenticação (Sprint 2)](./docs/02_engenharia_software/atividade_auth_sprint2.md)**: Enunciado da atividade que substitui o auth placeholder por JWT e bcrypt, com critérios de aceite (Definition of Done).

## 3. Arquitetura Técnica e Banco de Dados

Guias que definem *como* o software será construído, estabelecendo os padrões de código, frameworks e infraestrutura.

* **[Arquitetura Macro do Projeto](./docs/03_arquitetura_tecnica/arquitetura_projeto_backend.md)**: Visão de alto nível das tecnologias escolhidas (FastAPI, PostgreSQL, RabbitMQ, Docker), padrões de comunicação e segurança.
* **[Padrão de Arquitetura do FastAPI](./docs/03_arquitetura_tecnica/arquitetura_backend_fastapi.md)**: Convenção rigorosa da estrutura de pastas, arquivos e camadas (MVC/Clean Architecture) que o backend em Python deverá seguir.
* **[Diretrizes do Front-End](./docs/03_arquitetura_tecnica/arquitetura_frontend.md)**: Guia de arquitetura do client, fluxos de telas (Mermaid), integração assíncrona (polling) e segurança com JWT.
* **[Modelagem de Dados e Banco](./docs/03_arquitetura_tecnica/modelagem_dados_postgres.md)**: Dicionário de dados, relacionamentos e Diagrama Entidade-Relacionamento (ER) que fundamenta o sistema no PostgreSQL.
* **[Modelagem NoSQL (MongoDB)](./docs/03_arquitetura_tecnica/modelagem_dados_mongodb.md)**: Estrutura de documentos, trilha de auditoria e sincronização (CQRS) no MongoDB.
* **[Diagramas Técnicos (Classes e Sequência)](./docs/03_arquitetura_tecnica/diagramas_projeto.md)**: Visualização da modelagem orientada a objetos (SQLAlchemy) e fluxo temporal de interações das telas com a API.
* **[Estrutura de Diretórios (Monorepo)](./docs/03_arquitetura_tecnica/estrutura_pastas.md)**: Guia de organização de pastas no padrão Monorepo com Docker para frontend, gateway e microsserviços.

## 4. Guias de Instalação e Tutoriais

Manuais práticos para configuração rápida do ambiente local de desenvolvimento.

* **[Guia de Instalação do Ambiente](./docs/04_guias_tutoriais/guia_instalacao.md)**: Passo a passo para Linux e Windows abrangendo Docker, Python (venv/Poetry), npm (Vite) e comandos úteis do Alembic.
* **[Guia de Containerização com Docker](./docs/04_guias_tutoriais/guia_docker.md)**: Como subir todo o ambiente (bancos, RabbitMQ, backend, worker e frontend) com um comando, portas expostas e variáveis de ambiente.
* **[Guia de Testes Automatizados](./docs/04_guias_tutoriais/guia_testes.md)**: Organização da suíte pytest, fixtures do `conftest.py` e como os alunos devem escrever novos testes de rota e repositório.

---

*Esta documentação é viva e poderá ser atualizada pelo professor ao longo das Sprints conforme a evolução e necessidade da turma.*
