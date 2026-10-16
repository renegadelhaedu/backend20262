from banco import db
from models import Project


def buscar_por_id(project_id):
    return db.session.get(Project, project_id)


def listar_todos():
    return Project.query.order_by(Project.created_at.desc()).all()


def salvar(project):
    db.session.add(project)
    db.session.commit()
    return project
