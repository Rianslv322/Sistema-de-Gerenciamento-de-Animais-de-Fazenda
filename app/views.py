from app import app
from flask import render_template, url_for

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

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

