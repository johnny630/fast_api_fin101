# fast_api_fin101
fast api fin101

## Environment
python: 3.10.2 + pyenv + pip-tools

`python3 -m venv .venv`
`. .venv/bin/activate` activate the corresponding environment

install pip-tools
https://github.com/jazzband/pip-tools
1. `python -m pip install pip-tools`
2. create requirements.in and dev-requirements.in
3. `pip-compile` or `python -m piptools compile` will create `requirements.txt` file.
4. `pip-compile dev-requirements.in` will create `dev-requirements.txt` file.
5. `pip-sync dev-requirements.txt requirements.txt` 正式安裝 (只下`pip-sync` 只會執行requirements.txt)