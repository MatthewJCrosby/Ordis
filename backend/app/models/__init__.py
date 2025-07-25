import os
import importlib
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def load_models():
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"{__name__}.{filename[:-3]}"
            importlib.import_module(module_name)
