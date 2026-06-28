# Diagramas Técnicos do Projeto (Classes e Sequência)

Este documento apresenta os diagramas de **Classes** e de **Sequência** do sistema de reservas, servindo de guia para o desenvolvimento do banco de dados (SQLAlchemy), lógica do backend (FastAPI) e comportamento das interfaces (Front-End).

---

## 1. Diagrama de Classes (Domínio / SQLAlchemy)

Este diagrama representa a estrutura de classes de modelo (entities) que mapeiam o banco de dados PostgreSQL via ORM, destacando seus atributos principais, relacionamentos e métodos de lógica de negócio:

```mermaid
classDiagram
    class Usuario {
        +UUID id
        +String nome
        +String email
        +String senha_hash
        +Boolean is_admin
        +autenticar() Boolean
    }

    class Cidade {
        +UUID id
        +String nome
        +String estado
        +JSONB limite_territorial
    }

    class Hotel {
        +UUID id
        +String nome
        +UUID cidade_id
        +Int categoria_estrelas
        +calcular_media_avaliacoes() Float
    }

    class Quarto {
        +UUID id
        +UUID hotel_id
        +String numero
        +String tipo
        +Float preco_diaria
        +Int max_adultos
        +Int max_criancas
        +verificar_disponibilidade(checkin, checkout) Boolean
    }

    class TarifaTemporada {
        +UUID id
        +String nome
        +Date data_inicio
        +Date data_fim
        +Float multiplicador
        +UUID hotel_id
        +esta_ativa(data) Boolean
    }

    class Reserva {
        +UUID id
        +UUID usuario_id
        +UUID quarto_id
        +Date data_checkin
        +Date data_checkout
        +Int quantidade_adultos
        +Int quantidade_criancas
        +Boolean early_checkin
        +Boolean late_checkout
        +Boolean necessita_berco
        +String tarifa_tipo
        +Date data_limite_cancelamento
        +Float valor_total
        +String status
        +Float valor_multa_cancelamento
        +calcular_preco_final() Float
        +cancelar() Boolean
    }

    class Avaliacao {
        +UUID id
        +UUID usuario_id
        +UUID hotel_id
        +Int nota
        +String comentario
        +DateTime data_publicacao
    }

    class ServicoAdicional {
        +UUID id
        +String nome
        +Float preco
    }

    %% Relacionamentos e Multiplicidades
    Cidade "1" --> "*" Hotel : sedia
    Hotel "1" --> "*" Quarto : oferece
    Hotel "1" --> "*" TarifaTemporada : aplica
    Usuario "1" --> "*" Reserva : realiza
    Quarto "1" --> "*" Reserva : aluga
    Usuario "1" --> "*" Avaliacao : publica
    Hotel "1" --> "*" Avaliacao : recebe
    Reserva "*" --> "*" ServicoAdicional : contrata
```

---

## 2. Diagrama de Sequência (Ciclo de Vida da Reserva e Telas)

Este diagrama detalha a linha do tempo e a troca de mensagens desde a busca de hotéis pelo cliente até a confirmação assíncrona da reserva, mostrando a relação entre as **telas (front-end)**, **API (FastAPI)**, **filas (RabbitMQ)**, **workers** e as **persistências (SQL e NoSQL)**:

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as Hóspede (Usuário)
    participant Front as Front-End (Telas)
    participant API as FastAPI (Backend)
    participant SQL as PostgreSQL (Transacional)
    participant Fila as RabbitMQ (Fila)
    participant Worker as Worker (Fila)
    participant NoSQL as MongoDB (Audit/Cache)

    %% Passo 1: Busca
    Note over Cliente, Front: [Tela 2: Home e Busca de Hoteis]
    Cliente->>Front: Filtra por Cidade, Datas e Hóspedes
    Front->>API: GET /api/v1/busca (cidade_id, checkin, checkout, hospedes)
    API->>NoSQL: Consulta catálogo desnormalizado (catalogo_hoteis)
    NoSQL-->>API: Retorna documento com Hoteis e Quartos
    API-->>Front: JSON estruturado de hotéis/quartos
    Front->>Front: Renders "Listagem de Hoteis"
    
    %% Passo 2: Seleção e Checkout
    Note over Cliente, Front: [Tela 3: Detalhes do Hotel & Quartos]
    Cliente->>Front: Seleciona Quarto e avança para Checkout
    Note over Cliente, Front: [Tela 4: Checkout e Customizacao]
    Cliente->>Front: Seleciona extras (early checkin, reembolso, cafe da manha)
    
    %% Passo 3: Criação de Reserva
    Cliente->>Front: Clica em "Confirmar e Pagar"
    Front->>Front: Renders "Tela 5: Processando Reserva" (Loading)
    Front->>API: POST /api/v1/reservas (dados_reserva)
    
    Note over API: Calcula valor base preliminar<br/>e cria reserva com status "Pendente"
    API->>SQL: INSERT INTO reservas (status='Pendente', valor_total, ...)
    API->>Fila: Publica ID da Reserva na fila "solicitacoes-reserva"
    API-->>Front: HTTP 202 Accepted {id: "reserva-uuid", status: "Pendente"}
    
    %% Passo 4: Polling e Background Processing (Paralelos)
    par Loop de Polling do Front-End (A cada 3 segundos)
        loop Enquanto status for "Pendente"
            Front->>API: GET /api/v1/reservas/{uuid}
            API->>SQL: SELECT status FROM reservas WHERE id={uuid}
            SQL-->>API: Retorna status (Pendente/Confirmada/Cancelada)
            API-->>Front: JSON {status: ...}
        end
    and Processamento do Worker (Assíncrono)
        Fila->>Worker: Consome evento com ID da Reserva
        Note over Worker: Valida choque de datas no período<br/>Calcula tarifas de temporada e crianças<br/>Simula pagamento (2s)
        
        alt Sucesso no pagamento e vaga livre
            Worker->>SQL: UPDATE reservas SET status='Confirmada' WHERE id={uuid}
            Worker->>NoSQL: Insere log "PAGAMENTO_APROVADO" (historico_auditoria)
        else Falha ou Choque de Datas
            Worker->>SQL: UPDATE reservas SET status='Cancelada' WHERE id={uuid}
            Worker->>NoSQL: Insere log "RESERVA_CANCELADA" com motivo (historico_auditoria)
        end
    end

    %% Passo 5: Fim do Polling
    Front->>Front: Detecta status != "Pendente" (Polling encerra)
    
    alt Status == "Confirmada"
        Front->>Front: Renders "Tela 6: Voucher/Sucesso" (Confirmação na tela)
    else Status == "Cancelada"
        Front->>Front: Renders "Tela 3: Detalhes" com mensagem de erro (Toast)
    end
```
