from app import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, login_required

from app.forms import UsuarioForm, LoginForm, AnimalForm

@app.route('/')
def home():
    if (current_user.is_authenticated):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = UsuarioForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/sair')
def sair():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/animal')
@login_required
def animal():
    return render_template('animal.html')

@app.route('/cadastro-animal', methods=['GET', 'POST'])
@login_required
def cadastro_animal():
    form = AnimalForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('animal'))
    return render_template('cadastro_animal.html', form=form)

@app.route('/alimentacao')
@login_required
def alimentacao():
    return render_template('alimentacao.html')

@app.route('/saude')
@login_required
def saude():
    return render_template('saude.html')

@app.route('/vacinas')
@login_required
def vacinas():
    return render_template('vacinas.html')

@app.route('/relatorio')
@login_required
def relatorio():
    return render_template('relatorio.html')
