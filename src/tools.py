import re
from functools import lru_cache
from contextlib import closing

import sqlite3
import pandas as pd
from langchain.tools import tool
from langchain_community.document_loaders import PyMuPDFLoader

from src.config import settings


@lru_cache()
def get_document() -> str:
    """Carrega o PDF de políticas da loja e retorna o conteúdo documento."""
    pages = PyMuPDFLoader(str(settings.PDF_PATH)).load()
    return "\n".join(
        f"{p.page_content.strip()}" for p in pages
    )


def _connect_readonly() -> sqlite3.Connection:
    """Conecta ao banco de dados SQLite em modo somente leitura."""
    uri = f"{settings.DB_PATH.resolve().as_uri()}?mode=ro"
    return sqlite3.connect(uri, uri=True)

def get_schema() -> str:
    """Monta uma descrição do banco (DDL + 2 linhas de exemplo por tabela) para o prompt."""
    parts = []
    with closing(_connect_readonly()) as conn:
        tables = conn.execute(
            "SELECT name, sql FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()
        for name, ddl in tables:
            sample = pd.read_sql_query(f'SELECT * FROM "{name}" LIMIT 2', conn)
            parts.append(f"{ddl}\n-- Exemplo de linhas:\n{sample.to_string(index=False)}")
    return "\n\n".join(parts)


@tool 
def consult_sql(query: str) -> str:
    """Executa uma consulta SQL (SQLite, somente SELECT) no banco de dados da loja.
 
    Use para perguntas sobre dados: pedidos, clientes, produtos, categorias,
    estoque, vendas, faturamento, preços, etc.
    Envie UMA única instrução SELECT (ou WITH ... SELECT), sem ponto e vírgula no meio.
    Retorna o resultado em formato de tabela, ou uma mensagem de erro que você
    pode usar para corrigir a query e tentar de novo.
    """
    q = query.strip().rstrip(";").strip()
 
    if not re.match(r"^(select|with)\b", q, re.IGNORECASE):
        return "Erro: apenas consultas SELECT são permitidas."
    if ";" in q:
        return "Erro: envie apenas uma instrução SQL, sem ';' no meio."
 

    try:
        with closing(_connect_readonly()) as conn:
            df = pd.read_sql_query(q, conn)
    except Exception as e:  # devolve o erro ao modelo para ele se autocorrigir
        return f"Erro ao executar a query: {e}"
 
    if df.empty:
        return "Nenhum resultado encontrado."
 
    out = df.to_markdown(index=False)
    return out