from models import Application
from repositories import application_repository, project_repository


class ServiceError(Exception):
    pass


def candidatar(student, project_id):
    project = project_repository.buscar_por_id(project_id)
    if not project:
        raise LookupError("Projeto não encontrado.")
    if application_repository.buscar_do_aluno_no_projeto(student.id, project.id):
        raise ServiceError("Você já se candidatou a este projeto.")
    return application_repository.salvar(Application(student_id=student.id, project_id=project.id))


def listar_do_projeto(project_id):
    return application_repository.listar_do_projeto(project_id)


def listar_do_aluno(student_id):
    return application_repository.listar_do_aluno(student_id)


def decidir(application_id, professor, decision):
    if decision not in ("aceitar", "recusar"):
        raise LookupError("Decisão inválida.")
    application = application_repository.buscar_por_id(application_id)
    if not application:
        raise LookupError("Candidatura não encontrada.")
    if application.project.owner_id != professor.id:
        raise PermissionError
    application.status = "Aceita" if decision == "aceitar" else "Recusada"
    return application_repository.atualizar(application)
