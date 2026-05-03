from flask import Blueprint, request, jsonify, current_app
from flask_login import login_user, logout_user
from models import db, Admin
from itsdangerous import URLSafeTimedSerializer
import re

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def is_valid_email(email):
    return re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)


def generate_token(admin):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return s.dumps({"id": admin.id, "email": admin.email}, salt="reset")


def verify_token(token):
    s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        return s.loads(token, salt="reset", max_age=3600)
    except:
        return None


@auth_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm = data.get("confirmPassword")

        if not all([name, email, password, confirm]):
            return jsonify({"error": "All fields required"}), 400

        if not is_valid_email(email):
            return jsonify({"error": "Invalid email"}), 400

        if password != confirm:
            return jsonify({"error": "Passwords do not match"}), 400

        if Admin.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 409

        admin = Admin(full_name=name, email=email)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        return jsonify({"success": True, "user": admin.to_dict()}), 201

    except:
        db.session.rollback()
        current_app.logger.error("Signup error", exc_info=True)
        return jsonify({"error": "Server error"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        admin = Admin.query.filter_by(email=data.get("email")).first()

        if not admin or not admin.check_password(data.get("password")):
            return jsonify({"error": "Invalid email or password"}), 401

        login_user(admin, remember=data.get("rememberMe", False))

        return jsonify({"success": True, "user": admin.to_dict()})

    except:
        return jsonify({"error": "Server error"}), 500


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot():
    try:
        email = request.get_json().get("email")
        admin = Admin.query.filter_by(email=email).first()

        if admin:
            token = generate_token(admin)
            current_app.logger.info(f"RESET LINK: {token}")

        return jsonify({"success": True})

    except:
        return jsonify({"error": "Server error"}), 500


@auth_bp.route("/reset-password", methods=["POST"])
def reset():
    try:
        data = request.get_json()

        payload = verify_token(data.get("token"))

        if not payload:
            return jsonify({"error": "Invalid token"}), 400

        admin = Admin.query.get(payload["id"])
        admin.set_password(data.get("new_password"))

        db.session.commit()

        return jsonify({"success": True})

    except:
        db.session.rollback()
        return jsonify({"error": "Server error"}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"success": True})