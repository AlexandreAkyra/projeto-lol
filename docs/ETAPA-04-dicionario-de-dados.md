# Etapa 4 — Dicionário de Dados

Mapa entre as perguntas de negócio (Etapa 2) e os campos reais do JSON da Riot.

**Fonte:** `data/raw/partidas.jsonl` — 5.000 partidas, ranqueada solo/duo (queue 420),
BR1, coletadas em 29/07/2026.

---

## 1. Perfil da coleta

| Característica | Valor |
|---|---|
| Partidas | 5.000 |
| `queueId` | 420 em 100% |
| `endOfGameResult` | `GameComplete` em 100% |
| Duração mín / mediana / máx | 65 s / 27,8 min / 56,5 min |
| Partidas com < 5 min (remakes) | 222 (4,4%) |
| Campos por partida | 16 em `info` + 155 × 10 jogadores + 2 times |

### Distribuição por patch

| `gameVersion` | Patch divulgado | Partidas | % |
|---|---|---|---|
| 16.13 | 26.13 | 2.305 | 46,1% |
| 16.14 | 26.14 | 2.655 | 53,1% |
| 16.15 | 26.15 | 40 | 0,8% |

> ⚠️ A numeração interna (`gameVersion`) **não** é a numeração de divulgação.
> `16.14` = patch 26.14. Registrar isso no README para não confundir quem ler.

---

## 2. Estrutura do JSON

```
partida
├── metadata
│   ├── dataVersion
│   ├── matchId              ← chave primária da partida
│   └── participants[]       ← lista de puuids
└── info
    ├── gameCreation / gameStartTimestamp / gameEndTimestamp
    ├── gameDuration         ← em segundos
    ├── gameVersion          ← patch (numeração interna)
    ├── queueId              ← 420 = ranked solo/duo
    ├── mapId / gameMode / gameType / platformId
    ├── endOfGameResult
    ├── teams[]  (2 itens)
    │   ├── teamId           ← 100 = azul, 200 = vermelho
    │   ├── win              ← booleano
    │   ├── bans[]
    │   └── objectives
    │       ├── champion     ← FIRST BLOOD mora aqui
    │       ├── tower / inhibitor
    │       ├── baron / dragon / riftHerald
    │       └── horde (larvas) / atakhan
    └── participants[] (10 itens, 155 campos cada)
```

Cada objetivo tem o mesmo formato: `{"first": bool, "kills": int}`.

---

## 3. Mapa: pergunta → campo

**Nível** indica de onde o dado vem: `partida`, `time` ou `jogador`.

| PN | O que preciso medir | Caminho no JSON | Nível |
|----|---------------------|-----------------|-------|
| PN01 | Primeiro Barão | `info.teams[].objectives.baron.first` | time |
| PN01 | Vitória do time | `info.teams[].win` | time |
| PN03 | Primeira torre | `info.teams[].objectives.tower.first` | time |
| PN05 | First blood | `info.teams[].objectives.champion.first` | time |
| PN06 | Primeiro dragão | `info.teams[].objectives.dragon.first` | time |
| PN06 | Arauto | `info.teams[].objectives.riftHerald.first` | time |
| PN06 | Alma do dragão | ⚠️ **não existe** — derivar de `dragon.kills >= 4` | time |
| PN08 | Duração da partida | `info.gameDuration` (segundos) | partida |
| — | Identificador da partida | `metadata.matchId` | partida |
| — | Patch | `info.gameVersion` | partida |

### Nível do jogador

| PN | O que preciso medir | Caminho no JSON | Nível |
|----|---------------------|-----------------|-------|
| PN04 | Vision score | `info.participants[].visionScore` | jogador → somar por time |
| PN07 | CS (tropas de rota) | `info.participants[].totalMinionsKilled` | jogador |
| PN07 | CS (selva) | `info.participants[].neutralMinionsKilled` | jogador |
| PN07 | Abates do time | `info.teams[].objectives.champion.kills` | **time** |
| — | Rota do jogador | `info.participants[].teamPosition` | jogador |
| — | Campeão | `info.participants[].championName` | jogador |
| — | Ouro do jogador | `info.participants[].goldEarned` | jogador |
| — | Time do jogador | `info.participants[].teamId` (100 = azul, 200 = vermelho) | jogador |
| — | Vitória do jogador | `info.participants[].win` | jogador |

> **Sobre `challenges.goldPerMinute`:** existe e está presente em 100% dos
> participantes, mas o objeto `challenges` não é documentado oficialmente pela Riot
> e seus campos mudam entre patches. Preferimos derivar de campos primitivos:
> `goldEarned ÷ (gameDuration / 60)`. Regra geral: **calcular a partir do dado
> bruto é mais estável do que confiar num campo derivado que você não controla.**

### Verificações de integridade (5.000 partidas)

| Verificação | Resultado |
|---|---|
| Participantes sem `challenges` | 0 |
| `championName` vazio | 0 |
| `teamPosition` vazio | **13** (0,026%) |
| `teamPosition` = TOP / JUNGLE | 10.000 cada (exatamente 2 por partida) |

---

## 4. Decisões de limpeza (Tarefa 4.2)

Cada uma vira uma regra de filtro na Etapa 5.

### D1 — Remakes (partidas curtas)

**Fato:** 222 partidas (4,4%) duram menos de 5 minutos. `endOfGameResult` diz
`GameComplete` mesmo assim, então esse campo não serve para identificá-las.

**Efeito se não filtrar:** entram como partidas legítimas com zero objetivos e
resultado quase sorteado, diluindo o efeito medido de todos os fatores.

- **Decisão:** `Filtrar` (filtrar / manter)
- **Regra exata:** `gameDuration >= 300` (ex: `gameDuration >= 300`)
- **Justificativa:** `Não faz sentido considerarmos remakes, um remake não é merito, é ocasionado por um erro técnico`

### D2 — Patch 26.15 (pós-reset de temporada)

**Fato:** 40 partidas (0,8%) são do patch seguinte, jogadas após o reset da
temporada.

- **Decisão:** `Filtrar` (filtrar / manter)
- **Justificativa:** `Como são tão poucos e são de uma nova reset de season, acredito que será melhor não considerarmos`

### D3 — Objetivos extras no ranking do PN06

**Fato:** `horde` (larvas do Vazio) e `atakhan` estão coletados e têm o mesmo
formato dos demais objetivos. Entrariam no ranking sem custo adicional.

- **Decisão:** incluir somente `horde`
- **Justificativa:** as larvas do Vazio são objetivo ativo e disputado; o atakhan
  foi removido do jogo, e o campo permanece na API apenas como resquício do esquema.

**Comprovação empírica (nas 5.000 partidas):**

| Objetivo | Times com `first` | Total de `kills` | Conclusão |
|---|---|---|---|
| `horde` | 4.753 | 14.233 | ativo e disputado |
| `atakhan` | **0** | **0** | campo morto |

> Zero ocorrências em 5.000 partidas e nos três patches. O campo existe no esquema,
> mas nunca traz dado. Se entrasse no ranking do PN06, produziria "0 pp de impacto"
> — um número que pareceria um achado e seria apenas um campo vazio.
>
> **Lição:** campo presente no esquema ≠ dado presente. Sempre confira a
> distribuição antes de incluir uma variável numa análise.

Observação: 5.000 − 4.753 = 247 partidas sem nenhum time pegando larvas. Muito
próximo das 222 partidas com menos de 5 minutos (D1) — ou seja, quase todas são
remakes. Duas verificações independentes apontando para a mesma sujeira.

### D4 — Jogadores sem posição definida

**Fato:** 13 participantes (de 50.000) têm `teamPosition` vazio.

**Efeito se não tratar:** aparecem como uma "rota" em branco em qualquer análise
por posição.

**Investigação (os 13 casos):**

| Campo alternativo | Resultado |
|---|---|
| `individualPosition` | `"Invalid"` nos 13 — **não resolve** |
| `lane` / `role` | `NONE`/`SUPPORT` em 11 casos; `BOTTOM`/`SUPPORT` em 2 |

**Interação com a D1:** os 13 estão em 13 partidas distintas, e **11 delas duram
menos de 5 minutos**. Ou seja, a regra D1 (filtrar remakes) já elimina 11 dos 13
casos antes de a D4 sequer ser aplicada.

Sobram **2 partidas** (`BR1_3259125288`, 24 min e `BR1_3265533780`, 23 min), ambas
com `lane = BOTTOM` e `role = SUPPORT` — recuperáveis como `UTILITY`.

- **Decisão:** descartar as 2 partidas restantes
- **Justificativa:** 2 partidas em ~4.778 (0,04%) não alteram nenhum resultado.
  Recuperar a posição via `lane` + `role` funcionaria, mas adicionaria um caminho
  de código especial para ganhar 0,04% de amostra. Descartar é mais simples de
  explicar e de auditar.
- **Regra:** descartar partidas em que algum participante tenha `teamPosition` vazio

> **Lição:** regras de limpeza não são independentes. Decidir a D4 isoladamente
> teria levado a construir tratamento para 13 casos, quando a D1 já resolvia 11.
> Aplique primeiro os filtros amplos e baratos, **depois** meça de novo o que sobrou.

---

## 5. Anotações para etapas futuras

- **Etapa 5 (limpeza):** aplicar as regras D1, D2 e D3
- **Etapa 6 (atributos):** criar `alma_do_dragao` = `dragon.kills >= 4`
- **Etapa 6 (atributos):** criar `cs_por_minuto` = (minions + monstros neutros) ÷ (duração em min)
- **Etapa 12 (README):** documentar a mistura de patches 26.13/26.14 e a
  divergência entre numeração interna e divulgada
