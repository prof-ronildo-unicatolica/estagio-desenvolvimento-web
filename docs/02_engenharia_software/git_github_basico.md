# O Básico de Git, GitHub e Gitflow

Este guia apresenta os conceitos essenciais do Git e GitHub, detalhando o fluxo de trabalho Gitflow, convenções de nomenclatura para branches e o padrão para mensagens de commit.

---

## 1. Comandos Básicos do Git

Aqui estão os comandos mais comuns para o dia a dia:

### Configuração Inicial
```bash
# Configurar nome de usuário e email
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### Inicialização e Clonagem
```bash
# Iniciar um novo repositório local
git init

# Clonar um repositório existente do GitHub
git clone https://github.com/usuario/repositorio.git
```

### Trabalhando com Alterações
```bash
# Verificar o status dos arquivos modificados
git status

# Adicionar arquivos específicos para a área de preparação (staging)
git add nome-do-arquivo.ext

# Adicionar todos os arquivos modificados de uma vez
git add .

# Criar um commit com as alterações (preferência por mensagens curtas e de linha única)
git commit -m "feat: adiciona nova funcionalidade de login"

# Ver o histórico de commits
git log --oneline
```

### Sincronizando com o GitHub (Remoto)
```bash
# Enviar commits locais para o repositório remoto (GitHub)
git push origin nome-da-branch

# Baixar e integrar as atualizações do repositório remoto para o local
git pull origin nome-da-branch
```

---

## 2. Autenticação com Chaves SSH (Linux e Windows)

Desde 2021 o GitHub **não aceita mais senha** para operações de `git push` / `git pull` via HTTPS. Você tem duas opções: usar um *Personal Access Token* (que expira e precisa ser recriado) ou configurar uma **chave SSH** — que você configura uma vez e nunca mais digita senha. **Usaremos SSH na disciplina.**

### 2.1. Como funciona (o conceito)

Uma chave SSH é um **par de arquivos** que se completam:

| Arquivo | Nome típico | O que é | Onde vai |
|---|---|---|---|
| Chave **privada** | `id_ed25519` | Sua identidade secreta | **Fica só no seu computador. NUNCA compartilhe, nunca commite.** |
| Chave **pública** | `id_ed25519.pub` | O "cadeado" derivado da privada | Você **cola no GitHub** |

O GitHub guarda o cadeado (pública); seu PC guarda a chave (privada). Quando você faz `push`, os dois conversam e provam que combinam — sem nunca transmitir a chave privada.

> ⚠️ **Regra de ouro:** o arquivo que você copia e cola no GitHub é **sempre** o que termina em `.pub`. Se você colar o outro por engano, considere a chave comprometida e gere um par novo.

```mermaid
flowchart LR
    A[1. Gerar o par<br/>ssh-keygen] --> B[2. Iniciar o agente<br/>ssh-agent + ssh-add]
    B --> C[3. Copiar a chave PÚBLICA<br/>id_ed25519.pub]
    C --> D[4. Colar no GitHub<br/>Settings > SSH and GPG keys]
    D --> E[5. Testar<br/>ssh -T git@github.com]
    E --> F[6. Clonar/usar a URL SSH<br/>git@github.com:usuario/repo.git]
```

---

### 2.2. Passo 1 — Verificar se você já tem uma chave

Antes de gerar uma nova, veja se já existe alguma (é comum já ter de projetos antigos).

**Linux (Terminal) / Windows (Git Bash):**
```bash
ls -al ~/.ssh
```

**Windows (PowerShell):**
```powershell
ls $env:USERPROFILE\.ssh
```

Se aparecer um par como `id_ed25519` e `id_ed25519.pub` (ou `id_rsa` / `id_rsa.pub`), você já tem uma chave e pode **pular para o passo 4** (copiar a pública). Se der erro dizendo que o diretório não existe, ou a pasta estiver vazia, siga para o passo 2.

---

### 2.3. Passo 2 — Gerar a chave

O comando é **idêntico** nos três ambientes (Linux, Git Bash e PowerShell). Use o **mesmo e-mail cadastrado no GitHub**:

```bash
ssh-keygen -t ed25519 -C "seu.email@exemplo.com"
```

> **Por que `ed25519`?** É o algoritmo moderno recomendado pelo GitHub: mais seguro e com chaves menores que o RSA.
> Se o seu sistema for antigo e reclamar que não conhece `ed25519`, use: `ssh-keygen -t rsa -b 4096 -C "seu.email@exemplo.com"` (e daí em diante troque `id_ed25519` por `id_rsa` nos comandos seguintes).

O terminal fará **três perguntas**:

1. **`Enter file in which to save the key (/home/voce/.ssh/id_ed25519):`**
   → Apenas aperte **Enter** para aceitar o local padrão. (Só mude se você já tiver outra chave e não quiser sobrescrevê-la — nesse caso, digite um nome novo, ex: `/home/voce/.ssh/id_ed25519_faculdade`.)

2. **`Enter passphrase (empty for no passphrase):`**
   → Uma senha extra que protege o arquivo da chave privada caso alguém copie seu computador. **Recomendado**: digite uma. Se quiser praticidade total, aperte Enter para deixar vazio. *(Nada aparece na tela enquanto você digita — isso é normal.)*

3. **`Enter same passphrase again:`**
   → Repita a senha (ou Enter novamente).

Ao final você verá algo como:
```
Your identification has been saved in /home/voce/.ssh/id_ed25519
Your public key has been saved in /home/voce/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:AbCdEf... seu.email@exemplo.com
```

Pronto: os dois arquivos foram criados.

---

### 2.4. Passo 3 — Registrar a chave no `ssh-agent`

O `ssh-agent` é um programa que guarda sua chave em memória para você não precisar digitar a *passphrase* a cada `push`.

#### 🐧 Linux
```bash
# Inicia o agente na sessão atual
eval "$(ssh-agent -s)"

# Adiciona sua chave privada ao agente (note: SEM o .pub)
ssh-add ~/.ssh/id_ed25519
```
> **Observação:** no Linux, o `eval "$(ssh-agent -s)"` vale só para o terminal aberto. Na maioria das distribuições com ambiente gráfico (GNOME/KDE) o agente já sobe sozinho no login e você só precisa do `ssh-add`. Se quiser garantir, adicione as duas linhas ao final do seu `~/.bashrc` ou `~/.zshrc`.

#### 🪟 Windows — PowerShell (recomendado)
Abra o **PowerShell como Administrador** apenas para os dois primeiros comandos:
```powershell
# Habilita o serviço do ssh-agent para iniciar junto com o Windows
Set-Service -Name ssh-agent -StartupType Automatic

# Inicia o serviço agora
Start-Service ssh-agent
```
Depois, em um PowerShell **normal**:
```powershell
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

#### 🪟 Windows — Git Bash
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

Se tudo deu certo, a resposta será: `Identity added: /home/voce/.ssh/id_ed25519 (seu.email@exemplo.com)`.

---

### 2.5. Passo 4 — Copiar a chave **pública**

Este é o passo em que mais se erra. **Copie o conteúdo do arquivo `.pub`** — inteiro, sem quebras de linha, sem espaços sobrando no início ou no fim.

#### 🐧 Linux
```bash
# Opção A: copiar direto para a área de transferência (X11)
xclip -selection clipboard < ~/.ssh/id_ed25519.pub

# Opção B: Wayland (GNOME/KDE modernos)
wl-copy < ~/.ssh/id_ed25519.pub

# Opção C (sempre funciona): exibir na tela e copiar com o mouse
cat ~/.ssh/id_ed25519.pub
```
> Se o `xclip` não estiver instalado: `sudo apt install xclip` (Debian/Ubuntu) ou `sudo dnf install xclip` (Fedora). Se estiver sem interface gráfica, use a opção C.

#### 🪟 Windows — PowerShell
```powershell
# Copia direto para a área de transferência
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# Ou apenas exibir na tela para copiar com o mouse
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

#### 🪟 Windows — Git Bash
```bash
clip < ~/.ssh/id_ed25519.pub
```

O conteúdo copiado deve ter **uma única linha** parecida com esta:
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIH8kL2mQp0rS3tUvWxYz1a2B3c4D5e6F7g8H9i0JkLmN seu.email@exemplo.com
```

> ❌ **Se o texto começar com `-----BEGIN OPENSSH PRIVATE KEY-----`, PARE.** Você abriu a chave **privada** por engano (esqueceu o `.pub`). Não cole isso em lugar nenhum.

---

### 2.6. Passo 5 — Colar no GitHub (onde exatamente)

1. Faça login no [github.com](https://github.com).
2. Clique na **sua foto de perfil**, no canto superior direito → **Settings**.
   *(Atalho: acesse direto <https://github.com/settings/keys>)*
3. No menu lateral esquerdo, procure a seção **Access** e clique em **SSH and GPG keys**.
4. Clique no botão verde **New SSH key**.
5. Preencha o formulário:
   - **Title:** um apelido para identificar a máquina, ex: `Notebook Dell - Linux` ou `PC Laboratório - Windows`. Serve só para você saber qual chave revogar depois.
   - **Key type:** deixe em **Authentication Key**.
   - **Key:** **cole aqui** (Ctrl+V) o conteúdo do arquivo `.pub` que você copiou no passo 4.
6. Clique em **Add SSH key**. O GitHub pode pedir sua senha da conta para confirmar.

A chave aparecerá na lista com o *fingerprint* e a data. **Uma chave por computador**: se você usa o notebook de casa e o PC do laboratório, gere um par em cada máquina e cadastre as duas chaves públicas.

---

### 2.7. Passo 6 — Testar a conexão

**Linux, Git Bash ou PowerShell — o comando é o mesmo:**
```bash
ssh -T git@github.com
```

Na **primeira vez**, aparecerá um aviso sobre a autenticidade do host:
```
The authenticity of host 'github.com (140.82.121.4)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```
Digite **`yes`** e Enter. *(Esse fingerprint é o oficial do GitHub — se o seu for diferente, não continue.)*

**Resposta de sucesso:**
```
Hi seu-usuario! You've successfully authenticated, but GitHub does not provide shell access.
```

> A frase *"does not provide shell access"* **não é erro** — é o comportamento esperado. Se apareceu o seu nome de usuário, está tudo certo.

---

### 2.8. Passo 7 — Usar SSH nos repositórios

Configurar a chave não muda automaticamente os repositórios que você já clonou por HTTPS. Você precisa usar a **URL SSH**.

**Ao clonar um repositório novo:** na página do repositório, clique em **Code** → aba **SSH** → copie a URL (ela começa com `git@github.com:`, não com `https://`).
```bash
git clone git@github.com:usuario/repositorio.git
```

**Para converter um repositório que você já clonou por HTTPS:**
```bash
# 1. Ver qual URL está configurada hoje
git remote -v

# 2. Trocar para SSH
git remote set-url origin git@github.com:usuario/repositorio.git

# 3. Conferir se mudou
git remote -v
```

A partir daqui, `git push` e `git pull` funcionam sem pedir usuário e senha.

---

### 2.9. Extra: mais de uma conta GitHub na mesma máquina

É comum ter uma conta pessoal e outra institucional. Como o GitHub **não aceita a mesma chave pública em duas contas**, você precisa de um par de chaves por conta e de um "apelido" para cada uma.

**1. Gere uma segunda chave com nome próprio:**
```bash
ssh-keygen -t ed25519 -C "seu.email@universidade.edu.br" -f ~/.ssh/id_ed25519_universidade
```

**2. Cadastre `id_ed25519_universidade.pub` na conta institucional** (mesmo passo 5, mas logado na outra conta).

**3. Crie/edite o arquivo `~/.ssh/config`** (no Windows: `C:\Users\SeuUsuario\.ssh\config`) definindo um apelido por conta:
```
# Conta pessoal (chave padrão)
Host github.com-pessoal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# Conta da universidade
Host github.com-universidade
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_universidade
```

**4. Use o apelido no lugar de `github.com` na URL do remote:**
```bash
git clone git@github.com-universidade:usuario/repositorio.git

# ou, em um repositório já existente:
git remote set-url origin git@github.com-universidade:usuario/repositorio.git
```

**5. Teste cada conta separadamente:**
```bash
ssh -T git@github.com-pessoal
ssh -T git@github.com-universidade
```
Cada comando deve responder com o nome de usuário **daquela** conta.

> **Não esqueça do `user.email` local:** o e-mail do commit é independente da chave SSH. Dentro do repositório da faculdade, rode `git config user.email "seu.email@universidade.edu.br"` (sem o `--global`) para que os commits apareçam vinculados à conta certa.

---

### 2.10. Problemas comuns e soluções

| Mensagem de erro | Causa provável | Como resolver |
|---|---|---|
| `Permission denied (publickey)` | A chave não foi cadastrada no GitHub, ou não está no `ssh-agent` | Rode `ssh-add -l` para listar as chaves carregadas. Se disser *"The agent has no identities"*, refaça o passo 3. Confirme também que a chave pública está em <https://github.com/settings/keys> |
| `Could not open a connection to your authentication agent` | O `ssh-agent` não está rodando | Linux/Git Bash: `eval "$(ssh-agent -s)"`. PowerShell: `Start-Service ssh-agent` (como Admin) |
| `git@github.com: Permission denied` só em **um** repositório | Você é colaborador mas o remote está errado, ou não aceitou o convite | Verifique `git remote -v` e aceite o convite que chegou no e-mail/notificações do GitHub |
| Ainda pede **usuário e senha** no push | O repositório continua apontando para HTTPS | Refaça o passo 7 (`git remote set-url`) |
| `WARNING: UNPROTECTED PRIVATE KEY FILE!` (Linux) | Permissões do arquivo estão abertas demais | `chmod 700 ~/.ssh` e `chmod 600 ~/.ssh/id_ed25519` |
| `ssh: connect to host github.com port 22: Connection timed out` | A rede (comum em Wi-Fi de instituições) bloqueia a porta 22 | Use a porta 443 do GitHub: crie/edite `~/.ssh/config` com as linhas abaixo |

**Contornando o bloqueio da porta 22** — crie o arquivo `~/.ssh/config` (Linux/Git Bash) ou `C:\Users\SeuUsuario\.ssh\config` (Windows) com:
```
Host github.com
  Hostname ssh.github.com
  Port 443
  User git
```
Depois teste novamente com `ssh -T git@github.com`.

---

### 2.11. Checklist final

- [ ] Par de chaves gerado (`id_ed25519` e `id_ed25519.pub` existem em `~/.ssh`)
- [ ] Chave privada adicionada ao `ssh-agent` (`ssh-add -l` mostra a chave)
- [ ] Chave **pública** colada em <https://github.com/settings/keys>
- [ ] `ssh -T git@github.com` responde com `Hi seu-usuario!`
- [ ] `git remote -v` mostra uma URL começando com `git@github.com:`
- [ ] A chave **privada** nunca foi enviada a ninguém nem commitada no repositório

---

## 3. Gitflow: O Fluxo de Trabalho

O **Gitflow** é um modelo de ramificação (branching) estruturado que define um controle rigoroso em torno do lançamento do projeto. Ele atribui papéis muito específicos a diferentes branches e define como e quando elas devem interagir.

### Branches Principais (Eternas)

Estas branches sempre existem no repositório:

- **`main`** (ou `master`): Contém o código de produção. Sempre deve estar em um estado funcional e estável. Todo código aqui já foi testado e aprovado.
- **`develop`**: A branch de integração. Todas as novas funcionalidades (features) são mescladas (merged) aqui. É o "próximo release" em construção.

### Diagrama do Fluxo (Gitflow)

```mermaid
gitGraph
    commit id: "Inicial"
    branch develop
    commit id: "Setup"
    branch feature/nova-tela
    commit id: "Tela v1"
    commit id: "Tela v2"
    checkout develop
    merge feature/nova-tela
    branch release/v1.0.0
    commit id: "Ajustes finais"
    checkout main
    merge release/v1.0.0 tag: "v1.0.0"
    checkout develop
    merge release/v1.0.0
    checkout main
    branch hotfix/erro-critico
    commit id: "Corrige bug em prod"
    checkout main
    merge hotfix/erro-critico tag: "v1.0.1"
    checkout develop
    merge hotfix/erro-critico
```

---

## 4. Padrões de Nomenclatura de Branches

Para organizar o desenvolvimento, usamos branches temporárias que são criadas a partir da `develop` (ou `main` em casos urgentes) e depois mescladas de volta.

### Tipos de Branches de Desenvolvimento

- **`feature/`** ou **`feat/`**:
  - **Para que serve:** Desenvolver novas funcionalidades.
  - **Origem:** `develop`
  - **Destino:** `develop`
  - **Exemplo:** `feature/nova-tela-de-perfil`, `feature/login-com-google`

- **`bugfix/`** ou **`fix/`**:
  - **Para que serve:** Corrigir bugs não críticos encontrados no ambiente de desenvolvimento (`develop`).
  - **Origem:** `develop`
  - **Destino:** `develop`
  - **Exemplo:** `fix/erro-calculo-carrinho`

- **`hotfix/`**:
  - **Para que serve:** Correções emergenciais diretamente em produção. É a única branch de suporte que deve nascer da `main`.
  - **Origem:** `main`
  - **Destino:** `main` e `develop` (para garantir que a correção não se perca)
  - **Exemplo:** `hotfix/crash-na-tela-inicial`

- **`release/`**:
  - **Para que serve:** Preparação para um novo lançamento em produção. Usada para pequenos ajustes finais, correção de bugs de última hora e preparação de metadados (como versão).
  - **Origem:** `develop`
  - **Destino:** `main` e `develop`
  - **Exemplo:** `release/v1.2.0`

---

## 5. Convenção de Commits (Conventional Commits)

Seguimos o padrão do *Conventional Commits* para facilitar a leitura do histórico e a geração automática de changelogs. 

> **Nota sobre o Estilo:** Mantenha as mensagens de commit curtas, diretas e, de preferência, em uma única linha.

### Estrutura
`<tipo>: <descrição curta>`

### Tipos de Commits Permitidos

- **`feat`**: Adição de uma nova funcionalidade (feature).
  - *Ex: `feat: cria endpoint para listagem de usuários`*
- **`fix`**: Correção de um bug (bugfix/hotfix).
  - *Ex: `fix: resolve erro de null pointer no calculo de juros`*
- **`perf`**: Mudança de código que melhora a performance, sem alterar o comportamento externo.
  - *Ex: `perf: otimiza query de busca no banco de dados`*
- **`refactor`**: Refatoração de código (não adiciona feature nem corrige bug, apenas melhora a estrutura interna).
  - *Ex: `refactor: extrai logica de validacao para classe separada`*
- **`docs`**: Alterações apenas na documentação (README, swagger, etc).
  - *Ex: `docs: atualiza readme com instrucoes de setup local`*
- **`style`**: Mudanças de formatação ou estilo (espaços em branco, formatação, falta de ponto e vírgula, etc) que não afetam o significado do código.
  - *Ex: `style: formata arquivos com prettier`*
- **`test`**: Adição de testes ausentes ou correção de testes existentes.
  - *Ex: `test: adiciona cobertura para o servico de pagamento`*
- **`chore`**: Atualizações de tarefas de build, configurações de pacotes, dependências ou ferramentas auxiliares que não modificam o código fonte de produção.
  - *Ex: `chore: atualiza versao do react para 18`*
- **`ci`**: Mudanças nos arquivos e scripts de configuração de Integração Contínua (CI) (ex: GitHub Actions, Travis, etc).
  - *Ex: `ci: adiciona pipeline de deploy para staging`*

---

## 6. Dinâmica de Acesso ao Repositório

Para a disciplina, os repositórios oficiais seguirão um modelo centralizado para simular o controle de qualidade corporativo:

* **Professor (Admin):** É o dono/administrador do repositório. Ele configura regras de proteção (impedindo push direto na `main` e `develop`), monitora as métricas de contribuição individual e pode aprovar/reprovar *Pull Requests*.
* **Alunos (Collaborators):** Vocês serão convidados para o repositório como colaboradores com permissão de escrita (*Write*). Isso permite clonar, criar branches (`feature/`, `bugfix/`) e enviar (*push*) essas branches para o GitHub. **Vocês não podem commitar diretamente nas branches protegidas**.

---

## 7. O Ciclo de Vida de uma Entrega (Pull Request)

Todo código novo deve passar por um processo de revisão. O fluxo prático para entregar uma tarefa é o seguinte:

```mermaid
flowchart TD
    A[Atualiza a develop local] --> B[Cria branch feature/tarefa]
    B --> C[Codifica e faz Commits]
    C --> D[Push da branch para o GitHub]
    D --> E[Abre um Pull Request - PR]
    E --> F{Revisão - Code Review}
    F -->|Aprovado| G[Merge para a develop]
    F -->|Solicita Mudanças| C
```

### Boas Práticas para Descrição de Pull Requests (PRs)

O PR é onde você "vende" o seu código para o revisor (seus colegas de equipe ou o professor). Uma descrição vazia ou muito vaga atrasa a aprovação e dificulta o entendimento do que foi feito.

#### Exemplo de PR Ruim
**Título:** `Ajustes`
**Descrição:** `Fiz a tela de login.`
*(Por que é ruim? Não explica o que foi feito, como testar e nem se há alguma pendência ou dependência).*

#### Exemplo de PR Excelente
**Título:** `feat: implementa rota e validacao de login`
**Descrição:**
```markdown
## O que foi feito?
- Criada a rota `/api/v1/login` utilizando FastAPI.
- Adicionada validação de hash da senha no banco PostgreSQL.
- Retorno do token JWT em caso de sucesso.
- Tratamento de erro (HTTP 401) para credenciais inválidas.

## Como testar?
1. Rode as migrações do banco: `alembic upgrade head`
2. Suba o servidor com `uvicorn main:app --reload`
3. Envie um POST para `/api/v1/login` usando o Postman ou Swagger.

## Observações
- A lógica de expiração do token está mockada para 24h, ajustaremos na próxima sprint.
```

---

## 8. Integração de Código: Merge vs Rebase e Resolução de Conflitos

Quando você trabalha em equipe, é comum que a branch `develop` receba novos commits enquanto você ainda está trabalhando na sua branch `feature`. Para manter sua branch atualizada, você precisará integrar essas mudanças.

### Merge vs Rebase

Existem duas formas principais de trazer as atualizações da `develop` para a sua branch atual:

* **`git merge develop`**: Pega todas as mudanças da `develop` e cria um *novo commit de merge* na sua branch. 
  * *Pró:* Preserva o histórico exato de como as coisas aconteceram (não reescreve o passado).
  * *Contra:* O histórico pode ficar poluído com muitos commits de "Merge branch develop into feature...".
* **`git rebase develop`**: "Desconecta" os seus commits temporariamente, puxa as atualizações da `develop` e então aplica os seus commits *no topo* do histórico atualizado.
  * *Pró:* Mantém o histórico linear e limpo.
  * *Contra:* Você está reescrevendo o histórico da sua branch. (Regra de ouro: **Nunca faça rebase em branches públicas como main ou develop**, apenas na sua branch local de feature).

Para a disciplina, recomendamos o uso de `git merge` local ou a interface do GitHub para resolver integrações no PR.

### Como Resolver Conflitos de Merge

Conflitos ocorrem quando duas pessoas alteram **a mesma linha do mesmo arquivo**. O Git não sabe qual versão manter e pede sua ajuda.

**Cenário:** Você tentou fazer um `git merge develop` na sua branch e o terminal mostrou:
`CONFLICT (content): Merge conflict in main.py`

**Passo a Passo para Resolver:**

1. **Abra o arquivo conflitante (ex: `main.py`) no seu editor (VS Code).**
   O editor destacará as áreas de conflito com marcadores do Git:
   ```python
   <<<<<<< HEAD (Current Change - A sua alteração)
   print("Olá, Turma A!")
   =======
   print("Olá, Mundo!")
   >>>>>>> develop (Incoming Change - O que veio da develop)
   ```
2. **Escolha a versão correta:** Apague os marcadores (`<<<<<<<`, `=======`, `>>>>>>>`) e deixe o código exatamente como ele deve ficar na versão final (pode ser a sua, a do colega, ou uma mistura das duas). No VS Code, você pode usar os botões *Accept Current Change*, *Accept Incoming Change* ou *Accept Both Changes*.
3. **Marque como resolvido:** Volte ao terminal e adicione o arquivo corrigido:
   ```bash
   git add main.py
   ```
4. **Finalize o Merge:**
   ```bash
   git commit -m "Merge: resolve conflitos com develop em main.py"
   ```
   *(Se você estava fazendo um rebase, o comando seria `git rebase --continue`).*

---

## 9. Resumo do Fluxo Diário

1. **Sincronize:** Atualize sua `develop` local: `git checkout develop` -> `git pull origin develop`
2. **Isole:** Crie sua branch a partir dela: `git checkout -b feature/minha-nova-tarefa`
3. **Desenvolva:** Codifique e faça commits seguindo o padrão: `git add .` -> `git commit -m "feat: implementa logica inicial"`
4. **Publique a branch:** Envie sua branch para o repositório remoto: `git push origin feature/minha-nova-tarefa`
5. **Entregue para Revisão:** Vá ao GitHub e abra um **Pull Request (PR)** da sua branch para a `develop`, preenchendo uma descrição clara.
