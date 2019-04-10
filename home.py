from flask import Flask, render_template, redirect, request, session, url_for, flash
from tinydb import TinyDB, Query
import hashlib
import time

db = TinyDB('database/db.json')
User = Query()

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'gr33nh4wkplsnoh4x5' # technically, this shouldn't be pushed

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
		user = request.form['user']
		
		password = request.form['pass']
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		if db.search((User.name == user) & (User.password == password)):

			session['username'] = user
			return redirect(url_for('dash'))
		else:
			flash('Invalid username or password')
			
	return render_template('login.html')

#Logout page
@app.route('/logout')
def logout():
   session.pop('username', None)
   flash("You have been logged-out.")
   return redirect(url_for('login'))
   
#Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if session.get("username") != None:
		return redirect(url_for('dash'))
	elif request.method == 'POST':
	
		user = request.form['user']
		email = request.form['email']
		password = request.form['pass']
		password2 = request.form['pass2']
		
		if password != password2:
			flash('Your passwords do not match.')
			return render_template('signup.html')
		elif user and email and password and password2:
			password = hashlib.md5(password.encode('utf-8')).hexdigest()
			db.insert({'time': time.time(),'name': user, 'email': email,'password': password})
			flash("You have successfully signed-up!")
			return redirect(url_for('login'))
	else:
		return render_template('signup.html')

#dashboard page
@app.route('/dash')
def dash():
	if session.get("username") == None:
		return redirect(url_for('login'))
	return render_template('dash.html')

#seating page
@app.route('/seat', methods=['GET', 'POST'])
def seat():
	if session.get("username") == None:
		return redirect(url_for('login'))
	if request.method == 'POST':
		seats = request.form['seats']
		templist = []
		
		p1 = Person("John")
		p2 = Person("Sarah", [0])
		p3 = Person("Jim")
		p4 = Person("Bill")
		templist.append(p1)
		templist.append(p2)
		templist.append(p3)
		templist.append(p4)
		
		for guest in generateSeating(templist, int(seats)):
			print ("Person: " + guest.name + " is sitting at: " + str(guest.tableNum))
		
	return render_template('seat.html')


class Person:
	def __init__(self, name, hatesID = [], loveID= []):
		self.name = name
		self.hatesID = hatesID
		self.loveID = loveID
		self.tableNum = None
		
def worksForTable(person, table): # Person can sit at the table
	for hateIndex in person.hatesID: # for everyone they hate
		if (hateIndex in table): # if person hates anyone at the table
			return False
	return True

def generateSeating(registered_people = [], seat_at_table = 0):
	processing_people= []
	processing_people = registered_people.copy() # Everyone Ready for processing
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
				atTable.clear()
			
	return registered_people;


###remove later
#to run locally just type 'python3 home.py'
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)