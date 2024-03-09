from flask import  render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Chat, User, Comment
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
import bcrypt
from datetime import datetime


@app.errorhandler(401)
def unauthorized(error):
    flash('Você precisa fazer login para acessar esta página.', 'error')
    return redirect(url_for('login'))

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
            flash(f'Bem vindo(a) {user.name}! Aproveite o Real Blog!', 'success')
            return redirect(url_for('feed')) 
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

@app.route('/new_post')
@login_required
def new_post():
    return render_template('create_post.html', username=current_user.name)
 
@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        chat = request.form['chat']
        if len(chat) > 1500:
            flash('O limite do post é de 1500 caracteres.', 'error')
            return redirect('new_post')
        username = request.form['username']
        data = Chat(username=username,title=title, chat=chat )
        db.session.add(data)
        db.session.commit()
        flash('Postagem feita com sucesso!', 'success')
        return redirect(url_for('feed'))

@app.route('/feed')
@login_required
def feed():
    data = Chat.query.all()
    return render_template("feed.html", data=data, user=current_user)


@app.route('/post_detail/<int:id>', methods=['GET', 'POST'])
@login_required
def post_detail(id):
    post = Chat.query.get_or_404(id)
    comment = Comment.query.filter_by(post_id=id).all()

    if request.method == 'POST':
        username = request.form['name']
        comment = request.form['comment']
        data = Comment(post_id=id,username=username, comment=comment)
        db.session.add(data)
        db.session.commit()
        flash('Comentário enviado com sucesso')
        return redirect(url_for('post_detail', id=id))
    
    return render_template('post_detail.html', post=post, comment=comment, user=current_user)


@app.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Chat.query.get_or_404(id)

    if post.username == current_user.name:
        db.session.delete(post)
        db.session.commit()
        flash('Post removido com sucesso!', 'success')
        return redirect(url_for('feed'))
    else:
        flash('Você não possui essa permissão.', 'error')
        return redirect(url_for('feed'))
    

@app.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(name=username).first()
    if user:
        data = Chat.query.filter_by(username=username).all()
        return render_template('profile.html', username=username, data=data)
    else:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('feed'))
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
def about():
    return render_template('about.html')



app.run(debug=True)