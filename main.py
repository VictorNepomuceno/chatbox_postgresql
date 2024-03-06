from flask import  render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Chat, User
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
import bcrypt


def check_password(password, hash_password):
    return bcrypt.checkpw(password.encode('utf-8'), hash_password)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':    
        name = request.form['name']
        password = request.form['pwd']
        user = User.query.filter_by(name=name).first()

        if user and check_password(password, user.password):
            login_user(user)
            flash(f'Bem vindo(a) {user.name}! Aproveite o Real Chat!', 'success')
            return redirect(url_for('dashboard')) 
        else:
            flash('Usuário ou senha inválidos', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['pwd']
            user = User(name=name, email=email, phone=phone, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Registro feito com sucesso!', 'success')
            return redirect(url_for('login'))
    except IntegrityError:
        flash("Email ou Usuário já cadastrado, tente novamente", 'error')
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')



app.run(debug=True)