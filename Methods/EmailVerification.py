# Author Jason Charles & Shane Okukenu

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

app.config['MAIL_USERNAME'] = email #os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = password #os.environ.get('MAIL_PASSWORD')

mail =Mail(app)


def createEmailtoken(email,password,username):
    list=[email,password,username]
    token = seralizer.dumps(list, salt ='email-confirm')
    return token


#function to send emails to specified users with a link
def Send(subject,link,recipient,body):
    msg = Message(subject, sender='MFA Team', recipients=[recipient])
    msg.html = body+'<br>'+'<a href='+link+'>'+'Please Click here to Activate Account'+'</a>'
    with app.app_context():
        mail.send(msg)
    return render_template("login.html")


def confirmToken(token):
    try:       
        info = seralizer.loads(token, salt ='email-confirm', max_age = 300)
        
    except SignatureExpired:
        return'<h1>The Signature has expired</h1>'

    user_instance =Models.DatabaseStruct()      
    user_instance.InsertUser(info[0],info[1],info[2])
    
    return redirect(url_for('Login'))


def Register(email,password,username):
    regtoken = createEmailtoken(email,password,username)
    link = url_for('emailVerificationhandler', token = regtoken, _external=True)
    subject = "Confirm MFA Account"
    body = '<h3>Good day / evening </h3><p>This has been sent to confirm the email address and activate the account of a recently created MFA account please click the link to activate account</p>'
    return Send(subject,link,email,body)

