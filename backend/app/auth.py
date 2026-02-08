from flask import request
from app.models import get_db
import jwt

SECRET_KEY = "chave-secreta"

def token_required():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None

    token = auth.split(" ")[1]

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM token_blacklist WHERE token = ?", (token,))
        if cur.fetchone():
            return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except Exception:
        return None
