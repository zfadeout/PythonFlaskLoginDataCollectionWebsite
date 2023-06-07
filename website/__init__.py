#Creating a flask app
#Importing SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#os stands for opperating system
from os import path
#Importing loginManager to manage the login as specified
from flask_login import LoginManager

#Initializing SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"

#Function named create app
def create_app():
    #File name
    app = Flask(__name__)
    #Security for cookies on the website
    app.config['SECRET_KEY'] = 'blyat suka majit'
#File to store SQLAlchemy database
#Using the f string to store the database in the "website" folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
#Telling the database that this is the app that is being used
    db.init_app(app)

#Importing views and auth
    from .views import views
    from .auth import auth

#Registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all()

#After creating the database0
    login_manager = LoginManager()
    #Redirecting the user if they are not logged in to 'auth.login'
    login_manager.login_view = 'auth.login'
    #Telling login_manager which app we are using
    login_manager.init_app(app)

#Telling flask how to load a user while looking for a specific user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#The function below will create a database if there is not an existing database
def create_database(app):
#Checking if the database exists 
    if not path.exists('website/' + DB_NAME):
#If it does not then we create it
        db.create_all(app=app)
        print('Created Database!')