from flask import render_template, request, redirect, url_for
import psycopg2
from datetime import datetime
from app import app  # Importa a instância da app

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password="postgres"
    )
    return conn

@app.route('/')
def formulario_livro():
    return render_template('index.html')  # Certifique-se de que esse arquivo existe em app/templates

@app.route('/submit', methods=['POST'])
def submit_livro():
    titulo = request.form['titulo']
    autor = request.form['autor']
    data = request.form['ano']
    genero = request.form['genero']
    valor = request.form['valor']

    try:
        ano_publicacao = datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        return "Formato de data inválido. Por favor, insira a data no formato AAAA-MM-DD."

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO Livros (titulo, autor, ano_publicacao, genero, valor) VALUES (%s, %s, %s, %s, %s)',
                (titulo, autor, ano_publicacao, genero, valor))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('formulario_livro'))

@app.route('/search', methods=['GET'])
def search_livro():
    search_id = request.args['search']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Livros WHERE id = %s', (search_id,))
    livro = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('index.html', livro=livro)

@app.route('/loan', methods=['POST'])
def loan_livro():
    nome = request.form['nome']
    email = request.form['email']
    livro_id = int(request.form['livro_id'])
    data_inicio = request.form['data_inicio']
    data_expiracao = request.form['data_expiracao']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO Usuarios (nome, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING RETURNING id', (nome, email))
    usuario_id = cur.fetchone() if cur.rowcount > 0 else None

    if usuario_id is None:
        cur.execute('SELECT id FROM Usuarios WHERE email = %s', (email,))
        usuario_id = cur.fetchone()

    cur.execute('INSERT INTO Emprestimos (livro_id, usuario_id, data_inicio, data_expiracao) VALUES (%s, %s, %s, %s)',
                (livro_id, usuario_id, data_inicio, data_expiracao))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('formulario_livro'))
