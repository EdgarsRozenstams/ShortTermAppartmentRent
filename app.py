#Name   :Edgars Rozenstams
#C-Code :C00195570
from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_table import Table, Col, LinkCol
from passlib.hash import sha256_crypt #password hashing
from functools import wraps

import pprint

from dbconnect import Connect, registerUser, registerProperty, getUserProps, getAllProps, updateUser, Search, getUserDetails, getUserId

app = Flask(__name__)
app.secret_key = 'dad555ass34dawddasfrjegb/1kjbvr/o'

Counties = []

def getCounties():
    with open("Counties.txt", "r") as c:
        for line in c:
            Counties.append(line.strip())

getCounties()

class propTable(Table):#table for user properties in the account page
	classes = ['proptable'] #table css class

	User = Col('User', show=False)
	address = Col('Address')
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

    return render_template('account.html', title = fname+' '+lname , fname = fname , lname = lname, email = email, phone = phone, table=table)

@app.route('/login', methods=["GET","POST"])
def Login():
    if session.get('logged_in') == True: #stops you logging in twice.
        if session['logged_in'] == True:
            return redirect(url_for("Account"))
    else:
        try:
            if request.form["submit"]:
                
                session['userData'] = getUserDetails(request.form['Email'])
                session['userId'] = getUserId(request.form['Email'])

                psw = session['userData']['password']  #gets the password from the json document 
                
                if sha256_crypt.verify(request.form['Password'],psw): ##if the hashed input password is equal to the hashed saved password
                    session['logged_in'] = True
                    session['username'] = session['userData']['name'] #users name
                    
                    #flash("You are now Logged in ")
                    return redirect(url_for("Account"))

        except Exception as e:
                error = "Invalid credentials, try again."
                return render_template("login.html", title = 'Account Login', error = error)  

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

@app.route('/Register', methods=["GET","POST"])
def CreateAccount():
    try:
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

                if x > 0:  # check if a person has an already existing account
                    flash("That username is already taken, please choose another")
                    return render_template('createAccount.html', title='Register')

                else:
                    post = {"name": fname, "surname": sname,
                            "email": email, "phone": phone,
                            "password": sha256_crypt.encrypt(str(request.form['Password']))}
                    registerUser(post)
                    flash("Thanks for registering!")
                    return render_template('login.html', title='Account')
    except Exception as e:
        return render_template('createAccount.html', title='Register')

@app.route('/EditProfile', methods=["GET","POST"])
@login_required
def EditProfile():
    try:
        fname = session['userData']['name']
        sname = session['userData']['surname']
        email = session['userData']['email']
        phone = session['userData']['phone']

        if request.form["submit"]:
            print("first test")
            #read in field values to save as new account details
            fname = request.form['FName']
            sname = request.form['SName']
            email = request.form['Email']
            phone = request.form['Phone']

            session['post'] = session['userData']

            #replaces user data
            session['post']["name"] = fname
            session['post']["surname"] = sname
            session['post']["email"] = email
            session['post']["phone"]= phone
            #print("after update values")

            updateUser(session['post'],session['userId'])

        return redirect(url_for("Account"))

    except Exception as e:
        return render_template('editAccount.html', title = 'Edit Profile', fname = fname, sname = sname, email = email, phone = phone)

@app.route('/registerProp', methods=["GET","POST"])
@login_required
def registerProp():
    try:
        if request.form["submit"]:
            address = []
            county = request.form['county']
            
            address.append(county)
            address.append(request.form['address1'])
            address.append(request.form['address2'])
            
            address = ', '.join(address)
            #strips the ", " is last fiels is not filled in
            if address.endswith(' '):
                address = address[:-2]
            
            cost = int(request.form['cost'])
            desc = request.form['desc']
            amenities = request.form['amenities']
            bed = int(request.form['bed'])
            bath = int(request.form['bath'])
        
            post={"User": session['userData']['email'],"county":county ,"address": address,"cost":cost,"description":desc,"amenities":amenities,"Bedrooms":bed,"bathrooms":bath}
            
            registerProperty(post)
            #flash("Property has been registered")
            return redirect(url_for("Account"))
    
    except Exception as e:
        return render_template('registerProp.html', title = 'Register Property', counties = Counties)

@app.route('/property', methods=["GET","POST"])
def property():
    #try:

    return render_template('property.html', title = 'Property')



if __name__ == '__main__':
    app.run(debug=True)

