#Name   :Edgars Rozenstams
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_table import Table, Col, LinkCol
from passlib.hash import sha256_crypt #password hashing
from functools import wraps

#from logging.config import dictConfig

from dbconnect import Connect, registerUser, registerProperty, getUserProps, getAllProps, updateUser

app = Flask(__name__)
app.secret_key = 'dadass34dawddasfrjegb/1kjbvr/o'

class propTable(Table):
	
	classes = ['proptable'] #table css class
	
	User = Col('User', show=False)
	Addres = Col('Addres')
	cost = Col('Cost')
	description = Col('Description')
	amenities = Col('Amenities')
	Bedrooms = Col('Bedrooms')
	bathrooms = Col('Bathrooms')

@app.route('/')
def Home():
    properties = getAllProps()
    return render_template('home.html', title = 'Home',properties = properties)

@app.route('/account')
def Account():
    #flash(session['data'])
    fname = session['data']['name']
    lname = session['data']['surname']
    email = session['data']['email']
    phone = session['data']['phone']
    
	#TODO: change session[data] to session[userdata]
	
    properties = getUserProps(session['data']['email'])
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
		
        session['data'] = data
        psw = data['password']  #gets the password from the json document 
        
        if sha256_crypt.verify(request.form['Password'],psw): ##if the hashed input password is equal to the hashed saved password
            session['logged_in'] = True
            session['username'] = data['name'] #users name
            
            flash("You are now Logged in ")
            return redirect(url_for("Account"))

        else:
             flash("Invalid Credentials, try again")
             error = "Invalid Credentials, try again"
         
    return render_template('account.html', title = 'Account Login',error =  error)

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

        if x > 0:
            flash("That username is already taken, please choose another")
            return render_template('toolbar.html', title = 'Register')

        else:
            post={"name": fname, "surname": sname, "email": email, "phone": phone, "password": sha256_crypt.encrypt(str(request.form['Password']))}
            registerUser(post)
            flash("Thanks for registering!")

    return render_template('createAccount.html', title = 'Register')

@app.route('/EditProfile')
@login_required
def EditProfile(): 
	fname = session['data']['name']
	sname = session['data']['surname']
	email = session['data']['email']
	phone = session['data']['phone']	
		
	return render_template('editAccount.html', title = 'Edit Profile', fname = fname, sname = sname, email = email, phone = phone)
	
@app.route('/UpdateProfile', methods=["GET","POST"] )
@login_required
def UpdateProfile():
		if request.form["submit"]:
		
			fname = request.form['FName']
			sname = request.form['SName']
			email = request.form['Email']
			phone = request.form['Phone']

		post = session['data']
		
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
        cost = request.form['cost']
        desc = request.form['desc']
        amenities = request.form['amenities']
        bed = request.form['bed']
        bath = request.form['bath']
    
    post={"User": session['data']['email'],"Addres": address,"cost":cost,"description":desc,
          "amenities":amenities,"Bedrooms":bed,"bathrooms":bath}
    
    registerProperty(post)
    flash("Property has been registered")
    return redirect(url_for("Account"))
    

if __name__ == '__main__':
    app.run(debug=True)

