#Name   :Edgars Rozenstams

from flask import Flask, render_template, request, session, flash, redirect, url_for
from dbconnect import Connect, registerUser
from wtforms import Form
from passlib.hash import sha256_crypt #password hashing

from logging.config import dictConfig


# might have to use WTForms


app = Flask(__name__)
app.secret_key = 'dadass34dawddasfrjegb/1kjbvr/o'


@app.route('/')
def Home():
    return render_template('toolbar.html', title = 'Rent Search')

@app.route('/account')
def Account():
    return render_template('account.html', title = 'Account Login')
    
    
@app.route('/ProcessLogin',methods=["GET","POST"])
def AccountLogin():
    db = Connect()
    
    if request.form["submit"]:
        
        data = db.TestColl.find_one({"email": request.form['Email']})
        psw = data['password']  #gets the third item in the JSON data which is the password 
        
        if sha256_crypt.verify(request.form['Password'],psw): ##if the hashed input password is equal to the hashed saved password
            session['logged_in'] = True
            session['username'] = data['name'] #users name
            
            flash("You are now Logged in ")
            return redirect(url_for("Account"))
        
        else:
             flash("Invalid Credentials, try again")
             error = "Invalid Credentials, try again"
         
        
        
    return render_template('account.html', title = 'Account Login',error =  error)


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

