from app import db, login_manager
from flask_login import UserMixin
from datetime import date, datetime

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
    monitoramento = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

    alimentacoes = db.relationship("Alimentacao", back_populates="animal", lazy=True)
    saudes = db.relationship("Saude", back_populates="animal", lazy=True)
    vacinas = db.relationship("Vacina", back_populates="animal", lazy=True)

    @property
    def idade(self):
        hoje = date.today()

        anos = hoje.year - self.data_nascimento.year
        meses = hoje.month - self.data_nascimento.month

        if hoje.day < self.data_nascimento.day:
            meses -= 1

        if meses < 0:
            anos -= 1
            meses += 12

        return f"{anos} anos e {meses} meses"

class Alimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_racao = db.Column(db.String(100), nullable=False)    
    quantidade = db.Column(db.Float, nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)

    animal = db.relationship("Animal", back_populates="alimentacoes", lazy=True)

class Saude(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doenca_condicao = db.Column(db.String(100), nullable=False) 
    tratamento = db.Column(db.String(100), nullable=False) 
    ultima_consulta = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)

    animal = db.relationship("Animal", back_populates="saudes", lazy=True)

class Vacina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_vacina = db.Column(db.String(150), nullable=False)
    data_aplicacao = db.Column(db.Date, nullable=False)
    prox_aplicacao = db.Column(db.Date)
    animal_id = db.Column(db.Integer, db.ForeignKey("animal.id"), nullable=False)

    animal = db.relationship("Animal", back_populates="vacinas", lazy=True)
