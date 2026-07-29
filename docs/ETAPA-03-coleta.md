# Etapa 3 — Coleta de Dados (Riot API)

Documento de referência. Vamos construir o coletor em partes, testando cada uma.

---

## 1. O que é uma API

Quando você abre `op.gg` no navegador, o servidor te devolve uma **página** —
HTML, com cores, botões e imagens, feita para humano ler.

Uma **API** é a mesma ideia, mas o servidor devolve **dados puros** em vez de
página. Sem cor, sem botão: só a informação, num formato que programa consegue
ler (JSON).

A Riot API é um conjunto de URLs. Você acessa a URL certa, ela devolve JSON.
É literalmente isso.

---

## 2. Autenticação

Toda requisição precisa provar quem você é. A chave vai num **cabeçalho**
(*header*) chamado `X-Riot-Token`:

```python
headers = {"X-Riot-Token": "RGAPI-sua-chave-aqui"}
requests.get(url, headers=headers)
```

**Por que no header e não na URL?** URLs aparecem em logs de servidor, no
histórico do navegador, em mensagens de erro. Header é bem menos exposto. Colocar
segredo em URL é um erro clássico de segurança.

---

## 3. Códigos de status que importam

Toda resposta HTTP vem com um número. Os que você vai encontrar:

| Código | Significa | O que fazer |
|---|---|---|
| **200** | deu certo | seguir |
| **403** | chave inválida ou **expirada** | gerar chave nova no portal |
| **404** | não encontrado | jogador/partida não existe — pular e seguir |
| **429** | **estourou o limite** de requisições | esperar e tentar de novo |
| **5xx** | erro do lado da Riot | esperar e tentar de novo |

O **429** é o que mais vai aparecer, e tratá-lo bem é metade do trabalho de um
coletor. A resposta traz um header `Retry-After` dizendo quantos segundos esperar.

---

## 4. Os dois roteamentos (erro nº 1 de iniciante)

A Riot tem dois tipos de endereço, e usar o errado dá 404:

| Tipo | Domínio | Usado por |
|---|---|---|
| **Plataforma** | `br1.api.riotgames.com` | league-v4, summoner-v4 — contas e ranking |
| **Regional** | `americas.api.riotgames.com` | match-v5, account-v1 — partidas |

Regra prática: **coisas de jogador → `br1`. Coisas de partida → `americas`.**

Os dois já estão no seu `.env` como `RIOT_PLATFORM` e `RIOT_REGION`.

---

## 5. A cadeia de coleta — o mapa

Você não consegue pedir "me dá 5.000 partidas de alto elo do BR". Precisa
percorrer uma cadeia:

```
PASSO 1 — Quem são os jogadores de alto elo?
  GET br1.../lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5
  GET br1.../lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5
  GET br1.../lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5
  → 3 chamadas, devolvem a lista inteira de jogadores de cada tier

PASSO 2 — Quais partidas cada jogador jogou?
  GET americas.../lol/match/v5/matches/by-puuid/{puuid}/ids
      ?queue=420&startTime={epoch}&endTime={epoch}&start=0&count=100
  → 1 ou mais chamadas por jogador; devolve só os IDs

PASSO 3 — O que aconteceu em cada partida?
  GET americas.../lol/match/v5/matches/{matchId}
  → 1 chamada por partida  ← aqui está o grosso do custo

PASSO 4 — Evolução minuto a minuto (só subamostra ~1.500)
  GET americas.../lol/match/v5/matches/{matchId}/timeline
  → 1 chamada por partida da subamostra
```

Entre o passo 2 e o 3 entra a **deduplicação**: vários jogadores do seu pool
jogaram a mesma partida, e o mesmo `matchId` vai aparecer repetido. Coletar
duplicado é desperdiçar chamada.

---

## 6. Limites da chave de desenvolvimento

- **20 requisições por segundo**
- **100 requisições a cada 2 minutos** ← este é o que manda
- **A chave expira em 24 horas**

O segundo limite dá ~50 req/min, ou ~3.000 req/hora. Faça a conta do seu projeto
antes de rodar, e escreva o coletor para ser **retomável** — se cair, continua de
onde parou em vez de recomeçar.

---

## 7. Regra de ouro: inspecione antes de parsear

Documentação de API fica desatualizada. A Riot já mudou campos de lugar mais de
uma vez (por exemplo, a migração de `summonerId` para `puuid`).

**Nunca escreva o código que lê a resposta antes de ter olhado uma resposta real.**

O fluxo correto é sempre:

1. Fazer **uma** chamada
2. Imprimir o JSON e olhar com os próprios olhos
3. Só então escrever o código que extrai os campos

Iniciante faz o contrário: escreve 200 linhas baseado em tutorial de 2021, roda,
toma `KeyError`, e não entende por quê.

---

## 8. Tarefa 3.1 — sua primeira chamada

Arquivo: `src/collect/teste_api.py`

Objetivo: fazer **uma** chamada e descobrir o que ela devolve. Nada mais.
Sem laço, sem salvar arquivo, sem tratar erro.

O esqueleto está no arquivo com 5 `TODO`. Ao terminar, me mande:

1. O status code que você recebeu
2. As chaves do topo da resposta
3. Quantos jogadores vieram
4. **Um jogador inteiro impresso** — é isso que vai definir o passo 2 da cadeia

> A pergunta que essa tarefa responde: **os jogadores vêm com `puuid` direto, ou
> só com `summonerId`?** Se vier `puuid`, seguimos direto para o passo 2. Se vier
> só `summonerId`, cada jogador vai exigir uma chamada extra de conversão — o que
> muda bastante a conta de custo da coleta.
