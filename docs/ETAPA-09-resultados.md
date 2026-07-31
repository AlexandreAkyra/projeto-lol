# Etapa 9 — Resultados

**Base:** 4.741 partidas ranqueadas solo/duo de alto elo (Mestre, Grão-Mestre e
Desafiante) do servidor BR1, patches 26.13 e 26.14, coletadas em 29/07/2026.

---

## O resultado principal (PN06)

**Ranking dos fatores por taxa de vitória de quem conquistou o objetivo:**

| # | Fator | Vence | Times que conquistaram |
|---|---|---|---|
| 1 | **Alma do dragão** | **88,0%** | 1.230 |
| 2 | Primeiro Barão | 80,6% | 3.599 |
| 3 | Primeira torre | 69,7% | 4.693 |
| 4 | Arauto | 66,9% | 3.973 |
| 4 | Vantagem de visão | 66,9% | 4.659 |
| 6 | Primeiro dragão | 61,3% | 4.712 |
| 7 | First blood | 56,7% | 4.740 |
| 8 | Larvas do Vazio | 55,6% | 4.716 |

### Por que esta métrica, e não a diferença entre "com" e "sem"

A consulta original também calculava a diferença entre a taxa de vitória de quem
teve o fator e de quem não teve. **Essa medida está contaminada** e produz um
ranking diferente (Barão em 1º, alma em 2º).

O motivo: quando **nenhum** dos times conquista o objetivo, os dois entram no
grupo "sem" — e naquela partida um vence e o outro perde, sempre 50/50. Quanto
mais raro o objetivo, mais o grupo "sem" é inflado por essas partidas neutras, e
mais a diferença encolhe artificialmente.

| Fator | Partidas em que ocorreu | Partidas sem o objetivo |
|---|---|---|
| First blood | 4.740 (100%) | 1 |
| Primeira torre | 4.693 (99%) | 48 |
| Primeiro Barão | 3.599 (76%) | 1.142 |
| **Alma do dragão** | **1.230 (26%)** | **3.511** |

A alma é rara: 74% das partidas não tiveram alma nenhuma, e todos aqueles times
entraram no grupo "sem" com 50% de vitória garantida.

**Prova:** para objetivos que quase sempre ocorrem, as duas medidas coincidem
exatamente. A discrepância cresce na proporção da raridade.

| Fator | Diferença esperada | Diferença medida | Discrepância | % sem o objetivo |
|---|---|---|---|---|
| Larvas | 11,2 | 11,2 | 0,0 | 1% |
| Primeira torre | 39,4 | 39,0 | 0,4 | 1% |
| Primeiro Barão | 61,2 | 49,4 | 11,8 | 24% |
| Alma do dragão | 76,0 | 43,6 | 32,4 | 74% |

Por isso o ranking usa a taxa de vitória de quem conquistou — ela compara, dentro
da mesma partida, quem pegou contra quem não pegou, sem partidas neutras na conta.

---

## Respostas por pergunta

| Pergunta | Resultado |
|---|---|
| **PN01** — Primeiro Barão | 80,6% (3.599 times) |
| **PN02** — Ouro aos 15 min | ❌ não respondida (exige endpoint de timeline) |
| **PN03** — Primeira torre | 69,7% (4.693 times) |
| **PN04** — Vantagem de visão | 66,9% (4.659 partidas) |
| **PN05** — First blood | 56,7% (4.740 times) |
| **PN06** — Ranking consolidado | ver tabela acima |
| **PN07** — Farm vs abates | ❌ não respondida (trabalho futuro) |
| **PN08** — Duração | curta 1.389 · média 2.757 · longa 595 |

---

## Hipóteses vs realidade

Todas as hipóteses foram registradas **antes** de qualquer dado ser analisado.

| Fator | Previsto | Real | Direção do erro |
|---|---|---|---|
| Primeiro Barão | 70–79% | 80,6% | subestimou |
| Primeira torre | 59–65% | 69,7% | subestimou |
| First blood | 51–55% | 56,7% | subestimou |
| **Visão** | **70–78%** | **66,9%** | **superestimou** |

**Ordem prevista para o PN06:**
alma > barão > torre > dragão > arauto > first blood

**Ordem real:**
alma > barão > torre > **arauto > dragão** > first blood

Uma única troca, entre dois fatores separados por 5,6 pontos.

### O que isso revela

**A ordem estava certa; as magnitudes, não.** A intuição de quem joga acerta o
ranking relativo dos fatores, mas erra o tamanho do efeito.

**E erra em direções opostas dependendo do tipo de fator.** Objetivos concretos
(Barão, torre, first blood) foram subestimados nos três casos. A vantagem difusa
(visão) foi superestimada.

Hipótese para explicar: objetivos concretos são eventos pontuais e anunciados
pelo jogo — fáceis de lembrar, difíceis de dimensionar. Visão é o acúmulo
invisível de centenas de sentinelas, e a comunidade compensa isso com um discurso
que exagera sua importância.

---

## Limitações destes resultados

**Associação, não causalidade.** Nenhum número aqui prova que o fator *causa* a
vitória. A alma do dragão exige vencer quatro disputas de objetivo ao longo de
20+ minutos — os 88% descrevem times que já vinham dominando, não uma receita
para virar partida perdida.

O caso da visão é o mais explícito: time que está ganhando morre menos, controla
mais mapa e por isso wardeia mais. Parte dos 66,9% é a vitória causando a visão,
não o contrário.

**Recorte de elo e região.** Só Mestre+ do BR1. Não se pode afirmar que valha
para elos baixos nem para outras regiões.

**Dois patches misturados.** A amostra cobre 26.13 (46%) e 26.14 (53%).

**Observações não independentes.** Os 600 jogadores semente são 3,6% dos
jogadores da amostra, mas aparecem em 13,3% das linhas — sobre-representação de
cerca de 3,8x, inerente ao método de coleta por histórico.

---

## Trabalho futuro

- **PN02** — exige o endpoint de *timeline* da Riot, que dobraria o custo de
  coleta. Foi planejado na Etapa 3 e não executado.
- **PN07** — comparar farm e abates exige agregar jogadores por time excluindo o
  suporte e normalizar duas métricas em escalas diferentes.
- **Controle de confundidores** — restringir a análise a partidas equilibradas no
  momento do objetivo (ex.: diferença de ouro abaixo de 500 aos 10 min) para
  separar efeito de sintoma.
- **Comparação entre elos** — repetir a análise em Prata e Esmeralda para
  identificar quais fatores são propriedades do jogo e quais são do nível de
  habilidade.
