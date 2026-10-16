from flask import abort, flash, session

from repositories import user_repository


def usuario_atual():
    user_id = session.get("user_id")
    return user_repository.buscar_por_id(user_id) if user_id else None


def exigir_perfil(role):
    user = usuario_atual()
    if not user:
        flash("Entre na sua conta para continuar.", "error")
        return None
    if user.role != role:
        abort(403)
    return user
