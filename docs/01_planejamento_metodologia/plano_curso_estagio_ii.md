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
  * **Scrum Master:** Responsável por garantir que a equipe entenda e aplique as práticas ágeis, removendo impedimentos do dia a dia.
  * **Developers (Equipe de Desenvolvimento):** Os alunos, responsáveis por planejar as tarefas, codificar, testar e entregar os incrementos de software a cada Sprint.
* **Sprint:** Um ciclo de trabalho fixo e curto (neste caso, 1 ou 2 semanas) onde um conjunto de tarefas é planejado, executado e entregue como uma parte funcional e testável do software.
* **Épicos (Epics):** Grandes iniciativas ou funcionalidades macro do sistema que não podem ser concluídas em uma única Sprint (ex: "Módulo de Reservas de Hotel" ou "Sistema de Autenticação"). Eles são quebrados em tarefas menores.
* **Histórias de Usuário (User Stories):** Descrições curtas e simples de uma funcionalidade, escritas sob a perspectiva de quem deseja a nova capacidade (ex: *"Como administrador, eu quero cadastrar um novo hotel, para que ele fique disponível na plataforma"*). Elas devem caber dentro de uma única Sprint.

---

## 3. Metodologia de Avaliação e Dinâmica de Aula

A disciplina adota o modelo pedagógico de Aprendizagem Baseada em Projetos (Project-Based Learning - PBL) combinado com Práticas Ágeis.

* **Dinâmica das Aulas Semanais:** Cada aula funciona como a transição de um Sprint. Inicia-se com um alinhamento rápido (similar a uma *Sprint Planning/Daily* adaptada) e segue para o desenvolvimento supervisionado.
* **Sprint Review Quinzenal:** A cada duas semanas, as equipes realizam uma cerimônia oficial de revisão, demonstrando o incremento do software funcional.
* **Avaliação Oral/Apresentação:** Juntamente com a Sprint Review, os alunos passam por uma arguição oral para defender as escolhas técnicas, design de código e arquitetura.
* **Avaliação por Pares (Peer Review):** Mecanismo opcional a ser refinado para que os membros do grupo avaliem a contribuição técnico-comportamental mútua, refletindo as avaliações de desempenho do mercado.

### Dinâmica das Equipes e Gerenciamento de Repositórios

Para simular um ambiente corporativo real e garantir uma avaliação justa do esforço individual, a disciplina adotará a seguinte estrutura de desenvolvimento:

* **Tamanho das Equipes:** 3 a 5 alunos. Este tamanho é ideal para permitir a divisão clara de papéis (ex: Frontend, Backend, Banco de Dados, DevOps, QA) e facilitar o trabalho colaborativo.
  * **Algoritmo de Divisão Automática (Sem Discussão):** Para qualquer quantidade de alunos $N$ na turma, a divisão das equipes é calculada de forma puramente matemática e determinística para priorizar grupos equilibrados de 3 e 4 alunos:
    * Para $N < 3$: Não é possível formar equipes regulares (tamanho mínimo de 3).
    * Para $3 \le N \le 5$: Forma-se **1 única equipe** de tamanho $N$.
    * Para $N = 6$: **2 equipes de 3** ($3 + 3$).
    * Para $N = 7$: **2 equipes** ($4 + 3$).
    * Para $N \ge 8$: O número total de equipes é dado por $T = \lceil N / 4 \rceil$ (arredondado para cima). A distribuição exata é:
      * **Equipes de 4 integrantes:** $x = N - 3T$
      * **Equipes de 3 integrantes:** $y = 4T - N$
    * **Exemplos práticos da aplicação da regra:**
      * **Turma de 12 alunos:** $T = 3$ equipes &rarr; $x = 3$ equipes de 4, $y = 0$ equipes de 3 ($4+4+4$)
      * **Turma de 13 alunos:** $T = 4$ equipes &rarr; $x = 1$ equipe de 4, $y = 3$ equipes de 3 ($4+3+3+3$)
      * **Turma de 14 alunos:** $T = 4$ equipes &rarr; $x = 2$ equipes de 4, $y = 2$ equipes de 3 ($4+4+3+3$)
      * **Turma de 15 alunos:** $T = 4$ equipes &rarr; $x = 3$ equipes de 4, $y = 1$ equipe de 3 ($4+4+4+3$)
      * **Turma de 22 alunos:** $T = 6$ equipes &rarr; $x = 4$ equipes de 4, $y = 2$ equipes de 3 ($4+4+4+4+3+3$)
  * **Nomenclatura das Equipes:** Para manter a neutralidade e a padronização, cada equipe formada receberá um nome genérico seguindo o alfabeto fonético internacional de acordo com sua ordem (iniciais A, B, C, D, E, F, G...):
    * **Equipe 1:** Alpha (Alfa)
    * **Equipe 2:** Bravo
    * **Equipe 3:** Charlie
    * **Equipe 4:** Delta
    * **Equipe 5:** Echo
    * **Equipe 6:** Foxtrot
    * **Equipe 7:** Golf
    * (Seguindo a ordem alfabética para equipes adicionais: Hotel, India, Juliet, Kilo, Lima, Mike, November, Oscar, Papa...)
* **Posse e Controle dos Repositórios (GitHub):** Os repositórios oficiais de cada projeto (ex: `est_web_turma_a_alpha`, `est_web_turma_a_bravo`, `est_web_turma_b_alpha`) serão criados e mantidos sob administração direta do professor (preferencialmente através de uma *GitHub Organization* dedicada à disciplina).
* **Alunos como Colaboradores:** Os membros de cada equipe receberão convites como *colaboradores* de seus respectivos repositórios. Essa abordagem assegura a integridade do projeto (evitando exclusões acidentais) e permite a aplicação de regras corporativas.
* **Fluxo de Trabalho Obrigatório (Pull Requests):** A branch principal (`main`) de todos os repositórios será protegida (*Branch Protection Rules*). Todo código novo deverá obrigatoriamente ser desenvolvido em branches paralelas (ex: `feature/nova-rota`) e submetido via *Pull Request* (PR) para revisão e merge.
* **Avaliação de Contribuição Individual (Auditoria):** O desenvolvimento do projeto não receberá apenas uma nota global. O professor utilizará as métricas e histórico do repositório (quantidade e qualidade de commits, PRs abertos, revisões de código feitas, aba *Insights/Contributors*) como ferramenta principal para auditar a participação real de cada aluno no desenvolvimento do software.

---

## 4. Projeto Prático e Arquitetura

O detalhamento técnico do projeto da disciplina, incluindo a stack de tecnologia (FastAPI, PostgreSQL, RabbitMQ), a modelagem de banco de dados e o planejamento das sprints técnicas, foi movido para um documento separado para melhor organização.

**Consulte o documento técnico aqui:** 
[Arquitetura e Projeto de Backend](../03_arquitetura_tecnica/arquitetura_projeto_backend.md)
