from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.models import user
import bcrypt
from website import db
from flask_login import login_user, login_required, logout_user, current_user
#flask_login handle user authentication, manage user sessions
#flask_login works with any authentication method and can integrate with databases to manage user data.
auth = Blueprint('auth', __name__)

@auth.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        pasword = request.form.get('passowrd')
        password2 = request.form.get('password2')
        hashed_passw = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())
        user = user.query.filter_by(email).first()
        if user:
            print("Error, Email Already Exist!")
        elif  not username:
            return "Missing username!"
        elif not email:
            return "Missing email!"
        elif pasword != password2:
            return "Error, Password dont match"
        elif not password:
            return "Missing password!"
        elif length(password) < 5:
            return "Please use strong password!"
        #hashing the pass before store it on db
        else:
            new_user = user(username = username, password = hashed_passw, email = email)
            db.session.add(user)
            db.session.commit()
            login_user(new_user, remeber = True)
            return f"Accout Created Successfully!"
            return redirect(url_of('views.home'))
    return  render_tempelete('register.html', user=current_user)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('passowrd')
        if not email:
            return "Missing Email!"
        if not password:
            return "Missing Passowd!"
    #using query to db to determine if the user of this email is found or not
        user = user.query.filter_by(email = email).first()
        if not user:
            return "User Not Found!"
    #when user is found , determine if the password match the hashed password, else: the pass is wrong
        else:
            if bcrypt.checkpw(password.encode("UTF-8"), user.hashed_passw):
        #When a user logs in, the server creates a session for that user
        #This session can store the user’s ID, indicating that they are authenticated
        #session["user_id"] = user.i
                login_user(user, remeber=True)
                return redirect(url_for('views.home'))
            else:
                return "Wrong Password!"
    return render_tempelete('login.html', user=current_userl, title="Login To-Do List")
@auth.route('/logout')
@login_required
def logout():
    #clear session data bec it`s hold info about currently logged-in user
    logout_user()
    #redirect user for another page such like login page
    return redirect(url_for('login'))

