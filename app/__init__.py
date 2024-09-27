# app/__init__.py

from flask import Flask

app = Flask(__name__)

# Importando as rotas
from app.routes.routes import *  # Certifique-se de que o caminho esteja correto

# Se você tiver configurações específicas, adicione aqui
# app.config.from_object('config')  # Se estiver usando config.py