# Projeto Aberto

Aplicação Flask para professores publicarem projetos acadêmicos e alunos se candidatarem. O professor proprietário é o único que pode aceitar ou recusar candidaturas.

## Organização do código

- `app.py`: fábrica da aplicação e registro das blueprints.
- `banco.py`: configuração da conexão e instância SQLAlchemy.
- `models.py`: modelos persistidos.
- `controllers/`: rotas agrupadas em blueprints, uma por arquivo.
- `services/`: regras de negócio.
- `repositories/`: consultas e gravações no banco.

As camadas não importam `app.py`. A extensão é declarada em `banco.py` e conectada à aplicação pela fábrica `create_app()`, evitando importações circulares.

## Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000. O banco SQLite `projetos.db` é criado automaticamente.

## Executar com Gunicorn

```bash
export SECRET_KEY='uma-chave-secreta-forte'
gunicorn --bind 0.0.0.0:8000 app:app
```

Por padrão, SQLite grava o banco em `instance/projetos.db`. Para usar outro endereço, configure `DATABASE_URL`, por exemplo `sqlite:////caminho/absoluto/projetos.db`.
