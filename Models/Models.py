# Author: Shane Okukenu 

from Keywords import Variables
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask,request
import bcrypt,datetime


class User:
    def __init__(self, username,password,email):
        self.username = username
        self.password = password
        self.email = email


    def get_account_details(self):        
        return[self.username,self.password,self.email]


class MyMongoDB(object):
    def __init__(self):
        self._client = MongoClient('localhost', 27017)
        self.db = self._client[Variables.siteLabels.DatabaseName]


class DatabaseStruct:
    def __init__(self):
        pass   


    def InsertUser(self,email,password,username):

        hashpass=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt() )
        model=MyMongoDB()
        users=model.db.users
        users.insert_one({
            Variables.databaseLabels().Username : username,
            Variables.databaseLabels().Password: hashpass,
            Variables.databaseLabels().EmailAddress :email
            
         }) 

    def InsertAdmin(self):     

        model=MyMongoDB()
        user_admin=model.db.user_admin

        if request.form.get('perm1') is None:
            perm1= " "
        else:
             perm1=request.form.get('perm1')

        if request.form.get('perm2') is None:
            perm2= " "
        else:
             perm2=request.form.get('perm2')

        if request.form.get('perm3') is None:
            perm3= " "
        else:
             perm3=request.form.get('perm3')

        if request.form.get('perm4') is None:
            perm4= " "
        else:
             perm4=request.form.get('perm4')

        permission_set={'one':perm1,'two':perm2,'three':perm3,'four':perm4}
        password=request.form.get('password')     
        hashpass=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt() )

        user_admin.insert_one({
            Variables.databaseLabels().Username :request.form.get('username'),
            Variables.databaseLabels().EmailAddress :request.form.get('email'),
            Variables.databaseLabels().Password: hashpass,
            Variables.databaseLabels().Permissions:permission_set 
         }) 


    def InsertFormData(self):   
        datestring=request.form.get('DOB')
        date_object = datetime.datetime(int(datestring[0:4] ),int(datestring[5:7]),int(datestring[8:10]))
        timestamp = datetime.datetime.now() 
        hashpass=bcrypt.hashpw(request.form.get('password').encode('UTF-8'), bcrypt.gensalt() )
        col = MyMongoDB()
        diasporaList=col.db.diasporaList

        diasporaList.insert_one({
                    Variables.databaseLabels().Username : request.form.get('username'),
                    Variables.databaseLabels().EmailAddress : request.form.get('email'),
                    Variables.databaseLabels().Password: hashpass,
                    Variables.databaseLabels().Firstname: request.form.get('first-name'),
                    Variables.databaseLabels().Middlename: request.form.get('middle-name'),
                    Variables.databaseLabels().Lastname: request.form.get('last-name'),
                    Variables.databaseLabels().Gender: request.form.get('gender'), 
                    Variables.databaseLabels().DOB: date_object,                    
                    Variables.databaseLabels().Occupation: request.form.get('occupation'),
                    Variables.databaseLabels().FieldofStudy: request.form.get('field-study'),
                    Variables.databaseLabels().EducationalInst: request.form.get('edu-inst'),
                    Variables.databaseLabels().Jobtitle: request.form.get('job-title'),
                    Variables.databaseLabels().Workplace: request.form.get('workplace-name'),
                    Variables.databaseLabels().BarbadosID:request.form.get('BId-num'),
                    Variables.databaseLabels().PhoneNumber: request.form.get('phone-num'),
                    Variables.databaseLabels().Nationality: request.form.get('country'),
                    Variables.databaseLabels().Parish: request.form.get('parish'),
                    Variables.databaseLabels().BarbadosAddress: request.form.get('address'),
                    Variables.databaseLabels().PurposeofTravel: request.form.get('radio'),
                    Variables.databaseLabels().CountryAbroad: request.form.get('country-abroad'),
                    Variables.databaseLabels().AddressAbroad: request.form.get('address-abroad'),
                    Variables.databaseLabels().CityorTown: request.form.get('city-town'),
                    Variables.databaseLabels().AbroadPhone: request.form.get('abroad-phone'),
                    Variables.databaseLabels().AbroadEmail: request.form.get('abroad-email'),
                    Variables.databaseLabels().EmergencyConFirstname: request.form.get('emerg-firstname'),
                    Variables.databaseLabels().EmergencyConLastname: request.form.get('emerg-lastname'),
                    Variables.databaseLabels().EmergencyConRel: request.form.get('emerg-rel'),
                    Variables.databaseLabels().EmergencyConPhone: request.form.get('emerg-phone'),
                    Variables.databaseLabels().EmergencyConEmail: request.form.get('emerg-email'),
                    Variables.databaseLabels().LastUpdated : timestamp      })   



class Graph:
    def __init__(self):
        pass


class Noticeboard: 
    def __init__(self): 
        pass

        
        