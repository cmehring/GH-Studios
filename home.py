from flask import Flask, render_template, redirect, request, session, url_for
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
			print "Failed"
			
	return render_template('login.html', form=1234)