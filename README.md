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

## API de consulta

A blueprint `controllers/api_controller.py` disponibiliza endpoints HTTP somente de leitura que retornam JSON:

- `GET /api/projetos`: lista projetos com título, descrição, requisitos, data de publicação e nome/ID do professor.
- `GET /api/alunos`: lista alunos com ID, nome e curso.

Esses endpoints não usam JWT nem outra autenticação. Restrinja o acesso ao servidor por firewall ou proxy para que fique disponível somente às máquinas e redes autorizadas. A resposta de alunos omite e-mail e outros dados de conta.

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

## Deploy com Docker Compose e PostgreSQL

Na máquina de deploy, clone o projeto, copie `.env.example` para `.env`, troque `POSTGRES_PASSWORD` e `SECRET_KEY` por valores fortes e inicie os serviços:

```bash
cp .env.example .env
# Edite .env antes de iniciar. Uma senha hexadecimal gerada por `openssl rand -hex 24`
# é adequada aqui, pois a senha faz parte da URL de conexão.
docker compose up -d --build
```

A aplicação fica disponível na porta definida por `APP_PORT` (8000 por padrão). O PostgreSQL não publica sua porta para a rede: só a aplicação no Compose o acessa. Os dados ficam no volume nomeado `postgres_data`; `docker compose down` preserva o volume. Para apagar o banco junto com os containers, seria necessário remover explicitamente esse volume.

O Compose limita a aplicação a 256 MB e o PostgreSQL a 512 MB, com um worker Gunicorn e parâmetros modestos para uma máquina de 1 GB. Ajuste esses limites se o sistema encerrar algum container por falta de memória. Faça backups regulares do banco.
