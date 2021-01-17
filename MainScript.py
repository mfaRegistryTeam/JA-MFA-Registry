# Author: Shane Okukenu

# Importing libraries
from flask import Flask, redirect, url_for, render_template, session,request,jsonify,make_response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from pymongo import MongoClient
from bson import ObjectId
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from Models import Models
from Keywords import Variables
from Methods import Queries, EmailVerification 
import os, pprint,bcrypt
import datetime,json
import threading
from datetime import timedelta
from flask.helpers import flash
import geocoder
from geopy.geocoders import Nominatim
from Models.forms import RegisterForm
import pymongo



app = Flask(__name__) 
mysecret='\xe9\xb9Y\xdd\xd0\xb7\xe7\xab\x9e\xd0\xc1}\x84\xd7\x1b\xc3\x0e\xdfp\xb8r8f\x02'
app.secret_key = mysecret  


# Establishing Database Connectivity
app.config['MONGO_URI'] = Variables.siteLabels().DatabaseURL
app.config['MONGO_DBNAME'] = Variables.siteLabels().DatabaseName
mongo=PyMongo(app)
SESSION_TYPE = Variables.siteLabels().SessionType


#Creation of collections
model=Models.MyMongoDB()

adminuser=model.db.user_admin
user=model.db.users
diasporaList=model.db.diasporaList
tempquery=model.db.tempquery



if diasporaList.find_one({}) is None:
    diasporaList.insert_one({Variables.databaseLabels().EmailAddress : 'test@yahoo.com'})
    diasporaList.delete_many({})


if tempquery.find_one({}) is None:
    tempquery.insert_one({Variables.databaseLabels().EmailAddress : 'test@yahoo.com'})
    tempquery.delete_many({})

if user.find_one({}) is None:
    user.insert_one({Variables.databaseLabels().EmailAddress : 'test@yahoo.com'})
    user.delete_many({})
    
if adminuser.find_one({}) is None:
    adminuser.insert_one({Variables.databaseLabels().EmailAddress : 'test@yahoo.com'})
    adminuser.delete_many({})

#Cleans Unverified Users
r=Queries.AdminQuery()
r.CleanUserList()
r.CleanDiasporaList()

# Main routing modules
@app.route('/')
def index():      
     if 'username' in session and model.db.users.find_one({Variables.databaseLabels.Username:session['username']}) is not None:
         return redirect(url_for("Account"))         
     else:
         #Landing page
         return render_template('landing.html')      
     
@app.route('/myaccount', methods=['POST','GET'])
def Account():
    if 'username' not in session:
        return redirect(url_for('index'))        
    r=Queries.SiteQuery()
    result=r.find_existing_registered()
    if result is not None:
        return redirect(url_for('View'))
    
    if  request.method =='POST':
        database=Models.DatabaseStruct()
        database.InsertFormData()       
        return redirect(url_for('View'))   
     
    today = datetime.datetime.now()        
    return render_template('account.html',timestamp=today,ses=session)

@app.route('/view', methods=['POST','GET'])
def View():
    if 'username' not in session:
        return redirect(url_for('index'))   

    r=Queries.SiteQuery()
    result=r.find_existing_registered()

    if result is None:
        return redirect(url_for('Account'))

    database=Models.DatabaseStruct()
    queryresult=database.ViewFormData()
         
    return render_template('view.html',queryresult=queryresult)

@app.route('/signup', methods=['POST','GET'])
def SigningUp():
    if 'username' in session:
        return redirect(url_for('index'))
        
    user_exists=Queries.SiteQuery()
    result=user_exists.find_existing_user()     
    if result is None:
        if request.form.get('password')==request.form.get('confirm_password') and request.form.get('password')  is not None:             
             user_instance =Models.DatabaseStruct()
             user_instance.InsertUser(request.form.get('email'),request.form.get('password'),request.form.get('username'))
             return redirect(url_for('index'))
        else:
            return render_template('signup.html') 
    else:

        return redirect(url_for('Error'))


@app.route('/login', methods=['POST','GET'])
def Login():
    if 'username' in session:
        return redirect(url_for('Account'))
            
    user_exists=Queries.SiteQuery()
    result=user_exists.find_existing_user()
         
    if result is not None :
        if bcrypt.checkpw(request.form.get('password').encode('UTF-8'), result[Variables.databaseLabels.Password]):
            session['username'] = result[Variables.databaseLabels.Username]
            session['email']= result[Variables.databaseLabels.EmailAddress]
            return redirect(url_for('Account'))        
        else:
            return redirect( url_for('Error')) 
               
    return render_template('login.html')   
   

@app.route('/PasswordReset', methods=['POST','GET'])
def password():
    if 'username' in session:
        return redirect(url_for('index'))  

    email=request.form.get('email') 
    if email is not None:
        user=Queries.SiteQuery
        result=user.find_existing_user
        if result is not None:           
            plink = EmailVerification.ChangePassword(email)
            return redirect(plink)
            
    else:
        return render_template('pchange1.html')  

    return render_template('error.html')

@app.route('/PasswordReset2/<token>')
def PasswordChangehandler(token):
    if 'username' in session:
        return redirect(url_for('index'))
   
    return EmailVerification.confirm_password(token)   

#refers to Password change
@app.route('/Change', methods=['POST'])
def FinalSteps():
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm_password']
    model=Models.MyMongoDB()
    r=Queries.SiteQuery()
    result1=r.find_existing_user()

    if password==confirm  and result1 and password is not None :
        hashpass=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())

        model.db.diasporaList.update_one(
            {Variables.databaseLabels().EmailAddress : email},
            {'$set':{Variables.databaseLabels().Password:hashpass}})

        model.db.users.update_one(
            {Variables.databaseLabels().EmailAddress : email},
            {'$set':{Variables.databaseLabels().Password:hashpass}})     

    return redirect(url_for('Login'))

@app.route("/error")
def Error():
    return render_template("error403.html")

@app.route("/errortimeout")
def ErrorTimeout():
    return render_template("errortimeout.html")


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)    
        session.pop('email', None)    
        return redirect(url_for('index'))         
    else:
        #Landing page
        return redirect(url_for('index'))
#-------------------------------------------------------------------------

@app.route('/adminlogout')
def adminlogout():
    if 'adminuser' in session:
        model.db.user_admin.update_one(
            {Variables.databaseLabels().Username : session['adminuser']},
            {'$set':{Variables.databaseLabels().Logged :False}}            
                   )
        session.pop('adminuser', None) 
        return redirect(url_for('adminlogin'))         
    else:
        #Landing page
        return redirect(url_for('adminlogin'))  

@app.route('/admin876delete876/<email>', methods=['POST','GET'])
def AdminDelete(email):
    if 'adminuser' not in session:    
        return redirect(url_for('adminlogin'))        
    database = Models.DatabaseStruct()
    database.AdminDeleteFormData(email)    
    return redirect(url_for('query'))

@app.route('/Adminview/<email>', methods=['POST','GET'])
def AdminView(email):
    if 'adminuser' not in session:    
        return redirect(url_for('adminlogin'))    
    database = Models.DatabaseStruct()
    queryresult = database.AdminViewFormData(email)
        
    return render_template('Adminview.html',queryresult=queryresult)

@app.route('/admin876register876', methods=['POST','GET'])
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
        return redirect(url_for('Error'))
        
    return render_template('adminregister.html')


@app.route("/admin876login876",methods=['POST','GET'])
def adminlogin():
    if 'adminuser' in session and model.db.user_admin.find_one({Variables.databaseLabels.Username:session['adminuser'],Variables.databaseLabels.Logged:True}):
        return redirect(url_for('query'))
    admin_exists=Queries.SiteQuery()
    result=admin_exists.find_admin()
    if result:
        if bcrypt.checkpw(request.form.get('password').encode('UTF-8'), result[Variables.databaseLabels.Password]) and result[Variables.databaseLabels.Logged]==False:
            
            session['adminuser']=result[Variables.databaseLabels.Username]
            model.db.user_admin.update_one(
                {Variables.databaseLabels().Username : session['adminuser']},
                {'$set':{Variables.databaseLabels().Logged :True}}               )

            # Add session to adminators as well
            q=Queries.AdminQuery()
            q.Indexing()
            #q.AutoEmail()  

            return redirect(url_for('query'))
            #return redirect(url_for('adminlogin'))
        else:
            return render_template('adminerror.html')
    else:
        return render_template('adminlogin.html')



@app.route("/adminquerywizard", methods=['POST','GET'])
def query():
    if 'adminuser' not in session:    
        return redirect(url_for('adminlogin')) 

    if request.method =='POST':
        adminquery=Queries.AdminQuery()  
        result=adminquery.MasterQuery()
        querycol=Models.MyMongoDB()
        querycol=querycol.db
        querycol=querycol.tempquery
        count =0
        querycol.delete_many({})
        for item in result:
            print(item)
            querycol.insert_one(item)        
        return redirect(url_for('admindemo'))
        
    return render_template('query.html')


@app.route("/queryresult", methods=['POST','GET'])
def admindemo():
    if 'adminuser' not in session:    
        return redirect(url_for('adminlogin')) 
    
    model=Models.MyMongoDB()
    querylist = model.db.tempquery
    a = querylist.find()
    userquerylist = list(a)    
    return render_template('AdminTable.html', title='Admin',userquerylist = userquerylist) 


@app.route('/update', methods=['POST','GET'])
def Update():
    if 'username' not in session:
        return redirect(url_for('index'))        
    r=Queries.SiteQuery()
    result=r.find_existing_registered()
    print(result)
    if result is None:
        return redirect(url_for('Account'))

    fullname = result[Variables.databaseLabels.Name]
    FirstName = fullname[Variables.databaseLabels.Firstname]
    LastName = fullname[Variables.databaseLabels.Lastname]
    MiddleName = fullname[Variables.databaseLabels.Middlename]
    DOB = result[Variables.databaseLabels.DOB]
    Gender = result[Variables.databaseLabels.Gender]
    MaritalStatus = result[Variables.databaseLabels.MaritalStatus]
    Occupation = result[Variables.databaseLabels.Occupation]
    Occupation_type = Occupation[Variables.databaseLabels.Type]
    Study_Details = Occupation[Variables.databaseLabels.StudyDetails]
    Institutional_Address= Occupation[Variables.databaseLabels.InstitutionAddress]


    JobClass = Occupation[Variables.databaseLabels.JobClass]
    Jobtitle = Occupation[Variables.databaseLabels.Jobtitle]
    Workplace_details = Occupation[Variables.databaseLabels.WorkplaceDetails]
    OccupationOther = Occupation[Variables.databaseLabels.Other]

    CountryofBirth = result[Variables.databaseLabels.CountryofBirth]
    JaPassportNumber = result[Variables.databaseLabels.JaPassportNumber]
    OtherNationality = result[Variables.databaseLabels.OtherNationality]
    #Nationality = result[Variables.databaseLabels.Nationality]
    OtherPassportNumber = result[Variables.databaseLabels.OtherPassportNumber]

    WhatsappNumber = result[Variables.databaseLabels.WhatsappNumber]
    Landline = result[Variables.databaseLabels.Landline]
    OtherContacts= result[Variables.databaseLabels.OtherContacts]
    JamaicaAddress = result[Variables.databaseLabels.JamaicaAddress]
    Street_Ja = JamaicaAddress[Variables.databaseLabels.Street]
    City_Ja = JamaicaAddress[Variables.databaseLabels.CityorTown]
    Parish_Ja = JamaicaAddress[Variables.databaseLabels.Parish]

    EmergencyDetails = result[Variables.databaseLabels.EmergDetails]
    EmergencyConFirstname = EmergencyDetails[Variables.databaseLabels.EmergencyConFirstname]
    EmergencyConLastname = EmergencyDetails[Variables.databaseLabels.EmergencyConLastname]
    EmergencyRel = EmergencyDetails[Variables.databaseLabels.EmergencyConRel]
    EmergencyConPhone = EmergencyDetails[Variables.databaseLabels.EmergencyConPhone]
    EmergencyConEmail = EmergencyDetails[Variables.databaseLabels.EmergencyConEmail]

    EmergencyConFirstname2 = EmergencyDetails[Variables.databaseLabels.EmergencyConFirstname2]
    EmergencyConLastname2 = EmergencyDetails[Variables.databaseLabels.EmergencyConLastname2]
    EmergencyRel2 = EmergencyDetails[Variables.databaseLabels.EmergencyConRel2]
    EmergencyConPhone2 = EmergencyDetails[Variables.databaseLabels.EmergencyConPhone2]
    EmergencyConEmail2 = EmergencyDetails[Variables.databaseLabels.EmergencyConEmail2]

    

    
    session['FirstName'] = FirstName
    session['LastName'] = LastName
    session['MiddleName'] = MiddleName
    session['DOB'] = DOB
    session['Gender'] = Gender
    session['MaritalStatus'] = MaritalStatus
    session['OccupationType']= Occupation_type  
    session['Study_Details'] = Study_Details
    session['Institutional_Address'] = Institutional_Address
    session['JobClass'] = JobClass
    session['Jobtitle'] = Jobtitle
    session['Workplace_details'] = Workplace_details
    session['OccupationOther'] = OccupationOther
    session['CountryofBirth'] = CountryofBirth
    session['JaPassportNumber'] = JaPassportNumber
    session['OtherNationality'] = OtherNationality
    session['OtherPassportNumber'] = OtherPassportNumber

    session['StreetJa'] = Street_Ja
    session['CityJa'] = City_Ja
    session['ParishJa'] = Parish_Ja
    session['Landline'] = Landline
    session['WhatsappNumber'] = WhatsappNumber
    session['OtherContacts'] = OtherContacts
    

    session['EmergencyConFirstname'] = EmergencyConFirstname
    session['EmergencyLastname'] = EmergencyConLastname
    session['EmergencyRel'] = EmergencyRel
    session['EmergencyConPhone'] = EmergencyConPhone
    session['EmergencyConEmail'] = EmergencyConEmail    

    session['EmergencyConFirstname2'] = EmergencyConFirstname2
    session['EmergencyLastname2'] = EmergencyConLastname2
    session['EmergencyRel2'] = EmergencyRel2
    session['EmergencyConPhone2'] = EmergencyConPhone2
    session['EmergencyConEmail2'] = EmergencyConEmail2    

      
    

    form = RegisterForm(request.form)
    
    if  request.method =='POST':
        database=Models.DatabaseStruct()
        database.UpdateFormData() 
        flash(f'Your Account has been updated', 'success')
        return redirect(url_for('Account'))

    form.first_name.data= session['FirstName']
    form.last_name.data = session['LastName']
    form.middle_name.data = session['MiddleName']
    form.Gender.data = session['Gender']
    form.marital_status.data = session['MaritalStatus']
    form.ja_passport_num.data = session['JaPassportNumber']
    form.other_passport_num.data = session['OtherPassportNumber']
    form.workplace_details.data = session['Workplace_details']
    form.street_jm.data = session['StreetJa']
    form.city_town_jm.data = session['CityJa']
    form.landline.data = session['Landline']
    form.whatsapp_num.data = session['WhatsappNumber']
    form.other_contacts.data = session['OtherContacts']
    
    form.study_details.data = session['Study_Details'] 
    form.edu_addr.data = session['Institutional_Address']
    form.job_title.data= session['Jobtitle']
    form.other.data = session['OccupationOther']
    

    form.emerg_firstname.data = session['EmergencyConFirstname'] 
    form.emerg_lastname.data = session['EmergencyLastname'] 
    form.emerg_rel.data = session['EmergencyRel']
    form.emerg_phone.data = session['EmergencyConPhone']
    form.emerg_email.data = session['EmergencyConEmail'] 

    form.emerg_firstname2.data = session['EmergencyConFirstname2'] 
    form.emerg_lastname2.data = session['EmergencyLastname2'] 
    form.emerg_rel2.data = session['EmergencyRel2']
    form.emerg_phone2.data = session['EmergencyConPhone2']
    form.emerg_email2.data = session['EmergencyConEmail2']
     
    today = datetime.datetime.now()  
    return render_template('update.html',timestamp=today, ses=session,form=form)  



# -------------------------------------------------------------------

if __name__ == "__main__":      
    app.run(debug=True)