from models import User
from repositories import user_repository


class ServiceError(Exception):
    pass


def cadastrar(name, email, password, role, course=""):
    if role not in ("professor", "student"):
        raise ServiceError("Tipo de cadastro inválido.")
    if not name or not email or len(password) < 8:
        raise ServiceError("Preencha nome e e-mail; a senha deve ter ao menos 8 caracteres.")
    if user_repository.buscar_por_email(email):
        raise ServiceError("Este e-mail já está cadastrado.")
    user = User(name=name, email=email, role=role, course=course or None)
    user.set_password(password)
    return user_repository.salvar(user)


def autenticar(email, password):
    user = user_repository.buscar_por_email(email)
    return user if user and user.check_password(password) else None
