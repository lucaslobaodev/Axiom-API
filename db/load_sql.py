from pathlib import Path

SQL_DIR = Path(__file__).parent.parent / "repository" / "sql"

def load_sql(filename: str) -> str:
    return (SQL_DIR / filename).read_text()
