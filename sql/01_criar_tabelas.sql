-- =========================================================================
-- Etapa 7 — Criação das tabelas
--
-- Banco: lol_analytics
-- Como rodar: pgAdmin > clique no banco lol_analytics > Tools > Query Tool
--             cole este arquivo inteiro e aperte F5
--
-- Este script é IDEMPOTENTE: pode ser executado quantas vezes quiser.
-- Os DROP no topo apagam tudo antes de recriar.
-- =========================================================================


-- -------------------------------------------------------------------------
-- LIMPEZA
-- A ordem importa: `jogadores` e `times` apontam para `partidas`, então
-- precisam ser apagados ANTES dela. O banco não deixa apagar uma tabela
-- que ainda tem outras dependendo dela — e isso é uma proteção, não um
-- estorvo.
-- -------------------------------------------------------------------------
DROP TABLE IF EXISTS jogadores;
DROP TABLE IF EXISTS times;
DROP TABLE IF EXISTS partidas;


-- =========================================================================
-- PARTIDAS — grão: 1 linha = 1 partida
-- =========================================================================
CREATE TABLE partidas (
    id_partida        VARCHAR(20)   PRIMARY KEY,
    duracao_segundos  INTEGER       NOT NULL,
    duracao_minutos   NUMERIC(6,2)  NOT NULL,
    faixa_duracao     VARCHAR(10)   NOT NULL,
    patch             VARCHAR(10)   NOT NULL,
    inicio_partida    TIMESTAMP     NOT NULL,

    -- CHECK impõe uma regra de domínio: o banco recusa qualquer linha que
    -- a viole. Estas duas codificam decisões do charter (regras D1 e D2).
    CONSTRAINT chk_duracao_minima
        CHECK (duracao_segundos >= 300),
    CONSTRAINT chk_faixa_valida
        CHECK (faixa_duracao IN ('curta', 'media', 'longa'))
);

COMMENT ON TABLE partidas IS
    'Partidas ranqueadas solo/duo de alto elo do BR1, coletadas em 29/07/2026';
COMMENT ON COLUMN partidas.patch IS
    'Numeracao INTERNA da Riot. 16.14 corresponde ao patch divulgado como 26.14';


-- =========================================================================
-- TIMES — grão: 1 linha = 1 time em 1 partida
-- =========================================================================
CREATE TABLE times (
    id_partida         VARCHAR(20)  NOT NULL,
    team_id            SMALLINT     NOT NULL,

    venceu             BOOLEAN      NOT NULL,

    primeiro_barao     BOOLEAN      NOT NULL,
    primeira_torre     BOOLEAN      NOT NULL,
    first_blood        BOOLEAN      NOT NULL,
    primeiro_dragao    BOOLEAN      NOT NULL,
    arauto             BOOLEAN      NOT NULL,
    larvas             BOOLEAN      NOT NULL,

    dragoes_abatidos   SMALLINT     NOT NULL,
    abates             SMALLINT     NOT NULL,
    torres_destruidas  SMALLINT     NOT NULL,
    vision_score       INTEGER      NOT NULL,
    alma_do_dragao     BOOLEAN      NOT NULL,

    -- CHAVE PRIMÁRIA COMPOSTA
    -- Nenhuma das duas colunas identifica uma linha sozinha: `id_partida`
    -- se repete (2 times por partida) e `team_id` se repete (só existe 100
    -- e 200). Juntas, são únicas. Isso é o grão da tabela virando regra.
    CONSTRAINT pk_times PRIMARY KEY (id_partida, team_id),

    -- CHAVE ESTRANGEIRA
    -- Impede que exista um time apontando para uma partida inexistente.
    -- ON DELETE CASCADE: se a partida for apagada, os times dela somem junto.
    CONSTRAINT fk_times_partida
        FOREIGN KEY (id_partida) REFERENCES partidas(id_partida)
        ON DELETE CASCADE,

    -- Regras de domínio
    CONSTRAINT chk_team_id
        CHECK (team_id IN (100, 200)),
    CONSTRAINT chk_dragoes
        CHECK (dragoes_abatidos >= 0),
    -- A alma exige 4 dragões. Esta linha torna impossível gravar o contrário.
    CONSTRAINT chk_alma_coerente
        CHECK (alma_do_dragao = (dragoes_abatidos >= 4))
);

COMMENT ON COLUMN times.team_id IS '100 = lado azul, 200 = lado vermelho';
COMMENT ON COLUMN times.vision_score IS 'Soma do vision score dos 5 jogadores do time';


-- =========================================================================
-- JOGADORES — grão: 1 linha = 1 jogador em 1 partida
-- =========================================================================
--
-- TAREFA 7.1 — escreva esta tabela.
--
-- Colunas (na ordem em que estão no parquet):
--   id_partida       texto, até 20   -- chave estrangeira para partidas
--   puuid            texto, até 100  -- o identificador tem ~78 caracteres
--   team_id          inteiro pequeno
--   venceu           booleano
--   nome_campeao     texto, até 30
--   rota             texto, até 10
--   kills            inteiro pequeno
--   deaths           inteiro pequeno
--   assists          inteiro pequeno
--   ouro             inteiro
--   cs_minion        inteiro pequeno
--   cs_jungle        inteiro pequeno
--   vision_score     inteiro pequeno
--   cs_total         inteiro pequeno
--   kda              decimal(6,2)
--   duracao_minutos  decimal(6,2)
--   cs_por_minuto    decimal(6,2)
--   ouro_por_minuto  decimal(7,2)   -- chega perto de 1000, precisa de 1 dígito a mais
--
-- Restrições que você precisa declarar:
--
--   1. PRIMARY KEY composta. Pense: o que identifica uma linha aqui de forma
--      única? Não é só id_partida (tem 10 por partida). Não é só puuid (um
--      jogador aparece em várias partidas). A resposta é a combinação dos dois.
--
--   2. FOREIGN KEY de id_partida para partidas, com ON DELETE CASCADE.
--
--   3. Uma FOREIGN KEY COMPOSTA de (id_partida, team_id) para times.
--      Isso garante que o time do jogador realmente existe naquela partida.
--      A sintaxe é a mesma, com as duas colunas entre parênteses nos dois lados.
--
--   4. Um CHECK para `rota`, aceitando apenas:
--      'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY'
--
--   5. Um CHECK garantindo que cs_total = cs_minion + cs_jungle.
--
-- =========================================================================

CREATE TABLE jogadores (
    id_partida         VARCHAR(20)   NOT NULL,
    puuid              VARCHAR(100)  NOT NULL,
    team_id            SMALLINT      NOT NULL,

    venceu             BOOLEAN       NOT NULL,

    nome_campeao       VARCHAR(30)   NOT NULL,
    rota               VARCHAR(10)   NOT NULL,
    kills              SMALLINT      NOT NULL,
    deaths             SMALLINT      NOT NULL,
    assists            SMALLINT      NOT NULL,
    ouro               INTEGER       NOT NULL,
    cs_minion          SMALLINT      NOT NULL,
    cs_jungle          SMALLINT      NOT NULL,
    vision_score       SMALLINT      NOT NULL,
    cs_total           SMALLINT      NOT NULL,
    kda                NUMERIC(6,2)  NOT NULL,
    duracao_minutos    NUMERIC(6,2)  NOT NULL,
    cs_por_minuto      NUMERIC(6,2)  NOT NULL,
    ouro_por_minuto    NUMERIC(7,2)  NOT NULL,


    -- Um jogador aparece em várias partidas; uma partida tem 10 jogadores.
    -- O par (partida, jogador) é o que identifica uma linha.
    CONSTRAINT pk_jogadores PRIMARY KEY (id_partida, puuid),

    -- CHAVE ESTRANGEIRA COMPOSTA
    -- Garante que o par (partida, time) existe de verdade na tabela `times`.
    -- Sem ela, seria possível gravar um jogador da partida X no time 300, ou
    -- no time de outra partida.
    --
    -- Repare que ela dispensa uma chave estrangeira só para `id_partida`:
    -- se o par existe em `times`, e `times` já referencia `partidas`, então
    -- a partida necessariamente existe. A regra vale por transitividade.
    CONSTRAINT fk_jogadores_time
        FOREIGN KEY (id_partida, team_id) REFERENCES times(id_partida, team_id)
        ON DELETE CASCADE,

    -- Só existem cinco posições no jogo.
    CONSTRAINT chk_rota
        CHECK (rota IN ('TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY')),

    -- Mesma ideia do chk_alma_coerente: a coluna derivada nunca pode
    -- descolar da fórmula que a define.
    CONSTRAINT chk_cs_total
        CHECK (cs_total = cs_minion + cs_jungle)
);

COMMENT ON COLUMN jogadores.puuid IS
    'Identificador do jogador na Riot. Nao contem nome nem dado pessoal';
COMMENT ON COLUMN jogadores.kda IS
    '(kills + assists) / max(deaths, 1). Zero mortes conta como uma';


-- =========================================================================
-- ÍNDICES
-- =========================================================================
-- Um índice é como o índice remissivo de um livro: em vez de ler todas as
-- páginas para achar um assunto, você consulta uma lista ordenada e vai
-- direto. Sem índice, o banco lê as 47.410 linhas a cada consulta.
--
-- As PRIMARY KEY já criam índice automaticamente. Estes são os extras,
-- para as colunas que você mais vai filtrar e agrupar nas queries da Etapa 9.
-- -------------------------------------------------------------------------
CREATE INDEX idx_partidas_patch  ON partidas(patch);
CREATE INDEX idx_partidas_faixa  ON partidas(faixa_duracao);
CREATE INDEX idx_times_venceu    ON times(venceu);

CREATE INDEX idx_jogadores_campeao ON jogadores(nome_campeao);
CREATE INDEX idx_jogadores_rota    ON jogadores(rota);


-- =========================================================================
-- CONFERÊNCIA
-- =========================================================================
SELECT table_name, column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
