from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
#create db instance
db = SQLAlchemy() 
DATA_BN = 'sqlite3.db'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATA_BN}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SECRET_KEY'] = 'abcdefghijk'
    #init db using flask app
    db.init_app(app)
    
    #import Blueprint
    from .views import views
    from .auth import auth
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    from .models import user, task
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    
def create_db(app):
    if not path.exists('website/' + DATA_BN):
        db.create_all(app=app)
        print("DataBase Created Successsfully!")
