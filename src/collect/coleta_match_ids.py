"""
Etapa 3 — Tarefa 3.5
Coleta os IDs de partida dos 600 jogadores da amostra semente.

Características:
  - respeita o limite da API (100 requisições a cada 2 minutos)
  - trata 429 (limite estourado) com espera e nova tentativa
  - é retomável: se cair, roda de novo e continua de onde parou

Como rodar (com o venv ativo):
    python src/collect/coleta_match_ids.py

Tempo estimado: ~15 minutos.
"""

import os
import json
import time
import random
from pathlib import Path
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
REGION = os.getenv("RIOT_REGION")
QUEUE = int(os.getenv("QUEUE_ID", 420))
DIAS = int(os.getenv("COLLECTION_DAYS", 30))

if not API_KEY:
    raise SystemExit("RIOT_API_KEY não encontrada. O arquivo .env existe e está preenchido?")

RAIZ = Path(__file__).resolve().parents[2]
DIR_INTERIM = RAIZ / "data" / "interim"

ARQ_AMOSTRA = DIR_INTERIM / "jogadores_amostra.json"
ARQ_PROGRESSO = DIR_INTERIM / "match_ids_por_jogador.json"
ARQ_FINAL = DIR_INTERIM / "match_ids_unicos.json"

PARTIDAS_POR_JOGADOR = 20
SEMENTE = 42

# 100 requisições a cada 2 minutos = 1,2 s por requisição.
# Uso 1,3 s para ter uma margem de segurança.
PAUSA = 1.3

HEADERS = {"X-Riot-Token": API_KEY}


# --- Funções de apoio ------------------------------------------------------

def salvar_json(objeto, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(objeto, f, ensure_ascii=False, indent=2)


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def buscar_ids(puuid, start_time, end_time, tentativas=3):
    """Busca os IDs de partida de um jogador, tratando limite de requisições.

    Se receber 429 (limite estourado), lê o header Retry-After — que diz quantos
    segundos esperar — dorme esse tempo e tenta de novo.
    """
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    params = {
        "queue": QUEUE,
        "startTime": start_time,
        "endTime": end_time,
        "start": 0,
        "count": 100,
    }

    for tentativa in range(tentativas):
        resposta = requests.get(url, headers=HEADERS, params=params)

        if resposta.status_code == 200:
            return resposta.json()

        if resposta.status_code == 429:
            espera = int(resposta.headers.get("Retry-After", 10))
            print(f"    limite atingido, esperando {espera}s...")
            time.sleep(espera + 1)
            continue

        if resposta.status_code >= 500:
            print(f"    erro {resposta.status_code} no servidor, tentando de novo...")
            time.sleep(5)
            continue

        # 403 = chave expirada. Precisa PARAR o script, não seguir adiante:
        # se continuasse, gravaria listas vazias para todos os jogadores restantes
        # e eles seriam pulados na próxima execução, com dado faltando em silêncio.
        if resposta.status_code == 403:
            salvar_json(progresso, ARQ_PROGRESSO)
            raise SystemExit(
                "\nChave da API expirada (403). O progresso foi salvo.\n"
                "Gere uma chave nova em developer.riotgames.com, atualize o .env\n"
                "e rode o script de novo — ele continua de onde parou."
            )

        # 404 = jogador sem histórico na janela. Acontece, é legítimo.
        print(f"    erro {resposta.status_code}: {resposta.text[:200]}")
        return []

    print("    desisti após todas as tentativas")
    return []


# --- Preparação ------------------------------------------------------------

amostra = ler_json(ARQ_AMOSTRA)
print(f"Jogadores na amostra: {len(amostra)}")

agora = datetime.now()
trinta_dias_atras = agora - timedelta(days=30)

end_time = int(agora.timestamp())
start_time = int(trinta_dias_atras.timestamp())

print(f"Janela: {datetime.fromtimestamp(start_time):%d/%m/%Y} a {datetime.fromtimestamp(end_time):%d/%m/%Y}")

# Retoma o progresso anterior, se existir.
# É isso que torna o script retomável: puuid que já está aqui não é buscado de novo.
progresso = ler_json(ARQ_PROGRESSO) if ARQ_PROGRESSO.exists() else {}
print(f"Jogadores já processados numa execução anterior: {len(progresso)}")

random.seed(SEMENTE)


# --- Coleta ----------------------------------------------------------------

inicio = time.time()

for i, jogador in enumerate(amostra, start=1):
    puuid = jogador["puuid"]

    if puuid in progresso:
        continue

    ids = buscar_ids(puuid, start_time, end_time)

    ids_escolhidos = random.sample(ids, min(PARTIDAS_POR_JOGADOR, len(ids)))

    progresso[puuid] = ids_escolhidos

    # Salva a cada 25 jogadores. Se o script morrer, perde no máximo 25.
    if i % 25 == 0:
        salvar_json(progresso, ARQ_PROGRESSO)
        decorrido = time.time() - inicio
        print(f"[{i}/{len(amostra)}] salvo — {decorrido/60:.1f} min decorridos")

    time.sleep(PAUSA)

salvar_json(progresso, ARQ_PROGRESSO)
print(f"\nColeta concluída em {(time.time() - inicio)/60:.1f} minutos")


# --- Consolidação ----------------------------------------------------------
ids_unicos = set()
for lista_de_ids in progresso.values():
    ids_unicos.update(lista_de_ids)

ids_unicos = sorted(ids_unicos)
salvar_json(ids_unicos, ARQ_FINAL)

total_bruto = sum(len(lista) for lista in progresso.values())
print(f"\nIDs coletados (com repetição): {total_bruto}")
print(f"IDs únicos após deduplicar:    {len(ids_unicos)}")
print(f"Taxa de sobreposição:          {1 - len(ids_unicos)/total_bruto:.1%}")
