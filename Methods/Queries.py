# Author : Shane Okukenu

from Keywords import Variables
from bson import ObjectId
from flask import Flask,request,session
import bcrypt,datetime,json,re
import datetime
from pymongo import MongoClient
from datetime import timedelta
from collections import Counter
from Models import Models
from Methods import EmailVerification
import threading
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut



class SiteQuery:
    def __init__(self):
       pass
    
    
    def find_existing_user(self):
        model=Models.MyMongoDB()
        userList = model.db.users
        try:
            if session['email'] is not None:
                a = userList.find_one({Variables.databaseLabels().EmailAddress:session['email']})                  
        except KeyError:
            a = userList.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email')})

        return a

    def find_existing_registered(self):
        model=Models.MyMongoDB()
        registeredList = model.db.diasporaList
        a = registeredList.find_one({Variables.databaseLabels().EmailAddress:session['email']})
        return a

    def find_existing_history(self):
        model=Models.MyMongoDB()
        HistList = model.db.Historical
        a = HistList.find_one({Variables.databaseLabels().EmailAddress:session['email']})
        return a
    

    def find_admin(self):
        model=Models.MyMongoDB()
        adminList = model.db.user_admin
        a = adminList.find_one({Variables.databaseLabels().Username: request.form.get('username'),
        Variables.databaseLabels().EmailAddress:request.form.get('email')})
        return a


class AdminQuery:
    def __init__(self):
        pass

    def CleanUserList(self):
        mthread=threading.Timer(60.0, self.CleanUserList) 
        mthread.setDaemon(True)   
        mthread.start()
        
        model=Models.MyMongoDB()  
        cur_date=datetime.datetime.now()
        five_minutes_ago=cur_date-timedelta(minutes=4) 
        a=model.db.users.find().count()         
        if a >0 :
            model.db.users.remove({'Added':{'$lte':five_minutes_ago},'Status':False})
#Examine this
    def CleanDiasporaList(self):
        mthread=threading.Timer(60.0, self.CleanDiasporaList) 
        mthread.setDaemon(True)   
        mthread.start()
        
        model=Models.MyMongoDB()  
        cur_date=datetime.datetime.now()
        one_day_ago=cur_date-timedelta(days=1) 
        a=model.db.diasporaList.find().count()      
        #should remove records in which the expected date of return is a behind the current day   
        if a >0 :
            model.db.diasporaList.remove({'Expected-ReturnDate':{'$lte':one_day_ago}})


    def AutoEmail(self):
        model=Models.MyMongoDB()
        # 10 days before Expected date of return
        a=model.db.diasporaList.find({'Expected-ReturnDate':{'$gte':datetime.datetime.now()},'Emailed_last':{'$lte':datetime.datetime.now()+timedelta(days=-14)}}).limit(5000)
        result=list(a)
        email_list=[]
        for x in result:
            b=x[Variables.databaseLabels().EmailAddress]
            email_list.append(b)

        for thisemail in email_list:             
            EmailVerification.EmailReminder(thisemail)
            model.db.diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : thisemail},
                    {'$set':{'Emailed_last':datetime.datetime.now()}})            
            
            


    def Indexing(self):
        model=Models.MyMongoDB()        
        #1
        model.db.diasporaList.create_index([ ('Name.Last',1), ('Name.First',1)],
                                          name= "LastNameCompoundIndex",
                                          background= True)
        #2
        model.db.diasporaList.create_index([ ('Gender', 1),('Name.Last',1), ('Name.First',1) ],
                                          name= "GenderNamesCompoundIndex",
                                          background= True )
        #3
        model.db.diasporaList.create_index( [ ('Country-of-Birth',1) ,('Gender', 1),('Name.Last',1), ('Name.First',1)],
                                           name= "NatGenderNamesNatCompIndex",
                                            background= True)
        #4       
        model.db.diasporaList.create_index( [ ('Country-of-Birth',1), ('Name.Last' , 1),('Name.First',1) ],
                                          name= "ClassifactionCompoundIndex",
                                          background= True )
        #5                               
        model.db.diasporaList.create_index( [ ('Address.Country',1),('Country-of-Birth',1),('Gender',1),('Name.Last',1),
                                          ('Name.First',1) ],
                                          name= "CountryAllCompoundIndex",
                                          background= True)
        
        
        #6
        model.db.diasporaList.create_index([ ('Occupation.Type',1),('Address.Country',1),('Country-of-Birth',1),
                                          ('Gender',1),('Name.Last',1), ('Name.First',1)],
                                          name= "OccupationAllCompoundIndex",
                                          background= True )      
        #7
        model.db.diasporaList.create_index([ ( 'Occupation.Job-Class',1),('Occupation.Type',1),('Address.Country',1),('Country-of-Birth',1),
                                          ('Gender',1),('Name.Last', 1), ('Name.First', 1)],
                                          name="OccupationJobsAllCompoundIndex",
                                          background= True )    
        #8
        model.db.diasporaList.create_index( [ ('Address-in-Jamaica.Parish',1),('Destination-Address.Country',1),
                                          ('Purpose-of-Travel',1),('Country-of-Birth',1),
                                          ('Gender',1),('Name.Last',1), ('Name.First' , 1 )],
                                          name= "AddressAllCompoundIndex",
                                          background= True)
        #9
        model.db.diasporaList.create_index([  ('Destination-Address.Country',1),('Address-in-Jamaica.Parish',1),('Purpose-of-Travel',1),
                                          ('Country-of-Birth',1),('Gender',1),('Name.Last', 1), ('Name.First',1) ],
                                          name= "CitizenAllCompoundIndex",
                                          background= True)
        #10                          
        model.db.diasporaList.create_index( [('Purpose-of-Travel',1),('Destination-Address.Country',1),('Address-in-Jamaica.Parish',1)
                                          ,('Country-of-Birth',1),('Gender',1),('Name.Last', 1), ('Name.First',1)] ,
                                          name= "DestinationAllCompoundIndex",
                                          background= True )
        #11
        model.db.diasporaList.create_index( [('Amount-of-Stops',1),('Country-of-Birth',1),('Gender',1),('Name.Last', 1), ('Name.First',1)],
                                          name= "AmountofStopsAllCompoundIndex",
                                          background= True )
        #12
        model.db.diasporaList.create_index( [ ('Duration',1),('Country-of-Birth',1),('Gender',1),
                                          ('Name.Last', 1), ('Name.First',1)],
                                          name= "DurationCompoundIndex",
                                          background= True )      

        #13
        model.db.diasporaList.create_index( [('Marital-Status',1),('Country-of-Birth',1),('Gender',1),('Name.Last', 1),
                                          ('Name.First',1) ],
                                          name= "MaritalAllCompoundIndex",
                                          background= True )  

    
    def MasterQuery(self):
        model=Models.MyMongoDB()
        # history = model.db.Historical

            #general
        firstname=request.form.get('firstname_search')
        middlename=request.form.get('middlename_search')
        lastname=request.form.get('lastname_search')        
        gender=request.form.get('gender_search')

        countryofbirth=request.form.get('nationality_search')        
        othernationality=request.form.get('other_nationality_search')

        passportnum=request.form.get('passport_search')
        otherpassportnum=request.form.get('other_passport_search')


        singlecountry=request.form.get('single_country_search')
        multicountry=request.form.get('multi_country_search')
        
       
        dob_start=request.form.get('DOB_start')
        if dob_start is'' :
            dob_start='1900-01-01'
        dob_start_1=datetime.datetime(int(dob_start[0:4] ),int(dob_start[5:7]),int(dob_start[8:10]))
        

        dob_end=request.form.get('DOB_end')
        if dob_end is '':
            dob_end= '1900-01-01'
        dob_end_1=datetime.datetime(int(dob_end[0:4] ),int(dob_end[5:7]),int(dob_end[8:10]))
              
        

        address=request.form.get('address_search')        
        order=request.form.get('order_search')

       

        emailaddress=request.form.get('email_search')        
        whatsapp=request.form.get('whatsapp_search')      
        other_contact=request.form.get('other_contact_search')      

        occupation_type=request.form.get('occupation_type_search')
        study_details=request.form.get('study_details_search')
        job_class= request.form.get('job_class_search')        
        

        numstops=request.form.get('stops_search')
        duration=request.form.get('duration_search')

            #citizen travelling        
        address_parish=request.form.get('jm_parish_search')
        
        purpose=request.form.get('purpose_search')


        dep_date_start=request.form.get('dep_date_start')
        if dep_date_start=='':
            dep_date_start='1900-01-01'
        exp_dep_st=datetime.datetime(int(dep_date_start[0:4] ),int(dep_date_start[5:7]),int(dep_date_start[8:10]))       


        dep_date_end=request.form.get('dep_date_end')
        if dep_date_end=='':
            dep_date_end='1900-01-01'
        exp_dep_end=datetime.datetime(int(dep_date_end[0:4] ),int(dep_date_end[5:7]),int(dep_date_end[8:10]))
        

        ret_date_start=request.form.get('ret_date_start')
        if ret_date_start=='':
            ret_date_start='1900-01-01'
        exp_ret_st=datetime.datetime(int(ret_date_start[0:4] ),int(ret_date_start[5:7]),int(ret_date_start[8:10]))
        
        
        ret_date_end=request.form.get('ret_date_end')
        if ret_date_end=='':
            ret_date_end='1900-01-01'
        exp_ret_end=datetime.datetime(int(ret_date_end[0:4] ),int(ret_date_end[5:7]),int(ret_date_end[8:10]))

        default_yr='1900-01-01'

       
        query = {}
        if firstname is not '':
            query.update({'Name.First':{'$regex':firstname,"$options": "-i"}})
         
        if middlename is not '':
            query.update({'Name.Middle':{'$regex':middlename,"$options": "-i"}})

        if emailaddress is not '':
            query.update({'Email-Address':{'$regex': emailaddress,"$options": "-i"}})


        if lastname is not '':
            query.update({'Name.Last':{'$regex':lastname,'$options':"-i"}})
        
       
        if gender is not None:
            query.update({Variables.databaseLabels().Gender:gender})

        if countryofbirth is not '':
           query.update( {Variables.databaseLabels().CountryofBirth:countryofbirth})
        
        if numstops is not None:
            query.update( {Variables.databaseLabels().AmountStops:numstops})

            #1
        if singlecountry is not '':
            query.update(  { "$or":[{'Country-One-Single.Airport-Stopover-Country':singlecountry},
                            {'Country-One-Single.Short-Ext-Country':singlecountry}] } )
            #2 -#5      

        if multicountry is not '':
                query.update(  { "$or":[{'Two-Countries.Country-One-Multi.Airport-Stopover-Country':multicountry},
                {'Two-Countries.Country-One-Multi.Short-Ext-Country':multicountry},
                {'Two-Countries.Country-Two.Airport-Stopover-Country':multicountry},
                {'Two-Countries.Country-Two.Short-Ext-Country':multicountry},

                {'Three-Countries.Country-One-Multi.Airport-Stopover-Country':multicountry},
                {'Three-Countries.Country-One-Multi.Short-Ext-Country':multicountry},
                {'Three-Countries.Country-Two.Airport-Stopover-Country':multicountry},
                {'Three-Countries.Country-Two.Short-Ext-Country':multicountry},
                {'Three-Countries.Country-Three.Airport-Stopover-Country':multicountry},
                {'Three-Countries.Country-Three.Short-Ext-Country':multicountry},

                {'Four-Countries.Country-One-Multi.Airport-Stopover-Country':multicountry},
                {'Four-Countries.Country-One-Multi.Short-Ext-Country':multicountry},
                {'Four-Countries.Country-Two.Airport-Stopover-Country':multicountry},
                {'Four-Countries.Country-Two.Short-Ext-Country':multicountry},
                {'Four-Countries.Country-Three.Airport-Stopover-Country':multicountry},
                {'Four-Countries.Country-Three.Short-Ext-Country':multicountry},
                {'Four-Countries.Country-Four.Airport-Stopover-Country':multicountry},
                {'Four-Countries.Country-Four.Short-Ext-Country':multicountry},

                {'Five-Countries.Country-One-Multi.Airport-Stopover-Country':multicountry},
                {'Five-Countries.Country-One-Multi.Short-Ext-Country':multicountry},
                {'Five-Countries.Country-Two.Airport-Stopover-Country':multicountry},
                {'Five-Countries.Country-Two.Short-Ext-Country':multicountry},
                {'Five-Countries.Country-Three.Airport-Stopover-Country':multicountry},
                {'Five-Countries.Country-Three.Short-Ext-Country':multicountry},
                {'Five-Countries.Country-Four.Airport-Stopover-Country':multicountry},
                {'Five-Countries.Country-Four.Short-Ext-Country':multicountry},
                {'Five-Countries.Country-Five.Airport-Stopover-Country':multicountry},
                {'Five-Countries.Country-Five.Short-Ext-Country':multicountry}               
                
                 ] } )   

        
        if duration is not '':
                query.update(  { "$or":[{'Country-One-Single.Duration':duration},{'Two-Countries.Country-One-Multi.Duration':duration},
                {'Two-Countries.Country-One-Multi.Duration':duration},
                {'Two-Countries.Country-Two.Duration':duration},
                {'Two-Countries.Country-Two.Duration':duration},

                {'Three-Countries.Country-One-Multi.Duration':duration},
                {'Three-Countries.Country-One-Multi.Duration':duration},
                {'Three-Countries.Country-Two.Duration':duration},
                {'Three-Countries.Country-Two.Duration':duration},
                {'Three-Countries.Country-Three.Duration':duration},
                {'Three-Countries.Country-Three.Duration':duration},

                {'Four-Countries.Country-One-Multi.Duration':duration},
                {'Four-Countries.Country-One-Multi.Duration':duration},
                {'Four-Countries.Country-Two.Duration':duration},
                {'Four-Countries.Country-Two.Duration':duration},
                {'Four-Countries.Country-Three.Duration':duration},
                {'Four-Countries.Country-Three.Duration':duration},
                {'Four-Countries.Country-Four.Duration':duration},
                {'Four-Countries.Country-Four.Duration':duration},

                {'Five-Countries.Country-One-Multi.Duration':duration},
                {'Five-Countries.Country-One-Multi.Duration':duration},
                {'Five-Countries.Country-Two.Duration':duration},
                {'Five-Countries.Country-Two.Duration':duration},
                {'Five-Countries.Country-Three.Duration':duration},
                {'Five-Countries.Country-Three.Duration':duration},
                {'Five-Countries.Country-Four.Duration':duration},
                {'Five-Countries.Country-Four.Duration':duration},
                {'Five-Countries.Country-Five.Duration':duration},
                {'Five-Countries.Country-Five.Duration':duration}               
                
                 ] } )   

        if address is not '':
            query.update({'Address-in-Jamaica.City/Town':{'$regex':address,"$options": "-i"}})

        if passportnum is not '':
            query.update({'Jamaican-Passport-Number':{'$regex':passportnum,"$options": "-i"}})

        if otherpassportnum is not '':
            query.update({'Other-Passport-Number':{'$regex':otherpassportnum,"$options": "-i"}})

        if whatsapp is not '':
            query.update({'Whatsapp-Number':{'$regex':whatsapp,"$options": "-i"}})

        if other_contact is not '':
            query.update({'OtherContact-Info':{'$regex':other_contact,"$options": "-i"}})
        

        if occupation_type is not None:
            query.update( {'Occupation.Type':occupation_type})

        if job_class is not '':
            query.update( {'Occupation.Job-Class':job_class})

        if address_parish is not '':
            query.update({'Address-in-Jamaica.Parish':address_parish})        

             
        if purpose is not '':
            query.update({Variables.databaseLabels().PurposeofTravel:purpose})       
         

        if dob_start !='1900-01-01':
            query.update({Variables.databaseLabels().DOB :{'$gte':dob_start_1,'$lte':dob_end_1}})

        if dep_date_start !='1900-01-01':
            query.update({'Travel-Date-Details.Expected-DepDate':{'$gte':exp_dep_st,'$lte':exp_dep_end}})

        if ret_date_start !='1900-01-01':
            query.update({'Travel-Date-Details.Expected-ReturnDate':{'$gte':exp_ret_st,'$lte':exp_ret_end}})           

        if study_details is not '':
            query.update({'Occupation.Study-Details':{'$regex':study_details,'$options':"-i"}})

        
        if othernationality is not '':
            query.update({Variables.databaseLabels().OtherNationality:othernationality})        

            
        # print("Query Here Below")
        # print("Single Country Selection",singlecountry)
        # print("Multi Country Selection",multicountry)
        # print(query)
        result = model.db.diasporaList.find(query)

                
        return result      

#Static Queries

 




