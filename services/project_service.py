from models import Project
from repositories import project_repository


class ServiceError(Exception):
    pass


def listar_projetos():
    return project_repository.listar_todos()


def criar_projeto(owner, title, description, requirements=""):
    if not title or not description:
        raise ServiceError("Informe o título e a descrição do projeto.")
    return project_repository.salvar(Project(
        title=title, description=description, requirements=requirements, owner_id=owner.id
    ))


def buscar_projeto(project_id):
    return project_repository.buscar_por_id(project_id)
