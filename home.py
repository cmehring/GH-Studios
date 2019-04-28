from flask import Flask, render_template, redirect, request, session, url_for, flash
from tinydb import TinyDB, Query
import hashlib
import time
import os
import git
from pathlib import Path

dirname = os.path.dirname(os.path.abspath(__file__))

# Database stuff
dataPath = os.path.join(dirname, 'database')
if not os.path.exists(dataPath):
		os.makedirs(dataPath)
		file = open(dataPath + '/db.json', 'w')
		file.write("")
		file.close()
		
db = TinyDB(os.path.join(dirname, 'database', 'db.json'))
query_db = Query()

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'gr33nh4wkplsnoh4x5' # technically, this shouldn't be pushed

#Git stuff
@app.route('/update')
def update():
	if session.get("username") != None:
		g = git.cmd.Git(dirname)
		g.reset('--hard')
		g.pull()
		# if pythonanywhere sever reset it by touching this file
		if os.path.isfile('/var/www/chrisdesigns_pythonanywhere_com_wsgi.py'):
			Path('/var/www/chrisdesigns_pythonanywhere_com_wsgi.py').touch()
		flash("You have updated the server.", "success")
		return redirect(url_for('dash'))
	return redirect(url_for('login'))
		

#Home page
@app.route('/')
def index():
    return render_template('index.html')

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	if session.get("username") != None:
		return redirect(url_for('dash'))
	if request.method == 'POST':
		email = request.form['email']
		
		password = request.form['pass']
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		if db.search((query_db.email == email) & (query_db.password == password)):

			session['username'] = email
			return redirect(url_for('dash'))
		else:
			flash('Invalid username or password', "danger")
			
	return render_template('login.html')

#Logout page
@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("You have been logged-out.", "success")
   return redirect(url_for('login'))
   
#Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if session.get("username") != None:
		return redirect(url_for('dash'))
	elif request.method == 'POST':
	
		name = request.form['name']
		email = request.form['email']
		password = request.form['pass']
		password2 = request.form['pass2']
		
		if password != password2:
			flash('Your passwords do not match.', "danger")
			return redirect(url_for('index'));
		elif name and email and password and password2:
			if (not db.contains(query_db.email == email)):
				password = hashlib.md5(password.encode('utf-8')).hexdigest()
				db.insert({'time': round(time.time()),'name': name, 'email': email,'password': password})
				flash("You have successfully signed-up!", "success")
			else:
				flash("This username already exits.", "danger")
				return redirect(url_for('index'));
			return redirect(url_for('login'))
			
		flash('You did not fill in one of the inputs!', "danger")
		return redirect(url_for('index'));
	else:
		return redirect(url_for('index'));

#Dashboard page
@app.route('/dash')
def dash():
	if session.get("username") == None:
		return redirect(url_for('login'))
	# get the user's data
	rsvp_code = db.search(query_db.email == session.get("username"))
	# turns it into hex to shorten the code
	rsvp_code = str(hex(int(rsvp_code[0]["time"]))).lstrip("0x").upper() 
	
	data = db.search(query_db.code == rsvp_code)
	
	flash("A total of " + str(len(data))  + " people have RSVP'd for your wedding using your code: " + rsvp_code, "primary")
	
	return render_template('dash.html')
#RSVP system
@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		code = request.form['code']
		# prepares the code to turn into hex
		codeHex = "0x" + code.lower()
		# turns the hex to int and compares it to db to fine if exists
		data = db.search(query_db.time == int(codeHex, 16))
		if (len(data) >= 1):
			db.insert({'code':  code,'name': name, 'email': email, 'hateList': {}, 'loveList': {}}) # todo: check if email exists to prevent duplicates
			flash("You have registered for " + data[0]["name"] + "'s wedding", "success")
		else:
			flash("This wedding code appears to be invalid.", "danger")
	return render_template('rsvp.html')
#Seating page
@app.route('/seat', methods=['GET', 'POST'])
def seat():
	if session.get("username") == None:
		return redirect(url_for('login'))
	if request.method == 'POST':
		seats = request.form['seats']
		templist = []
		# get the user's data
		rsvp_code = db.search(query_db.email == session.get("username"))
		# turns it into hex to shorten the code
		rsvp_code = str(hex(int(rsvp_code[0]["time"]))).lstrip("0x").upper() 
	
		data = db.search(query_db.code == rsvp_code)	
		
		if (int(seats) > 0):
			for person in data:
				templist.append(Person(person["name"], person["hateList"], person["loveList"]))
				
			for guest in generateSeating(templist, int(seats)):
				flash("Person: " + guest.name + " is sitting at: " + str(guest.tableNum + 1), "success")
		else:
			flash("Please enter more than one seat per table.", "danger")
			return redirect(url_for('seat'))
		
	return render_template('seat.html')
#RSVP system
@app.route('/pick')
def pick():
	return render_template('preferred.html')
#Timeline page
@app.route('/timeline')
def timeline():
	if session.get("username") == None:
		return redirect(url_for('login'))
	return render_template('timeline.html')

class Person:
	def __init__(self, name, hatesID = [], loveID= []):
		self.name = name
		self.hatesID = hatesID
		self.loveID = loveID
		self.tableNum = None
	def __lt__(self, other):
		return self.tableNum < other.tableNum
		
def worksForTable(person, table): # Person can sit at the table
	for hateIndex in person.hatesID: # for everyone they hate
		if (hateIndex in table): # if person hates anyone at the table
			return False
	return True

def generateSeating(registered_people = [], seat_at_table = 0):
	processing_people= []
	processing_people = registered_people[:] # Everyone Ready for processing
	atTable  = [] # temp list of people at the table
	expected_tables = 0
	while (len(processing_people) > 0 ):
		for guest in processing_people: # for everyone at the party
			if (seat_at_table != len(atTable)): # check if table full
				if worksForTable(guest, atTable):
					atTable.append(registered_people.index(guest)) # store the index value of this person in the array
					registered_people[registered_people.index(guest)].tableNum = expected_tables # set the table number for the person
					processing_people.remove(guest) # remove from being processed
			else:
				expected_tables += 1
				del atTable[:]
	registered_people.sort()
	return registered_people


###remove later
#to run locally just type 'python3 home.py'
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)