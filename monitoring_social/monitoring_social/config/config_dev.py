from pathlib import Path

from decouple import Config, RepositoryEnv

BASE_ENV_DIR = Path(__file__).resolve().parent.parent

DOTENV_FILE = f'{BASE_ENV_DIR}/.env.dev'
config = Config(RepositoryEnv(DOTENV_FILE))


NAME = config.get('NAME')
USER = config.get('USER')
PASSWORD = config.get('PASSWORD')
HOST = config.get('HOST')
PORT = config.get('PORT')
DJANGO_SECRETE_KEY_DEV = config.get('DJANGO_SECRETE_KEY')

