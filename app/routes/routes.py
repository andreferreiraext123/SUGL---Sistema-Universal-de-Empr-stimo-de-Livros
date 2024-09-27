# app/routes/routes.py

from flask import render_template
from app import app  # Importa a instância da app

@app.route('/')
def formulario_livro():
    return render_template('form.html')  # Certifique-se de que esse arquivo existe em app/templates

@app.route('/submit', methods=['POST'])
def submit_livro():
    return "Formulário enviado com sucesso!"
