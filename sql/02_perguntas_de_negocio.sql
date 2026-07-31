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
SELECT
    primeira_torre,
    COUNT(*)                            AS total_times,
    SUM(CAST(venceu AS INT))            AS vitorias,
    ROUND(AVG(CAST(venceu AS INT)), 4)  AS taxa_vitoria
FROM times
GROUP BY primeira_torre
ORDER BY primeira_torre;



-- =========================================================================
-- PN05 — First Blood
-- Hipótese registrada: entre 51% e 55% (o fator mais fraco da lista)
--
-- TAREFA: escreva a consulta.
-- =========================================================================
SELECT
    first_blood,
    COUNT(*)                            AS total_times,
    SUM(CAST(venceu AS INT))            AS vitorias,
    ROUND(AVG(CAST(venceu AS INT)), 4)  AS taxa_vitoria
FROM times
GROUP BY first_blood
ORDER BY first_blood;




-- =========================================================================
-- PN08 (parcial) — distribuição das partidas por faixa de duração
--
-- TAREFA: conte quantas partidas há em cada faixa de duração.
-- Dica: a tabela é `partidas` e a coluna é `faixa_duracao`.
--       Aqui não há taxa de vitória — só contagem.
-- =========================================================================
SELECT
    faixa_duracao,
    COUNT(*) AS total_partidas
FROM partidas
GROUP BY faixa_duracao
ORDER BY total_partidas DESC;



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

-- =========================================================================
-- PN06 ⭐ — RANKING CONSOLIDADO DE FATORES
--
-- "Ordenando todos os fatores binários medidos, qual é o ranking de
--  impacto na vitória?"
--
-- Esta é a consulta que responde a pergunta principal do projeto, e o
-- visual dela é a capa do dashboard.
--
-- Hipótese registrada (Patrick):
--   alma > barão > torre > dragão > arauto > first blood
--   com a alma e o barão acima de +20pp e o first blood entre +1 e +5pp
-- =========================================================================
WITH fatores AS (

    SELECT 'Alma do dragao'  AS fator,
           AVG(venceu::int) FILTER (WHERE alma_do_dragao)      AS wr_com,
           AVG(venceu::int) FILTER (WHERE NOT alma_do_dragao)  AS wr_sem,
           COUNT(*)         FILTER (WHERE alma_do_dragao)      AS times_com
    FROM times

    UNION ALL

    SELECT 'Primeiro Barao',
           AVG(venceu::int) FILTER (WHERE primeiro_barao),
           AVG(venceu::int) FILTER (WHERE NOT primeiro_barao),
           COUNT(*)         FILTER (WHERE primeiro_barao)
    FROM times

    UNION ALL

    SELECT 'Primeira torre',
           AVG(venceu::int) FILTER (WHERE primeira_torre),
           AVG(venceu::int) FILTER (WHERE NOT primeira_torre),
           COUNT(*)         FILTER (WHERE primeira_torre)
    FROM times

    UNION ALL

    SELECT 'Primeiro dragao',
           AVG(venceu::int) FILTER (WHERE primeiro_dragao),
           AVG(venceu::int) FILTER (WHERE NOT primeiro_dragao),
           COUNT(*)         FILTER (WHERE primeiro_dragao)
    FROM times

    UNION ALL

    SELECT 'Arauto',
           AVG(venceu::int) FILTER (WHERE arauto),
           AVG(venceu::int) FILTER (WHERE NOT arauto),
           COUNT(*)         FILTER (WHERE arauto)
    FROM times

    UNION ALL

    SELECT 'Larvas do Vazio',
           AVG(venceu::int) FILTER (WHERE larvas),
           AVG(venceu::int) FILTER (WHERE NOT larvas),
           COUNT(*)         FILTER (WHERE larvas)
    FROM times

    UNION ALL

    SELECT 'First blood',
           AVG(venceu::int) FILTER (WHERE first_blood),
           AVG(venceu::int) FILTER (WHERE NOT first_blood),
           COUNT(*)         FILTER (WHERE first_blood)
    FROM times
)
SELECT
    fator,
    ROUND(wr_com * 100, 1)              AS winrate_com,
    ROUND(wr_sem * 100, 1)              AS winrate_sem,
    ROUND((wr_com - wr_sem) * 100, 1)   AS diferenca_pp,
    times_com
FROM fatores
ORDER BY diferenca_pp DESC;

-- Repare que o resultado traz DUAS formas de medir "impacto":
--
--   winrate_com    quanto vence quem TEM o fator
--   diferenca_pp   o quanto TER o fator muda em relação a não ter
--
-- Ordene mentalmente por uma e depois pela outra. Se as duas listas
-- derem a mesma ordem, ótimo. Se derem ordens diferentes, você tem uma
-- decisão a tomar — e ela precisa ser justificada no README.


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
