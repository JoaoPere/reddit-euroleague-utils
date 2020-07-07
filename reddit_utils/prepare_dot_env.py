from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('..') / 'credentials_bot.env'
load_dotenv(dotenv_path=env_path)
