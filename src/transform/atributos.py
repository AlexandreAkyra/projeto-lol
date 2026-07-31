"""
Etapa 6 — Engenharia de atributos
Lê as tabelas de data/processed/, acrescenta colunas derivadas e salva de volta.

Colunas criadas:
  partidas   duracao_minutos, faixa_duracao
  times      alma_do_dragao
  jogadores  cs_total, kda, cs_por_minuto, ouro_por_minuto

Decisões documentadas:
  - KDA com 0 mortes é calculado como se fosse 1 morte (convenção do mercado)
  - Faixas de duração: curta < 25 min | média 25-35 | longa > 35

Como rodar (com o venv ativo, da raiz do projeto):
    python src/transform/atributos.py
"""

from pathlib import Path

import pandas as pd

# --- Caminhos --------------------------------------------------------------

RAIZ = Path(__file__).resolve().parents[2]

# Camadas separadas: este script LÊ de processed/ e ESCREVE em final/.
# Nunca escrever de volta na própria entrada — senão a segunda execução
# lê o resultado da primeira e o pipeline deixa de ser idempotente.
DIR_ENTRADA = RAIZ / "data" / "processed"
DIR_SAIDA = RAIZ / "data" / "final"
DIR_SAIDA.mkdir(parents=True, exist_ok=True)


# --- Leitura ---------------------------------------------------------------

def carregar():
    """Lê as três tabelas base e devolve na ordem partidas, times, jogadores."""
    partidas = pd.read_parquet(DIR_ENTRADA / "partidas.parquet")
    times = pd.read_parquet(DIR_ENTRADA / "times.parquet")
    jogadores = pd.read_parquet(DIR_ENTRADA / "jogadores.parquet")
    return partidas, times, jogadores


# --- Enriquecimento --------------------------------------------------------

def enriquecer_partidas(partidas):
    """Acrescenta duracao_minutos e faixa_duracao."""
    partidas = partidas.copy()   # nunca altere o DataFrame que veio de fora

    partidas["duracao_minutos"] = partidas["duracao_segundos"] / 60

    partidas["faixa_duracao"] = pd.cut(
        partidas["duracao_minutos"],
        bins=[0, 25, 35, 999],
        labels=["curta", "media", "longa"],
    )      

    return partidas


def enriquecer_times(times):
    """Acrescenta alma_do_dragao."""
    times = times.copy()
    times['alma_do_dragao'] = times["dragoes_abatidos"] >= 4

    return times

def enriquecer_jogadores(jogadores, partidas):
    """Acrescenta cs_total, kda, cs_por_minuto e ouro_por_minuto.

    Recebe `partidas` porque a duração da partida mora lá, e as métricas
    por minuto precisam dela.
    """
    jogadores = jogadores.copy()
    jogadores["cs_total"] = jogadores['cs_minion'] + jogadores['cs_jungle']
    jogadores["kda"] = (jogadores["kills"] + jogadores["assists"]) / jogadores["deaths"].clip(lower=1)

    jogadores = jogadores.merge(
        partidas[["id_partida", "duracao_minutos"]],
        on="id_partida",
        how="left",
    )

    jogadores['cs_por_minuto'] = jogadores['cs_total'] / jogadores['duracao_minutos']
    jogadores['ouro_por_minuto'] = jogadores['ouro'] / jogadores['duracao_minutos']
    
    return jogadores


# --- Validações ------------------------------------------------------------

def validar(partidas, times, jogadores):
    """Trava o pipeline se algum atributo derivado sair estranho."""

    # Nenhuma linha pode ter sumido nem aparecido
    assert len(jogadores) == len(partidas) * 10, "o merge alterou o número de linhas"

    # toda morte é o abate de alguém: as médias têm que ser quase iguais
    assert abs(jogadores["kills"].mean() - jogadores["deaths"].mean()) < 0.5, "kills e deaths descolaram"

    # KDA médio em qualquer elo fica entre 2 e 5
    assert 2 < jogadores["kda"].mean() < 5, "KDA médio fora da faixa plausível"

    # Nenhum valor vazio nas colunas novas
    novas = ["duracao_minutos", "faixa_duracao"]
    assert partidas[novas].notna().all().all(), "faixa_duracao com valor vazio"

    novas = ["cs_total", "kda", "cs_por_minuto", "ouro_por_minuto"]
    assert jogadores[novas].notna().all().all(), "atributo de jogador com valor vazio"

    # Sanidade de domínio: valores que o jogo não permite
    assert jogadores["kda"].min() >= 0, "KDA negativo"
    assert jogadores["cs_por_minuto"].min() >= 0, "CS por minuto negativo"
    assert jogadores["cs_por_minuto"].max() < 20, "alguém farmando mais de 20 CS/min"
    assert partidas["duracao_minutos"].min() >= 5, "sobrou remake"

    # A alma exige 4 dragões — nunca pode ser True com menos que isso
    almas = times[times["alma_do_dragao"]]
    assert (almas["dragoes_abatidos"] >= 4).all(), "alma marcada com menos de 4 dragões"

    print("  todas as validações passaram")


# --- Orquestração ----------------------------------------------------------

def main():
    print("Lendo tabelas processadas...")
    partidas, times, jogadores = carregar()

    print("Criando atributos...")
    partidas = enriquecer_partidas(partidas)
    times = enriquecer_times(times)
    jogadores = enriquecer_jogadores(jogadores, partidas)

    print("Validando...")
    validar(partidas, times, jogadores)

    print("Salvando...")
    partidas.to_parquet(DIR_SAIDA / "partidas.parquet", index=False)
    times.to_parquet(DIR_SAIDA / "times.parquet", index=False)
    jogadores.to_parquet(DIR_SAIDA / "jogadores.parquet", index=False)

    print(f"\n{'='*52}")
    print(f"partidas   {len(partidas):>7} linhas x {partidas.shape[1]:>2} colunas")
    print(f"times      {len(times):>7} linhas x {times.shape[1]:>2} colunas")
    print(f"jogadores  {len(jogadores):>7} linhas x {jogadores.shape[1]:>2} colunas")
    print(f"{'='*52}")

    print("\nDistribuição por faixa de duração:")
    print(partidas["faixa_duracao"].value_counts())

    print("\nAtributos dos jogadores:")
    print(jogadores[["cs_total", "kda", "cs_por_minuto", "ouro_por_minuto"]].describe().round(2))


if __name__ == "__main__":
    main()
