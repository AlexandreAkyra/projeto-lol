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
| **PN09** — Top 3 campeões por winrate | ver seção "Campeões" |
| **PN10** — Campeões mais escolhidos | ver seção "Campeões" |
| **PN11** — Alavancagem por rota | jungle lidera (3,32x) |

---

## O peso dos objetivos muda com a duração (PN08 detalhado)

Taxa de vitória de quem conquistou cada objetivo, quebrada por faixa de duração:

| Fator | Curta (<25 min) | Média (25–35) | Longa (>35) |
|---|---|---|---|
| Alma do dragão | **100,0%** (62) | 92,2% (822) | 75,7% (346) |
| Primeiro Barão | **98,5%** (473) | 82,8% (2.534) | 57,3% (592) |
| Primeira torre | 86,4% (1.341) | 65,6% (2.757) | 50,9% (595) |
| First blood | 63,4% (1.389) | 54,8% (2.757) | 49,5% (594) |

**Todo fator perde força conforme a partida se alonga.** O first blood, que vale
56,7% no geral, vira 49,5% em partidas longas — ou seja, **nada**. Em jogo de 40
minutos, quem matou primeiro aos 3 minutos tem exatamente a mesma chance que o
adversário.

### Os 100% são uma armadilha, não um troféu

A alma do dragão em partidas curtas venceu 62 de 62. Taxa de vitória de 100%.

Esse número não diz que a alma é imbatível — diz que **a seta da causalidade está
invertida**. A alma exige quatro dragões, e o quarto dragão raramente sai antes
dos 25 minutos. Fechar isso numa partida curta só acontece quando um time está
atropelando; a alma é o *sintoma* do atropelo, não a causa.

O mesmo vale para o Barão em partidas curtas (98,5%): ele nasce aos 20 minutos, e
partida "curta" acaba antes dos 25. Pegar Barão nessa janela significa pegá-lo e
encerrar em seguida.

> **Regra prática:** taxa de vitória de 100% quase nunca é um achado. É um aviso
> de que a variável está medindo o resultado, não prevendo ele.

---

## Campeões (PN09 e PN10)

### Top 3 por taxa de vitória em cada rota — mínimo 100 partidas

| Rota | 1º | 2º | 3º |
|---|---|---|---|
| TOP | Riven 58,6% (251) | Quinn 57,3% (110) | Zaahen 57,1% (126) |
| JUNGLE | XinZhao 56,4% (140) | Qiyana 53,7% (203) | Karthus 53,6% (125) |
| MIDDLE | Ekko 54,4% (125) | Malzahar 54,3% (173) | Lux 53,7% (311) |
| BOTTOM | Samira 59,1% (186) | Hwei 58,9% (158) | Viktor 57,8% (109) |
| UTILITY | Leona 57,2% (250) | Janna 55,4% (316) | Sona 53,8% (573) |

O corte de 100 partidas não foi restritivo: entre **25 e 39 campeões por rota**
passaram por ele. O ranking teve pool de sobra.

### Top 3 mais escolhidos em cada rota

| Rota | 1º | 2º | 3º |
|---|---|---|---|
| TOP | Gangplank 418 (43,8%) | Jax 342 (56,1%) | Malphite 318 (50,0%) |
| JUNGLE | LeeSin 626 (51,8%) | Kayn 481 (49,9%) | Viego 395 (50,9%) |
| MIDDLE | Zed 473 (49,7%) | Ahri 458 (47,6%) | Locke 442 (50,2%) |
| BOTTOM | Ezreal 599 (46,6%) | Caitlyn 546 (48,5%) | Jhin 510 (52,2%) |
| UTILITY | Nami 664 (44,6%) | Seraphine 623 (51,5%) | Sona 573 (53,8%) |

### O achado: popular não é o mesmo que forte

Confrontando as duas listas:

| | Mais escolhidos | Maior winrate |
|---|---|---|
| Taxa de vitória média | **49,8%** | **56,1%** |
| Partidas (mediana) | 473 | 165 |

**Os quinze campeões mais escolhidos têm winrate médio de 49,8% — praticamente o
acaso.** Enquanto isso, os quinze de maior winrate ficam em 56,1%, e são
escolhidos cerca de três vezes menos.

Só um campeão aparece nas duas listas: Sona.

Três explicações plausíveis, nenhuma testada aqui:

1. **Simetria.** Campeão muito jogado é também muito enfrentado. Todo mundo
   conhece o Ezreal, sabe o alcance dele, sabe quando ele tem Arcane Shift.
2. **Seleção de quem escolhe.** Campeão de nicho é escolhido por especialista;
   campeão popular é escolhido por todo mundo, inclusive por quem está
   experimentando.
3. **Motivo da escolha.** As pessoas escolhem por diversão, conforto e segurança
   de banimento — não por taxa de vitória.

### Ressalvas desta seção

**A ordem dentro do top 3 não é significativa.** Com 100 a 250 partidas, a margem
de erro de uma proporção é de aproximadamente ±7 a ±10 pontos percentuais. Samira
(59,1%) e Hwei (58,9%) estão separados por 0,2 ponto — isso é ruído. O que a
tabela sustenta é que esses campeões estão **acima de 50%**, não a ordem entre eles.

**Winrate não é força bruta do campeão.** Ela mistura o campeão com quem o
escolhe. Um campeão difícil, jogado só por especialistas, mostra winrate alto sem
ser "melhor".

**Recorte fixo.** Vale para Mestre+ do BR1 nos patches 26.13–26.14. Meta de
campeão muda a cada patch — esta tabela tem prazo de validade curto, ao contrário
do ranking de objetivos.

---

## Alavancagem individual por rota (PN11)

A pergunta "qual rota vence mais?" não tem resposta: toda partida tem um jogador
de cada rota nos dois times, então a taxa de vitória de qualquer rota é exatamente
50%. Sempre. Isso não é limitação da amostra — é aritmética.

A reformulação que tem resposta: **em qual rota o desempenho individual mais
separa quem venceu de quem perdeu?**

| Rota | KDA vencedor | KDA perdedor | Razão | Vantagem de ouro/min |
|---|---|---|---|---|
| **JUNGLE** | 6,32 | 1,91 | **3,32x** | 18,3% |
| MIDDLE | 4,87 | 1,63 | 2,99x | 16,7% |
| TOP | 3,91 | 1,34 | 2,92x | 18,1% |
| UTILITY | 5,87 | 2,14 | 2,74x | 14,0% |
| BOTTOM | 4,57 | 1,69 | 2,70x | 17,4% |

A selva é a rota onde o KDA mais discrimina vitória de derrota, e a única acima de
3x. Bottom é a menor.

**A ressalva é grande aqui.** Vencer *produz* KDA: time que ganha mata mais e
morre menos, por definição. A razão alta em todas as rotas (nenhuma abaixo de
2,7x) reflete principalmente isso, não influência individual.

O que **é** interpretável é a **comparação relativa entre rotas**, já que o viés
afeta as cinco igualmente. E parte do resultado da selva é estrutural: o jungler
circula pelo mapa e acumula assistências nas cinco rotas, o que infla o KDA em
partida ganha mais do que numa rota fixa.

Conclusão honesta: isto **sugere** que a selva é a rota com mais alavancagem
individual, mas não é prova. Uma resposta rigorosa exigiria comparar o mesmo
jogador em rotas diferentes ou medir vantagem antes do desfecho (ouro aos 15 min,
que é justamente o PN02 não respondido).

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
