# app/db.py
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "ai_search.db"


SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS docs USING fts5(
    doc_id UNINDEXED,
    title,
    body,
    tokenize = 'porter'
);
"""


RANK_SQL = """
SELECT doc_id, title, snippet(docs, 1, '<b>', '</b>', '…', 10) AS snippet
FROM docs
WHERE docs MATCH ?
ORDER BY rank
LIMIT ? OFFSET ?;
"""


COUNT_SQL = "SELECT count(*) FROM docs WHERE docs MATCH ?;"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA case_sensitive_like = OFF;")
    return conn


def init_db():
    conn = get_conn()
    with conn:
        conn.executescript(SCHEMA)
    conn.close()


def add_doc(doc_id: str, title: str, body: str):
    conn = get_conn()
    with conn:
        conn.execute(
            "INSERT INTO docs(doc_id, title, body) VALUES(?, ?, ?)", (doc_id, title, body))
    conn.close()


def search(query: str, limit: int = 5, offset: int = 0):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(RANK_SQL, (query, limit, offset))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"doc_id": r[0], "title": r[1], "snippet": r[2]} for r in rows
    ]


def count(query: str) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(COUNT_SQL, (query,))
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total
