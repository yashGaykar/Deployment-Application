"""SETTINGS FILE"""

import os
from dotenv import load_dotenv

DOTENV_PATH = '.env'
load_dotenv(DOTENV_PATH)

SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
BROKER_URL=os.environ.get("BROKER_URL")
BACKEND_URL=os.environ.get("BACKEND_URL")
