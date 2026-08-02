# Etapa 10 — Guia de montagem do dashboard

Guia passo a passo para montar o relatório em duas páginas no Power BI Desktop.

> **Menus em inglês.** Todos os nomes de menu, botão e campo aparecem em `inglês`
> (como está na sua instalação), com a tradução entre parênteses na primeira vez.

---

## Antes de começar

### Definir o tamanho da tela

1. Clique numa área **vazia** da página (nenhum visual selecionado)
2. No painel `Visualizations`, clique no ícone de **pincel** (`Format your visual`)
3. `Canvas settings` (configurações da tela) → `Type` → confirme **16:9** (1280 × 720)

Todas as coordenadas deste guia assumem esse tamanho.

### Aplicar um tema

Aba `View` (Exibição) → `Themes` (Temas) → escolha **Executive** ou **Innovate**.

Um tema define paleta, fontes e espaçamentos de uma vez. Sem ele, cada visual usa
o padrão e o conjunto fica com cara de rascunho.

### Como posicionar — leia esta parte antes de tentar

**Primeiro, ligue a grade.** Aba `View` → marque:

- ☑ `Gridlines` (linhas de grade)
- ☑ `Snap objects to grid` (alinhar objetos à grade)

A partir daí, arrastar um visual faz ele grudar na grade sozinho.

**Depois, use o alinhamento em lote.** Selecione vários visuais (clique no
primeiro, `Ctrl` + clique nos outros). Aparece a aba `Format` no topo:

- `Align` (alinhar) → `Align top` (alinhar em cima) — todos na mesma altura
- `Distribute horizontally` (distribuir horizontalmente) — espaçamento igual

Com os quatro cartões KPI, isso resolve em dois cliques.

**Por último, os números.** As coordenadas deste guia descrevem o layout; não
precisa digitar uma por uma. Se precisar, o caminho é:

> pincel (`Format your visual`) → `General` → `Properties` → `Size and style`
> Campos: `Horizontal position` (X), `Vertical position` (Y), `Width`, `Height`

Se digitar um valor e o visual **não pular na tela**, ele não foi aplicado —
confirme com `Enter`. E confira se `Lock aspect ratio` (bloquear proporção) está
**desligado**: com ele ligado, mexer na largura altera a altura sozinho.

### Renomear as páginas

Botão direito na aba **"Page 1"** na parte de baixo → `Rename page`.

- Página 1 → `Visão geral`
- Página 2 → `Detalhamento` (crie com o **+** ao lado da aba)

---

## Mapa: qual view alimenta qual visual

**Confira isto antes de montar cada visual.** Várias views têm colunas de mesmo
nome (`rota`, `nome_campeao`, `taxa_vitoria`, `partidas`), então um visual montado
na view errada fica *plausível* — números coerentes, resposta errada.

| Página | Visual | View |
|---|---|---|
| 1 | Cartões KPI | `vw_kpis` |
| 1 | Ranking de fatores | `vw_ranking_fatores` |
| 1 | Alavancagem por rota | `vw_alavancagem_rota` |
| 2 | Fatores por duração | `vw_fatores_por_duracao` |
| 2 | Distribuição por duração | `vw_duracao` |
| 2 | Top 3 por **taxa de vitória** | `vw_top_campeoes` |
| 2 | Top 3 **mais escolhidos** | `vw_campeoes_mais_usados` |

**Como conferir num visual já montado:** clique nele e olhe o painel `Data`
(dados), à direita. A tabela de origem fica destacada/expandida. Se a origem
estiver errada, o caminho mais rápido é **apagar o visual e refazer** — trocar a
fonte de um visual existente dá mais trabalho do que começar de novo.

---

# PÁGINA 1 — Visão geral

Responde: *o que decide uma partida de alto elo?*

```
┌──────────────────────────────────────────────────────────┐
│  TÍTULO                                                  │
├──────────┬──────────┬──────────┬──────────────────────────┤
│  KPI 1   │  KPI 2   │  KPI 3   │  KPI 4                   │
├──────────────────────────────┬───────────────────────────┤
│                              │                           │
│   RANKING DE FATORES         │   ALAVANCAGEM POR ROTA    │
│   (a resposta principal)     │                           │
│                              │                           │
├──────────────────────────────┴───────────────────────────┤
│  RESSALVA METODOLÓGICA                                   │
└──────────────────────────────────────────────────────────┘
```

## 1.1 — Título

Aba `Insert` (Inserir) → `Text box` (caixa de texto). Digite em duas linhas:

```
Fatores de vitória em partidas ranqueadas de alto elo
League of Legends · BR1 · Mestre, Grão-Mestre e Desafiante · patches 26.13–26.14
```

Formate a primeira linha com **20pt, negrito**; a segunda com **11pt, cinza**.

| `Horizontal position` | `Vertical position` | `Width` | `Height` |
|---|---|---|---|
| 20 | 15 | 1240 | 75 |

## 1.2 — Os quatro cartões (`vw_kpis`)

Visual: `Card` (cartão). Você já tem os quatro — só reposicione.

| Cartão | X | Y | `Width` | `Height` |
|---|---|---|---|---|
| Total de partidas | 20 | 100 | 295 | 105 |
| Jogadores distintos | 330 | 100 | 295 | 105 |
| Duração média (min) | 640 | 100 | 295 | 105 |
| Patches incluídos | 950 | 100 | 295 | 105 |

> **Atalho:** posicione só o primeiro. Depois selecione os quatro com `Ctrl` e use
> `Format` → `Align top` + `Distribute horizontally`.

**Formatação de cada cartão** (pincel → aba `Visual`):

- `Callout value` (valor de chamada) → `Font size` **24** · `Display units` **None**
- `Category label` (rótulo de categoria) → `Font size` **10**, cor cinza
- Aba `General` → `Effects` → `Visual border` ligado, `Rounded corners` **6**

> ⚠️ **O `Display units` precisa ser mudado em cada cartão, um por um.** Se ficar em
> `Auto`, o Power BI escreve `4,741K` em vez de `4.741` — ele abrevia mesmo quando
> não há o que abreviar. Abreviação existe para poupar espaço; num número de quatro
> dígitos ela só troca precisão por nada.

O texto do terceiro cartão está sendo cortado. Encurte para **"Duração média (min)"**
com `Rename for this visual` (renomear para este visual) no campo.

## 1.3 — Ranking de fatores (`vw_ranking_fatores`)

Você já tem. Só reposicione e ajuste.

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 20 | 215 | 700 | 355 |

**Ajustes** (pincel → aba `Visual`):

- Título: `Taxa de vitória de quem conquistou cada objetivo`
  (o recorte "alto elo BR1" já está no título da página — repetir é ruído)
- `Bars` → `Color` → um azul único para todas
- `X-axis` → `Range` → `Minimum` **0** · `Maximum` **100**
  *(fixar a escala impede que ela mude e distorça a comparação)*
- Arraste **`times_com_fator`** para a caixa `Tooltips` (dicas de ferramentas)

**Uma linha de referência em 50%** — o detalhe que mais agrega:

1. Com o visual selecionado, procure no painel `Visualizations` a aba de
   **análises** — o ícone de **lupa**, ao lado do pincel. Chama-se `Analytics`.
2. Dentro dela, procure `Constant line` (linha constante) e adicione uma
3. `Value` (valor): `50`
4. Ligue `Data label` (rótulo de dados)

> **Sobre o texto da linha:** não existe campo para digitar um texto livre. O
> rótulo mostra o **nome da linha**. Para trocá-lo, renomeie a própria linha
> constante — procure um **ícone de lápis** ao lado do nome dela — e depois
> ajuste `Style` para `Name` (só o nome) ou `Name and value` (nome e valor).
>
> Nomeie a linha como `Acaso (50%)`.

**Fazer a linha aparecer de verdade.** No padrão ela nasce fina, cinza-claro e
semitransparente — some atrás das barras. Nas opções da própria linha constante:

- `Color` → **vermelho escuro** ou **laranja** (qualquer cor fora da paleta das barras)
- `Transparency` → **0%**
- `Line style` → `Dashed` (tracejada) · `Width` → **3**

> **Por que tracejada e não sólida.** Linha sólida parece dado. Tracejada é
> convenção universal para *referência* — o leitor entende que aquilo não foi
> medido, é uma marca de comparação.

**O rótulo da linha: desligue.** Ele nasce em cima da barra mais longa e fica
ilegível. As opções de posicionamento não resolvem, porque **todas as barras
cruzam os 50%** — não existe ponto vazio na altura da linha.

Em vez de brigar com o rótulo, mova a explicação para o **subtítulo do gráfico**
(procure `Subtitle`, logo abaixo de `Title` na formatação):

```
A linha tracejada marca 50% — o resultado esperado do puro acaso
```

Fica maior, sempre legível, e num lugar que o leitor já percorre.

> **O princípio.** Rótulo dentro da área do gráfico compete por espaço com o dado.
> Quando os dois brigam, o dado ganha e o texto sai. Legenda, subtítulo e nota de
> rodapé existem exatamente para isso: são espaço que ninguém disputa.

Sem essa linha, o leitor não tem referência para saber se 55,6% é muito ou pouco.
Com ela, fica visível que as larvas mal se afastam do sorteio.

## 1.4 — Alavancagem por rota (`vw_alavancagem_rota`)

Visual: `Clustered bar chart` (gráfico de barras clusterizado — barras deitadas)

| Caixa | Campo |
|---|---|
| `Y-axis` | `rota` |
| `X-axis` | `razao_kda` (agregação: `Average`) |
| `Tooltips` | `kda_vencedor`, `kda_perdedor`, `vantagem_ouro_pct`, `jogadores` |

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 735 | 215 | 510 | 355 |

**Ajustes:**

- Título: `Onde o desempenho individual mais separa vencedor de perdedor`
- **Subtítulo** (procure `Subtitle` logo abaixo de `Title` na formatação):
  `A taxa de vitória por rota é sempre 50% — toda partida tem um jogador de cada rota nos dois times`
- `Rename for this visual` no campo do eixo X → `KDA do vencedor ÷ KDA do perdedor`
- Três pontinhos (`More options`) → `Sort axis` → `razao_kda` → `Sort descending`
- `Data labels` ligados → `Values` → `Decimal places` **1**
- Use uma **cor diferente** do gráfico anterior (ex: cinza-azulado)

> A cor diferente aqui tem função: sinaliza que este gráfico usa **outra métrica**.
> Se fosse do mesmo azul, o leitor compararia 3,3 com 88,0 — números sem relação.

**Confira contra estes valores:**

| Rota | `razao_kda` | KDA vencedor | KDA perdedor |
|---|---|---|---|
| JUNGLE | 3,32 | 6,32 | 1,91 |
| MIDDLE | 2,99 | 4,87 | 1,63 |
| TOP | 2,92 | 3,91 | 1,34 |
| UTILITY | 2,74 | 5,87 | 2,14 |
| BOTTOM | 2,70 | 4,57 | 1,69 |

## 1.5 — Ressalva metodológica

`Insert` → `Text box`, fonte **9pt cinza**:

```
Associação, não causa. A alma do dragão exige vencer quatro disputas de objetivo ao
longo de 20+ minutos — os 88% descrevem times que já vinham dominando, não uma receita
para virar um jogo perdido.

Base: 4.741 partidas ranqueadas solo/duo · BR1 · Mestre+ · patches 26.13 e 26.14 · coleta de 29/07/2026.
```

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 20 | 580 | 1225 | 120 |

> **Este texto já foi três vezes maior e não coube.** A tentação é reduzir a fonte
> até caber — e aí ninguém lê, o que é pior do que não ter escrito.
>
> A saída certa não é diminuir a letra, é **diminuir o texto** e colocar cada
> ressalva junto do gráfico que ela qualifica. O parágrafo sobre "taxa por rota é
> sempre 50%" virou subtítulo do gráfico 1.4, onde tem mais chance de ser lido.
> A discussão completa de limitações fica no README, que é onde cabe.
>
> **Regra:** ressalva de dashboard tem que ser lida em quatro segundos. O que não
> couber nesse orçamento pertence a outro lugar.

---

# PÁGINA 2 — Detalhamento

```
┌──────────────────────────────────────────────────────────────┐
│  TÍTULO + subtítulo com o achado                             │
├───────────────────────────┬─────────────────┬────────────────┤
│  FATORES POR DURAÇÃO      │  TOP 3 QUE      │  TOP 3 QUE     │
│  (colunas)                │  MAIS VENCEM    │  MAIS APARECEM │
├───────────────────────────┤  (matrix)       │  (matrix)      │
│  DISTRIBUIÇÃO DE DURAÇÃO  │                 │                │
│  (colunas)                │                 │                │
└───────────────────────────┴─────────────────┴────────────────┘
```

**A ideia do layout:** as duas tabelas de campeão ficam **lado a lado, na mesma
altura**. É isso que faz o leitor perceber sozinho que as listas quase não se
cruzam — só a Sona aparece nas duas. Se estivessem em cantos opostos da página,
essa comparação exigiria memória.

## 2.1 — Título da página

É a **caixa de texto no topo da página 2** — a mesma que hoje diz "Detalhamento
por duração de partida e por campeão". Clique nela e acrescente uma **segunda
linha**, menor e cinza:

```
Detalhamento: duração da partida e escolha de campeão
Os campeões mais escolhidos vencem 49,8% — os de maior taxa de vitória vencem 56,1%. Só um campeão está nas duas listas.
```

Primeira linha **18pt negrito**, segunda **11pt cinza**.

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 20 | 15 | 1240 | 70 |

> **Por que a segunda linha existe.** As duas matrizes de campeão estão lado a
> lado para serem comparadas — mas nada na tela diz ao leitor que ele deve
> compará-las, nem o que vai encontrar se o fizer. Ele vê duas tabelas parecidas e
> segue em frente.
>
> Um título que só nomeia ("Detalhamento por duração e por campeão") descreve o
> conteúdo. Um título que afirma ("os mais escolhidos vencem 49,8%") entrega o
> achado. **O segundo tipo é o que separa um relatório de um painel de números.**

## 2.2 — Fatores por duração (view: **`vw_fatores_por_duracao`**)

Visual: `Clustered column chart` (colunas agrupadas — barras em pé)

| Caixa | Campo |
|---|---|
| `X-axis` | `fator` |
| `Y-axis` | `taxa_vitoria` (`Average`) |
| `Legend` | `faixa_duracao` |
| `Tooltips` | `times_com_fator` |

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 20 | 95 | 600 | 295 |

**Ajustes:**

- Título: `Todo objetivo perde força conforme a partida se alonga`
- `Y-axis` → `Range` → `Minimum` **0** · `Maximum` **100**
- `Legend` → `Position` → `Top center`
- `Data labels` **desligados** (12 colunas com número viram poluição)
- **Ordem da legenda:** ver 2.7 — no padrão sai `curta, longa, media`, que é
  alfabético e não faz sentido nenhum

**Confira estes valores** — se não baterem, o visual está na view errada:

| Fator | Curta | Média | Longa |
|---|---|---|---|
| Alma do dragão | 100,0 | 92,2 | 75,7 |
| Primeiro Barão | 98,5 | 82,8 | 57,3 |
| Primeira torre | 86,4 | 65,6 | 50,9 |
| First blood | 63,4 | 54,8 | 49,5 |

> **Os 100% da alma em partidas curtas não são um erro — são o achado.** A alma
> exige quatro dragões, e o quarto raramente sai antes dos 25 minutos. Fechar isso
> numa partida curta só acontece quando um time já está atropelando. A alma é o
> sintoma do atropelo, não a causa. Vale a mesma leitura para o Barão (98,5%): ele
> nasce aos 20 min, e "partida curta" acaba antes dos 25.
>
> Taxa de vitória de 100% quase nunca é descoberta. É aviso de que a variável está
> **medindo** o resultado, não prevendo ele.

## 2.3 — Distribuição por duração (view: **`vw_duracao`**)

Visual: `Clustered column chart`

| Caixa | Campo |
|---|---|
| `X-axis` | `faixa_duracao` |
| `Y-axis` | `total_partidas` (`Sum`) |
| `Tooltips` | `duracao_media_min` |

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 20 | 400 | 600 | 300 |

- Título: `Quantas partidas em cada faixa de duração`
- `Data labels` ligados
- Valores esperados: curta **1.389** · média **2.757** · longa **595**

Este gráfico existe para dar contexto ao 2.2: ao ver que só 595 partidas são
"longas", o leitor entende por que aquelas colunas merecem mais desconfiança.

## 2.4 — Top 3 que mais vencem (view: **`vw_top_campeoes`**)

⚠️ **Esta é a view `vw_top_campeoes`.** Se aparecerem Ezreal, Caitlyn e Jhin no
bottom, você pegou a `vw_campeoes_mais_usados` por engano — esses são os mais
escolhidos, não os de maior taxa de vitória.

Visual: **`Matrix`**

| Caixa | Campo |
|---|---|
| `Rows` | `rota`, e **abaixo dele** `nome_campeao` |
| `Values` | `taxa_vitoria` (`Average`), `partidas` (`Sum`) |

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 635 | 95 | 300 | 605 |

**Ajustes, na ordem:**

1. **Expandir a hierarquia.** No topo do visual, use o botão que expande **todos**
   os níveis de uma vez (o de duas setas para baixo). Sem isso você vê só as rotas.

2. **Desligar os subtotais.** Procure na formatação uma seção chamada
   `Subtotals` e desligue **os de linha e o total geral**.

   > **Por que isso importa.** O Power BI calcula o subtotal como a média simples
   > das três porcentagens: `(48,5 + 46,6 + 52,2) ÷ 3 = 49,10`. Mas Ezreal tem 599
   > partidas e Jhin tem 510 — a conta correta pesa cada taxa pelo seu número de
   > partidas, e dá 48,95.
   >
   > Isso se chama **média de médias**, e é um dos erros mais comuns em dashboard.
   > Aqui a diferença é pequena; se um campeão tivesse 1.000 partidas e outro 100,
   > a média simples trataria os dois como iguais. Como não existe "taxa de vitória
   > média do top 3", o certo é não mostrar total nenhum.

3. **Ordenar por posição, não por nome** — ver a seção 2.6, logo abaixo. Não use
   a ordenação normal do Matrix aqui; ela bagunça a ordem das rotas.

4. Título: `Os 3 que mais vencem em cada rota (mín. 100 partidas)`

5. `Rename for this visual` nas colunas: `taxa_vitoria` → **`Vitórias %`**,
   `partidas` → **`Partidas`**

6. **Opcional, mas bom:** na formatação da coluna `taxa_vitoria`, procure
   `Conditional formatting` (formatação condicional) → `Data bars` (barras de
   dados). Isso desenha uma barra dentro da célula, proporcional ao valor — você
   ganha a leitura visual rápida **e** o número exato.

**Confira contra estes valores:**

| Rota | 1º | 2º | 3º |
|---|---|---|---|
| TOP | Riven 58,6 (251) | Quinn 57,3 (110) | Zaahen 57,1 (126) |
| JUNGLE | XinZhao 56,4 (140) | Qiyana 53,7 (203) | Karthus 53,6 (125) |
| MIDDLE | Ekko 54,4 (125) | Malzahar 54,3 (173) | Lux 53,7 (311) |
| BOTTOM | Samira 59,1 (186) | Hwei 58,9 (158) | Viktor 57,8 (109) |
| UTILITY | Leona 57,2 (250) | Janna 55,4 (316) | Sona 53,8 (573) |

> O "mín. 100 partidas" **no título** não é burocracia: sem ele, o leitor não sabe
> se o primeiro colocado tem base sólida ou três jogos de sorte. E a coluna
> `Partidas` fica visível de propósito — taxa sem base engana.

## 2.5 — Top 3 mais escolhidos (view: **`vw_campeoes_mais_usados`**)

Visual: **`Matrix`**, montado igual ao 2.4.

| Caixa | Campo |
|---|---|
| `Rows` | `rota`, e **abaixo dele** `nome_campeao` |
| `Values` | `partidas` (`Sum`), `taxa_vitoria` (`Average`) |

Repare que aqui a **ordem das colunas inverte**: `partidas` vem primeiro, porque é
o critério do ranking. A ordem das colunas comunica o que está sendo medido.

| X | Y | `Width` | `Height` |
|---|---|---|---|
| 950 | 95 | 310 | 605 |

**Mesmos ajustes do 2.4** — expandir, desligar `Subtotals`, ordenar (seção 2.6),
renomear colunas.

- Título: `Os 3 mais escolhidos em cada rota (sem corte mínimo)`
- Renomeie o cabeçalho da primeira coluna para `Rota` (maiúscula), igual à outra
  matriz — duas tabelas lado a lado com cabeçalhos diferentes parecem descuido

O `(sem corte mínimo)` é necessário: esta view **não** tem o filtro de 100
partidas, ao contrário da vizinha. Sem avisar, o leitor assume que as duas tabelas
seguem a mesma regra e compara coisas diferentes.

**Confira contra estes valores:**

| Rota | 1º | 2º | 3º |
|---|---|---|---|
| TOP | Gangplank 418 (43,8) | Jax 342 (56,1) | Malphite 318 (50,0) |
| JUNGLE | LeeSin 626 (51,8) | Kayn 481 (49,9) | Viego 395 (50,9) |
| MIDDLE | Zed 473 (49,7) | Ahri 458 (47,6) | Locke 442 (50,2) |
| BOTTOM | Ezreal 599 (46,6) | Caitlyn 546 (48,5) | Jhin 510 (52,2) |
| UTILITY | Nami 664 (44,6) | Seraphine 623 (51,5) | Sona 573 (53,8) |

## 2.6 — Ordenar as duas matrizes sem desalinhar as rotas

**O problema.** As duas tabelas ficam lado a lado justamente para serem comparadas:
quem lê `UTILITY` na esquerda espera achar `UTILITY` na mesma altura à direita. Mas
elas precisam de ordenações internas diferentes — uma por taxa de vitória, outra por
número de partidas.

Se você clicar no cabeçalho de uma coluna de valor, o Power BI reordena **as rotas
também**, pelo agregado daquela coluna. As duas tabelas se desalinham e a comparação
morre.

**Por que isso acontece.** A ordenação normal do Matrix é global: ela não sabe que
você quer congelar o nível de fora e mexer só no de dentro.

### A solução: `Sort by column`

As duas views já trazem uma coluna `posicao` (1, 2 e 3) calculada no SQL pela
função de janela `ROW_NUMBER()`. Ou seja: **a ordem correta já foi decidida no
banco.** Falta só o Power BI obedecer a ela em vez de ordenar alfabeticamente.

`Sort by column` é o recurso que diz "quando for ordenar este campo, use os valores
daquele outro". É o mesmo mecanismo que faz meses aparecerem em Jan, Fev, Mar em
vez de Abr, Ago, Dez.

**Passo a passo:**

1. Vá para a visão de **modelo** — o ícone na barra da esquerda que mostra as
   tabelas e suas relações (`Model view`)
2. Clique no campo `nome_campeao` **dentro de `vw_top_campeoes`**
3. Nas propriedades do campo, procure `Sort by column` e escolha **`posicao`**
4. **Repita** para o `nome_campeao` de `vw_campeoes_mais_usados`

   > São duas tabelas separadas, com campos de mesmo nome. Configurar uma não
   > configura a outra.

5. Volte ao relatório. Em cada matriz, garanta que a ordenação está por **`rota`**,
   crescente — se você já tinha clicado num cabeçalho de valor, desfaça isso

Resultado: as rotas ficam em ordem alfabética idêntica nas duas (BOTTOM, JUNGLE,
MIDDLE, TOP, UTILITY) e, dentro de cada rota, os campeões saem em 1º, 2º, 3º pelo
critério de cada tabela.

### Se o `Sort by column` der problema

Alternativa que sempre funciona: arraste **`posicao`** para a caixa `Rows`, entre
`rota` e `nome_campeao`.

A hierarquia vira `rota` → `posicao` → `nome_campeao`, e cada nível é ordenado pelo
seu próprio valor — rota alfabética, posição 1/2/3. Custa uma coluna extra de
indentação, mas é à prova de falha e ainda mostra o ranking explicitamente.

> **O conceito por trás.** Ordem é um dado, não um efeito colateral da
> apresentação. Quando a ordem importa, ela deve ser **calculada e armazenada** —
> foi o que o `ROW_NUMBER()` fez. Ferramenta de visualização é o último lugar onde
> se deve decidir ordenação, porque cada visual reinventa a regra e elas divergem.

## 2.7 — O mesmo problema em `curta / media / longa`

Repare na legenda do gráfico 2.2: ela sai **`curta, longa, media`**. Alfabético.

`media` vem antes de `longa` no dicionário, mas partida média é mais curta que
partida longa. É exatamente o caso do 2.6 outra vez: **uma ordem lógica que o
alfabeto não conhece.** O mesmo vale para o gráfico 2.3, que hoje ordena por
quantidade em vez de por duração.

A correção é a mesma, e começa no banco. As views `vw_duracao` e
`vw_fatores_por_duracao` agora trazem uma coluna `ordem_duracao` (1, 2, 3):

```sql
CASE faixa_duracao
    WHEN 'curta' THEN 1
    WHEN 'media'  THEN 2
    WHEN 'longa' THEN 3
END AS ordem_duracao
```

**O que fazer:**

1. Rode `sql/03_views_dashboard.sql` de novo no pgAdmin
2. No Power BI, `Refresh` — a coluna nova só aparece depois disso
3. Visão de **modelo** → campo `faixa_duracao` de **`vw_duracao`** →
   `Sort by column` → **`ordem_duracao`**
4. Repita para o `faixa_duracao` de **`vw_fatores_por_duracao`**
5. No gráfico 2.3, garanta que a ordenação está por `faixa_duracao` (e não por
   `total_partidas`, que é o padrão)

> Três lugares diferentes, um só conceito. Quando um padrão se repete assim, vale
> anotá-lo: **campo de texto com ordem própria sempre precisa de uma coluna
> numérica de apoio.** Meses, dias da semana, faixas etárias, níveis de
> severidade, elos do LoL — todos têm esse problema.

---

## Glossário rápido — inglês → português

| Power BI (inglês) | O que é |
|---|---|
| `Format your visual` | o ícone de pincel, onde fica toda a formatação |
| `General` → `Properties` → `Size and style` | posição e tamanho |
| `Horizontal position` / `Vertical position` | X / Y |
| `Lock aspect ratio` | trava a proporção (deixe desligado) |
| `Callout value` | o número grande do cartão |
| `Category label` | o rótulo abaixo do número |
| `Display units` → `None` | não abreviar (4.741 em vez de "4,74K") |
| `Data labels` | os números nas barras |
| `Decimal places` | casas decimais |
| `Range` → `Minimum` / `Maximum` | limites fixos do eixo |
| `Sort axis` → `Sort descending` | ordenar do maior para o menor |
| `Analytics` (lupa) | aba onde fica a linha de referência |
| `Constant line` | linha de referência |
| `Subtotals` | os totais por grupo do Matrix — **desligue** |
| `Conditional formatting` → `Data bars` | barrinha dentro da célula da tabela |
| `Rename for this visual` | apelidar o campo só naquele gráfico |
| `Tooltips` | o que aparece ao passar o mouse |
| `Gridlines` / `Snap objects to grid` | grade e encaixe |
| `Align top` / `Distribute horizontally` | alinhar e distribuir |

> **Se um menu não estiver onde este guia diz:** os nomes mudam entre versões do
> Power BI. Procure pela ideia (subtotal, linha de referência, ordenação) em vez do
> nome exato — e me diga o que aparece na sua tela.

---

## Checklist final

**Dados corretos** — isto vem antes da estética:

- [ ] Cada visual está na view certa (confira contra o mapa no topo deste guia)
- [ ] O top 3 por winrate mostra Samira/Hwei/Viktor no bottom — não Ezreal/Caitlyn/Jhin
- [ ] Os dois Matrix estão com `Subtotals` **desligados**
- [ ] Todo visual com taxa tem a contagem visível (coluna ou `Tooltips`)

**Apresentação:**

- [ ] Nenhum título de visual mostra nome de coluna do banco (`taxa_vitoria`, `nome_campeao`)
- [ ] Todo gráfico de percentual tem eixo fixo — nenhum com escala automática
- [ ] As duas páginas têm nome (não "Page 1" e "Page 2")
- [ ] A ressalva sobre causalidade está visível, não escondida
- [ ] Cores diferentes só onde há métricas diferentes
- [ ] Nenhum texto cortado com "..."
- [ ] O arquivo está salvo em `powerbi/dashboard_lol.pbix`

## Exportar para o README

`File` → `Export` → `Export to PDF`, ou use `Win + Shift + S` para capturar cada
página como imagem.

Salve em `powerbi/dashboard_pagina1.png` e `powerbi/dashboard_pagina2.png` — elas
vão para o README na Etapa 12. Quem abre um repositório no GitHub não instala
Power BI para ver o resultado; a imagem é o que vende o projeto.
