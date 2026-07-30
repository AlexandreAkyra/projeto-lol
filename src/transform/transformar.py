"""
Etapa 5 — Transformação
Lê o JSONL bruto e produz as três tabelas analíticas em data/processed/.

Entrada:  data/raw/partidas.jsonl          (5.000 partidas cruas da Riot API)
Saída:    data/processed/partidas.parquet  (1 linha = 1 partida)
          data/processed/times.parquet     (1 linha = 1 time em 1 partida)
          data/processed/jogadores.parquet (1 linha = 1 jogador em 1 partida)

Regras de limpeza aplicadas (ver docs/ETAPA-04-dicionario-de-dados.md):
  D1 - remove partidas com menos de 5 minutos (remakes)
  D2 - remove o patch 16.15 (pós-reset de temporada)
  D4 - remove partidas com algum jogador sem teamPosition

Como rodar (com o venv ativo, da raiz do projeto):
    python src/transform/transformar.py
"""

import json
from pathlib import Path

import pandas as pd

# --- Caminhos e constantes -------------------------------------------------

RAIZ = Path(__file__).resolve().parents[2]
ARQ_BRUTO = RAIZ / "data" / "raw" / "partidas.jsonl"
DIR_SAIDA = RAIZ / "data" / "processed"
DIR_SAIDA.mkdir(parents=True, exist_ok=True)

DURACAO_MINIMA = 300      # D1: segundos
PATCH_EXCLUIDO = "16.15"  # D2


# --- Leitura ---------------------------------------------------------------

def carregar_brutas(caminho):
    """Lê o JSONL e devolve a lista de partidas como dicionários."""
    with open(caminho, "r", encoding="utf-8") as f:
        return [json.loads(linha) for linha in f]


# --- Construção das tabelas ------------------------------------------------

def construir_partidas(brutas):
    """Grão: 1 linha = 1 partida. Aplica D1 e D2 (D4 vem depois)."""
    df = pd.json_normalize(brutas)          

    partidas = df[[
        "metadata.matchId",
        "info.gameDuration",
        "info.gameVersion",
        "info.gameStartTimestamp",
    ]].copy()

    partidas = partidas.rename(columns={
        "metadata.matchId": "id_partida",
        "info.gameDuration": "duracao_segundos",
        "info.gameVersion": "patch_jogo",
        "info.gameStartTimestamp": "inicio_ms",
    })

    partes = partidas["patch_jogo"].str.split(".")      # divide UMA vez
    partidas["patch"] = partes.str[0] + "." + partes.str[1]
    partidas["inicio_partida"] = pd.to_datetime(partidas["inicio_ms"], unit="ms")
    partidas = partidas.drop(columns=["patch_jogo", "inicio_ms"])

    partidas = partidas[partidas["duracao_segundos"] >= DURACAO_MINIMA]   # D1
    partidas = partidas[partidas["patch"] != PATCH_EXCLUIDO]              # D2

    return partidas.reset_index(drop=True)

def ids_sem_posicao(brutas):
    """D4: devolve o conjunto de matchIds com algum jogador sem teamPosition."""
    ids_ruins = set()
    for partida in brutas:
        for player in partida['info']['participants']:
            if player['teamPosition'] == "":
                ids_ruins.add(partida['metadata']['matchId'])
    return ids_ruins 


def construir_times(brutas):
    """Grão: 1 linha = 1 time em 1 partida."""
    time = []
    
    for partida in brutas:
        for equipe in partida['info']['teams']:
            partida_dict = {
                "id_partida": partida['metadata']['matchId'],
                "team_id": equipe["teamId"],
                "venceu": equipe["win"],
                "primeiro_barao": equipe['objectives']['baron']['first'],
                "primeira_torre": equipe['objectives']['tower']['first'],
                "first_blood": equipe['objectives']['champion']['first'],
                "primeiro_dragao": equipe['objectives']['dragon']['first'],
                "arauto": equipe["objectives"]["riftHerald"]["first"],
                "larvas": equipe["objectives"]["horde"]["first"],
                "dragoes_abatidos": equipe["objectives"]["dragon"]["kills"],
                "abates": equipe["objectives"]["champion"]["kills"],
                "torres_destruidas": equipe["objectives"]["tower"]["kills"],
            }
            time.append(partida_dict)
    return pd.DataFrame(time)

def construir_jogadores(brutas):
    """Grão: 1 linha = 1 jogador em 1 partida."""
    jogadores = []

    for partida in brutas:
        id_partida = partida["metadata"]["matchId"]
        for jogador in partida["info"]["participants"]:
            jogadores.append({
                "id_partida": id_partida,          # ← chave estrangeira
                "puuid": jogador["puuid"],         # ← identificador do jogador
                "team_id": jogador["teamId"],
                "venceu": jogador["win"],
                "nome_campeao": jogador["championName"],
                "rota": jogador["teamPosition"],
                "kills": jogador["kills"],
                "deaths": jogador["deaths"],
                "assists": jogador["assists"],
                "ouro": jogador["goldEarned"],
                "cs_minion": jogador["totalMinionsKilled"],
                "cs_jungle": jogador["neutralMinionsKilled"],
                "vision_score": jogador["visionScore"],
            })

    return pd.DataFrame(jogadores)
    

def agregar_visao(times, jogadores):
    """Soma o vision score dos 5 jogadores e acrescenta como coluna em `times`."""

    visao_por_time = (
    jogadores
    .groupby(["id_partida", "team_id"])["vision_score"]
    .sum()
    .reset_index()
    )

    times = times.merge(
    visao_por_time,
    on=["id_partida", "team_id"],
    how="left",
    )

    return times


# --- Validações ------------------------------------------------------------

def validar(partidas, times, jogadores):
    """Trava o pipeline se qualquer invariante for violada.

    Cada assert abaixo é uma verdade que TEM que valer. Se uma falhar, algo
    quebrou na transformação — e é melhor parar aqui do que salvar dado errado.
    """
    n = len(partidas)

    # Cardinalidade: 2 times e 10 jogadores por partida
    assert len(times) == n * 2, f"esperava {n*2} times, veio {len(times)}"
    assert len(jogadores) == n * 10, f"esperava {n*10} jogadores, veio {len(jogadores)}"

    # Chave primária: nenhuma partida repetida
    assert partidas["id_partida"].is_unique, "id_partida duplicado em partidas"

    # Integridade referencial: todo time e todo jogador aponta para uma partida existente
    ids = set(partidas["id_partida"])
    assert set(times["id_partida"]) <= ids, "times com partida inexistente"
    assert set(jogadores["id_partida"]) <= ids, "jogadores com partida inexistente"

    # Regra do jogo: em toda partida, um time ganha e o outro perde
    assert times["venceu"].mean() == 0.5, "média de vitórias diferente de 0,5"

    # Limpeza: as regras foram mesmo aplicadas
    assert partidas["duracao_segundos"].min() >= DURACAO_MINIMA, "sobrou remake"
    assert PATCH_EXCLUIDO not in set(partidas["patch"]), "sobrou partida do patch excluído"

    # Completude: nenhum campo essencial vazio
    for tabela, nome in [(partidas, "partidas"), (times, "times"), (jogadores, "jogadores")]:
        vazios = tabela.isna().sum().sum()
        assert vazios == 0, f"{nome} tem {vazios} valores vazios"

    print("  todas as validações passaram")


# --- Orquestração ----------------------------------------------------------

def main():
    print("Lendo dado bruto...")
    brutas = carregar_brutas(ARQ_BRUTO)
    print(f"  {len(brutas)} partidas cruas")

    print("Construindo tabela `partidas` (D1 + D2)...")
    partidas = construir_partidas(brutas)

    print("Aplicando D4...")
    ruins = ids_sem_posicao(brutas)
    partidas = partidas[~partidas["id_partida"].isin(ruins)]
    print(f"  {len(partidas)} partidas após limpeza")

    print("Construindo `times` e `jogadores`...")
    times = construir_times(brutas)
    jogadores = construir_jogadores(brutas)

    # Alinhamento: a tabela `partidas` é a dona da verdade sobre quais
    # partidas existem. As outras duas se ajustam a ela.
    validos = set(partidas["id_partida"])
    times = times[times["id_partida"].isin(validos)].reset_index(drop=True)
    jogadores = jogadores[jogadores["id_partida"].isin(validos)].reset_index(drop=True)

    print("Agregando vision score por time...")
    times = agregar_visao(times, jogadores)

    print("Validando...")
    validar(partidas, times, jogadores)

    print("Salvando...")
    partidas.to_parquet(DIR_SAIDA / "partidas.parquet", index=False)
    times.to_parquet(DIR_SAIDA / "times.parquet", index=False)
    jogadores.to_parquet(DIR_SAIDA / "jogadores.parquet", index=False)

    print(f"\n{'='*46}")
    print(f"partidas   {len(partidas):>7} linhas x {partidas.shape[1]:>2} colunas")
    print(f"times      {len(times):>7} linhas x {times.shape[1]:>2} colunas")
    print(f"jogadores  {len(jogadores):>7} linhas x {jogadores.shape[1]:>2} colunas")
    print(f"{'='*46}")


if __name__ == "__main__":
    main()
