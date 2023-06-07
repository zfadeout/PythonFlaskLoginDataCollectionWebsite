from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
#Hash's are able to secure a password which is able to be converted into something secure
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   
#Importing flask_login login_user, login_required, logout_user, and current_user
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

#Handling post requests ( so that login signup are able to accept post requests with GET and POST being requests )
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
#Form meaning all data was sent as a form
        email = request.form.get('email')
        password = request.form.get('password')
#Checking if user email and password is valid
        user = User.query.filter_by(email=email).first()
        if user:
            #Proccess of hasking the password and comparing it to the user password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                #Next line will login the user and "remember=true will remember that the user is logged in until they clear their browsing history or session"
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
#The root below makes sure that the user can't access contents below unless they are loggin in 
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
#Differentiating from get and post requests
    if request.method == 'POST':
#Using .get in order to obtain a specific atribute
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
#Flash function is used to flash a message
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #Creating a new user which is defined in models.py (line 2)
            #sha256 is a hash algorithm
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            #Adding new user to the database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            #Flashing the message
            flash('Account created!', category='success')
            #Redirecting the url for views.home to find what url maps to this function
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)