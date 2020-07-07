from dotenv import load_dotenv
from pathlib import Path

# Hardcoded to be called from top folder, i.e, relative '..' path


def prepareDotEnv():
    load_dotenv()
    env_path = Path('..') / 'credentials.env'
    load_dotenv(dotenv_path=env_path)


def prepareDotEnvBot():
    load_dotenv()
    env_path = Path('..') / 'credentials_bot.env'
    load_dotenv(dotenv_path=env_path)
