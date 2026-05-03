from flask import Flask
from flask_cors import CORS
from config import config
from extensions import db, login_manager, limiter
from models import Admin

from routes.auth import auth_bp
from routes.opportunity import op_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config["development"])

    CORS(app, supports_credentials=True)

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    app.register_blueprint(auth_bp)
    app.register_blueprint(op_bp)

    return app


# ✅ THIS PART WAS MISSING
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)