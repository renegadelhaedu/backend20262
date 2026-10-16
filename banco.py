import os

from flask_sqlalchemy import SQLAlchemy

# A extensão é declarada sem aplicação aqui e associada em create_app().
db = SQLAlchemy()

'''
Se for usar postgresql:
pip install "psycopg[binary]"
export DATABASE_URL="postgresql+psycopg://usuario:senha@localhost:5432/nome_do_banco"

'''


def configurar_banco(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///projetos.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
