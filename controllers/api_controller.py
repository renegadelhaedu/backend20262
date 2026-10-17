from flask import Blueprint, jsonify

from repositories import user_repository
from services import project_service

api_bp = Blueprint("api", __name__)


@api_bp.get("/projetos")
def listar_projetos():
    projetos = project_service.listar_projetos()
    return jsonify([
        {
            "id": projeto.id,
            "titulo": projeto.title,
            "descricao": projeto.description,
            "requisitos": projeto.requirements,
            "criado_em": projeto.created_at.isoformat(),
            "professor": {
                "id": projeto.owner.id,
                "nome": projeto.owner.name,
            },
        }
        for projeto in projetos
    ])


@api_bp.get("/alunos")
def listar_alunos():
    alunos = user_repository.listar_alunos()

    return jsonify([
        {
            "id": aluno.id,
            "nome": aluno.name,
            "curso": aluno.course,
        }
        for aluno in alunos
    ])
