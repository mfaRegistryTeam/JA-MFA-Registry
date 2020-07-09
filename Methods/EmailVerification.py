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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail




app = Flask(__name__)

# email = 'mfa.registry.team@gmail.com'
from_email_addr = os.environ.get('MFA_REGISTRY_EMAIL')

def send_heroku_mail(to_email_addr, subject, text=None, html=None):
    print(to_email_addr, from_email_addr, sep='|')
    mail_msg = Mail(from_email_addr, to_email_addr, subject, plain_text_content="It works bois!!" )

    try:
        api = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = api.send(mail_msg)

        if response.status_code != 200:
            print("Something went wrong")
            print(response.status_code)
            print(response.body)
            print(response.headers)
        else:
            return "Success"

    except Exception as e:
        print(e)



# password = 'valiantl3adershane'
seralizer = URLSafeTimedSerializer('ThisNeedstoChange')

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True

# app.config['MAIL_USERNAME'] = email #os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = password #os.environ.get('MAIL_PASSWORD')

# mail = Mail(app)

def formatBodyLink(subject, body, link, sender, recipient):
    msg= MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    html = """
    <html>
    <head></head>
    <body>""" + body + '<br>'+'<a href='+link+'>'+'Please Click here to Activate Account'+'</a>' + """
    </body>
    </html>
    """
    plainText = body + " " + link

    msg.attach(MIMEText(plainText,"plain"))
    msg.attach(MIMEText(html, "html"))

    return msg.as_string()
    
def formatBody(subject, body, sender, recipient):
    msg= MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    html = """
    <html>
    <head></head>
    <body>""" + body + """
    </body>
    </html>
    """
    plainText = body

    msg.attach(MIMEText(plainText,"plain"))
    msg.attach(MIMEText(html, "html"))

    return msg.as_string()

def sendEmail(subject,recipient,body):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email,password)
        server.sendmail(recipient, recipient, body)
        server.quit()
    except Exception as e:
        print(e, "email failed to send", sep='\n')

def createEmailtoken(email):
    list=[email]
    token = seralizer.dumps(list, salt ='email-confirm')
    return token


#function to send emails to specified users with a link
def Send(subject,link,recipient,body):
    html_msg = formatBodyLink(subject,body,link, os.environ.get('MFA_REGISTRY_EMAIL'),recipient)
    t = '<br>'+'<a href='+link+'>'+'Please Click here to Activate Account'+'</a>'
    send_heroku_mail(recipient, subject,html=html_msg )
    # sendEmail(subject,recipient,msg)
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
        return'<h1>The Signature has expired</h1>'
    
    return redirect(url_for('Login'))

def Register(email,password,username):
    regtoken = createEmailtoken(email)
    user_instance =Models.DatabaseStruct()
    user_instance.InsertUser(email,password,username)
    link = url_for('emailVerificationhandler', token = regtoken, _external=True)
    subject = "Confirm Ministry of Foreign Affairs and Trade Barbados National Registry Account"
    body = '<h3>Good day / evening </h3><p>This has been sent for email address confirmation and the activation of a recently created National Registry Account. Please click the link to activate account</p>'
    return Send(subject,link,email,body)

#-------------------------------------------------------------------------------------------------------
                                        #Password Change

def Send1(subject,link,recipient,body):
    msg = formatBodyLink(subject, body, link, email, recipient)
    t= '<br>'+'<a href='+link+'>'+'Please Click here to continue password change'+'</a>'
    sendEmail(subject,recipient,msg)
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
    msg = formatBody(subject, body, email, recipient)
    sendEmail(subject,recipient,msg)
    return "sent"

def EmailReminder(x):    
    email = x
    subject = "Barbados MFA Registry Account Update Reminder"
    body = '<h3>Good day / evening </h3><p>This is an email notification indicating it has been approximately 6 months since your last update. Please visit #urlhere to ensure your account information is current</p>'
    #add link to bring user directly to site
    return Sendmail(email,subject,body)