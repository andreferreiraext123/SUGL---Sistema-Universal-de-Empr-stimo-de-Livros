from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime
from app import app  # Importa a instância da app

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="biblioteca",
        user="postgres",
        password="postgres"
    )
    return conn


# Rota principal, que renderiza o formulário e a lista de livros
@app.route('/')
def formulario_livro():
    conn = get_db_connection()
    cur = conn.cursor()

    # Obter a lista de livros e o status de empréstimo
    cur.execute("""
        SELECT l.id, l.titulo, CASE 
            WHEN e.livro_id IS NOT NULL THEN 'Emprestado'
            ELSE 'Disponível'
        END AS status
        FROM Livros l
        LEFT JOIN Emprestimos e ON l.id = e.livro_id
    """)
    
    livros = cur.fetchall()

    # Obter a lista de livros disponíveis
    cur.execute("SELECT id FROM Livros WHERE id NOT IN (SELECT livro_id FROM Emprestimos)")
    livros_disponiveis = cur.fetchall()

    cur.close()
    conn.close()
    #print(livros_disponiveis)
    return render_template('index.html', livros=livros, livro_pesquisado=None, livros_disponiveis=livros_disponiveis)


# Rota para cadastro de livros
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

# Rota para pesquisar um livro pelo ID
@app.route('/search', methods=['GET'])
def search_livro():
    search_id = request.args['search']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, titulo, autor FROM Livros WHERE id = %s', (search_id,))
    livro_pesquisado = cur.fetchone()
    cur.execute("""
        SELECT l.id, l.titulo, CASE 
            WHEN e.livro_id IS NOT NULL THEN 'Emprestado'
            ELSE 'Disponível'
        END AS status
        FROM Livros l
        LEFT JOIN Emprestimos e ON l.id = e.livro_id
    """)
    
    livros = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', livros=livros, livro_pesquisado=livro_pesquisado)


# Rota para realizar empréstimo de livro
@app.route('/loan', methods=['POST'])
def loan_livro():
    nome = request.form['nome']
    email = request.form['email']
    livro_id = request.form['livro_id']
    print(livro_id)
    # Ajuste para garantir que estamos lidando com o valor correto
    livro_id = int(livro_id)
    print(livro_id)

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




# Rota para atualizar o status do livro
@app.route('/update_status', methods=['POST'])
def update_status():
    livro_id = request.form['livro_id']
    conn = get_db_connection()
    cur = conn.cursor()

    # Verifica se o livro está emprestado
    cur.execute('SELECT * FROM Emprestimos WHERE livro_id = %s', (livro_id,))
    emprestimo = cur.fetchone()

    if emprestimo:
        # Se está emprestado, remove o empréstimo, tornando o livro disponível
        cur.execute('DELETE FROM Emprestimos WHERE livro_id = %s', (livro_id,))
    else:
        # Se está disponível, cria um empréstimo fictício para teste (use seus dados reais)
        cur.execute('INSERT INTO Emprestimos (livro_id, usuario_id, data_inicio, data_expiracao) VALUES (%s, 1, NOW(), NOW() + INTERVAL \'7 days\')', (livro_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('formulario_livro'))



# Rota para excluir livro
@app.route('/delete/<int:livro_id>', methods=['POST'])
def delete_livro(livro_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Exclui o livro e qualquer empréstimo associado
    cur.execute('DELETE FROM Emprestimos WHERE livro_id = %s', (livro_id,))
    cur.execute('DELETE FROM Livros WHERE id = %s', (livro_id,))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('formulario_livro'))
