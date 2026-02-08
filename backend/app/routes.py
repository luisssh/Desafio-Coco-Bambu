from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import get_db
from app.auth import token_required
import jwt, datetime, sqlite3

routes = Blueprint("routes", __name__)
SECRET_KEY = "chave-secreta"

@routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = jwt.encode({
        "user_id": user["id"],
        "is_superuser": bool(user["is_superuser"]),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"access_token": token}), 200

@routes.route("/profile", methods=["GET"])
def profile():
    payload = token_required()
    if not payload:
        return jsonify({"error": "Token inválido"}), 401

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, name, email, is_superuser
            FROM users WHERE id = ?
        """, (payload["user_id"],))
        user = cur.fetchone()

    return jsonify(dict(user)), 200

@routes.route("/users", methods=["GET"])
def list_users():
    payload = token_required()
    if not payload or not payload["is_superuser"]:
        return jsonify({"error": "Acesso negado"}), 403

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email, is_superuser FROM users")
        users = [dict(u) for u in cur.fetchall()]

    return jsonify({"users": users}), 200

@routes.route("/users", methods=["POST"])
def create_user():
    payload = token_required()
    if not payload or not payload["is_superuser"]:
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, email, password, is_superuser)
            VALUES (?, ?, ?, ?)
        """, (
            data["name"],
            data["email"],
            generate_password_hash(data["password"]),
            int(data.get("is_superuser", 0))
        ))
        conn.commit()

    return jsonify({"msg": "Usuário criado"}), 201

@routes.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    payload = token_required()
    if not payload or not payload["is_superuser"]:
        return jsonify({"error": "Acesso negado"}), 403

    data = request.get_json()
    fields = []
    values = []

    if "name" in data:
        fields.append("name = ?")
        values.append(data["name"])

    if "email" in data:
        fields.append("email = ?")
        values.append(data["email"])

    if "password" in data:
        fields.append("password = ?")
        values.append(generate_password_hash(data["password"]))

    values.append(user_id)

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(f"""
            UPDATE users SET {", ".join(fields)}
            WHERE id = ?
        """, values)
        conn.commit()

    return jsonify({"msg": "Usuário atualizado"}), 200

@routes.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    payload = token_required()
    if not payload or not payload["is_superuser"]:
        return jsonify({"error": "Acesso negado"}), 403

    if payload["user_id"] == user_id:
        return jsonify({"error": "Você não pode se excluir"}), 400

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

    return jsonify({"msg": "Usuário removido"}), 200
