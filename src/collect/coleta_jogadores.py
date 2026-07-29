"""
Etapa 3 — Tarefa 3.3
Coleta a lista de jogadores de alto elo (Mestre, Grão-Mestre, Desafiante) do BR1,
salva as respostas cruas e sorteia a amostra semente de 600 jogadores.

Como rodar (com o venv ativo):
    python src/collect/coleta_jogadores.py
"""

import os
import json
import random
from pathlib import Path
from collections import Counter

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
PLATFORM = os.getenv("RIOT_PLATFORM")

if not API_KEY:
    raise SystemExit("RIOT_API_KEY não encontrada. O arquivo .env existe e está preenchido?")

# --- Caminhos ancorados na raiz do projeto ---------------------------------
# __file__ = este arquivo | parents[2] = sobe collect -> src -> raiz
RAIZ = Path(__file__).resolve().parents[2]
DIR_RAW = RAIZ / "data" / "raw"
DIR_INTERIM = RAIZ / "data" / "interim"

# Cria as pastas se não existirem (exist_ok evita erro se já existem)
DIR_RAW.mkdir(parents=True, exist_ok=True)
DIR_INTERIM.mkdir(parents=True, exist_ok=True)

ELOS = ["master", "grandmaster", "challenger"]
TAMANHO_AMOSTRA = 600
SEMENTE = 42  # fixa o sorteio para a coleta ser reproduzível


# --- Funções de apoio ------------------------------------------------------

def buscar_liga(elo):
    """Busca a liga de um elo e devolve o JSON COMPLETO da resposta.

    Devolve `dados` inteiro (e não só `dados['entries']`) porque o campo `tier`
    mora no topo da resposta — precisamos dele para carimbar os jogadores.
    """
    url = f"https://{PLATFORM}.api.riotgames.com/lol/league/v4/{elo}leagues/by-queue/RANKED_SOLO_5x5"
    headers = {"X-Riot-Token": API_KEY}

    resposta = requests.get(url, headers=headers)
    print(f"[{elo}] status {resposta.status_code}")

    if resposta.status_code != 200:
        print("Deu erro. Resposta do servidor:")
        print(resposta.text)
        raise SystemExit(1)

    return resposta.json()


def salvar_json(objeto, caminho):
    """Grava um objeto Python como arquivo JSON legível."""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(objeto, f, ensure_ascii=False, indent=2)
    print(f"  salvo em {caminho.relative_to(RAIZ)}")


def ler_json(caminho):
    """Lê um arquivo JSON e devolve o objeto Python correspondente."""
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


# --- PASSO 1: baixar e salvar o dado cru -----------------------------------

print("\n=== PASSO 1: baixando as ligas ===")

for elo in ELOS:
    caminho = DIR_RAW / f"liga_{elo}.json"
    if caminho.exists():
        print(f"[{elo}] já baixado, pulando")
        continue
    dados = buscar_liga(elo)
    salvar_json(dados, caminho)


# --- PASSO 2: juntar os três, carimbando o tier ----------------------------
# Repare que aqui a gente LÊ os arquivos que acabou de salvar, em vez de usar o
# que está na memória. Não é desperdício: é a prova de que o passo 1 funcionou, e
# a partir de agora você pode rodar os passos 2 a 4 sem gastar chamada de API.

print("\n=== PASSO 2: juntando os jogadores ===")

todos_jogadores = []

for elo in ELOS:
    dados = ler_json(DIR_RAW / f"liga_{elo}.json")
    for jogador in dados['entries']:
        jogador["tier"] = dados['tier']
        todos_jogadores.append(jogador)
    
    
print(f"Total de jogadores reunidos: {len(todos_jogadores)}")


# --- PASSO 3: sortear a amostra semente ------------------------------------

print("\n=== PASSO 3: sorteando a amostra ===")

random.seed(SEMENTE)

amostra = random.sample(todos_jogadores, TAMANHO_AMOSTRA)

print(f"Jogadores sorteados: {len(amostra)}")


# --- PASSO 4: salvar e conferir a composição -------------------------------

print("\n=== PASSO 4: salvando e conferindo ===")

salvar_json(amostra, DIR_INTERIM / "jogadores_amostra.json")

# Counter conta quantas vezes cada valor aparece.
# A expressão dentro dos parênteses percorre a amostra pegando só o campo "tier".
composicao = Counter(jogador["tier"] for jogador in amostra)

print("\nComposição da amostra:")
for tier, quantidade in composicao.most_common():
    print(f"  {tier:<12} {quantidade:>4}  ({quantidade / len(amostra):.1%})")