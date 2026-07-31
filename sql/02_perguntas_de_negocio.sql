-- =========================================================================
-- Etapa 9 — Consultas que respondem as perguntas de negócio
--
-- Cada bloco corresponde a uma pergunta do documento
-- docs/ETAPA-02-perguntas-de-negocio.md
--
-- Como rodar: pgAdmin > banco lol_analytics > Tools > Query Tool
--             Selecione UM bloco de cada vez e aperte F5.
--             (Se rodar o arquivo inteiro, só o resultado da última aparece.)
-- =========================================================================


-- =========================================================================
-- PN01 — Primeiro Barão
-- "Times que garantem o primeiro Barão vencem com que frequência?"
-- Hipótese registrada: entre 70% e 79%
-- =========================================================================
SELECT
    primeiro_barao,
    COUNT(*)                            AS total_times,
    SUM(CAST(venceu AS INT))            AS vitorias,
    ROUND(AVG(CAST(venceu AS INT)), 4)  AS taxa_vitoria
FROM times
GROUP BY primeiro_barao
ORDER BY primeiro_barao;

-- Anatomia deste SELECT:
--
--   COUNT(*)                  conta as linhas do grupo
--   CAST(venceu AS INT)       converte o booleano em 0 ou 1
--   SUM(...)                  soma esses 0 e 1 = quantas vitórias
--   AVG(...)                  média de 0 e 1 = a proporção de vitórias
--   ROUND(..., 4)             arredonda para 4 casas
--   GROUP BY primeiro_barao   calcula tudo isso separado para TRUE e FALSE
--
-- Sempre traga o COUNT junto da taxa. Uma taxa sem o tamanho da base
-- esconde se ela veio de 3 partidas ou de 3.000 (lição L6 do charter).


-- =========================================================================
-- PN03 — Primeira Torre
-- Hipótese registrada: entre 59% e 65%
--
-- TAREFA: escreva a consulta.
-- É o mesmo bloco do PN01, trocando a coluna do GROUP BY.
-- =========================================================================




-- =========================================================================
-- PN05 — First Blood
-- Hipótese registrada: entre 51% e 55% (o fator mais fraco da lista)
--
-- TAREFA: escreva a consulta.
-- =========================================================================




-- =========================================================================
-- PN08 (parcial) — distribuição das partidas por faixa de duração
--
-- TAREFA: conte quantas partidas há em cada faixa de duração.
-- Dica: a tabela é `partidas` e a coluna é `faixa_duracao`.
--       Aqui não há taxa de vitória — só contagem.
-- =========================================================================




-- =========================================================================
-- BÔNUS — sua primeira consulta com JOIN
--
-- Pergunta: qual a taxa de vitória por campeão na rota do meio,
--           considerando só campeões com pelo menos 30 partidas?
--
-- Esta usa uma tabela só (jogadores), mas introduz o HAVING.
-- =========================================================================
SELECT
    nome_campeao,
    COUNT(*)                            AS partidas,
    ROUND(AVG(CAST(venceu AS INT)), 4)  AS taxa_vitoria
FROM jogadores
WHERE rota = 'MIDDLE'
GROUP BY nome_campeao
HAVING COUNT(*) >= 30
ORDER BY taxa_vitoria DESC
LIMIT 10;

-- WHERE x HAVING — a diferença que confunde todo mundo:
--
--   WHERE   filtra LINHAS, antes de agrupar
--   HAVING  filtra GRUPOS, depois de agrupar
--
-- Aqui: WHERE descarta jogadores de outras rotas (linha a linha).
--       HAVING descarta campeões com poucas partidas (grupo a grupo).
--
-- O HAVING não é preciosismo: sem ele, um campeão jogado 2 vezes com
-- 2 vitórias apareceria em primeiro lugar com 100% de winrate.
