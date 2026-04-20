from psycopg2 import pool, errors as pg_errors
from psycopg2.extras import RealDictCursor
from db.load_sql import load_sql
from core.config import settings
from core.logger import setup_logger

logger = setup_logger(__name__)

_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    dbname=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
)

def get_connection():
    return _pool.getconn()

def release_connection(conn):
    _pool.putconn(conn)

def execute_query(filename: str, params: tuple = None, fetch: bool = False):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(load_sql(filename), params)
            if fetch:
                return cursor.fetchall()
            conn.commit()
    except pg_errors.UniqueViolation:
        conn.rollback()
        logger.warning("tentativa de inserção duplicada", extra={"filename": filename})
        raise ValueError("duplicate")
    except Exception as e:
        conn.rollback()
        logger.error("erro na query", extra={"filename": filename, "error": str(e)})
        raise
    finally:
        release_connection(conn)
