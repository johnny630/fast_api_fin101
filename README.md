# fast_api_fin101
fast api fin101

## Environment
python: 3.10.13 + pyenv + pip-tools

`python3 -m venv .venv`
`. .venv/bin/activate` activate the corresponding environment

install pip-tools
https://github.com/jazzband/pip-tools
1. `python -m pip install pip-tools`
2. create requirements.in and dev-requirements.in
3. `pip-compile` or `python -m piptools compile` will create `requirements.txt` file.
4. `pip-compile dev-requirements.in` will create `dev-requirements.txt` file.
5. `pip-sync dev-requirements.txt requirements.txt` 正式安裝 (只下`pip-sync` 只會執行requirements.txt)

## FastAPI
Create a main.py and simple ping API.
`uvicorn main:app --port 8000`  main is python main.py, app is FastAPI module
`uvicorn main:app --port 8000 --reload` development model, when code change server will auto reload.

## Alembic
Create SQLModel (Notice: circular import problem)
# https://sqlmodel.tiangolo.com/tutorial/code-structure/#make-circular-imports-work

```shell
pip install alembic

alembic init migrations
```
Then see the https://github.com/tiangolo/sqlmodel/issues/85 to revise code

Then continue run commands
```shell
alembic revision --autogenerate -m "init users and items table"
alembic upgrade head
```

If you want to downgrade
`alembic downgrade -1`

