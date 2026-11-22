# Captchas gen

A CAPTCHAS GEN project.

## Structure

```
CAPTCHASGEN/
├── client/
│   ├── src/
│   │   ├── main.py            # Ponto de entrada: login e menu principal
│   │   ├── app.py             # Gera a imagem de CAPTCHA
│   │   ├── captcha/
│   │   │   └── generator.py   # Cria a imagem; nos CAPTCHAs de texto, risca o código com traços
│   │   ├── captchas/          # Menu para criar, ver, editar e eliminar CAPTCHAs
│   │   │   ├── desafios.py    # Gera e resolve os desafios de cada tipo
│   │   │   ├── repositorio.py # Guarda os CAPTCHAs de cada utilizador na base de dados
│   │   │   └── imagem.py      # Mostrar no terminal / baixar a imagem de um CAPTCHA de texto
│   │   ├── config/
│   │   │   └── settings.py    # Tamanhos, cores, texto, pasta de saída
│   │   ├── storage/
│   │   │   ├── db.py          # Ligação e criação da base de dados SQLite
│   │   │   └── file_storage.py# Guarda a imagem em PNG
│   │   ├── user/
│   │   │   ├── main.py        # Menu de login / criação de conta
│   │   │   ├── accounts.py    # Criação de conta
│   │   │   └── login.py       # Início de sessão
│   │   └── utils/
│   │       ├── colors.py      # Cores aleatórias
│   │       └── terminal.py    # Mostra imagens no terminal
│   └── output/                # Imagens geradas (ignorada pelo git)
├── database/                  # databasecode.sql (esquema) e db.sqlite (ignorado pelo git)
├── tests/                     # Mesma estrutura que client/src/
│   ├── captcha/
│   ├── captchas/
│   ├── storage/
│   ├── user/
│   ├── utils/
│   └── test_app.py
├── pytest.ini                 # Diz ao pytest para importar a partir de client/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate    
pip install -r requirements.txt
```

## Run

```bash
cd client
python -m src.main        # Aplicação completa: login e depois menu principal
```

Cada parte também pode ser corrida sozinha:

```bash
python -m src.app         # Gera um CAPTCHA
python -m src.user.main   # Menu de login / criação de conta
python -m src.captchas.main  # Menu de gestão de CAPTCHAs
```

## Test

```bash
pip install pytest
pytest
```

## Git Workflow

All work goes through the `develop` branch. Do not commit directly to `main` or `develop`.

1. **Create a branch from `develop`**
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/your-feature-name
   ```
2. **Open a Pull Request into `develop`** once your changes are ready.
3. **Merge into `develop`** only after the PR has been reviewed and approved.
4. **Merge `develop` into `main`** as the final step, once everything on `develop` is complete and stable.

