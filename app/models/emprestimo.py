from app import db

class Emprestimo(db.Model):
    __tablename__ = 'emprestimos'
    id = db.Column(db.Integer, primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livros.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_expiracao = db.Column(db.Date, nullable=False)

    livro = db.relationship('Livro', backref=db.backref('emprestimos', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('emprestimos', lazy=True))
