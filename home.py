from flask import Flask, render_template, redirect, request, session, url_for, flash
from tinydb import TinyDB, Query
import hashlib
import time

db = TinyDB('database/db.json')
User = Query()

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'gr33nh4wkplsnoh4x5' # technically, this shouldn't be pushed


@app.route('/')
def index():
    return render_template('index.html', name=123)
	
@app.route('/login', methods=['GET', 'POST'])
def login():	 
	if request.method == 'POST':
		user = request.form['user']
		
		password = request.form['pass']
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		if db.search((User.name == user) & (User.password == password)):

			session['username'] = user
			return redirect(url_for('index'))
		else:
			flash('Invalid username or password')
			
	return render_template('login.html', form=1234)
	
@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("You have been logged-out.")
   return redirect(url_for('login'))
   
	
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
	
		user = request.form['user']
		email = request.form['email']
		password = request.form['pass']
		password2 = request.form['pass2']
		
		if password != password2:
			flash('Your passwords do not match.')
			return render_template('signup.html', form=1234)
		elif user and email and password and password2:
			password = hashlib.md5(password.encode('utf-8')).hexdigest()
			db.insert({'time': time.time(),'name': user, 'email': email,'password': password})
			flash("You have successfully signed-up!")
			return redirect(url_for('login'))
	else:
		return render_template('signup.html', form=1234)

#Python FlaskTest.py
if __name__ == '__main__':
    app.run(debug=True)