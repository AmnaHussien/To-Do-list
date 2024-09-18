from flask import Blueprint, render_template, request, flash, redirect, url_for
from website import db
from website.models import User
from website.models import Task
import website.template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
#flask_login handle user authentication, manage user sessions
#flask_login works with any authentication method and can integrate with databases to manage user data.
auth = Blueprint('auth', __name__)

@auth.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        #hashing the pass before store it on db
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Error, Email Already Exist!', category='error')
        elif  not username:
            flash('Missing Username!', category='error')
        elif not email:
            flash('Missing E-mail!', category='error')
        elif password != password2:
            flash('Error, Password dons`t match!', category='error')
        elif not password:
            flash('Missing Password!',category='error')
        elif len(password) < 5:
            flash('Please use strong password!', category='error')
        else:
            new_user = User(username = username,  email = email, password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            flash('Accout Created Successfully!', category='successfull')
            login_user(new_user, remember = True)
            return redirect(url_for('views.home'))
    return  render_template('signup.html', user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='successful')
                login_user(user, remember=True)
                return(redirect(url_for('views.home')))
            else:
                flash('Wrong Password, Try again', category='error')
        else:
            flash('Error, User Not Found !', category='error')
    
    return render_template('login.html', user=current_user)
@auth.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    #clear session data bec it`s hold info about currently logged-in user
    logout_user()
    #redirect user for login page
    return redirect(url_for('auth.login'))

