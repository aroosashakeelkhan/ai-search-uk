# tests/test_search.py
from app.db import init_db, add_doc, search


def setup_function():
    init_db()
    add_doc("1", "NHS Overview",
            "The NHS provides healthcare services across the UK including GP services.")


def test_search_basic():
    res = search("NHS")
    assert any("NHS" in r["title"] or "NHS" in r["snippet"] for r in res)
