from flask import Flask, render_template, redirect, request, session, url_for, flash
from tinydb import TinyDB, Query
import hashlib
import time
import os
import git
from pathlib import Path
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

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

#mail 
@app.route("/mail")
def mail():
	if session.get("username") != None:
		rsvp_code = db.search(query_db.email == session.get("username"))
		rsvp_code = str(hex(int(rsvp_code[0]["time"]))).lstrip("0x").upper() 
		
		rsvp_code = db.search(query_db.email == session.get("username"))
		# turns it into hex to shorten the code
		rsvp_code = str(hex(int(rsvp_code[0]["time"]))).lstrip("0x").upper() 
	
		users = db.search((query_db.code == rsvp_code) & (query_db.email != None))
		
		sucessStatus = True
		for users in db.search(query_db.code == rsvp_code ):
			if (sendmail(users["email"]) == False): # if any fails set status to false
				sucessStatus = False
				
		if (sucessStatus):
			flash("You have sent out reminders to set preferences for guest seating!", "success")
			return redirect(url_for('timeline'))
			
	flash("You have failed to send the email!", "danger")
	return redirect(url_for('login'))

def sendmail(usersemail):

	mail = Mail()
	mail.from_email = Email("RSVP@emails.pinchof.tech", "Wedding RSVP")
	mail.subject = "Set your seating preference!"

	personalization = Personalization()
	personalization.add_to(Email(usersemail))
	personalization.add_bcc(Email("RSVP@emails.pinchof.tech"))
	mail.add_personalization(personalization)
	mail.add_content(Content("text/html",'Please decide your seating by clicking the link: <br> ' + '<a href="http://chrisdesigns.pythonanywhere.com/pick?usercode=' + usersemail + '">Click here</a>'))
	
	mail.reply_to = Email("noreply@greenhawk.com")
	sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))	
	try:
		response =  sg.send(mail)
		if (response.status_code == 202 or response.status_code == 200):
			return True
	except Exception as e:
		print(e.message)
	return False

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
		return redirect(url_for('timeline'))
	return redirect(url_for('login'))
		

#Home page
@app.route('/')
def index():
    return render_template('index.html')

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
	if session.get("username") != None:
		return redirect(url_for('timeline'))
	if request.method == 'POST':
		email = request.form['email']
		
		password = request.form['pass']
		password = hashlib.md5(password.encode('utf-8')).hexdigest()
		if db.search((query_db.email == email) & (query_db.password == password)):

			session['username'] = email
			return redirect(url_for('timeline'))
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
		return redirect(url_for('timeline'))
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
			
			prefered = []
			for guest in generateSeating(templist, int(seats)):
				
				prefered.append([guest.name, str(guest.tableNum + 1)])
			return render_template("generated.html", guests=prefered)
		else:
			flash("Please enter more than one seat per table.", "danger")
			return redirect(url_for('seat'))
		
	return render_template('seat.html')

#RSVP rating system
@app.route('/pick', methods=['GET', 'POST'])
def pick():
	if request.args.get("usercode") != None:
		user = request.args.get("usercode")
		rsvp_code = db.search((query_db.email == user) & (query_db.code != None))
		guest_list = []
		
		if (len(rsvp_code) > 0):
			rsvp_code2 = rsvp_code[0]["code"]
			user_list = db.search((query_db.code == rsvp_code2) & (query_db.email != user))
			if request.method == 'POST':
				list = []
				splitList = []
				if "," in request.form['list']:
					splitList = request.form['list'].split(",")
				else:
					splitList.append(request.form['list'])
				for person in splitList:
					if (person != ""):
						email = db.search((query_db.code == rsvp_code2) & (query_db.name == person))
						print (person)
						list.append(email[0]["email"])
				db.update({'hateList': list}, query_db.email == user)
				flash("You have updated your seating preference. Please reference to see reflected values.", "success")
			for guest in user_list:
				guest_list.append([guest["name"], True if guest["email"] in rsvp_code[0]["hateList"] else False])
		else:
			flash("Invalid usercode: Please contact web-admins for new code.", "danger")
		return render_template('preferred.html', guests=guest_list)
	return redirect(url_for('rsvp'))

#Timeline page
@app.route('/timeline')
def timeline():
	if session.get("username") == None:
		return redirect(url_for('login'))
		
	# get the user's data
	rsvp_code = db.search(query_db.email == session.get("username"))
	# turns it into hex to shorten the code
	rsvp_code = str(hex(int(rsvp_code[0]["time"]))).lstrip("0x").upper() 
	
	data = db.search(query_db.code == rsvp_code)
	
	flash("A total of " + str(len(data))  + " people have RSVP'd for your wedding using your code: " + rsvp_code, "primary")
	return render_template('timeline.html')

#Budget 
@app.route('/budget', methods=['GET', 'POST'])
def budget():
	budget = 0
	ven_cost = 0
	cat_cost = 0
	ent_cost = 0
	per_cost = 0
	bar_cost = 0

	if session.get("username") == None:
		return redirect(url_for('login'))
	if request.method == 'POST':
		try:
			budget = int(request.form['budget'])
			ven_cost = int(request.form['ven-cost'])
			cat_cost = int(request.form['cat-cost'])
			ent_cost = int(request.form['ent-cost'])
			per_cost = int(request.form['per-cost'])
			bar_cost = int(request.form['bar-cost'])

			net_budget = ven_cost + ent_cost + per_cost + bar_cost + cat_cost
			budget_left = budget - net_budget

			if int(net_budget) > int(budget):
				flash("Warning: You are over the budget! Try cutting back on some of your costs", "danger")
				flash("Your Total Budget is $ " + str(budget) + "! You have spent $ " + str(net_budget),"danger")
				flash("You have: $ " + str(budget_left) + " left!" ,"danger")
				return redirect(url_for('budget'))
			elif (int(budget) > int(net_budget)):
				flash("Sucess! You are under budget! You're on your way!", "success")
				flash("Your Total Budget is $ " + str(budget) + "! You have spent $ " + str(net_budget),"success")
				flash("You have: $ " + str(budget_left) + " left!" ,"success")
				return redirect(url_for('budget'))
			elif (int(budget) == int(net_budget)):
				flash("Sucess! You are under budget! You're on your way!", "success")
				flash("You have: $ " + str(budget_left) + " left!" ,"success")
				return redirect(url_for('budget'))
			else:
				flash("Error: Make sure you filled in all the boxes!")
		
		except ValueError:
			flash("You left one or more boxes blank! Make sure you fill in all the boxes!", "danger")
		
	return render_template('budget.html')
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
		personsName = db.search((query_db.email == hateIndex) & (query_db.code != None))[0]["name"]
		if (personsName in table): # if person hates anyone at the table
			return False
	return True

def generateSeating(registered_people = [], seat_at_table = 0):
	processing_people= []
	wont_work = []
	processing_people = registered_people[:] # Everyone Ready for processing
	atTable  = [] # temp list of people at the table
	expected_tables = 0
	while (len(processing_people) > 0 ):
		for guest in processing_people: # for everyone at the party
			if (seat_at_table != len(atTable)): # check if table full
				if worksForTable(guest, atTable):
					atTable.append(guest.name) # store the name of this person in the array
					registered_people[registered_people.index(guest)].tableNum = expected_tables # set the table number for the person
					processing_people.remove(guest) # remove from being processed
				elif (len(processing_people) == len(wont_work)): # if we got through everyone and won't work we have to make a new table.
					expected_tables += 1
					del atTable[:]
					del wont_work[:]
				else:
					wont_work.append(guest.name)
			else:
				expected_tables += 1
				del atTable[:]
				del wont_work[:]
	registered_people.sort()
	return registered_people

###remove later
#to run locally just type 'python3 home.py'
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port=5000)
