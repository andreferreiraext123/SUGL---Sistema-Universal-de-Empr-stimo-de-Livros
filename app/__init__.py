from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configurando a aplicação com as configurações do arquivo config.py
app.config.from_object(Config)

# Inicializando o banco de dados
db = SQLAlchemy(app)

# Importando as rotas
from app.routes.routes import *  # Certifique-se de que o caminho esteja correto

# Criando as tabelas no banco de dados
with app.app_context():
    db.create_all()
