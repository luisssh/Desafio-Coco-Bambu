from app.models import init_db, get_db
from werkzeug.security import generate_password_hash
import os

if os.path.exists("database.db"):
    os.remove("database.db")

init_db()
conn = get_db()
cur = conn.cursor()

cur.execute("""
INSERT INTO users (name, email, password, is_superuser)
VALUES (?, ?, ?, 1)
""", ("Admin CocoBambu", "admin@email.com", generate_password_hash("admin123")))

conn.commit()
conn.close()

print("Admin criado: admin@email.com / admin123")
