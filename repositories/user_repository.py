from banco import db
from models import User


def buscar_por_id(user_id):
    return db.session.get(User, user_id)


def buscar_por_email(email):
    return User.query.filter_by(email=email).first()


def listar_alunos():
    return User.query.filter_by(role="student").order_by(User.name).all()


def salvar(user):
    db.session.add(user)
    db.session.commit()
    return user
