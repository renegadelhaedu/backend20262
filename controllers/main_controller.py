from flask import Blueprint, abort, flash, redirect, render_template, url_for

from controllers.helpers import usuario_atual
from repositories import user_repository
from services import application_service, project_service

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if usuario_atual():
        return redirect(url_for("main.dashboard"))
    return render_template("index.html", current_user=None)


@main_bp.route("/painel")
def dashboard():
    user = usuario_atual()
    if not user:
        return redirect(url_for("auth.login"))
    projects = project_service.listar_projetos()
    if user.role == "professor":
        return render_template("professor_dashboard.html", projects=projects, current_user=user)
    applications = {a.project_id: a for a in application_service.listar_do_aluno(user.id)}
    return render_template(
        "student_dashboard.html", projects=projects, applications=applications,
        current_user=user,
    )


@main_bp.route("/alunos")
def students():
    user = usuario_atual()
    if not user:
        flash("Entre na sua conta para consultar os alunos.", "error")
        return redirect(url_for("auth.login"))
    if user.role != "professor":
        abort(403)
    return render_template(
        "students.html", students=user_repository.listar_alunos(), current_user=user
    )


@main_bp.route("/projetos/<int:project_id>/candidatar", methods=["POST"])
def apply(project_id):
    from services.application_service import ServiceError

    user = usuario_atual()
    if not user:
        flash("Entre na sua conta para continuar.", "error")
        return redirect(url_for("auth.login"))
    if user.role != "student":
        abort(403)
    try:
        application_service.candidatar(user, project_id)
    except LookupError:
        abort(404)
    except ServiceError as error:
        flash(str(error), "error")
    else:
        flash("Candidatura enviada. O professor proprietário vai avaliá-la.", "success")
    return redirect(url_for("main.dashboard"))
