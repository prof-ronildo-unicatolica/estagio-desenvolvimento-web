# Estudo de Caso: Sistema de Reservas de Rede Hoteleira

Este documento descreve a problemática de negócios de uma franquia de hotéis que atua em múltiplas cidades e os motivos estratégicos pelos quais o CEO da rede precisa de um sistema integrado de reservas.

---

## 1. O Cenário Atual da Franquia

A rede hoteleira opera hotéis de diferentes categorias (de 1 a 5 estrelas) em diversas cidades do país. Atualmente, cada hotel gerencia suas operações de forma independente, utilizando sistemas locais legados, planilhas eletrônicas e até mesmo registros manuais. 

A comunicação com a matriz é realizada por meio de relatórios semanais de ocupação enviados por e-mail.

---

## 2. A Problemática de Negócio

A falta de um sistema centralizado e moderno gera sérios gargalos que impactam diretamente a rentabilidade e a imagem da franquia:

### A. Falta de Visibilidade Unificada (Decisões Estratégicas às Cegas)
Como o CEO e a equipe de gestão da franquia não possuem acesso em tempo real aos dados de ocupação e faturamento de cada filial, torna-se impossível realizar análises consolidadas rápidas. Perguntas cruciais como *"qual cidade está com a menor taxa de ocupação esta semana?"* ou *"qual categoria de hotel (ex: 3 estrelas) é mais lucrativa em determinada região?"* demoram dias para serem respondidas.

### B. O Problema do Overbooking (Concorrência e Reservas Duplicadas)
Sem validação de vagas em tempo real para reservas concorrentes ocorrendo no mesmo período, a rede sofre frequentemente com o *overbooking* (venda de mais quartos do que a capacidade real física do hotel). Isso resulta em custos adicionais para realocar hóspedes em hotéis concorrentes de última hora e em avaliações negativas na internet.

### C. Experiência de Checkout Lenta e Instável
O processo atual de reserva exige validações manuais de pagamento e disponibilidade. Em períodos de pico (como feriados nacionais ou férias de fim de ano), o servidor de aplicação local sofre lentidão sob carga excessiva, resultando em quedas de sistema, pagamentos duplicados ou carrinhos abandonados por lentidão.

### D. Segurança de Dados Fragilizada
Com dados espalhados em diferentes bancos locais e planilhas, não há controle rígido sobre quem acessa informações sensíveis dos clientes (dados cadastrais e históricos de hospedagem). A falta de uma política de controle de acesso unificada expõe a marca a riscos regulatórios e vazamento de informações.

---

## 3. Por que o CEO precisa deste Sistema?

A implementação da arquitetura baseada em **FastAPI, PostgreSQL, Alembic, JWT e RabbitMQ** resolve diretamente as dores da franquia, trazendo valor competitivo para a rede:

### A. Centralização de Dados e Inteligência de Mercado (PostgreSQL + Alembic)
Ao consolidar todas as cidades, filiais, quartos e reservas em um único banco de dados relacional (PostgreSQL), a gestão da franquia passa a contar com uma "única fonte da verdade". O uso do Alembic garante que qualquer alteração na estrutura de dados (como novos campos para promoções ou programas de fidelidade) seja propagada de forma segura e auditável para todas as instâncias do sistema.

### B. Escalabilidade sob Carga e Fim do Overbooking (RabbitMQ + Workers)
Ao invés de processar pagamentos e travar o banco de dados principal no momento em que o cliente clica em "Reservar", o FastAPI salva a intenção com status "Pendente" e delega o processamento ao RabbitMQ. 
* O Worker de mensageria analisa a disponibilidade de vagas de forma sequencial na fila, eliminando o risco de overbooking concorrente.
* Se a demanda explodir em um feriado, as solicitações aguardam ordenadamente na fila sem derrubar a API principal, garantindo alta disponibilidade da plataforma.

### C. Segurança e Compliance (JWT)
O uso de autenticação stateless baseada em JWT garante que as credenciais dos usuários nunca trafeguem expostas após o login. Além disso, permite a separação clara de papéis: o cliente comum tem acesso apenas às suas próprias reservas, enquanto o gestor da franquia possui privilégios de administrador para alterar tarifas, desativar quartos e gerenciar o catálogo de filiais.

### D. Automatização e Eficiência Operacional
Com o processamento de pagamentos simulado e a emissão automática do voucher de viagem por e-mail gerenciados de forma assíncrona, a rede reduz a necessidade de intervenção humana em tarefas administrativas repetitivas, permitindo que a equipe do hotel foque exclusivamente no atendimento físico aos hóspedes.
