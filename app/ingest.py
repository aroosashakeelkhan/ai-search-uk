# app/ingest.py
from pathlib import Path
import click
from bs4 import BeautifulSoup
import markdown
from app.db import init_db, add_doc


DATA_DIR = Path(__file__).resolve().parent / "sample_data"


@click.group()
def cli():
    pass


@cli.command()
@click.option('--path', type=click.Path(exists=True), default=str(DATA_DIR))
def run(path):
    """Ingest .md, .html, .txt files into FTS5."""
    init_db()
    p = Path(path)
    files = list(p.rglob("*.md")) + list(p.rglob("*.html")) + \
        list(p.rglob("*.txt"))
    for f in files:
        text = f.read_text(encoding='utf-8')
        if f.suffix == '.html':
            text = BeautifulSoup(text, 'html.parser').get_text("\n")
        if f.suffix == '.md':
            html = markdown.markdown(text)
            text = BeautifulSoup(html, 'html.parser').get_text("\n")
        title = f.stem.replace('_', ' ').title()
        add_doc(doc_id=str(f), title=title, body=text)
    click.echo(f"Ingested {len(files)} files from {path}")


if __name__ == '__main__':
    cli()
