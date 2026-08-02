from datetime import datetime, timedelta
import os
import json
import random
from pathlib import Path
from collections import Counter

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")
RIOT_REGION = os.getenv("RIOT_REGION")

if not API_KEY:
    raise SystemExit("RIOT_API_KEY não encontrada. O arquivo .env existe e está preenchido?")


agora = datetime.now()
trinta_dias_atras = agora - timedelta(days=30)

end_time = int(agora.timestamp())
start_time = int(trinta_dias_atras.timestamp())

puuid = 'VQazOr5t6J3_cfpiW2svloEQMjLrqW1yuC5jAF_0C1lpBo_C5SwUZ7Lf5oz0-CY3dAcnZwWWFuz8pg'
headers = {"X-Riot-Token": API_KEY}
url = f'https://{RIOT_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'


params = {"queue": 420, "startTime": start_time, "endTime": end_time, "start": 0, "count": 100}
resposta = requests.get(url, headers=headers, params=params)

print("Status code:", resposta.status_code)
if resposta.status_code != 200:
    print("Deu erro. Resposta do servidor:")
    print(resposta.text)
    raise SystemExit(1)

partidas = resposta.json()

print(f'Total de IDs: {len(partidas)}')
for i in range(0, 3):
    print(f'{i+1} ID: {partidas[i]}')