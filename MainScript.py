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
mysecret= 'o\x9e\xe6\x88:@L\xae\xa0\xf3,T\xfb\xc7\x1f\xf4\x12\xb2\xdd\x0c\x05\xcb>\x87'
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
Historical=model.db.Historical


if diasporaList.find_one({}) is None:
    diasporaList.insert_one({Variables.databaseLabels().EmailAddress : 'test@yahoo.com'})
    diasporaList.delete_many({})

if Historical.find_one({}) is None:
    Historical.insert_one({Variables.databaseLabels().EmailAddress : 'test@yahoo.com'})
    Historical.delete_many({})

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

# Main routing modules
@app.route('/')
def index():
     if 'username' in session and model.db.users.find_one({Variables.databaseLabels.Username:session['username'],'Status':True}) is not None:
         return redirect(url_for("Account"))
     else:
         #Landing page
         return render_template('landing.html')            


@app.route('/register', methods=['POST','GET'])
def Register():
    if 'username' not in session:
        return redirect(url_for('index'))
        
    r=Queries.SiteQuery()
    result=r.find_existing_registered()
    if result  is not None:
        return redirect(url_for('Account'))
    
    if  request.method =='POST':
        database=Models.DatabaseStruct()
        database.InsertFormData()  
        return redirect(url_for('Account'))
             
        
    return render_template('register.html')
        

@app.route('/update', methods=['POST','GET'])
def Update():
    if 'username' not in session:
        return redirect(url_for('index'))        
    r=Queries.SiteQuery()
    result=r.find_existing_registered()
    if result is None:
        return redirect(url_for('Account'))
    Nationality= result[Variables.databaseLabels.Nationality]
    IssuedPassportCountry = result[Variables.databaseLabels.IssuedPassportCountry]

    fullname = result[Variables.databaseLabels.Name]
    FirstName = fullname[Variables.databaseLabels.Firstname]
    LastName = fullname[Variables.databaseLabels.Lastname] 
    MiddleName = fullname[Variables.databaseLabels.Middlename]
    fullAddress= result[Variables.databaseLabels.Address]
    Street= fullAddress[Variables.databaseLabels.Street]
    City= fullAddress[Variables.databaseLabels.CityorTown]
    Country = fullAddress[Variables.databaseLabels.Country]
    EmergencyContact= result[Variables.databaseLabels.EmergDetails]
    EmergConFirstname= EmergencyContact[Variables.databaseLabels.EmergencyConFirstname]
    EmergConLastname= EmergencyContact[Variables.databaseLabels.EmergencyConLastname]
    EmergConRel= EmergencyContact[Variables.databaseLabels.EmergencyConRel]
    EmergConPhone= EmergencyContact[Variables.databaseLabels.EmergencyConPhone]
    EmergConEmail= EmergencyContact[Variables.databaseLabels.EmergencyConEmail]
    Classification = result[Variables.databaseLabels.Classification]
    Country_of_Issued_passport = result[Variables.databaseLabels.IssuedPassportCountry]
    BarbadianAddress = result[Variables.databaseLabels.BarbadosAddress]
    BAStreet = BarbadianAddress[Variables.databaseLabels.Street]
    BACity = BarbadianAddress[Variables.databaseLabels.CityorTown]
    BAParish= BarbadianAddress[Variables.databaseLabels.Parish]
    DestinationAddress = result[Variables.databaseLabels.AddressAbroad]
    street_abroad = DestinationAddress[Variables.databaseLabels.Street]
    city_abroad = DestinationAddress[Variables.databaseLabels.CityorTown]
    state_abroad = DestinationAddress[Variables.databaseLabels.State]
    country_abroad = DestinationAddress[Variables.databaseLabels.CountryAbroad]
    EmergDetailsAbroad = result[Variables.databaseLabels.EmergDetailsAbroad]
    EmergencyConFirstnameab = EmergDetailsAbroad[Variables.databaseLabels.EmergencyConFirstname]
    EmergencyConLastnameab = EmergDetailsAbroad[Variables.databaseLabels.EmergencyConLastname]
    EmergencyConRel = EmergDetailsAbroad[Variables.databaseLabels.EmergencyConRel]
    EmergencyConphoneab = EmergDetailsAbroad[Variables.databaseLabels.EmergencyConPhone]
    EmergencyConEmailab = EmergDetailsAbroad[Variables.databaseLabels.EmergencyConEmail]
    TravelDateDetails = result[Variables.databaseLabels.TravelDates]
    dept_date = TravelDateDetails[Variables.databaseLabels.DepDate]
    ret_date =  TravelDateDetails[Variables.databaseLabels.ReturnDate]
    PhoneNumberAbroad = result[Variables.databaseLabels.PhoneNumberAbroad]
    ResidentialPhoneNumAb = PhoneNumberAbroad[0][Variables.databaseLabels.ResidentialAbroad]
    ResidentialMobileAb = PhoneNumberAbroad[1][Variables.databaseLabels.MobileAbroad]
    ResidentialWhatsappAb = PhoneNumberAbroad[2][Variables.databaseLabels.WhatsappAbroad]
    AbroadEmail = result[Variables.databaseLabels.AbroadEmail]
    ResidentAbroadAddress= result[Variables.databaseLabels.ResidenceAbroadDetails]
    ResidentAbroadStreet= ResidentAbroadAddress[Variables.databaseLabels.Street]
    ResidentAbroadCity = ResidentAbroadAddress[Variables.databaseLabels.CityorTown]
    ResidentAbroadState= ResidentAbroadAddress[Variables.databaseLabels.State]
    ResidentAbroadCountry= ResidentAbroadAddress[Variables.databaseLabels.Country]
    ResidentAbroadLocation= ResidentAbroadAddress[Variables.databaseLabels.Location]
    ResidentialPhoneAbroad = result[Variables.databaseLabels.ResidentsAbroadPhone]
    ResidentialPhoneNumberAbroad = ResidentialPhoneAbroad[0][Variables.databaseLabels.ResidentialRes]
    ResidentialMobilePhoneAbroad = ResidentialPhoneAbroad[1][Variables.databaseLabels.MobileRes]
    ResidentialWhatsappAbroad = ResidentialPhoneAbroad[2][Variables.databaseLabels.WhatsappRes]
    WeChatId = result[Variables.databaseLabels.WeChatAB]
    AreasofInterest = result[Variables.databaseLabels.AreasofInterest]
    KnowledgeOfBB = result[Variables.databaseLabels.KnowledgeofBB]
    AreasofInterestfr= result[Variables.databaseLabels.AreasofInterestFr]

    Occupation = result[Variables.databaseLabels.Occupation]
    StudyLevel= Occupation[Variables.databaseLabels.StudyLevel]
    FieldofStudy= Occupation[Variables.databaseLabels.FieldofStudy]
    Type = Occupation[Variables.databaseLabels.Type]
    EducationalInstitute = Occupation[Variables.databaseLabels.EducationalInst]
    OccupationOther = Occupation[Variables.databaseLabels.Other]
    JobClass = Occupation[Variables.databaseLabels.JobClass]
    JobTitle= Occupation[Variables.databaseLabels.Jobtitle]
    Workplacename = Occupation[Variables.databaseLabels.Workplace]
    StatedReason = result[Variables.databaseLabels.POTdescription]
    PurposeOfTravel = result[Variables.databaseLabels.PurposeofTravel]


    session['ResidentAbroadCity'] = ResidentAbroadCity
    session['Workplacename'] = Workplacename
    session['JobTitle'] = JobTitle
    session['JobClass'] = JobClass
    session['OccupationOther'] = OccupationOther
    session['EducationalInstitute'] = EducationalInstitute
    session['Type'] = Type
    session['StudyLevel'] = StudyLevel
    session['Classification'] = result[Variables.databaseLabels.Classification]
    session['FirstName'] = FirstName
    session['MiddleName'] = MiddleName
    session['LastName'] = LastName
    session['Gender'] = result[Variables.databaseLabels.Gender] 
    session['DOB'] = result[Variables.databaseLabels.DOB]
    session['PassportNumber'] = result[Variables.databaseLabels.PassportNumber]
    session['Wechat'] = result[Variables.databaseLabels.WeChatID]
    session['PhoneNumber'] = result[Variables.databaseLabels.PhoneNumber]
    session['Street'] = Street
    session['City'] = City
    session['Country'] = Country
    session['EmergConFirstname'] = EmergConFirstname
    session['EmergConLastname'] = EmergConLastname
    session['EmergConRel'] = EmergConRel
    session['EmergConPhone'] = EmergConPhone
    session['EmergConEmail'] = EmergConEmail
    session['Purpose-of-Travel'] = StatedReason
    session['StatedReason'] = result[Variables.databaseLabels.POTdescription]
    session['AreasofInterestfr'] = AreasofInterestfr 
    session['KnowledgeOfBB'] = KnowledgeOfBB 
    session['AreasofInterest'] = AreasofInterest 
    session['WeChatId'] = WeChatId
    session['ResidentialWhatsappAbroad'] = ResidentialWhatsappAbroad
    session['ResidentialMobilePhoneAbroad'] = ResidentialMobilePhoneAbroad
    session['ResidentialPhoneNumberAbroad'] = ResidentialPhoneNumberAbroad
    session['ResidentAbroadLocation'] = ResidentAbroadLocation
    session['ResidentAbroadCountry'] = ResidentAbroadCountry
    session['ResidentAbroadState'] = ResidentAbroadState
    session['ResidentAbroadStreet'] = ResidentAbroadStreet
    session['AbroadEmail'] = AbroadEmail
    session['ResidentialWhatsappAb'] = ResidentialWhatsappAb
    session['ResidentialMobileAb'] = ResidentialMobileAb
    session['ResidentialPhoneNumAb'] = ResidentialPhoneNumAb
    session['ret_date'] = ret_date
    session['dept_date'] = dept_date
    session[' EmergencyConEmailab'] =  EmergencyConEmailab
    session['EmergencyConphoneab'] = EmergencyConphoneab
    session['EmergencyConRel'] = EmergencyConRel
    session['EmergencyConLastnameab'] = EmergencyConLastnameab
    session['EmergencyConFirstnameab '] = EmergencyConFirstnameab 
    session['country_abroad'] = country_abroad
    session['state_abroad'] = state_abroad
    session['city_abroad'] = city_abroad
    session['street_abroad'] = street_abroad
    session['BAParish'] = BAParish
    session['BACity'] = BACity
    session['BAStreet'] = BAStreet
    session['pp_country'] = IssuedPassportCountry
    session['Nationality'] = Nationality
    session['Country'] = Country
    session['country_ro'] = ResidentAbroadCountry
    session['job_class'] = JobClass
    session['field'] = FieldofStudy
    session['POT'] = PurposeOfTravel
    session['parishbb'] = BAParish
    session['Country-of-Issued-Passport'] = Country_of_Issued_passport

     
    form = RegisterForm(request.form)
    
    if  request.method =='POST':
        database=Models.DatabaseStruct()
        database.UpdateFormData() 
        flash(f'Your Account has been updated', 'success')
        return redirect(url_for('Account'))

    form.ResPhoneNumberAbroad.data =  session['ResidentialPhoneNumAb']
    form.ResMobileAbroad.data = session['ResidentialMobileAb'] 
    form.ResWhatsappAbroad.data = session['ResidentialWhatsappAb']
    form.ResWechatAB.data = session['WeChatId']
    form.AbroadEmail.data = session['AbroadEmail']
    form.resstreet_abroad.data = session['ResidentAbroadStreet']
    form.resstate_abroad.data = session['ResidentAbroadState']
    form.rescity_abroad.data = session['ResidentAbroadCity']
    form.ResidentialPhoneNumberAbroad.data = session['ResidentialPhoneNumberAbroad']
    form.MobilePhoneNumberAbroad.data = session['ResidentialMobilePhoneAbroad']
    form.ResidentialWhatsappAbroad.data = session['ResidentialWhatsappAb']
    form.WechatAB.data = session['WeChatId']
    form.AreaofInterestfr.data = session['AreasofInterestfr']
    form.KnowBarbados.data = session['KnowledgeOfBB']

    form.Firstname.data = session['FirstName']
    form.Middlename.data = session['MiddleName']
    form.Lastname.data = session['LastName']
    form.Gender.data = session['Gender']
    #form.dt.data = session['DOB']
    DOB = request.form.get('DOB')
    DOB = session['DOB']
    form.PassportNumber.data = session['PassportNumber']
    form.WeChat.data = session['Wechat']
    form.PhoneNumber.data = session['PhoneNumber']
    form.field_study_level.data = session['StudyLevel']
    form.edu_inst.data = session['EducationalInstitute']
    form.Jobtitle.data = session['JobTitle']
    form.Workplacename.data = session['Workplacename']
    form.OcpOther.data = session['OccupationOther']
    form.Street.data = session['Street']
    form.CityorTown.data = session['City']
    form.EmergencyConFirstname.data = session['EmergConFirstname']
    form.EmergencyConLastname.data = session['EmergConLastname']
    form.EmergencyConRel.data = session['EmergConRel']
    form.EmergencyConPhone.data = session['EmergConPhone']
    form.EmergencyConEmail.data = session['EmergConEmail']
    form.POT_des.data = session['StatedReason'] 
    form.street_bb.data = session['BAStreet']
    form.city_town_bb.data = session['BACity'] 
    form.street_abroad.data = session['street_abroad']
    form.city_abroad.data = session['city_abroad']
    form.state_abroad.data = session['state_abroad'] 
    form.EmergencyConFirstnameab.data = session['EmergencyConFirstnameab ']
    form.EmergencyConLastnameab.data = session['EmergencyConLastnameab']
    form.EmergencyConRelab.data = session['EmergencyConRel']
    form.EmergencyConPhoneab.data = session['EmergencyConphoneab']
    form.EmergencyConEmailab.data = session[' EmergencyConEmailab']

    dept_date = request.form.get('dep_date')
    dept_date= session['dept_date']

    ret_date = request.form.get('ret_date')
    ret_date= session['ret_date']   
      
    return render_template('update.html', form=form)


    # if 'username' not in session:
    #     return redirect(url_for('index'))        
    # r=Queries.SiteQuery()
    # result=r.find_existing_registered()    
    # if result is not None:
    #     return redirect(url_for('Account'))
    
    # if  request.method =='POST':
    #     database=Models.DatabaseStruct()
    #     database.UpdateFormData()            
        
    # return render_template('update.html')

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
            session['email']= result[Variables.databaseLabels.EmailAddress]
            return redirect(url_for('Account'))        
        else:
            return redirect( url_for('Error'))            
    else:
        
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
            EmailVerification.ChangePassword(email)
            return redirect(url_for('index'))
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


@app.route('/signup', methods=['POST','GET'])
def SigningUp():
    if 'username' in session:
        return redirect(url_for('index'))
        
    user_exists=Queries.SiteQuery()
    result=user_exists.find_existing_user()     
    if result is None:
        if request.form.get('password')==request.form.get('confirm_password') and request.form.get('password')  is not None:
             link = EmailVerification.Register(request.form.get('email'),request.form.get('password'),request.form.get('username'))
             
             #return render_template('login.html')
             return redirect(link)
        else:
            return render_template('signup.html') 
    else:

        return redirect(url_for('Error'))


@app.route("/myaccount")
def Account():
    if 'username' in session and model.db.users.find_one({Variables.databaseLabels.Username:session['username'],'Status':True}) is not None:
        
        return render_template("account.html")          
    else:
        #Landing page
        return redirect(url_for("index")) 


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
        session.pop('adminuser', None)    

        return redirect(url_for('adminlogin'))         
    else:
        #Landing page
        return redirect(url_for('adminlogin'))     


@app.route("/admin")
def adminindex():
    if 'adminuser' in session:
        return redirect(url_for('query'))

        #  return redirect(url_for("admindashboard"))
    else:
         #Admin login page
         return redirect(url_for("adminlogin"))


@app.route("/admin246login642",methods=['POST','GET'])
def adminlogin():
    if 'adminuser' in session and model.db.user_admin.find_one({Variables.databaseLabels.Username:session['adminuser']}) is not None:
        return redirect(url_for('admindashboard'))
    admin_exists=Queries.SiteQuery()
    result=admin_exists.find_admin()
    if result:
        if bcrypt.checkpw(request.form.get('password').encode('UTF-8'), result[Variables.databaseLabels.Password]):
            session['adminuser']=result[Variables.databaseLabels.Username]
            # Add session to adminators as well
            q=Queries.AdminQuery()
            q.Indexing()
            q.AutoEmail()

            a=q.DatabaseTotal()
            print(a)
            return redirect(url_for('query'))
            #return redirect(url_for('adminlogin'))
        else:
            return render_template('adminerror.html')
    else:
        return render_template('adminlogin.html')

@app.route("/api")
def api():
    adminquery = Queries.AdminQuery()  

    total_reg = adminquery.DatabaseTotal()
    total_abroad = adminquery.DatabaseCitizensTravellingBB()
    frens_bbos = adminquery.DatabaseOverseasResidentBB()

    countries = ("St Barthelemy", "Barbados", "Denmark", "Curaco", "St Lucia")

    map_mark_cnt = {c : v for c, v in ((entry, adminquery.CountryMarker(entry)) for entry in countries)}

    result = \
    f"""
    total_reg:{total_reg},
    total_study_abr: {total_abroad},
    frens_bbos: {frens_bbos},
    markers: {map_mark_cnt}

    """ \
        .replace('\n', '')
    # result = {"total_reg": total_reg, 
    # "total_study_abr": total_abroad,
    # "frens_bbos": frens_bbos,
    # "markers": map_mark_cnt}

    print("result is: ", result)
    
    res = make_response(json.dumps(result, separators=(',', ':')), 200)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res



       
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
        # return render_template("AdminDash.html")
        return redirect(url_for("query")) 
    else:
        #Landing page
        return redirect(url_for("adminlogin")) 


@app.route('/Adminview/<email>', methods=['POST','GET'])
def AdminView(email):
    if 'adminuser' not in session:    
        return redirect(url_for('adminlogin')) 
   

    database = Models.DatabaseStruct()
    queryresult = database.AdminViewFormData(email)
    if queryresult is None:
        return redirect(url_for('AdminView'))
    print(queryresult)
    print(email)    
    return render_template('Adminview.html',queryresult=queryresult)



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
    
    return render_template('AdminTable.html', title='Admin', userquerylist = userquerylist)     
 


# -------------------------------------------------------------------

if __name__ == "__main__":      
    app.run(debug=True)