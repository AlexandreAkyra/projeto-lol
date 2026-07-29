# Etapa 1 — Planejamento do Projeto

> Preencha os campos marcados com `>>>`. Este documento é o **contrato do projeto**:
> tudo que você fizer depois precisa ser coerente com o que está escrito aqui.

---

## 1. Project Charter (Termo de Abertura)

### 1.1 Pergunta principal

**Quais fatores mais influenciam a vitória em partidas ranqueadas de alto elo
(Mestre, Grão-Mestre e Desafiante) no servidor brasileiro de League of Legends?**

*Enquadramento:* o alto elo é usado como **modelo de referência** — o que fazem
os jogadores cuja execução é consistente o bastante para que a estratégia, e não
o erro individual, decida a partida. A pergunta original ("em partidas ranqueadas
de LoL") era ampla demais para o recorte definido na seção 1.2.

### 1.2 Escopo — as 6 decisões obrigatórias

Cada decisão abaixo muda completamente o resultado da análise.
Não existe resposta "certa" — existe resposta **justificada**.

| # | Decisão | Sua escolha | Justificativa (1 frase) |
|---|---------|-------------|-------------------------|
| 1 | **Região / plataforma** (ex: BR1, NA1, EUW1, KR) | BR1 | Vou escolher a BR1, pois é o server que eu jogo e entendo melhor |
| 2 | **Fila** (Ranked Solo/Duo = queue 420, Flex = 440) | Ranked Solo/Duo = queue 420 | Vou escolher a Solo/Duo pois a flex não é muito levada a sério e tem muita gente só jogando for fun na flex testando campeoes em rotas que nao deveriam, fazendo builds completamente fora do meta, na Solo/Duo as pessoas só jogam pra realmente ganhar e aprender a como jogar |
| 3 | **Faixa de elo** (ex: só Emerald, ou Diamond+, ou várias faixas comparadas) | Mestre, grão-mestre e desafiante |  Na API da riot tem uma seçao dedicada para esses 3 elos, onde posso pegar o PUUID dos players que estão nestes elos e depois usar esses PUUIDS para pegar o historico de partida destes players |
| 4 | **Janela temporal / patch** (ex: últimos 30 dias, patch 26.x) | últimos 30 dias | Irei utilizar os ultimos 30 dias, pois a duração de um patch é muito pequeno, e se eu for patch por patch, preciso esperar até quase o final para ter bastante dados para analisar |
| 5 | **Volume alvo de partidas** (ex: 3.000 partidas) | 5.000 partidas | Acredito que essa é uma boa faixa de partidas, não são muitas partidas a ponto de ficar inviavel o tempo de espera e correr risco de perder tudo, e o suficiente pra ter uma boa média |
| 6 | **Grão (unidade de análise)** — cada linha da tabela final representa o quê? | 1 linha = 1 jogador em 1 partida | Quero trabalhar com muitas informaçoes da API |

**Sobre a decisão 6 (grão), as opções são:**

- `1 linha = 1 partida` → 3.000 partidas = 3.000 linhas
- `1 linha = 1 time em 1 partida` → 3.000 partidas = 6.000 linhas
- `1 linha = 1 jogador em 1 partida` → 3.000 partidas = 30.000 linhas

Dica: você provavelmente vai precisar de **mais de um** grão. Isso é normal e vira
mais de uma tabela no banco.

### 1.3 Fora do escopo (o que NÃO vamos fazer)

> **Definição:** "fora do escopo" NÃO é o que os dados impedem de responder.
> É o que você **conseguiria** responder e escolheu **não** responder.
> Se fosse impossível, não precisava estar escrito aqui.

**Teste do "quase entrou":** se o item nunca passou pela sua cabeça como
possibilidade real, ele é ruído. `Não vamos analisar Valorant` é inútil.
`Não vamos responder qual a melhor build por campeão` é útil — porque você
realmente pensou nisso.

#### As 4 categorias (use como cardápio, escolha 3 a 5 itens)

**A. Perguntas adjacentes — daria outro projeto**
São perguntas legítimas, respondíveis com os mesmos dados, mas que respondem
a *outra* coisa que não "o que faz ganhar".
- Ex: tier list de campeões por rota · melhor build/itemização · pathing de jungler
· composições de time · análise de bans e draft

**B. Métodos que não vamos usar**
Delimita a profundidade técnica.
- Ex: modelo preditivo de machine learning · inferência causal (só vamos medir
associação, não causa) · análise minuto a minuto da timeline · análise de séries
temporais entre patches

**C. Populações não cobertas**
É o espelho negativo da sua seção 1.2 — cada escolha ali exclui algo aqui.
- Ex: outras regiões · outras filas (Flex, ARAM, normal) · outros patches ·
cenário profissional/competitivo

**D. Entregáveis que não vamos produzir**
Delimita o esforço de engenharia.
- Ex: pipeline automatizado/agendado · dashboard em tempo real · API própria ·
deploy em nuvem · testes automatizados

#### Sua lista

Formato: **o que não vamos fazer** + **por quê** + (opcional) *"fica como trabalho futuro"*.

1. Não iremos análisar outras filas além de rankeada Solo/Duo, pois estas filas são mais casuais e não remetem o que realmente é viavel para ganhar
2. Não vamos análisar a composição do time, somente o que é feito na partida para alcançar a vitoria 
3. Não vamos fazer analise de serie temporal entre patches, pois deixaria o projeto muito complexo pra mim que precisa terminar rapido o projeto
4. Não será análisado picks e bans durante a champion select, quero analisar somente o que acontece durante a partida
5. não sera avaliado o pathing do jungle, é algo muito especifico para a pergunta principal, daria pra fazer outro projeto só pra essa lane
6. Não vamos produzir tier list de campeões nem análise de builds/itemização. São perguntas de *meta report* ("o que as pessoas jogam"), e não de fator de vitória ("o que faz ganhar") — dariam um segundo projeto. *Fica como trabalho futuro.*

### 1.4 Critério de sucesso

> "Este projeto estará concluído quando eu conseguir mostrar, com dados, os
> **8 a 10** fatores mais associados à vitória em partidas de alto elo do BR1,
> e explicar cada um deles em **um dashboard no Power BI, apoiado por um README
> no GitHub**."

#### Critérios de aceite

Um critério de sucesso só serve se for **verificável** — se der para responder
sim ou não olhando o projeto. "Fazer um bom dashboard" não é critério, é desejo.

| # | Critério | Como verificar |
|---|----------|----------------|
| 1 | Pipeline reprodutível | Alguém clona o repositório, cria o `.env`, roda os scripts na ordem e chega no mesmo banco |
| 2 | Volume mínimo de dados | ≥ 5.000 partidas **distintas** (deduplicadas por `matchId`) carregadas no PostgreSQL |
| 3 | Toda pergunta tem resposta | Cada pergunta de negócio da Etapa 2 tem uma query em `sql/` que a responde |
| 4 | Todo visual tem pergunta | Cada gráfico do dashboard rastreia até uma pergunta de negócio — nenhum gráfico "decorativo" |
| 5 | Ranking de fatores entregue | Existe um visual que ordena os fatores por força de associação com a vitória |
| 6 | Limitações comunicadas | O README traz a seção 1.5 deste documento, em especial a limitação de causalidade |
| 7 | Nenhum segredo versionado | `git log -p` não contém chave da Riot nem senha do banco em nenhum commit |
| 8 | README completo | Contém: problema, escopo, stack, como rodar, resultados, limitações, trabalho futuro |

#### Fora do critério de sucesso (para não se cobrar demais)

- O dashboard não precisa ser bonito de agência — precisa ser **legível e honesto**
- Os achados não precisam ser surpreendentes; confirmar o senso comum **com dados**
  também é resultado válido
- O projeto não precisa provar causalidade (ver L1 na seção 1.5)

### 1.5 Limitações conhecidas (preencher agora, usar no README depois)

Analista sênior escreve as limitações **antes** de coletar, não depois.

> **Formato obrigatório:** `FATO` (o que é verdade sobre os dados) → `CONSEQUÊNCIA`
> (por que a conclusão pode estar errada por causa disso).
> Se a frase não tem as duas partes, é **escopo**, não limitação.

**L1 — Associação, não causalidade**
A análise usa dados observacionais: as partidas simplesmente aconteceram, não houve
experimento controlado. **Portanto**, quando um fator aparecer associado à vitória,
não é possível afirmar que ele *causa* a vitória. Um time que pega o primeiro dragão
vence mais, mas pegar o dragão pode ser *sintoma* de uma vantagem que já existia
(prioridade de rota, vantagem de ouro) e não a causa dela. Todo resultado deve ser
lido como "acontece junto com", não como "faz acontecer".

**L2 — Recorte de elo**
A amostra contém apenas Mestre, Grão-Mestre e Desafiante, uma fração mínima e
atípica da base de jogadores. **Portanto**, os fatores identificados descrevem o
que decide partidas entre jogadores de execução consistente. Não se pode afirmar
que valem para elos baixos, onde a variância de erro individual é maior e pode
sobrepor qualquer fator estratégico.

**L3 — Recorte de região**
Toda a amostra vem do BR1. **Portanto**, os resultados carregam as particularidades
do meta e do estilo de jogo brasileiros, e podem não se reproduzir em regiões com
cultura de jogo diferente (ex.: KR, EUW).

**L4 — Viés de atividade**
As partidas vêm do histórico de jogadores ativos na janela de 30 dias, e quem joga
mais contribui com mais partidas. **Portanto**, a amostra é dominada por jogadores
de alto volume. Se o comportamento deles difere do jogador ocasional de alto elo,
as médias ficam puxadas na direção deles.

**L5 — Elo é uma foto do momento da coleta**
O tier de cada jogador é lido no dia da coleta, mas as partidas são de até 30 dias
antes. **Portanto**, partidas jogadas quando a pessoa ainda era Diamante aparecem
rotuladas como Mestre, contaminando levemente o recorte de elo.

**L6 — As observações não são independentes**
O pool de alto elo do BR1 é pequeno, então os mesmos jogadores aparecem em muitas
partidas (e a mesma partida chega por vários jogadores, exigindo deduplicação por
`matchId`). **Portanto**, mesmo após deduplicar, as partidas não são eventos
independentes: um punhado de *one-tricks* ou de duos frequentes pode influenciar
desproporcionalmente os números de um campeão ou de uma estratégia.

#### Mitigação — preencher (vira "Trabalho futuro" no README)

Para cada limitação, o que você faria se tivesse tempo e recursos ilimitados?

| Limitação | Como mitigaria |
|---|---|
| **L1 — causalidade** | O ideal (experimento aleatorizado) é impossível: não dá para sortear quais times pegam o dragão. O caminho viável é **controlar por confundidores** — comparar apenas partidas que estavam equilibradas no momento do objetivo (ex.: diferença de ouro aos 10 min abaixo de 500) e verificar se o fator ainda prevê vitória. Se o efeito some, era sintoma; se resiste, é candidato a causa. Com os dados de *timeline* da API dá para checar também a **ordem temporal**: a vantagem veio antes ou depois do objetivo? |
| **L2 — elo** | Coletar uma amostra paralela de 2 ou 3 faixas distantes (ex.: Prata e Esmeralda), via endpoint `league-v4/entries`, e repetir a mesma análise. Fatores que se mantêm em todos os elos são propriedades do jogo; fatores que invertem são propriedades do nível de habilidade. |
| **L3 — região** | Replicar a coleta em KR e EUW e comparar os rankings de fatores. Um fator que aparece nas três regiões é do jogo; um que só aparece no BR é do meta local. Custo baixo: o script de coleta já é parametrizado por região no `.env`. |
| **L4 — atividade** | Impor um **teto de partidas por jogador** (ex.: no máximo 15 por jogador na amostra final), achatando a contribuição de quem joga 300 partidas por mês. Alternativa mais sofisticada: ponderar cada partida pelo inverso do total de partidas daquele jogador. |
| **L5 — snapshot de elo** | Encurtar a janela de coleta (7 a 14 dias em vez de 30) reduz a chance de o jogador ter mudado de tier dentro do período. A solução real exige histórico de elo, que a API não fornece retroativamente — logo, a mitigação estrutural é **coletar snapshots periódicos ao longo do tempo** e construir esse histórico para projetos futuros. |
| **L6 — independência** | Deduplicar por `matchId` é obrigatório e não opcional. Além disso: aplicar o mesmo teto de partidas por jogador da L4, e **sempre reportar o número de jogadores distintos ao lado do número de partidas**. Um campeão com 90% de winrate em 40 partidas jogadas por 2 pessoas é uma informação muito diferente de 40 partidas jogadas por 35 pessoas. |

---

## 2. Estrutura de pastas a criar

```
projeto-lol/
├── data/
│   ├── raw/            # dado bruto da API — NUNCA editar, NUNCA versionar
│   ├── interim/        # dado meio-tratado (checkpoints)
│   └── processed/      # dado final, pronto pro banco
├── notebooks/          # exploração (bagunça permitida)
├── src/                # código de produção (limpo, reutilizável)
│   ├── collect/        # coleta da API
│   ├── transform/      # limpeza e feature engineering
│   └── load/           # carga no PostgreSQL
├── sql/                # DDL (criação de tabelas) e queries analíticas
├── powerbi/            # arquivo .pbix
├── docs/               # documentação e este charter
├── .env                # SEGREDOS (API key, senha do banco) — não versionar
├── .env.example        # modelo do .env, sem valores reais — versionar
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 3. Checklist da Etapa 1

- [ ] Estrutura de pastas criada
- [ ] Ambiente virtual criado e ativado
- [ ] Pacotes instalados (`pandas`, `requests`, `python-dotenv`, `sqlalchemy`, `psycopg2-binary`, `jupyter`)
- [ ] `requirements.txt` gerado
- [ ] `.gitignore` criado (com `.env`, `data/raw/`, `venv/`)
- [ ] `.env.example` criado
- [ ] Seções 1.2 a 1.5 deste documento preenchidas

---

## 4. Comandos de referência (Windows / PowerShell)

```powershell
# Criar as pastas
cd C:\Users\Admin\Desktop\projeto-lol
mkdir data\raw, data\interim, data\processed, notebooks, src\collect, src\transform, src\load, sql, powerbi

# Criar e ativar o ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# Se der erro de política de execução, rode uma vez:
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# Instalar pacotes (com o venv ATIVO — o prompt mostra "(venv)")
pip install pandas requests python-dotenv sqlalchemy psycopg2-binary jupyter

# Congelar as versões
pip freeze > requirements.txt
```

---

## 5. O que me enviar ao terminar

1. A saída de `pip list` (ou o conteúdo do `requirements.txt`)
2. O conteúdo do seu `.gitignore`
3. Este documento com as seções 1.2 a 1.5 preenchidas
