import os

from flask import Flask

from banco import configurar_banco, db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "altere-esta-chave-antes-de-publicar"
    )

    configurar_banco(app)

    from models import User  

    with app.app_context():
        db.create_all()


    from controllers.auth_controller import auth_bp
    from controllers.api_controller import api_bp
    from controllers.main_controller import main_bp
    from controllers.professor_controller import professor_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(professor_bp, url_prefix="/professor")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5190, debug=os.environ.get("FLASK_DEBUG") == "1")
