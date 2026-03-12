from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, FloatField
from wtforms.validators import DataRequired, Email, ValidationError, Optional
from flask_login import current_user

from app import db, bcrypt
from app.models import Usuario, Animal

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

    def save(self):
        animal = Animal(
            nome = self.nome.data,
            especie = self.especie.data,
            data_nascimento = self.data_nascimento.data,
            peso = self.peso.data,
            observacoes = self.observacoes.data,
            usuario_id = current_user.id
        )

        db.session.add(animal)
        db.session.commit()
