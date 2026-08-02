# Etapa 2 — Perguntas de Negócio

> Objetivo: quebrar a pergunta principal do charter em perguntas que o SQL
> consegue responder.

**Pergunta principal (charter, seção 1.1):**
Quais fatores mais influenciam a vitória em partidas ranqueadas de alto elo
(Mestre, Grão-Mestre e Desafiante) no servidor brasileiro?

---

## 1. Como escrever uma pergunta que presta

Toda pergunta precisa das três partes:

1. **Métrica** — o que vai ser medido
2. **População** — sobre quais partidas
3. **Comparação** — contra qual referência

E precisa passar em dois testes:

- **Teste do formato:** consigo desenhar a resposta antes de rodar a query?
- **Teste da decisão:** se a resposta for A em vez de B, algum jogador jogaria diferente?

---

## 2. Categorias de fatores (use para gerar ideias)

Cubra pelo menos 4 categorias. Isso evita escrever dez perguntas todas sobre abates.

| Categoria | Exemplos de fatores |
|---|---|
| **Objetivos neutros** | primeiro dragão, alma do dragão, arauto, primeiro Barão, Barões totais |
| **Estruturas** | primeira torre, placas, torres totais, inibidores |
| **Economia** | ouro total, diferença de ouro, CS por minuto, participação no ouro do time |
| **Combate** | first blood, abates totais, KDA, dano a campeões, participação em abates |
| **Visão** | sentinelas colocadas, sentinelas destruídas, sentinelas de controle, vision score |
| **Tempo** | duração da partida, momento do primeiro objetivo |
| **Snowball** | vantagem convertida — quem abriu vantagem cedo fechou a partida? |

---

## 3. Fonte de dados — atenção ao custo

A API tem dois endpoints diferentes por partida:

| Fonte | O que traz | Custo |
|---|---|---|
| `match` | estatísticas **finais** da partida (totais, resultado) | 1 chamada |
| `match + timeline` | evolução **minuto a minuto** (ouro aos 10 min, ordem dos eventos) | 2 chamadas |

Toda pergunta que fale em "aos X minutos" ou "quem chegou primeiro" precisa de
timeline — e **dobra o tempo de coleta**. Marque isso na tabela, porque essa
decisão define o script da Etapa 3.

---

## 4. Suas perguntas

> Preencha de 8 a 12 linhas. As duas primeiras são modelo — não apague, use como
> referência de nível de detalhe.

### PN01 — modelo preenchido

| Campo | Conteúdo |
|---|---|
| **Categoria** | Objetivos neutros |
| **Pergunta** | Times que garantem o primeiro Barão vencem com que frequência, comparado à média geral de 50%? |
| **Métrica** | Taxa de vitória (%) dos times que pegaram o primeiro Barão |
| **Comparação** | Contra 50% (baseline de qualquer partida) |
| **Fonte** | `match` |
| **Hipótese** | Entre **70% e 79%**. O buff é forte e costuma fechar a partida, mas o Barão vem tarde e normalmente quem pega já estava à frente — parte desse número é consequência da vantagem, não causa dela. |
| **Formato da resposta** | Um número único + a diferença em pontos percentuais |
| **Prioridade** | Alta |

### PN02 — modelo preenchido

| Campo | Conteúdo |
|---|---|
| **Categoria** | Economia |
| **Pergunta** | Como a taxa de vitória varia conforme a diferença de ouro do time aos 15 minutos? |
| **Métrica** | Taxa de vitória (%) por faixa de diferença de ouro (de -4000 a +4000, em faixas de 1000) |
| **Comparação** | Entre as faixas |
| **Fonte** | `match + timeline` ⚠️ dobra o custo de coleta |
| **Hipótese** | Relação crescente, provavelmente em S: até ~1000 de diferença muda pouco, acima de ~2500 a curva dispara. Em alto elo espero a curva mais íngreme que em elo baixo, porque a vantagem é melhor convertida. |
| **Formato da resposta** | Tabela de 2 colunas (faixa de ouro, winrate) → vira gráfico de linha |
| **Prioridade** | Alta |

---

> **Sobre as hipóteses:** as de **PN01, PN03, PN05 e PN06** foram registradas por
> mim em **29/07/2026**, antes de qualquer dado ser coletado. As de PN02, PN04,
> PN07 e PN08 seguem como rascunho e podem ser ajustadas até o início da coleta —
> depois disso, não valem mais.

### PN03

| Campo | Conteúdo |
|---|---|
| **Categoria** | Estruturas |
| **Pergunta** | Times que derrubam a primeira torre vencem com que frequência, comparado à média geral de 50%? |
| **Métrica** | Taxa de vitória (%) do time que derrubou a primeira torre |
| **Comparação** | Contra 50%, e contra o efeito do primeiro dragão |
| **Fonte** | `match` |
| **Hipótese** | Entre **59% e 65%**. Libera rotação e ouro para o time inteiro, mas em alto elo quem perde a torre sabe se reorganizar — a vantagem é real e menor do que costuma parecer. |
| **Formato da resposta** | Um número + diferença em pontos percentuais |
| **Prioridade** | Alta |

### PN04

| Campo | Conteúdo |
|---|---|
| **Categoria** | Visão |
| **Pergunta** | Times com mais visão vencem mais? E o efeito é grande comparado ao dos objetivos? |
| **Métrica** | **Principal:** taxa de vitória (%) do time com maior *vision score* na partida. **Secundária:** winrate por faixa de diferença de vision score (mostra se o efeito cresce com o tamanho da vantagem) |
| **Comparação** | Entre as faixas, e contra o tamanho do efeito dos objetivos (PN01, PN03) |
| **Fonte** | `match` |
| **Hipótese** | chuto entre 70% a 78%, visão em league of legends é absurdamente importante, e um time com mais visão pode criar mais estrategias, e tambem um time que está na frente, geralmente impede o outro de wardar o mapa, então acredito que isso influencia MUITO a taxa de vitoria |
| **Formato da resposta** | Tabela (faixa de vision score, winrate) → gráfico de linha |
| **Prioridade** | Alta |

### PN05

| Campo | Conteúdo |
|---|---|
| **Categoria** | Combate |
| **Pergunta** | *First blood* importa de verdade, ou o impacto é menor do que a comunidade acredita? |
| **Métrica** | Taxa de vitória (%) do time que fez o first blood |
| **Comparação** | Contra 50%, e contra todos os outros fatores do PN06 |
| **Fonte** | `match` |
| **Hipótese** | Entre **51% e 55%** — quase irrelevante. Em alto elo uma morte precoce se recupera com facilidade. Espero que seja o fator **mais fraco de toda a lista**. |
| **Formato da resposta** | Um número + diferença em pontos percentuais |
| **Prioridade** | Média |

### PN06 — ⭐ pergunta principal do dashboard

| Campo | Conteúdo |
|---|---|
| **Categoria** | Transversal (consolida todas) |
| **Pergunta** | Ordenando todos os fatores binários medidos, qual é o ranking de impacto na vitória? |
| **Métrica** | Para cada fator (primeiro Barão, alma do dragão, primeira torre, primeiro dragão, arauto, first blood): diferença em pontos percentuais entre a winrate de quem teve e de quem não teve |
| **Comparação** | Entre os fatores |
| **Fonte** | `match` |
| **Hipótese** | Ordem esperada: **alma do dragão > primeiro Barão > primeira torre > primeiro dragão > arauto > first blood**. A alma é bônus permanente e exige controle de mapa a partida inteira; o Barão é forte, mas temporário. Em números: alma e Barão acima de +20pp, primeira torre entre +9 e +15pp, first blood entre +1 e +5pp. *(As posições de primeiro dragão e arauto são inferidas — ajustar se discordar.)* |
| **Formato da resposta** | Ranking → gráfico de barras horizontal ordenado |
| **Prioridade** | Alta |

> Esta é a pergunta que responde diretamente a pergunta principal do charter, e o
> visual dela é a capa do dashboard. Atende ao critério de aceite nº 5 da seção 1.4.

### PN07

| Campo | Conteúdo |
|---|---|
| **Categoria** | Economia + Combate |
| **Pergunta** | O que separa mais o vencedor do perdedor: vantagem de farm (CS/min) ou vantagem de abates? |
| **Métrica** | Taxa de vitória (%) por faixa de diferença de CS/min **e** por faixa de diferença de abates, na mesma escala. **O CS considera apenas TOP, JUNGLE, MIDDLE e BOTTOM — o suporte (UTILITY) é excluído da conta.** |
| **Comparação** | Entre os dois fatores |
| **Fonte** | `match` |
| **Hipótese** *(rascunho)* | Abates devem mostrar associação mais forte, porque geram objetivos. Mas o CS deve ser o indicador mais "honesto": farm alto é causa de vantagem, enquanto abates são parcialmente consequência dela. |
| **Formato da resposta** | Duas curvas no mesmo gráfico, eixo X normalizado |
| **Prioridade** | Média |

> **Decisão: excluir o suporte da conta de CS.**
>
> Medição na amostra (CS por minuto, média por rota):
>
> | BOTTOM | MIDDLE | TOP | JUNGLE | **UTILITY** |
> |---|---|---|---|---|
> | 7,62 | 7,30 | 7,30 | 6,99 | **1,17** |
>
> As quatro primeiras rotas dependem de farm e ficam todas perto de 7. O suporte fica
> em 1,17 porque **não é função dele farmar** — ele cede as tropas para o atirador.
>
> Manter o suporte na conta não acrescenta informação sobre vantagem de farm; apenas
> puxa a média do time para baixo de forma igual dos dois lados, comprimindo a escala
> e aproximando os grupos que a análise quer separar.
>
> Portanto, o "CS do time" no PN07 é a soma de **4 jogadores**, não 5. Como a regra
> vale igualmente para os dois times, a comparação permanece justa.

### PN08

| Campo | Conteúdo |
|---|---|
| **Categoria** | Tempo |
| **Pergunta** | Os fatores de vitória mudam conforme a duração da partida? |
| **Métrica** | Efeito (diferença de winrate em pp) de cada fator do PN06, segmentado por faixa de duração: até 25 min, 25–35 min, acima de 35 min |
| **Comparação** | Do mesmo fator entre as faixas de duração |
| **Fonte** | `match` |
| **Hipótese** *(rascunho)* | First blood e primeira torre devem pesar bastante em partidas curtas e quase desaparecer nas longas. Barão e alma do dragão devem fazer o caminho inverso. Se confirmar, mostra que "o que faz ganhar" depende do tipo de partida. |
| **Formato da resposta** | Matriz fator × faixa de duração (heatmap) |
| **Prioridade** | Média |

---

## Perguntas acrescentadas em 01/08/2026

> Estas três entraram **depois** da análise, na revisão de escopo registrada no
> charter. Por isso **não têm hipótese** — uma previsão feita agora, com os dados
> já vistos, não valeria nada.

### PN09 — Top 3 campeões por taxa de vitória, por rota

| Campo | Conteúdo |
|---|---|
| **Métrica** | Taxa de vitória (%) por campeão e rota, **mínimo de 100 partidas** |
| **Por que o corte de 100** | Com 30 partidas a margem de erro é de ±14 pontos; com 100 cai para ±8. Um campeão com 80% em 30 jogos pode ter valor real entre 66% e 94% |
| **Formato** | Barras por rota, com a contagem de partidas visível |
| **View** | `vw_top_campeoes` |

### PN10 — Top 3 campeões mais escolhidos, por rota

| Campo | Conteúdo |
|---|---|
| **Métrica** | Contagem de partidas por campeão e rota |
| **Sem corte mínimo** | Seria circular: se a pergunta é "quais os mais jogados", filtrar por volume já embute a resposta |
| **View** | `vw_campeoes_mais_usados` |

### PN11 — Em qual rota o desempenho individual mais pesa?

**A pergunta que NÃO deu para responder:** *"qual rota tem maior taxa de vitória?"*

Ela é **estruturalmente impossível**. Toda partida tem um jogador de cada rota em
cada time — um vence, o outro perde. A taxa de vitória de qualquer rota é
exatamente 50%, sempre. Verificado na amostra:

```
TOP 50,00%  ·  JUNGLE 50,00%  ·  MIDDLE 50,00%  ·  BOTTOM 50,00%  ·  UTILITY 50,01%
```

Coletar mais dados não mudaria nada. É uma identidade aritmética, não um achado.

**A reformulação que tem resposta:**

| Campo | Conteúdo |
|---|---|
| **Pergunta** | Em qual rota o desempenho individual mais separa quem venceu de quem perdeu? |
| **Métrica** | Razão entre o KDA médio dos vencedores e o dos perdedores, por rota. E a vantagem percentual de ouro/min |
| **Leitura** | Razão alta = maior peso do jogador individual. Razão baixa = maior dependência do time |
| **Ressalva** | Parte da diferença é causalidade reversa — especialmente na selva, onde o jungler acumula assistências das jogadas do time inteiro |
| **View** | `vw_alavancagem_rota` |

---

### Cobertura e custo

| Verificação | Resultado |
|---|---|
| Categorias cobertas | 7 (objetivos, economia, estruturas, visão, combate, transversal, tempo) |
| Perguntas de prioridade **Alta** | 5 (PN01, PN02, PN03, PN04, PN06) — dentro do limite de 6 |
| Perguntas que exigem `timeline` | apenas 1 (PN02) |

**Decisão sobre o PN02 — opção (a) ✅**

O PN02 é a única pergunta que precisa de dados minuto a minuto. Coletar `timeline`
das 5.000 partidas dobraria o custo, então ela será coletada apenas para uma
**subamostra aleatória de ~1.500 partidas**.

Justificativa: o PN02 produz uma curva agregada (winrate por faixa de ouro), e
1.500 partidas dão precisão de sobra para isso. O custo total de coleta sobe cerca
de 30% em vez de 100%.

> ⚠️ A subamostra precisa ser **aleatória**, não "as 1.500 primeiras". Pegar as
> primeiras introduziria viés — tenderiam a vir dos mesmos jogadores ou das mesmas
> datas. Isso será tratado no script da Etapa 3.

---

## 5. Priorização

Nem toda pergunta cabe no projeto. Classifique cada uma:

- **Alta** — responde diretamente a pergunta principal, e o dado é barato de obter
- **Média** — agrega contexto, ou é cara (timeline) mas relevante
- **Baixa** — curiosidade; entra só se sobrar tempo

Regra: **no máximo 6 perguntas de prioridade Alta.** São elas que vão virar as
páginas principais do dashboard. Se tudo é prioridade, nada é.

---

## 6. Checklist da Etapa 2

- [ ] 8 a 12 perguntas escritas
- [ ] Pelo menos 4 categorias diferentes cobertas
- [ ] Toda pergunta tem uma **comparação** explícita
- [ ] Toda pergunta tem **hipótese escrita antes** de qualquer dado ser coletado
- [ ] Toda pergunta tem o **formato da resposta** desenhado
- [ ] Fonte marcada (`match` ou `match + timeline`)
- [ ] Prioridade atribuída, com no máximo 6 "Alta"
