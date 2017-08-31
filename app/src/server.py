from src import app
from flask import jsonify, request
import requests
import json
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
#from flask_mysqldb import MySQL
#from data import Articles
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField
#from passlib.hash import sha256_crypt
from functools import wraps

#check if logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash('Unauthorized, please log in','danger')
            return redirect(url_for('login'))
    return wrap

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

class RegisterForm(Form):
	name=StringField('Name',[validators.Length(min=1,max=30)])
	username=StringField('Username',[validators.Length(min=1,max=100)])
	email=StringField('Email',[validators.Length(min=1,max=50)])
	password=PasswordField('Password',[
		validators.DataRequired(),
		validators.EqualTo('confirm',message='Passwords do not match')
		])
	confirm=PasswordField('Confirm Password')
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password=form.password.data
        url = 'http://auth.c100.hasura.me/signup'
        data = {'username': username, 'password': password}
        headers = {'Content-Type' : 'application/json'}

        r = requests.post(url, data=json.dumps(data), headers=headers)
        #a=r.json()
        #token=a['auth_token']

        #return json.dumps(r.json(), indent=4)
        #return r['auth_token']
        '''
        mysqldb things:-
        cur=mysql.connection.cursor()
        cur.execute("insert into users(name,email,username,password) values (%s, %s, %s, %s)",(name,email,username,password))
        mysql.connection.commit()
        cur.close()'''
        flash('You are now registered','success')
        return redirect(url_for('index'))
    return render_template('register.html',form=form)

#login part
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username= request.form['username']
        password=request.form['password']
        #making request to login endpoint
        url = 'http://auth.c100.hasura.me/login'
        data = {'username': username, 'password': password}
        headers = {'Content-Type' : 'application/json'}
        try:

            r = requests.post(url, data=json.dumps(data), headers=headers)
            a=r.json()
            token=a['auth_token']
            if r.status_code==200:
                if token:
                    flash("You are now logging in","success")
                    return redirect(url_for('home'))
                else:
                    flash('Password wrong','warning')
                    return redirect(url_for('login'))


            else:
                error='Something is fishy! Try again.'
                flash(error,"warning")
                return redirect(url_for('login'))


        except Exception as e:
            print(e)
            flash("Invalid Credentials or Credentials don't match","warning")
            return redirect(url_for('login'))



        '''
        old mysqldb version:-
        cur=mysql.connection.cursor()

        #get user by username
        result=cur.execute("select * from users where username=%s",[username])
        if result>0:
            data=cur.fetchone()
            password=data['password']
            #compare the passwords
            if sha256_crypt.verify(password_candidate,password):
                session['logged_in']=True
                session['username']=username
                flash('You are now logged in','success')
                return redirect(url_for('dashboard'))
            else:
                error='Password wrong'
                return render_template('login.html',error=error)
            #close connection
            cur.close()
        else:
            error='Username not found'
            return render_template('login.html',error=error)
            '''

    return render_template('login.html')
