import os

from flask import Flask

from banco import configurar_banco, db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "altere-esta-chave-antes-de-publicar"
    )

    configurar_banco(app)

    # Registra os modelos no SQLAlchemy antes de criar as tabelas.
    from models import User  

    with app.app_context():
        db.create_all()

    # As blueprints são importadas depois da inicialização da extensão. Nenhuma
    # camada importa este módulo, evitando dependências circulares com app.py.
    from controllers.auth_controller import auth_bp
    from controllers.main_controller import main_bp
    from controllers.professor_controller import professor_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(professor_bp, url_prefix="/professor")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
