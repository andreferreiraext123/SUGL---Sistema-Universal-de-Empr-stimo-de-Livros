from flask import Flask

app = Flask(__name__)

# Importando as rotas
from app.routes.routes import *
