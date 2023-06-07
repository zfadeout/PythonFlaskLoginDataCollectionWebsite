#Creating database models
#Importing from the website folder package db not DB.NAME
from . import db
#Flask_login is a module that helps users log in and Usermixin is where the user object needs to inherit from
from flask_login import UserMixin
#importing a function named func to let sqlalchemy to get current date and time mentioned in line 13
from sqlalchemy.sql import func

#Database model essentially conveying to python that all notes need to look like this
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
#ID field is going to be an interger, db.ForeignKey is to pass the value of an existing user to this field (One to many relationship)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#Defining a layout or structure using columns within the imorted sql database: db
class User(db.Model, UserMixin):
#Our id is primary_key which is the uniqe identifier 
    id = db.Column(db.Integer, primary_key=True)
#Strings with maximum length and unique=true means that no user can have an identical email as anothe user
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
#Used to access user notes
    notes = db.relationship('Note')