import os
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from db.load_sql import load_sql

load_dotenv()

_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

def get_connection():
    return _pool.getconn()

def release_connection(conn):
    _pool.putconn(conn)

def execute_query(
        filename: str, 
        params: tuple = None, 
        fetch: bool = False
        ):
    
    conn = get_connection()
    
    try:
        with conn.cursor(
            cursor_factory=RealDictCursor
            ) as cursor:
            cursor.execute(
                load_sql(filename), params
                )
            if fetch:
                return cursor.fetchall()
            conn.commit()
    finally:
        release_connection(conn)
