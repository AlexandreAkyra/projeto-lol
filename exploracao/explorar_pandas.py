"""
Etapa 5 — Tarefa 5.1
Primeiro contato com Pandas: carregar o JSONL e ver o que acontece.

Este script não transforma nada. Ele só olha — mesmo espírito da tarefa 3.1.

Como rodar (com o venv ativo, da raiz do projeto):
    python src/transform/explorar_pandas.py
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ARQ_PARTIDAS = RAIZ / "data" / "raw" / "partidas.jsonl"

# Lemos só 100 linhas. O arquivo inteiro tem 350 MB e carregá-lo em memória
# para uma exploração seria desperdício de tempo e RAM.
df = pd.read_json(ARQ_PARTIDAS, lines=True, nrows=100)


print("=" * 60)
print("1. FORMATO")
print("=" * 60)
# .shape devolve (linhas, colunas)
print("shape:", df.shape)
print("colunas:", list(df.columns))


print()
print("=" * 60)
print("2. TIPOS DE CADA COLUNA")
print("=" * 60)
# .dtypes mostra o tipo que o Pandas inferiu para cada coluna.
# Tipos comuns: int64, float64, bool, object (= qualquer coisa que não seja
# número ou booleano — texto, dicionário, lista...)
print(df.dtypes)


print()
print("=" * 60)
print("3. AS PRIMEIRAS LINHAS")
print("=" * 60)
# .head(n) mostra as n primeiras linhas. Sem argumento, mostra 5.
print(df.head(3))


print()
print("=" * 60)
print("4. O QUE TEM DENTRO DE UMA CÉLULA?")
print("=" * 60)
# .iloc[linha, coluna] pega uma célula pela POSIÇÃO (índice numérico).
# Existe também .loc, que pega pelo RÓTULO. Vamos ver os dois adiante.
primeira_celula = df.iloc[0]["info"]

print("tipo da célula:", type(primeira_celula))
print()

# ----------------------------------------------------------------------
# TODO 1 — Imprima as CHAVES dessa célula.
#
# Se ela for um dicionário, o método é o mesmo que você usou na tarefa 3.1.
# ----------------------------------------------------------------------
print("chaves dentro da célula 'info':", primeira_celula.keys())


print()
print("=" * 60)
print("5. A PERGUNTA DA TAREFA")
print("=" * 60)
print("""
O JSON tinha 16 campos em 'info' + 155 por jogador + os objetivos dos times.
O DataFrame tem quantas colunas?

Responda, no final desta execução:
  a) Quantas colunas o Pandas criou?
  b) Por que não criou uma coluna para cada campo do JSON?
  c) O que isso significa para o seu trabalho na Etapa 5?
""")
