"""
Etapa 8 — Carga no PostgreSQL
Lê as tabelas de data/final/ e insere no banco lol_analytics.

Pré-requisito: rodar sql/01_criar_tabelas.sql no pgAdmin antes.

Este script é IDEMPOTENTE: limpa as tabelas antes de inserir, então pode ser
executado quantas vezes quiser sem duplicar dado.

Como rodar (com o venv ativo, da raiz do projeto):
    python src/load/carregar_banco.py
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

RAIZ = Path(__file__).resolve().parents[2]
DIR_FINAL = RAIZ / "data" / "final"

# --- Conexão ---------------------------------------------------------------
# A "string de conexão" é um endereço que descreve tudo que o banco precisa:
#
#   postgresql+psycopg2://usuario:senha@servidor:porta/banco
#   └────────┘ └───────┘  └────┘ └───┘ └───────┘ └───┘ └───┘
#    dialeto    driver              credenciais         qual banco
#
# Atenção: se a senha tiver caracteres especiais (@ : / ?), eles precisam ser
# codificados. Com "admin" não há problema.

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", "5432")
PGDATABASE = os.getenv("PGDATABASE", "lol_analytics")
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD")

if not PGPASSWORD:
    raise SystemExit("PGPASSWORD não encontrada no .env")

URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"

# O "engine" é a fábrica de conexões. Ele não conecta agora — só guarda como
# conectar quando alguém precisar.
engine = create_engine(URL)

# A ordem importa: `times` depende de `partidas`, `jogadores` depende de `times`.
ORDEM_CARGA = ["partidas", "times", "jogadores"]


# --- Funções ---------------------------------------------------------------

def testar_conexao():
    """Falha cedo e com mensagem clara se o banco não estiver acessível."""
    with engine.connect() as conn:
        versao = conn.execute(text("SELECT version()")).scalar()
    print(f"  conectado: {versao.split(',')[0]}")


def limpar_tabelas():
    """Esvazia as três tabelas, preservando a estrutura.

    TRUNCATE apaga todas as linhas de uma vez. É muito mais rápido que
    DELETE, que remove linha por linha registrando cada uma.

    CASCADE é necessário por causa das chaves estrangeiras: sem ele, o banco
    recusa esvaziar `partidas` enquanto houver linhas em `times` apontando
    para ela.
    """
    with engine.begin() as conn:   # begin() abre uma transação
        conn.execute(text("TRUNCATE jogadores, times, partidas CASCADE"))
    print("  tabelas esvaziadas")


def carregar(nome):
    """Lê o parquet e insere na tabela de mesmo nome."""
    df = pd.read_parquet(DIR_FINAL / f"{nome}.parquet")

    # `faixa_duracao` veio do pd.cut como tipo "category", que o banco não
    # conhece. Convertemos para texto simples.
    for coluna in df.columns:
        if isinstance(df[coluna].dtype, pd.CategoricalDtype):
            df[coluna] = df[coluna].astype(str)

    df.to_sql(
        nome,
        engine,
        if_exists="append",   # NUNCA "replace" — ele apagaria a tabela e as restrições
        index=False,          # não gravar o índice do Pandas como coluna
        chunksize=1000,       # envia de 1.000 em 1.000 em vez de linha a linha
        method="multi",       # agrupa vários INSERT num comando só
    )
    print(f"  {nome:<12} {len(df):>6} linhas inseridas")
    return len(df)


def conferir():
    """Confere no banco o que realmente foi gravado."""

    consultas = {
        "partidas": "SELECT COUNT(*) FROM partidas",
        "times": "SELECT COUNT(*) FROM times",
        "jogadores": "SELECT COUNT(*) FROM jogadores"
    }

    print("\n  contagem no banco:")
    with engine.connect() as conn:
        for nome, sql in consultas.items():
            total = conn.execute(text(sql)).scalar()
            print(f"    {nome:<12} {total:>6}")

    sql_barao = 'SELECT AVG(CAST(venceu AS INT)) FROM times WHERE primeiro_barao'

    with engine.connect() as conn:
        taxa = conn.execute(text(sql_barao)).scalar()
    print(f"\n  winrate com primeiro Barão: {float(taxa):.1%}   (esperado: 80,6%)")


# --- Orquestração ----------------------------------------------------------

def main():
    print("Testando conexão...")
    testar_conexao()

    print("Limpando tabelas...")
    limpar_tabelas()

    print("Carregando (na ordem das dependências)...")
    for nome in ORDEM_CARGA:
        carregar(nome)

    print("Conferindo...")
    conferir()

    print("\nCarga concluída.")


if __name__ == "__main__":
    main()
