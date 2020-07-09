# Author Shane Okukenu & Jason Charles

from flask import Flask, url_for, render_template,redirect
from flask_mail import Mail, Message 
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from bson import ObjectId
import os,sys,bcrypt
from Keywords import Variables
from datetime import datetime
from Models import Models
import smtplib


app = Flask(__name__)

email = 'mfa.registry.team@gmail.com'
password = 'valiantl3adershane'
seralizer = URLSafeTimedSerializer('ThisNeedstoChange')

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

app.config['MAIL_USERNAME'] = email #os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = password #os.environ.get('MAIL_PASSWORD')

mail =Mail(app)


def createEmailtoken(email):
    list=[email]
    token = seralizer.dumps(list, salt ='email-confirm')
    return token


#function to send emails to specified users with a link
def Send(subject,link,recipient,body):
    msg = Message(subject, sender='Ministry of Foreign Affairs and Trade Barbados National Registry Team', recipients=[recipient])
    msg.html = body+'<br>'+'<a href='+link+'>'+'Please Click here to Activate Account'+'</a>'
    with app.app_context():
        mail.send(msg)
    return render_template("login.html")


def confirmToken(token):
    model=Models.MyMongoDB()
    users=model.db.users
    try:       
        info = seralizer.loads(token, salt ='email-confirm', max_age = 300)
        users.update_one(
            {Variables.databaseLabels().EmailAddress : info[0]},
            {'$set':{'Status':True}})  

        # This history collection is created once for the user at the same time his user document is verified
        history=model.db.Historical
        HistoryList=[]
        history.insert_one({
            Variables.databaseLabels().EmailAddress :info[0],
            Variables.databaseLabels().History: HistoryList
            })            
    except SignatureExpired:
        return render_template("errortimeout.html")
    
    return redirect(url_for('Login'))

def Register(email,password,username):
    regtoken = createEmailtoken(email)
    user_instance =Models.DatabaseStruct()
    user_instance.InsertUser(email,password,username)
    link = url_for('emailVerificationhandler', token = regtoken, _external=True)
    subject = "Confirm Ministry of Foreign Affairs and Trade Barbados National Registry Account"
    body = '<h3>Good day / evening </h3><p>This has been sent for email address confirmation and the activation of a recently created National Registry Account. Please click the link to activate account</p>'
    #return Send(subject,link,email,body)
    return link

#-------------------------------------------------------------------------------------------------------
                                        #Password Change

def Send1(subject,link,recipient,body):
    msg = Message(subject, sender='Ministry of Foreign Affairs and Trade Barbados National Registry Team', recipients=[recipient])
    msg.html = body+'<br>'+'<a href='+link+'>'+'Please Click here to continue password change'+'</a>'
    with app.app_context():
        mail.send(msg)
    return redirect(url_for('Login'))

def createPasswordtoken(email):
    list=[email]
    token =seralizer.dumps(list, salt ='password-change')
    return token

def ChangePassword(email):
    changetoken = createPasswordtoken(email)
    plink = url_for('PasswordChangehandler', token = changetoken, _external=True)
    subject = "Barbados MFA Registry Account Password Change Request"
    body = '<h3>Good day / evening </h3><p>This email has been sent to confirm you wish to change your Registry Account password.</p>'    
    return Send1(subject,plink,email,body)


def confirm_password(token):
    try: info = seralizer.loads(token, salt='password-change', max_age=300)
    except SignatureExpired:
        return'<h1>The Signature has expired</h1>'
    email = info[0]
    return render_template("pchange2.html", value = email)



#---------------------------------------------------------------------------------------------------------



def Sendmail(recipient,subject,body):
    msg = Message(subject, sender='Ministry of Foreign Affairs and Trade Barbados National Registry Team', recipients=[recipient])
    msg.html = body+'<br>'
    with app.app_context():
        mail.send(msg)
    return "sent"

def EmailReminder(x):    
    email = x
    subject = "Barbados MFA Registry Account Update Reminder"
    body = '<h3>Good day / evening </h3><p>This is an email notification indicating it has been approximately 6 months since your last update. Please visit #urlhere to ensure your account information is current</p>'
    #add link to bring user directly to site
    return Sendmail(email,subject,body)