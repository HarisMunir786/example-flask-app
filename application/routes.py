from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Post, User
from application.forms import RegisterForm, LoginForm, PostForm

@app.route('/')
@app.route('/home')
@login_required
def home():
    post = Post.query.first()
    return render_template('home.html', title='Home', post=post)

@app.route('/about')
def about():
        return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = User(
            email=register_form.email.data,
            password=bcrypt.generate_password_hash(register_form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(
            title=post_form.title.data,
            content=post_form.content.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html', title='Post', form=post_form)

