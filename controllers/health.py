from fastapi import APIRouter, HTTPException
from db.connection import get_connection, release_connection

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="banco indisponível")
    finally:
        if conn:
            release_connection(conn)
