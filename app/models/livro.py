from app import db

class Livro(db.Model):
    __tablename__ = 'livros'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    autor = db.Column(db.String(255), nullable=False)
    ano_publicacao = db.Column(db.Integer)
    genero = db.Column(db.String(100))
    valor = db.Column(db.Numeric(10, 2))
