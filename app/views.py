from app import app
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user

from app.forms import UsuarioForm

@app.route('/')
def home():
    pass

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = UsuarioForm()
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/cadastro-animal')
def cadastro_animal():
    return render_template('cadastro_animal.html')

@app.route('/saude-animal')
def saude_animal():
    return render_template('saude_animal.html')

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html')

@app.route('/relatorio-status')
def relatorio_status():
    return render_template('relatorio_status.html')

@app.route('/relatorio-alimentacao')
def relatorio_alimentacao():
    return render_template('relatorio_alimentacao.html')

@app.route('/relatorio-saude')
def relatorio_saude():
    return render_template('relatorio_saude.html')