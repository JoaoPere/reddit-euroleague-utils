from dotenv import load_dotenv
from pathlib import Path


def get_bot_credentials():
    load_dotenv()
    env_path = Path('..') / 'credentials_bot.env'
    load_dotenv(dotenv_path=env_path)


def get_test_credentials():
    load_dotenv()
    env_path = Path('..') / 'credentials.env'
    load_dotenv(dotenv_path=env_path)
