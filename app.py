"""Punto de entrada de la aplicación MiniCore – Comisiones (Flask, patrón MVC)."""
import os

from flask import Flask

from controllers.comision_controller import comision_bp
from models import db
from seed import cargar_datos

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "minicore.db")
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=os.getenv("SECRET_KEY", "dev-minicore"),
    )
    if config:
        app.config.update(config)

    # Render entrega URLs "postgres://"; SQLAlchemy necesita "postgresql://"
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if uri.startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = uri.replace("postgres://", "postgresql://", 1)

    db.init_app(app)
    app.register_blueprint(comision_bp)

    with app.app_context():
        db.create_all()
        cargar_datos()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
