from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from controllers.helpers import exigir_perfil
from services import application_service, project_service
from services.project_service import ServiceError as ProjectServiceError

professor_bp = Blueprint("professor", __name__)


@professor_bp.route("/projetos/novo", methods=["GET", "POST"])
def create_project():
    user = exigir_perfil("professor")
    if not user:
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        try:
            project_service.criar_projeto(
                user, request.form.get("title", "").strip(),
                request.form.get("description", "").strip(),
                request.form.get("requirements", "").strip(),
            )
        except ProjectServiceError as error:
            flash(str(error), "error")
        else:
            flash("Projeto publicado.", "success")
            return redirect(url_for("main.dashboard"))
    return render_template("project_form.html", current_user=user)


@professor_bp.route("/projetos/<int:project_id>")
def project_applications(project_id):
    user = exigir_perfil("professor")
    if not user:
        return redirect(url_for("auth.login"))
    project = project_service.buscar_projeto(project_id)
    if not project:
        abort(404)
    if project.owner_id != user.id:
        abort(403)
    applications = application_service.listar_do_projeto(project.id)
    return render_template(
        "applications.html", project=project, applications=applications, current_user=user
    )


@professor_bp.route("/candidaturas/<int:application_id>/<decision>", methods=["POST"])
def decide_application(application_id, decision):
    user = exigir_perfil("professor")
    if not user:
        return redirect(url_for("auth.login"))
    try:
        application = application_service.decidir(application_id, user, decision)
    except LookupError:
        abort(404)
    except PermissionError:
        abort(403)
    flash("Candidatura atualizada.", "success")
    return redirect(url_for("professor.project_applications", project_id=application.project_id))
