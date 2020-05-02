# Author: Shane Okukenu

# Importing libraries
from flask import Flask, redirect, url_for, render_template, session,request
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from Models import Models
from Keywords import Variables
from Methods import Queries, EmailVerification 
import os, pprint,bcrypt
import datetime
from flask.helpers import flash


app = Flask(__name__) 
mysecret=os.urandom(24)
app.secret_key = mysecret  


# Establishing Database Connectivity
app.config['MONGO_URI'] = Variables.siteLabels().DatabaseURL
app.config['MONGO_DBNAME'] = Variables.siteLabels().DatabaseName
mongo=PyMongo(app)
SESSION_TYPE = Variables.siteLabels().SessionType


#Creation of collections
model=Models.MyMongoDB()
if 'user_admin' not in model.db.list_collection_names():
    adminuser=model.db["user_admin"]
elif 'users' not in model.db.list_collection_names():
    user=model.db["users"]
elif 'diasporaList' not in model.db.list_collection_names():
    diasporaList=model.db["diasporaList"]
else:
    pass

#  = mongo.db.adminuser
# user= mongo.db.users  
# = mongo.db.diasporaList


# Main routing modules
@app.route('/')
def index():
     if 'username' in session and model.db.users.find_one({Variables.databaseLabels.Username:session['username']}) is not None:
         return redirect(url_for("Account"))
     else:
         #Landing page
         return render_template('landing.html') 
           

# existing_user=Queries.SiteQuery()        
        # result=existing_user.find_existing_user2()
        # #Next Two lines for testing purposes --already in insertuser function
        # password=request.form.get('password')
        # hashpass=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt() ) 
        # 
@app.route('/register', methods=['POST','GET'])
def Register():
    if  request.method =='POST':
        database=Models.DatabaseStruct()
        database.InsertFormData()               
        
    return render_template('register.html')


@app.route('/confirm_email/<token>')
def emailVerificationhandler(token):
    return EmailVerification.confirmToken(token)


@app.route('/login', methods=['POST','GET'])
def Login():
    if 'username' in session:
        return redirect(url_for('index'))
    user_exists=Queries.SiteQuery()
    result=user_exists.find_existing_user()     
    if result :
        if bcrypt.checkpw(request.form.get('password').encode('UTF-8'), result[Variables.databaseLabels.Password]):
            session['username'] = result[Variables.databaseLabels.Username]
            return redirect(url_for('Account'))        
        else:
            return redirect( url_for('Error'))            
    else:
        flash("Incorrect Username or Password")
        return render_template('login.html')




@app.route('/signup', methods=['POST','GET'])
def SigningUp():
    if 'username' in session:
        return redirect(url_for('index'))
        
    user_exists=Queries.SiteQuery()
    result=user_exists.find_existing_user()     
    if result is None:
        if request.form.get('password')==request.form.get('confirm_password') and request.form.get('password')  is not None:
             EmailVerification.Register(request.form.get('email'),request.form.get('password'),request.form.get('username'))
             return render_template('login.html')
        else:
            return render_template('signup.html') 
    else:

        return render_template('error.html')
    


@app.route("/myaccount")
def Account():
    if 'username' in session and model.db.users.find_one({Variables.databaseLabels.Username:session['username']}) is not None:
        return render_template("account.html")
    else:
        #Landing page
        return redirect(url_for("index")) 


@app.route("/error")
def Error():
    return render_template("error.html")


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)        
        return redirect(url_for('index'))         
    else:
        #Landing page
        return redirect(url_for('index'))

#-------------------------------------------------------
@app.route("/admin")
def adminindex():
    if 'adminuser' in session:
         return redirect(url_for("admindashboard"))
    else:
         #Admin login page
         return redirect(url_for("adminlogin"))


@app.route("/admin246login642", methods=['POST','GET'])
def adminlogin():
    if 'adminuser' in session and model.db.user_admin.find_one({Variables.databaseLabels.Username:session['adminuser']}) is not None:
        return redirect(url_for('admindashboard'))

    admin_exists=Queries.SiteQuery()
    result=admin_exists.find_admin()      
    
    if result :
        if bcrypt.checkpw(request.form.get('password').encode('UTF-8'), result[Variables.databaseLabels.Password]):
            session['adminuser'] = result[Variables.databaseLabels.Username]
            return redirect(url_for('admindashboard'))
        
        else:
            return redirect( url_for('error'))
            
    else:
        return render_template('adminlogin.html')

@app.route('/admin246register642', methods=['POST','GET'])
def AdminRegister(): 
    if  request.method =='POST':
        existing_user=Queries.SiteQuery()        
        result=existing_user.find_admin()
        if result is None:
            if request.form.get('password')==request.form.get('confirm_password'):               
                database=Models.DatabaseStruct()
                database.InsertAdmin()
                
                return redirect(url_for('adminlogin'))
            #error regarding password matching or email verification
        return redirect(url_for('error'))
        
    return render_template('adminregister.html')


@app.route("/adminDashboard")
def admindashboard():
    if 'adminuser' in session:
        return render_template("AdminDash.html")
    else:
        #Landing page
        return redirect(url_for("adminindex")) 


@app.route("/adminquerywizard")
def query():
    if 'adminuser' in session:
        return render_template('query.html')
    else:
        #Landing page
        return redirect(url_for('adminindex'))       


# -------------------------------------------------------------

if __name__ == "__main__":      
    app.run(debug=True)