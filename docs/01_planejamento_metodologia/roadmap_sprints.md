# Roadmap de Sprints: Entregas Semanais (Backend + Frontend)

Este documento detalha a **divisão semanal das entregas** do projeto prático (Sistema de Reservas de Rede Hoteleira) ao longo das **15 sprints** de desenvolvimento ativo, conforme a estrutura macro definida no [Plano de Curso](./plano_curso_estagio_ii.md) e mapeada no [Cronograma 2026.2](./cronograma_aulas_2026_2.md).

Cada sprint tem duas trilhas paralelas (**Backend** e **Frontend**) e uma **Definição de Pronto (DoD)** — o incremento demonstrável que a equipe apresenta na transição da aula seguinte. As trilhas são pensadas para que o front sempre tenha um contrato de API estável para consumir na mesma sprint ou na anterior.

> **Legenda:** 🔵 Backend · 🟢 Frontend · ✅ Entrega/DoD · ⭐ Sprint Review quinzenal (arguição oral do incremento).

---

## Visão geral (Sprint ↔ Aula ↔ Tema)

| Sprint | Aula | Tema central | Review |
| :---: | :---: | :--- | :---: |
| — | 01 | Planejamento, equipes e escopo | |
| **S1** | 02 | Fundação: setup, Docker, modelos e migração inicial | |
| **S2** | 03 | **Autenticação & Autorização (JWT/RBAC)** — *construída pelos alunos* | ⭐ |
| **S3** | 04 | Catálogo: CRUD de Cidades e Hotéis (admin) | |
| **S4** | 05 | Quartos e Busca pública (CQRS/MongoDB) | ⭐ |
| **S5** | 06 | Motor de precificação (regras de negócio + testes) | |
| **S6** | 07 | Reserva assíncrona (RabbitMQ + Worker) | ⭐ |
| **S7** | 08 | Painel do Hóspede e estabilização do MVP | |
| — | 09 | **Mid-term Review** (demo do MVP + retrospectiva) | |
| **S8** | 10 | Cancelamento e políticas de multa | |
| **S9** | 11 | Avaliações de estadia | ⭐ |
| **S10** | 12 | CRUDs admin restantes e trilha de auditoria | |
| **S11** | 13 | Resiliência e requisitos não-funcionais | ⭐ |
| **S12** | 14 | Qualidade, cobertura de testes e documentação de API | |
| **S13** | 15 | Refino de UX e casos de borda | ⭐ |
| **S14** | 16 | Dockerização final e seeds de demonstração | |
| **S15** | 17 | Code freeze e preparação da defesa | ⭐ |
| — | 18 | Buffer (imprevistos / ensaio) | |
| — | 19 | Defesa de Arquitetura e apresentações finais | |

---

## Primeiro Ciclo (Sprints 1–7) — Construção do MVP

### Sprint 1 — Fundação e Setup (Aula 02)
* 🔵 Inicializar o projeto (Poetry/pip), subir **Docker Compose** (PostgreSQL, MongoDB, RabbitMQ), montar a arquitetura em camadas (`api/schemas/services/repositories/models`), `config`, `/health`. Primeiros modelos (`Usuario`, `Cidade`, `Hotel`) e **migração inicial + seed** via Alembic (admin, cidades, hotéis 1–5★).
* 🟢 Scaffolding do front (Vite + React + Bootstrap), estrutura de pastas, layout base (navbar + rotas), cliente HTTP (axios/fetch) com `baseURL` e tela-esqueleto de navegação.
* ✅ `docker compose up` sobe toda a stack; `GET /health` responde 200; o front renderiza o shell com rotas vazias.

### Sprint 2 — Autenticação & Autorização (Aula 03) ⭐
> **Sprint dedicada à construção do auth pelos próprios alunos.** O exemplo base já traz um auth **propositalmente básico** (`if/else`, sem hash nem token real) que deve ser **substituído** pela versão segura. Objetivos, arquivos e critérios de aceite na [Atividade de Auth (Sprint 2)](../02_engenharia_software/atividade_auth_sprint2.md).
* 🔵 Substituir o placeholder: implementar `security.py` (hash **bcrypt** + geração/validação de **JWT**), model/migração de `Usuario`, rotas `POST /auth/register` e `POST /auth/login`, guards `get_current_user` / `get_current_admin` (**RBAC**, `is_admin`) e `GET /auth/me`. **RFO01, RFO02, RFO03.** Testes da suíte de auth verdes.
* 🟢 Tela de **Login/Cadastro**, armazenamento do token, interceptor `Authorization: Bearer` + tratamento de `401` (limpar token e redirecionar), e **guarda de rotas** (cliente × admin).
* ✅ Cadastro + login ponta a ponta; rota protegida bloqueia sem token; cliente não acessa rota de admin (403); admin acessa. **Suíte pytest de auth passando.**

### Sprint 3 — Catálogo: Cidades e Hotéis (Aula 04)
* 🔵 Models `Cidade` (`limite_territorial` GeoJSON/JSONB), `Hotel` (`categoria_estrelas`, `cidade_id`), `Comodidade` + associativa. Migrações. **CRUD admin** (protegido por `is_admin`) de cidades/hotéis/comodidades + rota pública de listagem.
* 🟢 **Painel Admin** — CRUD de Cidades e Hotéis (tabelas + formulários) atrás do guard de admin.
* ✅ Admin cadastra cidade + hotel; a listagem pública retorna os dados cadastrados.

### Sprint 4 — Quartos e Busca Pública (Aula 05) ⭐
* 🔵 Model `Quarto` (tipo, `preco_diaria`, `max_adultos`/`max_criancas`) + CRUD admin. Projeção desnormalizada `catalogo_hoteis` no **MongoDB** e sua sincronização. Endpoint de busca por cidade/estrelas consumindo o Mongo (**RFO04**). *(Bônus: filtro territorial RFO05.)*
* 🟢 **Home** com filtros (cidade, datas, hóspedes adultos/crianças, estrelas), listagem de hotéis com *skeletons*, e tela **Detalhes do Hotel & Quartos**.
* ✅ Busca ponta a ponta lendo do Mongo; detalhes listam os quartos com capacidades.

### Sprint 5 — Motor de Precificação (Aula 06)
* 🔵 `reserva_service`: cálculo de diárias (base + `TarifaTemporada`, bebê 0–5 grátis, criança 6–12 = 50%, early/late +30%, serviços adicionais, desconto não-reembolsável −10%). Models/CRUD de `TarifaTemporada` e `ServicoAdicional`. **Testes unitários ≥ 70%** na camada de services (**RFO07, RFO08, RFO09, RNFO07**).
* 🟢 Tela de **Checkout** com cálculo dinâmico espelhando as regras (preview do total), seleção de tarifa/opcionais/serviços.
* ✅ Preço calculado idêntico entre o preview do front e o back; suíte de testes de preço verde.

### Sprint 6 — Reserva Assíncrona (Aula 07) ⭐
* 🔵 Model `Reserva`. `POST /reservas` cria status `Pendente`, publica em `solicitacoes-reserva` e responde **202** (**RFO06**). **Worker** consome: valida overbooking (**consumo serial por quarto, RNFO03**), simula pagamento (2s), confirma/cancela e grava auditoria no Mongo (`historico_auditoria`, **RFO11**).
* 🟢 Fluxo **Checkout → Processando** (short polling `GET /reservas/{id}` a cada 3s) **→ Voucher/Erro**.
* ✅ Reserva assíncrona ponta a ponta; overbooking evitado (dois pedidos simultâneos → um confirma, um cancela).

### Sprint 7 — Painel do Hóspede e Estabilização (Aula 08)
* 🔵 `GET /reservas` (do usuário logado) e `GET /reservas/{id}`. Hardening: validações de capacidade e tratamento inicial de erros.
* 🟢 Painel **Minhas Reservas** com badges de status.
* ✅ **MVP navegável fim-a-fim** (login → busca → reserva → minhas reservas). Congelar escopo para o mid-term.

---

## 🏁 Aula 09 — Mid-term Review
Demonstração do MVP, retrospectiva geral e ajuste de escopo do segundo ciclo. **Não é sprint.**

---

## Segundo Ciclo (Sprints 8–15) — Regras avançadas, qualidade e entrega

### Sprint 8 — Cancelamento e Políticas (Aula 10)
* 🔵 `POST /reservas/{id}/cancelar`: regra de 48h, multa de 1 diária (reembolsável tardio) ou 100% (não reembolsável) — **RFO10**. Atualiza status + auditoria.
* 🟢 Botão **Cancelar Reserva** no painel, com `data_limite_cancelamento` e aviso de multa.
* ✅ Cancelamento com multas corretas nos 4 cenários.

### Sprint 9 — Avaliações (Aula 11) ⭐
* 🔵 Model `Avaliacao`. `POST /avaliacoes` com restrição **RFO12** (só reserva `Confirmada` com check-out no passado). Média de avaliações no catálogo/detalhe.
* 🟢 Formulário de avaliação (nota + comentário) nas estadias concluídas; exibir média nos detalhes.
* ✅ Fluxo de avaliação restrito corretamente e média exibida.

### Sprint 10 — CRUDs Admin restantes e Auditoria (Aula 12)
* 🔵 CRUD completo de **Tarifas de Temporada** e **Serviços/Comodidades**. Endpoint admin de leitura da **trilha de auditoria** do Mongo (**UC11**).
* 🟢 Painel admin de Tarifas/Serviços e visualização dos logs de auditoria.
* ✅ Gestor gerencia tarifas/serviços; logs operacionais visíveis.

### Sprint 11 — Resiliência e Não-Funcionais (Aula 13) ⭐
* 🔵 **RNFO02** (< 200ms na criação), **RNFO06** (respostas `503` amigáveis / reconexão ao broker), paginação e índices.
* 🟢 **RNFO05** responsividade mobile-first, *skeletons* e tratamento global de erros/`401`.
* ✅ App responsivo; falhas de infra degradam graciosamente (sem crash da API).

### Sprint 12 — Qualidade, Cobertura e Documentação (Aula 14)
* 🔵 Elevar cobertura (services ≥ 70% + testes de rota e worker), **coleção Postman** e revisão do **Swagger**.
* 🟢 Testes de componentes-chave e ajustes de UX.
* ✅ CI verde, cobertura atingida, Postman/Swagger completos.

### Sprint 13 — Refino de UX e Casos de Borda (Aula 15) ⭐
* 🔵🟢 Tratar edge cases (datas inválidas, capacidade excedida, berço para bebês, isenções), mensagens de erro, formatação de moeda/data e acessibilidade.
* ✅ Fluxos robustos a entradas inválidas; UX polida.

### Sprint 14 — Dockerização Final e Demonstração (Aula 16)
* 🔵🟢 `docker-compose` completo (front nginx + api + worker + bancos), **seeds ricos de demonstração**, `.env` e README de execução.
* ✅ `docker compose up` sobe o sistema inteiro pronto para demo.

### Sprint 15 — Code Freeze e Preparação da Defesa (Aula 17) ⭐
* 🔵🟢 Bugfixes finais, hardening de segurança (expiração de JWT, CORS, `is_admin`), roteiro da apresentação e diagramas atualizados.
* ✅ **Release candidate** congelado; ensaio da Defesa de Arquitetura.

---

## Aulas 18–19
* **Aula 18 (Buffer):** reposições, imprevistos institucionais ou ensaio das apresentações.
* **Aula 19:** Apresentações finais e **Defesa de Arquitetura** (*Architecture Review Board*).

---

## Observações de planejamento
* **Front sempre atrás de um contrato estável:** cada tela consome uma API entregue na mesma sprint ou anterior — por isso auth (S2) e catálogo (S3–S4) vêm antes do checkout (S5–S6).
* **As Sprint Reviews quinzenais** caem no fim das sprints 2, 4, 6, 9, 11, 13 e 15 (aulas 03, 05, 07, 11, 13, 15, 17).
* **Equipes menores (3 alunos):** priorizar o caminho crítico (S1→S7) e tratar RFO05 (territorial) e parte do polimento (S13) como bônus.
