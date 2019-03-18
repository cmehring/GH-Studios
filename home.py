from flask import Flask, render_template, redirect, request, session, url_for, flash
from werkzeug.security import check_password_hash
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
		if user == "admin" and password == "1234":
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