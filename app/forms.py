from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FloatField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, ValidationError, Optional
from flask_login import current_user

from app import db, bcrypt
from app.models import Usuario, Animal, Alimentacao, Saude, Vacina

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    btnSubmit = SubmitField('Entrar')

    def login(self):
        user = Usuario.query.filter_by(email=self.email.data).first()

        if (user):
            if (bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8'))):
                return user
            else:
                raise Exception('Senha incorreta!')
        else:
            raise Exception('Usuário não encontrado!')

class UsuarioForm(FlaskForm):
    nome = StringField('Nome Completo/Razão Social:', validators=[DataRequired()])
    documento = StringField('CPF/CNPJ:', validators=[DataRequired()])
    cep = StringField('CEP:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha:', validators=[DataRequired()])
    btnSubmit = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if (user):
            raise ValidationError('Email já cadastrado!')
        
    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))

        usuario = Usuario(
            nome = self.nome.data,
            documento = self.documento.data,
            cep = self.cep.data,
            email = self.email.data,
            senha = senha
        )
        
        db.session.add(usuario)
        db.session.commit()

        return usuario
    
class AnimalForm(FlaskForm):
    nome = StringField('Nome:', validators=[DataRequired()])
    especie = SelectField('Espécie:', choices=[
        ("Vaca", "Vaca"),
        ("Cabrito", "Cabrito"),
        ("Galinha", "Galinha"),
        ("Cavalo", "Cavalo"),
        ("Porco", "Porco"),
        ("Ovelha", "Ovelha"),
        ("Cachorro", "Cachorro"),
        ("Égua", "Égua"),
        ("Outro", "Outro")
    ], validators=[DataRequired()])
    data_nascimento = DateField("Data de Nascimento: ", validators=[DataRequired()])
    peso = FloatField('Peso (kg): ', validators=[Optional()])
    observacoes = TextAreaField('Observações: ')
    btnSubmit = SubmitField("Cadastrar Animal")

    def save(self, usuario_id):
        animal = Animal(
            nome = self.nome.data,
            especie = self.especie.data,
            data_nascimento = self.data_nascimento.data,
            peso = self.peso.data,
            observacoes = self.observacoes.data,
            usuario_id = usuario_id
        )

        db.session.add(animal)
        db.session.commit()

class AlimentacaoForm(FlaskForm):
    animal_id = SelectField("Animal:", coerce=int, validators=[DataRequired()])
    tipo_racao = StringField("Tipo de ração:", validators=[DataRequired()])
    quantidade = FloatField("Quantidade (kg):", validators=[DataRequired()])
    data_hora = DateTimeLocalField("Data e hora da alimentação:", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    btnSubmit = SubmitField("Cadastrar Alimentação")

    def save(self):
        alimentacao = Alimentacao(
            animal_id = self.animal_id.data,
            tipo_racao = self.tipo_racao.data,
            quantidade = self.quantidade.data,
            data_hora = self.data_hora.data
        )

        db.session.add(alimentacao)
        db.session.commit()

class SaudeForm(FlaskForm):
    animal_id = SelectField("Animal:", coerce=int, validators=[DataRequired()])
    doenca_condicao = StringField("Doença/Condição:", validators=[DataRequired()])
    tratamento = StringField("Tratamento:", validators=[DataRequired()])
    ultima_consulta = DateField("Data da consulta:")
    observacoes = TextAreaField("Observações:")
    btnSubmit = SubmitField("Cadastrar Saúde")

    def save(self):
        saude = Saude(
            animal_id = self.animal_id.data,
            doenca_condicao = self.doenca_condicao.data,
            tratamento = self.tratamento.data,
            ultima_consulta = self.ultima_consulta.data,
            observacoes = self.observacoes.data
        )

        db.session.add(saude)
        db.session.commit()

class VacinaForm(FlaskForm):
    animal_id = SelectField("Animal", coerce=int, validators=[DataRequired()])
    nome_vacina = StringField("Nome da vacina", validators=[DataRequired()])
    data_aplicacao = DateField("Data da aplicação: ", validators=[DataRequired()])
    prox_aplicacao = DateField("Proxima aplicação: ", validators=[DataRequired()])
    btnSubmit = SubmitField("Cadastrar Vacina")

    def save(self):
        vacina = Vacina(
            animal_id = self.animal_id.data,
            nome_vacina = self.nome_vacina.data,
            data_aplicacao = self.data_aplicacao.data,
            prox_aplicacao = self.prox_aplicacao.data
        )

        db.session.add(vacina)
        db.session.commit()
