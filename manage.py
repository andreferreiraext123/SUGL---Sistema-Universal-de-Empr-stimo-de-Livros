from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inicializando a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializando o banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importando os modelos
from app.models import livro, usuario, emprestimo

if __name__ == '__main__':
    app.run(debug=True)
