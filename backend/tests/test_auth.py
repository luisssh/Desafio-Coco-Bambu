import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models import get_db
from werkzeug.security import generate_password_hash


def setup_admin():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT OR IGNORE INTO users (id, name, email, password, is_superuser)
            VALUES (?, ?, ?, ?, ?)
        """, (
            1,
            "Admin",
            "admin@email.com",
            generate_password_hash("admin123"),
            1
        ))
        conn.commit()


def test_login_ok():
    app = create_app()
    app.testing = True
    client = app.test_client()

    setup_admin()

    res = client.post("/login", json={
        "email": "admin@email.com",
        "password": "admin123"
    })

    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_login_fail():
    app = create_app()
    app.testing = True
    client = app.test_client()

    res = client.post("/login", json={
        "email": "admin@email.com",
        "password": "errada"
    })

    assert res.status_code == 401


def test_profile_sem_token():
    app = create_app()
    app.testing = True
    client = app.test_client()

    res = client.get("/profile")
    assert res.status_code == 401
