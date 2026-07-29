"""
Etapa 3 — Tarefa 3.1
Objetivo: fazer UMA chamada à Riot API e inspecionar o que ela devolve.

Este script NÃO coleta nada e NÃO salva nada. Ele só olha.
Escrever o parser antes de ver a resposta é como traduzir um texto sem lê-lo.

Como rodar (com o venv ativo, a partir da raiz do projeto):
    python src/collect/teste_api.py
"""

import os
import json

import requests
from dotenv import load_dotenv

# Lê o arquivo .env e joga as variáveis para dentro de os.environ
load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
PLATFORM = os.getenv("RIOT_PLATFORM")  # br1

# Trava de segurança: falha cedo e com mensagem clara se o .env não foi lido
if not API_KEY:
    raise SystemExit("RIOT_API_KEY não encontrada. O arquivo .env existe e está preenchido?")

url = f'https://{PLATFORM}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5'

headers = {"X-Riot-Token": API_KEY}


resposta = requests.get(url, headers=headers)

print("Status code:", resposta.status_code)

if resposta.status_code != 200:
    print("Deu erro. Resposta do servidor:")
    print(resposta.text)
    raise SystemExit(1)

dados = resposta.json()  # transforma o JSON da resposta em dicionário Python

print("\nChaves do topo:", list(dados.keys()))

jogadores = dados['entries']
print("Total de jogadores:", len(jogadores))

print("\nUm jogador de exemplo:")
print(json.dumps(jogadores[0], indent=2))
