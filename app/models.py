from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    documento = db.Column(db.String(255), unique=True, nullable=False)
    cep = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)

    animais = db.relationship('Animal', backref='usuario', lazy=True)


    def primeiro_nome(self):
        return self.nome.split()[0]
    
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    peso = db.Column(db.Float)
    observacoes = db.Column(db.Text)

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
