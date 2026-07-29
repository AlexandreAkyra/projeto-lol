"""
Etapa 3 — Tarefa 3.6
Coleta o detalhe de 5.000 partidas e salva em JSONL.

Características:
  - sorteia 5.000 IDs dos ~10.500 coletados, com semente fixa
  - salva em JSONL (uma partida por linha, escrita por acréscimo)
  - é retomável: relê o que já foi salvo e continua de onde parou
  - respeita o limite da API e trata 429 / 5xx / 403

Como rodar (com o venv ativo):
    python src/collect/coleta_partidas.py

Tempo estimado: ~1h40. Espaço em disco: ~350 MB.
Pode interromper com Ctrl+C e retomar depois.
"""

import os
import json
import time
import random
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
REGION = os.getenv("RIOT_REGION")
QTD_ALVO = int(os.getenv("TARGET_MATCHES", 5000))

if not API_KEY:
    raise SystemExit("RIOT_API_KEY não encontrada. O arquivo .env existe e está preenchido?")

RAIZ = Path(__file__).resolve().parents[2]
DIR_RAW = RAIZ / "data" / "raw"
DIR_INTERIM = RAIZ / "data" / "interim"

ARQ_IDS = DIR_INTERIM / "match_ids_unicos.json"
ARQ_IDS_ALVO = DIR_INTERIM / "match_ids_alvo.json"
ARQ_PARTIDAS = DIR_RAW / "partidas.jsonl"

SEMENTE = 42
PAUSA = 1.3

HEADERS = {"X-Riot-Token": API_KEY}


# --- Funções de apoio ------------------------------------------------------

def salvar_json(objeto, caminho):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(objeto, f, ensure_ascii=False, indent=2)


def ler_json(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def acrescentar_jsonl(objeto, caminho):
    """Acrescenta um objeto como uma linha no arquivo JSONL.

    Modo "a" = append. Não reescreve nada do que já está lá.
    O ensure_ascii=False mantém acentos legíveis; SEM indent, porque cada
    objeto precisa caber em exatamente uma linha.
    """
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(json.dumps(objeto, ensure_ascii=False) + "\n")


def ids_ja_coletados(caminho):
    """Lê o JSONL existente e devolve o conjunto de matchIds já salvos.

    É isso que torna o script retomável. Linha corrompida (queda no meio de uma
    escrita) é ignorada — na pior das hipóteses aquela partida é rebaixada.
    """
    if not caminho.exists():
        return set()

    coletados = set()
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            try:
                partida = json.loads(linha)
                coletados.add(partida["metadata"]["matchId"])
            except (json.JSONDecodeError, KeyError):
                continue
    return coletados


def buscar_partida(match_id, tentativas=3):
    """Busca o detalhe de uma partida, tratando limites e erros."""
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"

    for _ in range(tentativas):
        resposta = requests.get(url, headers=HEADERS)

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

        if resposta.status_code == 403:
            raise SystemExit(
                "\nChave da API expirada (403). Tudo que foi coletado está salvo.\n"
                "Gere uma chave nova em developer.riotgames.com, atualize o .env\n"
                "e rode o script de novo — ele continua de onde parou."
            )

        print(f"    erro {resposta.status_code} em {match_id}: {resposta.text[:150]}")
        return None

    print(f"    desisti de {match_id}")
    return None


# --- Preparação ------------------------------------------------------------

ids_disponiveis = ler_json(ARQ_IDS)
print(f"IDs disponíveis: {len(ids_disponiveis)}")

# O conjunto alvo é fixado UMA vez e salvo. Se fosse resorteado a cada execução,
# uma retomada mudaria o alvo no meio do caminho e a amostra viraria uma colcha
# de retalhos de vários sorteios diferentes.
if ARQ_IDS_ALVO.exists():
    ids_alvo = ler_json(ARQ_IDS_ALVO)
    print(f"Alvo já sorteado numa execução anterior: {len(ids_alvo)} partidas")
else:
    random.seed(SEMENTE)
    ids_alvo = sorted(random.sample(ids_disponiveis, min(QTD_ALVO, len(ids_disponiveis))))

    salvar_json(ids_alvo, ARQ_IDS_ALVO)
    print(f"Alvo sorteado e salvo: {len(ids_alvo)} partidas")

coletados = ids_ja_coletados(ARQ_PARTIDAS)
faltam = [mid for mid in ids_alvo if mid not in coletados]

print(f"Já coletadas: {len(coletados)}")
print(f"Faltam:       {len(faltam)}")

if not faltam:
    raise SystemExit("Nada a fazer — a coleta já está completa.")

print(f"\nTempo estimado: {len(faltam) * PAUSA / 60:.0f} minutos\n")


# --- Coleta ----------------------------------------------------------------

inicio = time.time()
erros = 0

for i, match_id in enumerate(faltam, start=1):
    partida = buscar_partida(match_id)

    if partida is None:
        erros += 1
    else:
        acrescentar_jsonl(partida, ARQ_PARTIDAS)

    if i % 100 == 0:
        decorrido = time.time() - inicio
        restante = (len(faltam) - i) * (decorrido / i)
        print(
            f"[{i}/{len(faltam)}] "
            f"{decorrido/60:.0f} min decorridos, "
            f"~{restante/60:.0f} min restantes, "
            f"{erros} erros"
        )

    time.sleep(PAUSA)


# --- Resumo ----------------------------------------------------------------

total_final = len(ids_ja_coletados(ARQ_PARTIDAS))
tamanho_mb = ARQ_PARTIDAS.stat().st_size / (1024 * 1024)

print(f"\n{'='*50}")
print(f"Coleta concluída em {(time.time() - inicio)/60:.0f} minutos")
print(f"Partidas no arquivo: {total_final}")
print(f"Erros:               {erros}")
print(f"Tamanho do arquivo:  {tamanho_mb:.0f} MB")
print(f"{'='*50}")
