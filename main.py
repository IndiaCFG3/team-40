from datetime import datetime

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy.orm import relationship, backref
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = "Thisisasecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anudip.db'
db= SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


Bootstrap(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(15))
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))
    location = db.Column(db.String(100),nullable=False)
    contact = db.Column(db.String(15),unique=True)
    type = db.Column(db.Integer)
    op_id = db.Column(db.Integer)

class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(15), nullable=False)
    contact = db.Column(db.String(15),unique=True, nullable=False)
    email = db.Column(db.String(50),unique=True)
    qual = db.Column(db.String(50))
    age =  db.Column(db.Integer)
    gender = db.Column(db.String(10))
    prev_courses = db.Column(db.String(50))
    course_preference = db.Column(db.String(50))

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    location = db.Column(db.String(100),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    date_time = db.Column(db.DATETIME,nullable=False)
    status = db.Column(db.BOOLEAN,default=False)
    mob_id = db.Column(db.Integer)

class Target(db.Model):
    __tablename__ = 'target'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    mob_id = db.Column(db.Integer)
    op_id = db.Column(db.Integer)
    target_count = db.Column(db.Integer)
    date_posted = db.Column(db.DATETIME,nullable=False,default=datetime.now)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    email = StringField("Email Id", validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Invalid Email ID"), Length(max=50)])
    location = StringField("Location", validators=[InputRequired(), Length(min=4, max=15)])
    contact = StringField("Contact", validators=[InputRequired(), Length(min=10, max=10)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(form.email.data)
        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember.data)
                if user.type==2:
                    return redirect('/mobiliser/dashboard')
                else:
                    return redirect('/dashboard')
        return '<h1>Invalid Email and password</h1>'+str(user)


    if form.validate_on_submit():
        return form.email.data + form.password.data

    return render_template('login.html', form=form)


@app.route('/signup',methods=['GET','POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method='sha256')
        new_user = User(name=form.name.data,email=form.email.data,password=hashed_password,location=form.location.data,contact=form.contact.data)
        db.session.add(new_user)
        db.session.commit()
        redirect('/login')

    return render_template('signup.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard_manager():
    return render_template('dashboard.html',user=current_user.name)

@app.route('/mobiliser/dashboard')
@login_required
def dashboard_mob():
    return render_template('mobdashboard.html',user=current_user.name)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if request.method == 'POST':
        print("hello")
        user = User.query.filter_by(id=current_user.id).first()
        user.name = request.form['name']
        user.contact = request.form['contact']
        user.center = request.form['center']
        db.session.commit()
        redirect('/profile')
    return render_template('userprofile.html',user=current_user)

@app.route('/event/add',methods=['GET','POST'])
@login_required
def add_event():
    if request.method == "POST":
        event = Event(name=request.form['eve_name'],location=request.form['eve_location'],date_time=  datetime.strptime(request.form['eve_date']+" "+request.form['eve_time'], '%Y-%m-%d %H:%M'),mob_id=current_user.id)
        db.session.add(event)
        db.session.commit()
        redirect('/event/add')
    return render_template('eventform.html',user=current_user)

@app.route('/report',methods=['GET','POST'])
@login_required
def show_report():
    mob = User.query.filter_by(op_id=current_user.id).all()

    return render_template('operationalReport.html',mob=mob,user=current_user)

@app.route('/myevents',methods=['GET','POST'])
@login_required
def show_myevents():
    events = Event.query.filter_by(mob_id=current_user.id,status='0').all()

    return render_template('mobEvents.html',events=events,user=current_user)

@app.route('/editevent/<int:id>',methods=['GET','POST'])
@login_required
def edit_myevent(id):
    event = Event.query.filter_by(id = id).first()
    print(str(event.name))
    return render_template('eventFormEdit.html',event=event,user=current_user)

@app.route("/upload/<int:id>", methods=['GET', 'POST'])
def upload_file(id):
    if request.method == 'POST':
        request.get_array(field_name='file')

    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (csv, tsv, csvz, tsvz only)</h1>
    <form action="" method='POST' enctype=multipart/form-data>
    <p><input type='file' name='file'><input type='submit' value='Upload'></p>
   </form>
    '''

@app.route('/newuser',methods=['GET','POST'])
@login_required
def newuser():
    if request.method == 'POST':
        print("Hello")
        hashed_password = generate_password_hash(password=request.form['user_pass'],method='sha256')
        user = User(name=request.form['user_name'],email=request.form['user_email'],location=request.form['user_loc'],contact=request.form['user_pno'],password=hashed_password,type=request.form['type'])
        db.session.add(user)
        db.session.commit()
        redirect('/newuser')

    return render_template('newuser.html',user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
