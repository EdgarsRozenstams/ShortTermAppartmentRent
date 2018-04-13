#Name   :Edgars Rozenstams

from flask import Flask, render_template, request, session, flash, redirect
from dbconnect import Connect, registerUser

#might have to use WTForms


app = Flask(__name__)
app.secret_key = 'dadass34dawddasfrjegb/1kjbvr/o'


@app.route('/')
def Home():
    return render_template('toolbar.html', title = 'Rent Search')


@app.route('/AccountLogin')
def AccountLogin():
    return render_template('account.html', title = 'Account Login')


@app.route('/Register')
def CreateAccount():
    return render_template('CreateAccount.html', title = 'Register')


@app.route('/ProcessRegistration', methods=["POST"])
def ProcessRegistration():

    if request.form["submit"]:
        fname = request.form['FName']
        sname = request.form['SName']
        email = request.form['Email']
        phone = request.form['Phone'] #check if its a number crete seppereate function for validation
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
            post={"name": fname, "surname": sname, "email": email, "phone": phone, "password": psw}
            print(post)
            registerUser(post)
            flash("Thanks for registering!")

    return render_template('CreateAccount.html', title = 'Register')

if __name__ == '__main__':
    app.run(debug=True)

