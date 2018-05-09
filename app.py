#Name   :Edgars Rozenstams
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_table import Table, Col, LinkCol
from passlib.hash import sha256_crypt #password hashing
from functools import wraps

#from logging.config import dictConfig

from dbconnect import Connect, registerUser, registerProperty, getUserProps, getAllProps, updateUser,Search

app = Flask(__name__)
app.secret_key = 'dad555ass34dawddasfrjegb/1kjbvr/o'

Counties = []

def getCounties():
    with open("Counties.txt", "r") as c:
        for line in c:
            Counties.append(line.strip())


getCounties()

class propTable(Table):
	
	classes = ['proptable'] #table css class
	
	User = Col('User', show=False)
	Addres = Col('Addres')
	cost = Col('Cost')
	description = Col('Description')
	amenities = Col('Amenities')
	Bedrooms = Col('Bedrooms')
	bathrooms = Col('Bathrooms')

# passes the counties to the rent search in the template
@app.context_processor
def inject_counties():
    return dict(counties = Counties)
    
    
@app.route('/')
def Home():
    properties = getAllProps()
    return render_template('home.html', title = 'Home',properties = properties)

@app.route('/rent', methods=["GET","POST"])
def Rent():
    if request.form["submit"]:

        session['location'] = request.form['county']
        session['minCost'] = request.form['minPrice']
        session['maxCost'] = request.form['maxPrice']
        session['minBed'] = request.form['minBed']
        session['maxBed'] = request.form['maxBed']

    #flash([session['location'],minCost, maxCost, minBed, maxBed])

    session['searchProps'] = Search(session['location'],session['minCost'], session['maxCost'], session['minBed'], session['maxBed'])

    return render_template('results.html' , title = 'Rent', properties = session['searchProps'])

@app.route('/account')
def Account():
    fname = session['userData']['name']
    lname = session['userData']['surname']
    email = session['userData']['email']
    phone = session['userData']['phone']

    properties = getUserProps(session['userData']['email'])
    table = propTable(properties)

    return render_template('account.html', title = 'Account', fname = fname , lname = lname, email = email, phone = phone, table=table)

@app.route('/login')
def Login():
    return render_template('login.html', title = 'Account Login')

@app.route('/ProcessLogin',methods=["GET","POST"])
def AccountLogin():
    db = Connect()
    users = db.TestColl
    
    if request.form["submit"]:

        data = users.find_one({"email": request.form['Email']},{'_id': 0}) #strips the _id as the obj type has problems ,{'_id': 0}
		
        session['userData'] = data
        psw = data['password']  #gets the password from the json document 
        
        if sha256_crypt.verify(request.form['Password'],psw): ##if the hashed input password is equal to the hashed saved password
            session['logged_in'] = True
            session['username'] = data['name'] #users name
            
            flash("You are now Logged in ")
            return redirect(url_for("Account"))

        else:
             flash("Invalid Credentials, try again")
             return render_template('login.html', title = 'Account Login')

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):  # argument and key word args
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            flash("You Need To Be Logged In")
            return redirect(url_for('Login'))
    return wrap

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You Have Been logged out")
    return redirect(url_for("Home"))
  
@app.route('/Register')
def CreateAccount():
    return render_template('createAccount.html', title = 'Register')
	
@app.route('/ProcessRegistration', methods=["GET","POST"])
def ProcessRegistration():

    if request.form["submit"]:
        fname = request.form['FName']
        sname = request.form['SName']
        email = request.form['Email']
        phone = request.form['Phone'] 
        psw = request.form['Password']
        confirmPsw = request.form['psw-repeat']

    if psw == confirmPsw:
        db = Connect()
        collection = db.TestColl

        x = collection.count({"email": email})

        if x > 0: #check if a person has an already existing account
            flash("That username is already taken, please choose another")
            return render_template('createAccount.html', title = 'Register')

        else:
            post={"name": fname, "surname": sname, "email": email, "phone": phone, "password": sha256_crypt.encrypt(str(request.form['Password']))}
            registerUser(post)
            flash("Thanks for registering!")
            return render_template('login.html', title = 'Account')

    

@app.route('/EditProfile')
@login_required
def EditProfile(): 
	fname = session['userData']['name']
	sname = session['userData']['surname']
	email = session['userData']['email']
	phone = session['userData']['phone']	
		
	return render_template('editAccount.html', title = 'Edit Profile', fname = fname, sname = sname, email = email, phone = phone)
	
@app.route('/UpdateProfile', methods=["GET","POST"] )
@login_required
def UpdateProfile():
		if request.form["submit"]:
		
			fname = request.form['FName']
			sname = request.form['SName']
			email = request.form['Email']
			phone = request.form['Phone']

		post = session['userData']
		
		#replaces user data
		post["name"] = fname
		post["surname"] = sname
		post["email"] = email
		post["phone"]= phone
		
		flash(post)
		
		updateUser(post)
	
@app.route('/registerProp')
@login_required
def registerProp():
    return render_template('registerProp.html', title = 'Register Property')

@app.route('/propRegistrationHandling', methods=["GET","POST"])
def propHandling():
    if request.form["submit"]:
        
        address = request.form['address']
        cost = int(request.form['cost'])
        desc = request.form['desc']
        amenities = request.form['amenities']
        bed = int(request.form['bed'])
        bath = int(request.form['bath'])
    
    post={"User": session['userData']['email'],"Addres": address,"cost":cost,"description":desc,
          "amenities":amenities,"Bedrooms":bed,"bathrooms":bath}
    
    registerProperty(post)
    flash("Property has been registered")
    return redirect(url_for("Account"))
    

if __name__ == '__main__':
    app.run(debug=True)

