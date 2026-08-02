-- =========================================================================
-- Etapa 10 — Views para o dashboard
--
-- Uma VIEW é uma consulta guardada com um nome. Ela não copia dado: toda vez
-- que alguém a consulta, o banco executa a query por baixo. O Power BI a
-- enxerga como se fosse uma tabela comum.
--
-- Por que usar views aqui: o Power BI trabalha muito melhor com dado já no
-- formato do gráfico. Toda a transformação pesada fica no banco, onde é mais
-- fácil de escrever, ler e auditar.
--
-- Como rodar: pgAdmin > banco lol_analytics > Tools > Query Tool > F5
-- =========================================================================

-- A ordem importa: vw_top_campeoes depende de vw_campeoes, então precisa ser
-- apagada primeiro. O banco recusa apagar uma view que outra usa.
DROP VIEW IF EXISTS vw_top_campeoes;
DROP VIEW IF EXISTS vw_campeoes_mais_usados;
DROP VIEW IF EXISTS vw_fatores_por_duracao;
DROP VIEW IF EXISTS vw_alavancagem_rota;
DROP VIEW IF EXISTS vw_ranking_fatores;
DROP VIEW IF EXISTS vw_kpis;
DROP VIEW IF EXISTS vw_campeoes;
DROP VIEW IF EXISTS vw_duracao;


-- =========================================================================
-- 1. RANKING DE FATORES  (o gráfico principal — PN06)
--
-- Cada fator vira uma LINHA, com a taxa de vitória de quem o conquistou.
-- Cada bloco é a mesma consulta: filtra quem tem o fator e calcula a média
-- de vitórias desse grupo.
-- =========================================================================
CREATE VIEW vw_ranking_fatores AS

    SELECT 'Alma do dragão'        AS fator,
           ROUND(AVG(venceu::int) * 100, 1) AS taxa_vitoria,
           COUNT(*)                AS times_com_fator
    FROM times WHERE alma_do_dragao

    UNION ALL
    SELECT 'Primeiro Barão', ROUND(AVG(venceu::int) * 100, 1), COUNT(*)
    FROM times WHERE primeiro_barao

    UNION ALL
    SELECT 'Primeira torre', ROUND(AVG(venceu::int) * 100, 1), COUNT(*)
    FROM times WHERE primeira_torre

    UNION ALL
    SELECT 'Arauto', ROUND(AVG(venceu::int) * 100, 1), COUNT(*)
    FROM times WHERE arauto

    UNION ALL
    SELECT 'Primeiro dragão', ROUND(AVG(venceu::int) * 100, 1), COUNT(*)
    FROM times WHERE primeiro_dragao

    UNION ALL
    SELECT 'First blood', ROUND(AVG(venceu::int) * 100, 1), COUNT(*)
    FROM times WHERE first_blood

    UNION ALL
    SELECT 'Larvas do Vazio', ROUND(AVG(venceu::int) * 100, 1), COUNT(*)
    FROM times WHERE larvas

    -- A visão precisa comparar os dois times da mesma partida (auto-join),
    -- por isso este bloco é diferente dos outros.
    UNION ALL
    SELECT 'Vantagem de visão',
           ROUND(AVG(t1.venceu::int) * 100, 1),
           COUNT(*)
    FROM times t1
    JOIN times t2 ON t1.id_partida = t2.id_partida
                 AND t1.team_id   <> t2.team_id
    WHERE t1.vision_score > t2.vision_score;


-- =========================================================================
-- 2. KPIs  (os números grandes do topo do dashboard)
--
-- Uma view de uma linha só, com os totais do projeto.
-- =========================================================================
CREATE VIEW vw_kpis AS
SELECT
    (SELECT COUNT(*) FROM partidas)                       AS total_partidas,
    (SELECT COUNT(DISTINCT puuid) FROM jogadores)         AS jogadores_distintos,
    (SELECT ROUND(AVG(duracao_minutos), 1) FROM partidas) AS duracao_media_min,
    (SELECT COUNT(DISTINCT patch) FROM partidas)          AS patches;


-- =========================================================================
-- 3. CAMPEÕES  (taxa de vitória por campeão e rota)
--
-- O HAVING de 30 partidas evita rankings baseados em 2 ou 3 jogos.
-- A coluna `partidas` fica visível de propósito: taxa sem base engana.
-- =========================================================================
CREATE VIEW vw_campeoes AS
SELECT
    nome_campeao,
    rota,
    COUNT(*)                          AS partidas,
    ROUND(AVG(venceu::int) * 100, 1)  AS taxa_vitoria,
    ROUND(AVG(kda), 2)                AS kda_medio,
    ROUND(AVG(cs_por_minuto), 2)      AS cs_por_minuto
FROM jogadores
GROUP BY nome_campeao, rota
HAVING COUNT(*) >= 100;   -- corte definido na revisão de escopo de 01/08/2026


-- =========================================================================
-- 3b. TOP 3 CAMPEÕES POR ROTA — maior taxa de vitória (mín. 100 partidas)
--
-- Conceito novo: FUNÇÃO DE JANELA (window function).
--
--   ROW_NUMBER() OVER (PARTITION BY rota ORDER BY taxa_vitoria DESC)
--   └──────────┘      └───────────────┘ └──────────────────────────┘
--   numera 1,2,3...   reinicia a cada    define a ordem da numeração
--                     rota
--
-- É como um GROUP BY que, em vez de colapsar as linhas num total, mantém todas
-- e acrescenta uma coluna com a posição de cada uma dentro do seu grupo.
-- Depois basta filtrar posicao <= 3.
-- =========================================================================
DROP VIEW IF EXISTS vw_top_campeoes;


CREATE VIEW vw_top_campeoes AS
SELECT rota, nome_campeao, partidas, taxa_vitoria, posicao
FROM (
    SELECT
        rota,
        nome_campeao,
        partidas,
        taxa_vitoria,
        -- O desempate por `partidas` não é detalhe: Nautilus (409 jogos) e Sona
        -- (573) empatam em 53,8% na UTILITY. Sem um segundo critério, o Postgres
        -- escolhe qualquer um dos dois, e o resultado pode MUDAR entre execuções.
        -- Consulta que não devolve sempre a mesma resposta não é auditável.
        ROW_NUMBER() OVER (
            PARTITION BY rota
            ORDER BY taxa_vitoria DESC, partidas DESC, nome_campeao
        ) AS posicao
    FROM vw_campeoes
) ranqueado
WHERE posicao <= 3;


-- =========================================================================
-- 3c. TOP 3 CAMPEÕES MAIS ESCOLHIDOS POR ROTA
--
-- Aqui NÃO há corte mínimo: a pergunta é "o que as pessoas mais jogam", e
-- cortar por volume seria circular — o corte já é o próprio critério.
-- =========================================================================
DROP VIEW IF EXISTS vw_campeoes_mais_usados;

CREATE VIEW vw_campeoes_mais_usados AS
SELECT rota, nome_campeao, partidas, taxa_vitoria, posicao
FROM (
    SELECT
        rota,
        nome_campeao,
        COUNT(*)                                                  AS partidas,
        ROUND(AVG(venceu::int) * 100, 1)                          AS taxa_vitoria,
        ROW_NUMBER() OVER (
            PARTITION BY rota
            ORDER BY COUNT(*) DESC, nome_campeao
        ) AS posicao
    FROM jogadores
    GROUP BY rota, nome_campeao
) ranqueado
WHERE posicao <= 3;


-- =========================================================================
-- 4. DURAÇÃO  (distribuição das partidas por faixa — PN08)
-- =========================================================================
-- A coluna `ordem_duracao` existe só para ordenar. "curta, media, longa" é uma
-- ordem LÓGICA que o alfabeto não conhece — sozinho ele produz "curta, longa,
-- media". Como toda ordem que importa, ela é calculada aqui e não na ferramenta
-- de visualização.
CREATE VIEW vw_duracao AS
SELECT
    faixa_duracao,
    CASE faixa_duracao
        WHEN 'curta' THEN 1
        WHEN 'media' THEN 2
        WHEN 'longa' THEN 3
    END                                 AS ordem_duracao,
    COUNT(*)                            AS total_partidas,
    ROUND(AVG(duracao_minutos), 1)      AS duracao_media_min
FROM partidas
GROUP BY faixa_duracao;


-- =========================================================================
-- 5. FATORES POR FAIXA DE DURAÇÃO  (PN08 completo)
--
-- A pergunta: o peso de cada fator muda conforme a partida é curta ou longa?
--
-- Aqui aparece o JOIN entre duas tabelas: `times` tem os fatores, `partidas`
-- tem a duração. A ligação é feita pelo id_partida.
-- =========================================================================
DROP VIEW IF EXISTS vw_fatores_por_duracao;

-- O SELECT de fora existe por um motivo só: acrescentar `ordem_duracao` uma vez,
-- em vez de repetir o CASE nos quatro blocos do UNION ALL. Regra escrita quatro
-- vezes é regra que vai divergir na quinta.
CREATE VIEW vw_fatores_por_duracao AS
SELECT
    faixa_duracao,
    CASE faixa_duracao
        WHEN 'curta' THEN 1
        WHEN 'media' THEN 2
        WHEN 'longa' THEN 3
    END AS ordem_duracao,
    fator,
    taxa_vitoria,
    times_com_fator
FROM (

    SELECT p.faixa_duracao,
           'Primeiro Barão'                   AS fator,
           ROUND(AVG(t.venceu::int) * 100, 1) AS taxa_vitoria,
           COUNT(*)                           AS times_com_fator
    FROM times t JOIN partidas p ON t.id_partida = p.id_partida
    WHERE t.primeiro_barao
    GROUP BY p.faixa_duracao

    UNION ALL
    SELECT p.faixa_duracao, 'Alma do dragão',
           ROUND(AVG(t.venceu::int) * 100, 1), COUNT(*)
    FROM times t JOIN partidas p ON t.id_partida = p.id_partida
    WHERE t.alma_do_dragao
    GROUP BY p.faixa_duracao

    UNION ALL
    SELECT p.faixa_duracao, 'Primeira torre',
           ROUND(AVG(t.venceu::int) * 100, 1), COUNT(*)
    FROM times t JOIN partidas p ON t.id_partida = p.id_partida
    WHERE t.primeira_torre
    GROUP BY p.faixa_duracao

    UNION ALL
    SELECT p.faixa_duracao, 'First blood',
           ROUND(AVG(t.venceu::int) * 100, 1), COUNT(*)
    FROM times t JOIN partidas p ON t.id_partida = p.id_partida
    WHERE t.first_blood
    GROUP BY p.faixa_duracao

) base;


-- =========================================================================
-- 6. ALAVANCAGEM INDIVIDUAL POR ROTA
--
-- A pergunta ingênua seria "qual rota tem maior taxa de vitória?". Ela é
-- IMPOSSÍVEL de responder: toda partida tem um jogador de cada rota em cada
-- time, então a taxa de vitória de qualquer rota é exatamente 50%. Sempre.
-- Não é limitação da amostra — é como o jogo é construído.
--
-- A reformulação que TEM resposta: em qual rota o desempenho individual mais
-- separa quem venceu de quem perdeu? Rota com diferença grande sugere maior
-- peso do jogador; diferença pequena sugere maior dependência do time.
-- =========================================================================
DROP VIEW IF EXISTS vw_alavancagem_rota;

CREATE VIEW vw_alavancagem_rota AS
SELECT
    rota,

    ROUND(AVG(kda) FILTER (WHERE venceu), 2)          AS kda_vencedor,
    ROUND(AVG(kda) FILTER (WHERE NOT venceu), 2)      AS kda_perdedor,
    ROUND(
        AVG(kda) FILTER (WHERE venceu)
        / AVG(kda) FILTER (WHERE NOT venceu)
    , 2)                                              AS razao_kda,

    ROUND(AVG(ouro_por_minuto) FILTER (WHERE venceu), 0)     AS ouro_min_vencedor,
    ROUND(AVG(ouro_por_minuto) FILTER (WHERE NOT venceu), 0) AS ouro_min_perdedor,
    ROUND((
        AVG(ouro_por_minuto) FILTER (WHERE venceu)
        / AVG(ouro_por_minuto) FILTER (WHERE NOT venceu) - 1
    ) * 100, 1)                                       AS vantagem_ouro_pct,

    COUNT(*)                                          AS jogadores
FROM jogadores
GROUP BY rota;


-- =========================================================================
-- CONFERÊNCIA
-- =========================================================================
SELECT * FROM vw_alavancagem_rota ORDER BY razao_kda DESC;
