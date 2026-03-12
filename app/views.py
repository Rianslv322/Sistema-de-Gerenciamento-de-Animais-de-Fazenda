from app import app, db
from flask import render_template, url_for, request, redirect
from flask_login import login_user, logout_user, current_user, login_required

from app.models import Animal, Alimentacao
from app.forms import UsuarioForm, LoginForm, AnimalForm, AlimentacaoForm

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


# Rotas - Animais
@app.route('/animal', methods=['GET', 'POST'])
@login_required
def animal():
    animais = Animal.query.filter_by(usuario_id = current_user.id).all()
    return render_template('animal.html', animais=animais)

@app.route('/cadastro-animal', methods=['GET', 'POST'])
@login_required
def cadastro_animal():
    form = AnimalForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('animal'))
    return render_template('cadastro_animal.html', form=form)

@app.route('/editar-animal/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_animal(id):
    animal = Animal.query.get_or_404(id)

    form = AnimalForm(obj=animal)

    if form.validate_on_submit():
        form.populate_obj(animal)

        db.session.commit()

        return redirect(url_for('animal'))
    return render_template('cadastro_animal.html', form=form)

@app.route('/excluir-animal/<int:id>')
@login_required
def excluir_animal(id):
    animal = Animal.query.get_or_404(id)

    db.session.delete(animal)
    db.session.commit()

    return redirect(url_for('animal'))

# Rotas - Alimentação
@app.route('/alimentacao', methods=['GET', 'POST'])
@login_required
def alimentacao():
    alimentacoes = Alimentacao.query.join(Animal).filter(Animal.usuario_id == current_user.id).all()
    return render_template('alimentacao.html', alimentacoes=alimentacoes)

@app.route('/cadastro-alimentacao', methods=['GET', 'POST'])
@login_required
def cadastro_alimentacao():
    form = AlimentacaoForm()
    animais = Animal.query.filter_by(usuario_id=current_user.id).all()
    form.animal_id.choices = [(animal.id, f"{animal.nome} ({animal.especie})") for animal in animais]

    if form.validate_on_submit():
        form.save()
        return redirect(url_for('alimentacao'))

    return render_template('cadastro_alimentacao.html', form=form)

@app.route('/editar-alimentacao/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_alimentacao(id):
    alimentacao = Alimentacao.query.get_or_404(id)

    form = AlimentacaoForm(obj=alimentacao)
    animais = Animal.query.filter_by(usuario_id=current_user.id).all()
    form.animal_id.choices = [(animal.id, f"{animal.nome} ({animal.especie})") for animal in animais]

    if form.validate_on_submit():
        form.populate_obj(alimentacao)

        db.session.commit()

        return redirect(url_for('alimentacao'))
    return render_template('cadastro_alimentacao.html', form=form)

@app.route('/excluir-alimentacao/<int:id>')
@login_required
def excluir_alimentacao(id):
    alimentacao = Alimentacao.query.get_or_404(id)

    db.session.delete(alimentacao)
    db.session.commit()

    return redirect(url_for('alimentacao'))

# Rotas - Saúdes
@app.route('/saude')
@login_required
def saude():
    return render_template('saude.html')

# Rotas - Vacinas
@app.route('/vacinas')
@login_required
def vacinas():
    return render_template('vacinas.html')

# Rotas - Relatório
@app.route('/relatorio')
@login_required
def relatorio():
    return render_template('relatorio.html')
