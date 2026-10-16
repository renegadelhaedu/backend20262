from banco import db
from models import Application


def buscar_por_id(application_id):
    return db.session.get(Application, application_id)


def buscar_do_aluno_no_projeto(student_id, project_id):
    return Application.query.filter_by(student_id=student_id, project_id=project_id).first()


def listar_do_aluno(student_id):
    return Application.query.filter_by(student_id=student_id).all()


def listar_do_projeto(project_id):
    return Application.query.filter_by(project_id=project_id).order_by(Application.created_at).all()


def salvar(application):
    db.session.add(application)
    db.session.commit()
    return application


def atualizar(application):
    db.session.commit()
    return application
