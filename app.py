#Name   :Edgars Rozenstams

from flask import Flask, render_template, request, session, flash, redirect, url_for
from dbconnect import Connect, registerUser
from wtforms import Form
from passlib.hash import sha256_crypt #password hashing
from bson.json_util import loads
from functools import wraps

from logging.config import dictConfig


# might have to use WTForms


app = Flask(__name__)
app.secret_key = 'dadass34dawddasfrjegb/1kjbvr/o'


@app.route('/')
def Home():
    return render_template('toolbar.html', title = 'Rent Search')

@app.route('/account')
def Account():
    #flash(session['data'])
    fname = session['data']['name']
    lname = session['data']['surname']
    email = session['data']['email']
    phone = session['data']['phone']
    
    return render_template('account.html', title = 'Account Login', fname = fname , lname = lname, email = email, phone = phone)
    

@app.route('/login')
def Login():
    return render_template('login.html', title = 'Account Login')
    

 
@app.route('/ProcessLogin',methods=["GET","POST"])
def AccountLogin():
    db = Connect()
    
    if request.form["submit"]:
        
        data = db.TestColl.find_one({"email": request.form['Email']},{'_id': 0}) #strips the _id as the obj type has problems
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
    return render_template('CreateAccount.html', title = 'Register')


@app.route('/ProcessRegistration', methods=["GET","POST"])
def ProcessRegistration():

    if request.form["submit"]:
        fname = request.form['FName']
        sname = request.form['SName']
        email = request.form['Email']
        phone = request.form['Phone']   #check if its a number crete seppereate function for validation
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
            print(post)
            registerUser(post)
            flash("Thanks for registering!")

    return render_template('CreateAccount.html', title = 'Register')

if __name__ == '__main__':
    app.run(debug=True)

