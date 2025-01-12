from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField
from wtforms.validators import InputRequired, Length, Email, Regexp, EqualTo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from call_json_server import RewardsPortalDB
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import os
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'photos')
 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
 
db = RewardsPortalDB()
current_day = datetime.utcnow().date().isoformat()
print("This is from app.py")
 
class User(UserMixin):
    def __init__(self, id):
        self.id = id
 
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
 
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20, message="Username must be between 4 and 20 characters")])
    first_name = StringField('First Name', validators=[InputRequired(), Regexp(r'^[a-zA-Z\s]+$', message="Only text allowed in the first name")])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name', validators=[InputRequired(), Regexp(r'^[a-zA-Z\s]+$', message="Only text allowed in the last name")])
    email_address = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=8, max=20, message='Password must be between 8 and 20 characters'),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+])[a-zA-Z0-9!@#$%^&*()_+]+$', message='Password must contain at least one uppercase letter, one lowercase letter, and one special character')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        InputRequired(),
        EqualTo('password', message='Passwords must match')
    ])                        
    photo = FileField('Photo', validators=[InputRequired()])
 
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    # Add other fields similar to the ones in the login form
 
class PersonalDetailsForm(FlaskForm):
   
    first_name = StringField('First Name', validators=[InputRequired(), Regexp(r'^[a-zA-Z\s]+$', message="Only text allowed in the first name")])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name', validators=[InputRequired(), Regexp(r'^[a-zA-Z\s]+$', message="Only text allowed in the last name")])
    email_address = StringField('Email', validators=[InputRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[InputRequired()])                        
    photo = FileField('Photo', validators=[InputRequired()])
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
    #if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        email_address = request.form['email_address']                                                                                              
        phone_number = request.form['phone_number']
        photo = request.files['photo']  # Handle file upload
        filename = f"{username}.{photo.filename.split('.')[-1]}"
        file_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(file_path)
        user_data = {
        "username":username,
        "password":password,
        "user_details": {
          "first_name": first_name,
          "middle_name": middle_name,
          "last_name": last_name,
          "photo": filename,
          "phone_number": phone_number,
          "email_address": email_address
        },
        "reward_points": 0,
        "signup_details": {
          "signup_date": datetime.utcnow().isoformat(),
        },
        "login_details": {
          "last_login_date": None,
          "current_login_date": current_day
        }
    }
        user_exists = db.user_exists(username)
        if user_exists:
            flash('Username already exists. Please choose another username.', 'error')
            return redirect(url_for('signup'))
 
        # Add user to the database (db.add_user(user_data)) - Use your database logic here
        db.add_user(user_data)
 
        session['username'] = username  # Store username in session upon successful signup
        flash('Sign up successful! Here is your dashboard.', 'success')
        return redirect(url_for('dashboard'))
 
    return render_template('signup.html', form=form)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['active_session']=True
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.find_user(username, password)
        if user:
            session['username'] = username  # Store username in session upon successful login
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template('login.html')
 
@app.route('/logout')
def logout():
    session['active_session']=False
    session.pop('username', None)  # Remove username from session upon logout
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))
 
 
@app.route('/personal_details', methods=['GET', 'POST'])
def personal_details():
   
    if 'username' in session and session['active_session']:
        user_details = db.get_user_details(session['username'])
        form = PersonalDetailsForm()
        if request.method == 'POST':
 
            first_name = user_details['first_name']
            middle_name = user_details['middle_name']
            last_name = user_details['last_name']
            email_address = user_details['email_address']
            phone_number = user_details['phone_number']
 
           # first_name = request.form['first_name']
            # middle_name = request.form['middle_name']
          #  last_name = request.form['last_name']
          #  email_address = request.form['email_address']
          #  phone_number = request.form['phone_number']
 
            updated_details = {
                "first_name":first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email_address": email_address,
                "phone_number": phone_number
            }
            db.update_personal_details(session['username'], updated_details)
            8
            # Handle photo upload
            if 'photo' in request.files:
                photo = request.files['photo']
                if photo.filename != '':
                    filename = secure_filename(photo.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    photo.save(file_path)
                    # Update the user's photo in the database
                    updated_details['photo'] = filename
                    db.update_personal_details(session['username'], updated_details)
 
            flash('Personal details updated successfully!', 'success')
            return redirect(url_for('personal_details'))
 
        return render_template('personal_details.html', user=user_details)
    else:
        flash('Please log in to view personal details.', 'error')
        return redirect(url_for('login'))
 
@app.route('/dashboard')
def dashboard():
    if 'username' in session and session['active_session']:
        return render_template('dashboard.html')
    else:
        flash('You need to login to access the dashboard.', 'error')
        return redirect(url_for('login'))
 
if __name__ == '__main__':
    app.run(debug=True)