# Plano de Ensino e Brainstorming: Estágio II em Desenvolvimento Web

Este documento consolida o planejamento inicial para a disciplina de **Estágio II em Desenvolvimento Web**, estruturada com base em metodologias ágeis (Scrum/Sprints) e focada em uma arquitetura robusta baseada em FastAPI, PostgreSQL, Alembic e autenticação JWT.

---

## 1. Estrutura Macroscópica da Disciplina

O semestre será composto por um total de **19 semanas (aulas)**, organizadas de forma a simular o ambiente de desenvolvimento de uma empresa de tecnologia.

* **Total de Aulas:** 19
* **Sprints:** 15 sprints semanais de desenvolvimento ativo.
* **Ciclo de Avaliação:** Quinzenal (a cada 2 sprints).

### Distribuição Proposta das 19 Aulas:
* **Aula 01:** Planejamento inicial, nivelamento da turma, formação das equipes e definição do escopo dos projetos.
* **Aulas 02 a 08 (Sprints 1 a 7):** Primeiro ciclo de desenvolvimento ativo.
* **Aula 09:** Revisão de meio de semestre (*Mid-term Review*), alinhamento de entregas, retrospectiva geral e ajustes de rota no escopo.
* **Aulas 10 a 17 (Sprints 8 a 15):** Segundo ciclo de desenvolvimento ativo e refinamentos.
* **Aula 18:** Aula de Margem/Buffer (Espaço reservado para eventuais imprevistos institucionais, reposições de feriados ou ensaio das apresentações).
* **Aula 19:** Apresentações finais, Defesa de Arquitetura (*Architecture Review Board*) e encerramento da disciplina.

---

## 2. Fundamentos da Metodologia Ágil (Scrum)

Para alinhar o vocabulário e o fluxo de trabalho durante a disciplina, adotaremos os seguintes conceitos do Scrum e desenvolvimento Ágil:

* **Scrum:** Um framework ágil estruturado para ajudar equipes a desenvolverem, entregarem e manterem produtos complexos. Ele é baseado no empirismo, focando na entrega de valor contínua e em ciclos iterativos.
* **Papéis do Scrum:**
  * **Product Owner (PO):** O professor da disciplina (ou um aluno designado) atua como o responsável por definir e priorizar as funcionalidades do sistema (Product Backlog) para maximizar o valor do produto.
  * **Scrum Master:** Um aluno da própria equipe, designado de forma **rotativa a cada Sprint**, responsável por garantir que a equipe entenda e aplique as práticas ágeis, removendo impedimentos do dia a dia. A rotação assegura que todos os integrantes exercitem a liderança e a facilitação ao longo do semestre.
  * **Developers (Equipe de Desenvolvimento):** Os alunos, responsáveis por planejar as tarefas, codificar, testar e entregar os incrementos de software a cada Sprint.
* **Sprint:** Um ciclo de trabalho fixo e curto (neste caso, **1 semana**, correspondente a cada aula) onde um conjunto de tarefas é planejado, executado e entregue como uma parte funcional e testável do software.
* **Épicos (Epics):** Grandes iniciativas ou funcionalidades macro do sistema que não podem ser concluídas em uma única Sprint (ex: "Módulo de Reservas de Hotel" ou "Sistema de Autenticação"). Eles são quebrados em tarefas menores.
* **Histórias de Usuário (User Stories):** Descrições curtas e simples de uma funcionalidade, escritas sob a perspectiva de quem deseja a nova capacidade (ex: *"Como administrador, eu quero cadastrar um novo hotel, para que ele fique disponível na plataforma"*). Elas devem caber dentro de uma única Sprint.

---

## 3. Metodologia de Avaliação e Dinâmica de Aula

A disciplina adota o modelo pedagógico de Aprendizagem Baseada em Projetos (Project-Based Learning - PBL) combinado com Práticas Ágeis.

* **Dinâmica das Aulas Semanais:** Cada aula funciona como a transição de um Sprint. Inicia-se com um alinhamento rápido (similar a uma *Sprint Planning/Daily* adaptada) e segue para o desenvolvimento supervisionado.
* **Sprint Review Quinzenal:** A cada duas semanas, as equipes realizam uma cerimônia oficial de revisão, demonstrando o incremento do software funcional.
* **Avaliação Oral/Apresentação:** Juntamente com a Sprint Review, os alunos passam por uma arguição oral para defender as escolhas técnicas, design de código e arquitetura.
* **Avaliação por Pares (Peer Review):** Mecanismo **obrigatório e estruturado** (baseado em rubrica simples) para que os membros do grupo avaliem a contribuição técnico-comportamental mútua, refletindo as avaliações de desempenho do mercado. Complementa — e não substitui — a auditoria objetiva do histórico do repositório.
* **Definição de Pronto (Definition of Done):** Um incremento só é considerado entregue quando atende, no mínimo, aos seguintes critérios: (1) o código passa nos testes automatizados existentes; (2) foi submetido e revisado via Pull Request; (3) não introduz erros de *lint*; e (4) a funcionalidade é demonstrável na Sprint Review. Este DoD serve de referência objetiva na avaliação de cada Sprint.

### Dinâmica das Equipes e Gerenciamento de Repositórios

Para simular um ambiente corporativo real e garantir uma avaliação justa do esforço individual, a disciplina adotará a seguinte estrutura de desenvolvimento:

* **Tamanho das Equipes:** até 5 alunos. Este tamanho permite a divisão clara de papéis (ex: Frontend, Backend, Banco de Dados, DevOps, QA) e mantém o número de projetos sob acompanhamento em um patamar que o professor consegue auditar semana a semana.
  * **Algoritmo de Divisão Automática (Sem Discussão):** Para qualquer quantidade de alunos $N$ na turma, a divisão é calculada de forma puramente matemática e determinística, minimizando a quantidade de equipes:
    * O número total de equipes é $T = \lceil N / 5 \rceil$ (arredondado para cima), limitado a **6 equipes** — o teto de projetos que a disciplina comporta acompanhar.
    * Os alunos, previamente embaralhados por sorteio, são distribuídos de forma **circular** entre as $T$ equipes. Assim a eventual sobra fica espalhada (equipes de 5 e de 4) em vez de concentrada em uma única equipe menor.
    * Na prática, isso significa $x = N - 4T$ equipes de 5 integrantes e $y = 5T - N$ equipes de 4.
    * **Exemplos práticos da aplicação da regra:**
      * **Turma de 30 alunos (Turma A):** $T = 6$ equipes &rarr; 6 equipes de 5 ($5+5+5+5+5+5$)
      * **Turma de 20 alunos (Turma B):** $T = 4$ equipes &rarr; 4 equipes de 5 ($5+5+5+5$)
      * **Turma de 22 alunos:** $T = 5$ equipes &rarr; 2 equipes de 5, 3 equipes de 4 ($5+5+4+4+4$)
      * **Turma de 13 alunos:** $T = 3$ equipes &rarr; 1 equipe de 5, 2 equipes de 4 ($5+4+4$)
  * **Sorteio:** a alocação dos alunos é feita por sorteio aleatório a partir da lista oficial de matriculados, com semente fixa para que o resultado seja reproduzível e auditável. A composição resultante de cada oferta é registrada em documento próprio (ex: [Equipes e Repositórios — 2026.2](equipes_2026_2.md)).
  * **Nomenclatura das Equipes:** Para manter a neutralidade e a padronização, cada equipe formada receberá um nome genérico seguindo o alfabeto fonético internacional de acordo com sua ordem (iniciais A, B, C, D, E, F):
    * **Equipe 1:** Alfa (grafada `alpha` nos nomes de repositório)
    * **Equipe 2:** Bravo
    * **Equipe 3:** Charlie
    * **Equipe 4:** Delta
    * **Equipe 5:** Echo
    * **Equipe 6:** Foxtrot
* **Posse e Controle dos Repositórios (GitHub):** Os repositórios oficiais de cada projeto seguem o padrão `est_web_<ano>_<semestre>_turma_<turma>_<equipe>` (ex: `est_web_2026_2_turma_a_alpha`, `est_web_2026_2_turma_a_bravo`, `est_web_2026_2_turma_b_alpha`). A inclusão do ano e do semestre no nome evita colisões e mantém a organização legível entre ofertas sucessivas da disciplina. Os repositórios serão criados e mantidos sob administração direta do professor (preferencialmente através de uma *GitHub Organization* dedicada à disciplina).
* **Alunos como Colaboradores:** Os membros de cada equipe receberão convites como *colaboradores* de seus respectivos repositórios. Essa abordagem assegura a integridade do projeto (evitando exclusões acidentais) e permite a aplicação de regras corporativas.
* **Fluxo de Trabalho Obrigatório (Pull Requests):** A branch principal (`main`) de todos os repositórios será protegida (*Branch Protection Rules*). Todo código novo deverá obrigatoriamente ser desenvolvido em branches paralelas (ex: `feature/nova-rota`) e submetido via *Pull Request* (PR) para revisão e merge.
* **Avaliação de Contribuição Individual (Auditoria):** O desenvolvimento do projeto não receberá apenas uma nota global. O professor utilizará as métricas e histórico do repositório (quantidade e qualidade de commits, PRs abertos, revisões de código feitas, aba *Insights/Contributors*) como ferramenta principal para auditar a participação real de cada aluno no desenvolvimento do software. A **revisão de Pull Requests dos colegas** também conta como contribuição avaliada, incentivando a colaboração real em vez do simples volume de commits.

---

## 4. Projeto Prático e Arquitetura

O detalhamento técnico do projeto da disciplina, incluindo a stack de tecnologia (FastAPI, PostgreSQL, RabbitMQ), a modelagem de banco de dados e o planejamento das sprints técnicas, foi movido para um documento separado para melhor organização.

**Consulte o documento técnico aqui:** 
[Arquitetura e Projeto de Backend](../03_arquitetura_tecnica/arquitetura_projeto_backend.md)
