from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from controllers.helpers import usuario_atual
from services.auth_service import ServiceError, autenticar, cadastrar

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro/<role>", methods=["GET", "POST"])
def register(role):
    if role not in ("professor", "student"):
        abort(404)
    if request.method == "POST":
        try:
            user = cadastrar(
                request.form.get("name", "").strip(),
                request.form.get("email", "").strip().lower(),
                request.form.get("password", ""), role,
                request.form.get("course", "").strip(),
            )
        except ServiceError as error:
            flash(str(error), "error")
        else:
            session["user_id"] = user.id
            flash("Cadastro realizado com sucesso.", "success")
            return redirect(url_for("main.dashboard"))
    return render_template("register.html", role=role, current_user=usuario_atual())


@auth_bp.route("/entrar", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = autenticar(request.form.get("email", "").strip().lower(),
                          request.form.get("password", ""))
        if user:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.dashboard"))
        flash("E-mail ou senha incorretos.", "error")
    return render_template("login.html", current_user=usuario_atual())


@auth_bp.route("/sair", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("main.index"))
