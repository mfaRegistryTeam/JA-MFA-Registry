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
            a = userList.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email'),'Status':True})

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


    def AutoEmail(self):
        model=Models.MyMongoDB()
        a=model.db.diasporaList.find({'Date-Last-Updated':{'$lte':datetime.datetime.now()+ timedelta(days=-183)},'Emailed_last':{'$lte':datetime.datetime.now()+timedelta(days=-4)}}).limit(5000)
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
        model.db.diasporaList.create_index( [ ('Nationality',1) ,('Gender', 1),('Name.Last',1), ('Name.First',1)],
                                           name= "NatGenderNamesNatCompIndex",
                                            background= True)
        #4       
        model.db.diasporaList.create_index( [ ('Classification', 1),('Nationality',1), ('Name.Last' , 1),('Name.First',1) ],
                                          name= "ClassifactionCompoundIndex",
                                          background= True )
        #5                               
        model.db.diasporaList.create_index( [ ('Address.Country',1),('Classification',1),('Nationality',1),('Gender',1),('Name.Last',1),
                                          ('Name.First',1) ],
                                          name= "CountryAllCompoundIndex",
                                          background= True)
        
        
        #6
        model.db.diasporaList.create_index([ ('Occupation.Type',1),('Address.Country',1),('Classification', 1),('Nationality',1),
                                          ('Gender',1),('Name.Last',1), ('Name.First',1)],
                                          name= "OccupationAllCompoundIndex",
                                          background= True )      
        #7
        model.db.diasporaList.create_index([ ( 'Occupation.Job-Class',1),('Occupation.Type',1),('Address.Country',1),('Classification', 1),('Nationality',1),
                                          ('Gender',1),('Name.Last', 1), ('Name.First', 1)],
                                          name="OccupationJobsAllCompoundIndex",
                                          background= True )    
        #8
        model.db.diasporaList.create_index( [ ('Address-in-Barbados.Parish',1),('Destination-Address.Country',1),
                                          ('Purpose-of-Travel',1),('Classification', 1),('Nationality',1),
                                          ('Gender',1),('Name.Last',1), ('Name.First' , 1 )],
                                          name= "AddressAllCompoundIndex",
                                          background= True)
        #9
        model.db.diasporaList.create_index([  ('Destination-Address.Country',1),('Address-in-Barbados.Parish',1),('Purpose-of-Travel',1),
                                          ('Classification', 1),('Nationality',1),('Gender',1),('Name.Last', 1), ('Name.First',1) ],
                                          name= "CitizenAllCompoundIndex",
                                          background= True)
        #10                          
        model.db.diasporaList.create_index( [('Purpose-of-Travel',1),('Destination-Address.Country',1),('Address-in-Barbados.Parish',1),
                                          ('Classification', 1),('Nationality',1),('Gender',1),('Name.Last', 1), ('Name.First',1)] ,
                                          name= "DestinationAllCompoundIndex",
                                          background= True )
        #11
        model.db.diasporaList.create_index( [('Residence-Abroad-Address.Country',1),('Areas-of-Interest',1),('Classification', 1),
                                          ('Nationality',1),('Gender',1),('Name.Last', 1), ('Name.First',1)],
                                          name= "ResidentAllCompoundIndex",
                                          background= True )
        #12
        model.db.diasporaList.create_index( [ ('Areas-of-Interest-fr',1),('Classification', 1),('Nationality',1),('Gender',1),
                                          ('Name.Last', 1), ('Name.First',1)],
                                          name= "AOIAllCompoundIndex",
                                          background= True )      

        #13
        model.db.diasporaList.create_index( [('Knowledge-of-BB',1),('Classification', 1),('Nationality',1),('Gender',1),('Name.Last', 1),
                                          ('Name.First',1) ],
                                          name= "KBBAllCompoundIndex",
                                          background= True )  

    
    def GetHistory(self,arrayfound):
        model=Models.MyMongoDB()
        history=model.db.Historical
        array_found=self.arrayfound
        found_doc_email=array_found[0][Variables.databaseLabels().EmailAddress]
        history_file_doc=history.find_one({Variables.databaseLabels().EmailAddress:found_doc_email})
        result=history_file_doc[Variables.databaseLabels().History]
        return result
        
        

    def MasterQuery(self):
        model=Models.MyMongoDB()
        history = model.db.Historical

            #general
        firstname=request.form.get('firstname_search')
        middlename=request.form.get('middlename_search')
        lastname=request.form.get('lastname_search')        
        gender=request.form.get('gender_search')
        
       
        dob_start=request.form.get('DOB_start')
        if dob_start is'' :
            dob_start='1900-01-01'
        dob_start_1=datetime.datetime(int(dob_start[0:4] ),int(dob_start[5:7]),int(dob_start[8:10]))
        

        dob_end=request.form.get('DOB_end')
        if dob_end is '':
            dob_end= '1900-01-01'
        dob_end_1=datetime.datetime(int(dob_end[0:4] ),int(dob_end[5:7]),int(dob_end[8:10]))
              
        

        address=request.form.get('address_search')
        country=request.form.get('country_search')

        nationality=request.form.get('nationality_search')        
        passportcountry=request.form.get('ppissue_search')
        passportnum=request.form.get('passport_search')        

        emailaddress=request.form.get('email_search')
        we_chat=request.form.get('wechat_search')
        phone=request.form.get('phone_search')      

        occupation_type=request.form.get('occupation_type_search')
        study_level=request.form.get('study_level_search')
        study_field=request.form.get('study_field_search')
        job_class= request.form.get('job_class_search')
        
        

        classification=request.form.get('class_search')

            #citizen travelling        
        address_parish=request.form.get('bb_parish_search')
        dest_country=request.form.get('dest_country_search')
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

            #resident overseas
        res_interests=request.form.get('interest_search')
        res_country=request.form.get('res_country_search')

            #friends barbados
        fr_interests=request.form.get('interestsfr_search')
        fr_country=request.form.get('countryfr_search')
        KnowledgeofBB=request.form.get('KBB_search')

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

        if nationality is not '':
           query.update( {Variables.databaseLabels().Nationality:nationality})
        
        if classification is not None:
            query.update( {Variables.databaseLabels().Classification:classification})

        if country is not '':
            query.update( {'Address.Country':country})

        if address is not '':
            query.update({'Address.City/Town':{'$regex':address,"$options": "-i"}})

        if passportnum is not '':
            query.update({'Passport-Number':{'$regex':passportnum,"$options": "-i"}})

        # if we_chat is not '':
        #     query.update({'WeChat-ID':{'$regex':we_chat,"$options": "-i"}})

        if phone is not '':
            query.update({'Phone-Number':{'$regex':phone,"$options": "-i"}})

        if occupation_type is not None:
            query.update( {'Occupation.Type':occupation_type})

        if job_class is not '':
            query.update( {'Ocuupation.Job-Class':job_class})

        if address_parish is not '':
            query.update({'Address-in-Barbados.Parish':address_parish})

        if dest_country is not '':
            query.update({'Destination-Address.Country':dest_country})

        if purpose is not '':
            query.update({Variables.databaseLabels().PurposeofTravel:purpose})
        
        
        if res_country is not '':
            query.update({'Residence-Abroad-Address.Country':res_country})        

        

        if fr_interests is None:
            pass
        if fr_interests is not None:  
                    
            query.update({Variables.databaseLabels().AreasofInterestFr:{'$all':[fr_interests]}})
        
        if KnowledgeofBB is None:
            pass
        if KnowledgeofBB is not None:
            
            query.update({Variables.databaseLabels().KnowledgeofBB:{'$all':[KnowledgeofBB]}})

       
         

        if dob_start !='1900-01-01':
            query.update({Variables.databaseLabels().DOB :{'$gte':dob_start_1,'$lte':dob_end_1}})

        if dep_date_start !='1900-01-01':
            query.update({'Travel-Date-Details.Expected-DepDate':{'$gte':exp_dep_st,'$lte':exp_dep_end}})

        if ret_date_start !='1900-01-01':
            query.update({'Travel-Date-Details.Expected-ReturnDate':{'$gte':exp_ret_st,'$lte':exp_ret_end}})

            

        if res_interests is None:
            pass
        if res_interests is not None:   
                     
            query.update({Variables.databaseLabels().AreasofInterest:{'$all':[res_interests]}})

        if study_field is not '':
            query.update({'Occupation.Field-of-Study':study_field})

        if study_level is not None:
            query.update({'Occupation.Level':study_level})

        if passportcountry is not '':
            query.update({Variables.databaseLabels().IssuedPassportCountry:passportcountry})

        

            
        # Each result represents a single person that is return from the query.
        # If 1 person is returned then as it stands the history of updates available for that person can be seen
        # using histlist from GetHistory() ordered by most recent first. Can see the logic in

        # If you trace and follow along I know you can see the logic

        result = model.db.diasporaList.find(query)

        #histlist=AdminQuery.GetHistory(array_found=result)
        
        return result  

    

#Static Queries
    def DatabaseTotal(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            querycol=model.db
            querycol=querycol.diasporaList
            result= querycol.find({})
            count =0            
            for item in result:
                print(item)
                count+=1  
        return count
    
    def DatabaseFriendsBB(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            querycol=model.db
            querycol=querycol.diasporaList
            result= querycol.find({'Classification':'Friend'})
            count =0            
            for item in result:
                print(item)
                count+=1  
        return count

    def DatabaseCitizensTravellingBB(self):        
        if 'adminuser' in session:            
            model=Models.MyMongoDB()
            querycol=model.db
            querycol=querycol.diasporaList
            result= querycol.find({'Classification':'CitizenTO'})
            count =0            
            for item in result:
                print(item)
                count+=1           
                       
        return count

    def DatabaseOverseasResidentBB(self):    
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        result= querycol.find({'Classification':'ResidentO'})
        count =0            
        for item in result:
            print(item)
            count+=1  
        return count
    
    def NAmericaResidentBB(self):
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        result=querycol.find({'Classification':'ResidentO','Residence-Abroad-Address.Location.0':{'$gte':7,'$lte':84},
            'Residence-Abroad-Address.Location.1':{'$gte':-180,'$lte':-20}})
        count = 0            
        for item in result:
            print(item)
            count+=1                                 
        return count

    def EUResidentBB(self):
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        result=querycol.find({'Classification':'ResidentO','Residence-Abroad-Address.Location.0':{'$gte':35,'$lte':72},
        'Residence-Abroad-Address.Location.1':{'$gte':-25,'$lte':65}})       
        count =0     
        for item in result:
            print(item)
            count+=1                    
        return count
    
    def AsiaResidentBB(self):
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        result=querycol.find({'Classification':'ResidentO','Residence-Abroad-Address.Location.0':{'$gte':-10,'$lte':80},
        'Residence-Abroad-Address.Location.1':{'$gte':-170,'$lte':25}})
        count =0            
        for item in result:
            print(item)
            count+=1                                                
        return count
    
    def AfricaResidentBB(self): 
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        result=model.db.diasporaList.find({'Classification':'ResidentO','Residence-Abroad-Address.Location.0':{'$gte':-37,'$lte':35},
        'Residence-Abroad-Address.Location.1':{'$gte':-17,'$lte':50}})
        count =0            
        for item in result:
            print(item)
            count+=1   

        return count

    def SAmericaResidentBB(self):
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        result=model.db.diasporaList.find({'Classification':'ResidentO','Residence-Abroad-Address.Location.0':{'$gte':-55,'$lte':12},
        'Residence-Abroad-Address.Location.1':{'$gte':-81,'$lte':-35}})
        count =0            
        for item in result:
            print(item)
            count+=1   

        return count

    #Takes string type of country name that matches the exact pattern in the html dropdown
    def CountryMarker(self,name):
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        lst=[]
        countries = [
            "Barbados","Canada","United Kingdom","United States of America","Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla",
            "Antigua & Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Belarus","Belgium","Belize",
            "Benin","Bermuda","Bhutan","Bolivia","Bonaire","Bosnia & Herzegovina","Botswana","Brazil","British Indian Ocean Ter","Brunei","Bulgaria","Burkina Faso",
            "Burundi","Cambodia","Cameroon","Canary Islands","Cape Verde","Cayman Islands","Central African Republic","Chad","Channel Islands","Chile","China",
            "Christmas Island","Cocos Island","Colombia","Comoros","Congo","Cook Islands","Costa Rica","Cote DIvoire","Croatia","Cuba","Curaco","Cyprus",
            "Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia",
            "Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","French Guiana","French Polynesia","French Southern Ter","Gabon","Gambia","Georgia",
            "Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guinea","Guyana","Haiti","Honduras","Hong Kong","Hungary",
            "Iceland","Indonesia","India","Iran","Iraq","Isle of Man","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea North",
            "Korea South","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia",
            "Madagascar","Malaysia","Malawi","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Midway Islands",
            "Moldova","Monaco","Mongolia","Montserrat","Morocco","Mozambique","Myanmar","Nambia","Nauru","Nepal","Netherland Antilles","Netherlands","Nevis",
            "New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Norway","Oman","Pakistan","Palau Island","Palestine","Panama",
            "Papua New Guinea","Paraguay","Peru","Phillipines","Pitcairn Island","Poland","Portugal","Puerto Rico","Qatar","Republic of Montenegro","Republic of Serbia",
            "Reunion","Romania","Russia","Rwanda","St Barthelemy","St Eustatius","St Helena","St Kitts-Nevis","St Lucia","St Maarten","St Pierre & Miquelon",
            "St Vincent & Grenadines","Saipan","Samoa","Samoa American","San Marino","Sao Tome & Principe","Saudi Arabia","Senegal","Seychelles","Sierra Leone",
            "Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria",
            "Tahiti","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tokelau","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Turks & Caicos Is",
            "Tuvalu","Uganda","Ukraine","United Arab Erimates","Uraguay","Uzbekistan","Vanuatu","Vatican City State","Venezuela","Vietnam","Virgin Islands (Brit)",
            "Virgin Islands (USA)","Wake Island","Wallis & Futana Is","Yemen","Zaire","Zambia","Zimbabwe"]

        for country in countries:
            geolocator = Nominatim(user_agent="Barbados")
            try:
                location = geolocator.geocode(country,timeout=16000) 
                latitude=location.latitude
                longitude=location.longitude  
            except GeocoderTimedOut as e:    
                print("Error: geocode failed on input %s with message %s"%(country,e.message))
                #redirect to another page?
                pass            
            result=model.db.diasporaList.find({'Classification':'ResidentO','Residence-Abroad-Address.Country':country})
            count =0            
            for item in result:                
                count+=1   
            lst.append([country,(latitude,longitude),count])
        return lst

    #Returns documents updated by the user in the past week
    def WeeklyUpdated(self):
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        cur_date=datetime.datetime.now()
        last_week=cur_date-timedelta(weeks=1)
        a=querycol.find({'Date-Last-Updated':{'$gte':last_week,'$lte':cur_date}}).sort([('Date-Last-Updated',-1)]).limit(50)
        lst=[]
        for item in a:
            lst.append(item)
        return lst

    #Returns documents added ie registrations in the past week
    def WeeklyAdded(self):        
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        cur_date=datetime.datetime.now()
        last_week=cur_date-timedelta(weeks=1)
        a=querycol.find({'Date-Added':{'$gte':last_week,'$lte':cur_date}}).sort([('Date-Added',-1)]).limit(50)
        lst=[]
        for item in a:
            lst.append(item)
        return lst

    #returns Top 4 interests of Residents overseas from the database info
    def InterestsCount(self):
        
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
        edu_col=querycol.find({'Areas-of-Interest':'Education'})
        count =0            
        for item in edu_col:
            count+=1  
        edu_count=count
        sprt_col=querycol.find({'Areas-of-Interest':'Sports'})
        count =0  
        for item in sprt_col:
            count+=1  
        sprt_count=count

        inv_col=querycol.find({'Areas-of-Interest':'Investment'})
        count =0  
        for item in inv_col:                
            count+=1  
        inv_count=count

        med_col=querycol.find({'Areas-of-Interest':'Medical'})
        count =0  
        for item in med_col:                
            count+=1  
        med_count=count

        vol_col=querycol.find({'Areas-of-Interest':'Volunteerism'})
        count =0  
        for item in vol_col:                
            count+=1  
        vol_count=count

        re_col=querycol.find({'Areas-of-Interest':'Real-Estate'})
        count =0  
        for item in re_col:                
            count+=1  
        re_count=count

        cult_col=querycol.find({'Areas-of-Interest':'Culture'})
        count =0  
        for item in cult_col:                
            count+=1  
        cult_count=count

        gen_col=querycol.find({'Areas-of-Interest':'Geneology'})
        count =0  
        for item in gen_col:   
            count+=1  
        gen_count=count

        oth_col=querycol.find({'Areas-of-Interest':'Other'})
        count =0  
        for item in oth_col:                
            count+=1  
        oth_count=count

        interest_dict={'Education':edu_count,'Sports':sprt_count,'Investment':inv_count,'Medical':med_count,
        'Volunteerism':vol_count,'Real-Estate':re_count,'Culture':cult_count,'Geneology':gen_count,'Other':oth_count}
        k = Counter(interest_dict) 
        fin_list=[]
        
        # Finding 4 highest values 
        high = k.most_common(4)           
        for i in high:
            fin_list.append((i[0],i[1])) 

        return fin_list  

# returns Top 4 interests of Friends of barbados overseas from the database info
    def InterestsCountFr(self):        
        model=Models.MyMongoDB()
        querycol=model.db
        querycol=querycol.diasporaList
                
        edu_col=querycol.find({'Areas-of-Interest-fr':'Education'})
        count =0            
        for item in edu_col:
            count+=1  
        edu_count=count
        sprt_col=querycol.find({'Areas-of-Interest-fr':'Sports'})
        count =0  
        for item in sprt_col:
            count+=1  
        sprt_count=count

        inv_col=querycol.find({'Areas-of-Interest-fr':'Investment'})
        count =0  
        for item in inv_col:                
            count+=1  
        inv_count=count

        med_col=querycol.find({'Areas-of-Interest-fr':'Medical'})
        count =0  
        for item in med_col:                
            count+=1  
        med_count=count

        vol_col=querycol.find({'Areas-of-Interest-fr':'Volunteerism'})
        count =0  
        for item in vol_col:                
            count+=1  
        vol_count=count

        re_col=querycol.find({'Areas-of-Interest-fr':'Real-Estate'})
        count =0  
        for item in re_col:                
            count+=1  
        re_count=count

        cult_col=querycol.find({'Areas-of-Interest-fr':'Culture'})
        count =0  
        for item in cult_col:                
            count+=1  
        cult_count=count

        gen_col=querycol.find({'Areas-of-Interest-fr':'Geneology'})
        count =0  
        for item in gen_col:                
            count+=1  
        gen_count=count

        oth_col=querycol.find({'Areas-of-Interest-fr':'Other'})
        count =0  
        for item in oth_col:                
            count+=1  
        oth_count=count       

        interest_dict={'Education':edu_count,'Sports':sprt_count,'Investment':inv_count,'Medical':med_count,
        'Volunteerism':vol_count,'Real-Estate':re_count,'Culture':cult_count,'Geneology':gen_count,'Other':oth_count}
        k = Counter(interest_dict) 
        fin_list_fr=[]
        
        # Finding 4 highest values 
        high = k.most_common(4)           
        for i in high:
            fin_list_fr.append((i[0],i[1])) 

        return fin_list_fr  


# returns Top 4  Job categories  from the database info
def JobClassCount(self):
    model=Models.MyMongoDB()
    querycol=model.db
    querycol=querycol.diasporaList

    adv_col=querycol.find({'Occupation.Job-Class':'Advertising,Promotions,Marketing'})
    count =0  
    for item in adv_col:                
        count+=1  
    adv_count=count       

    AE_col=querycol.find({'Occupation.Job-Class':'Architecture & Engineering'})
    count =0  
    for item in AE_col:                
        count+=1  
    AE_count=count

    busin_col=querycol.find({'Occupation.Job-Class':'Business'})
    count =0  
    for item in busin_col:                
        count+=1  
    busin_count=count     

    edu_col=querycol.find({'Occupation.Job-Class':'Education'})
    count =0  
    for item in edu_col:                
        count+=1  
    edu_count=count       

    fin_col=querycol.find({'Occupation.Job-Class':'Finance'})
    count =0  
    for item in fin_col:                
        count+=1  
    fin_count=count       

    heal_col=querycol.find({'Occupation.Job-Class':'Healthcare'})
    count =0  
    for item in heal_col:                
        count+=1  
    heal_count=count  

    info_col=querycol.find({'Occupation.Job-Class':'Information Technology'})
    count =0  
    for item in info_col:                
        count+=1  
    info_count=count       

    math_col=querycol.find({'Occupation.Job-Class':'Mathematics'})
    count =0  
    for item in math_col:                
        count+=1  
    math_count=count    

    sci_col=querycol.find({'Occupation.Job-Class':'Science'})
    count =0  
    for item in sci_col:                
        count+=1  
    sci_count=count  

    soc_col=querycol.find({'Occupation.Job-Class':'Social Services'})
    count =0  
    for item in soc_col:                
        count+=1  
    soc_count=count 

    oth_col=querycol.find({'Occupation.Job-Class':'Other'})
    count =0  
    for item in oth_col:                
        count+=1  
    oth_count=count       

    job_dict={'Advertising,Promotions,Marketing':adv_count,'Architecture & Engineering':AE_count,'Business':busin_count,
    'Education':edu_count,'Finance':fin_count,'Healthcare':heal_count,'Information Technology':info_count,
    'Mathematics':math_count,'Science':sci_count,'Social Services':soc_count,'Other':oth_count}
    k = Counter(job_dict) 
    job_list=[]
    
    # Finding 4 highest values 
    high = k.most_common(4)           
    for i in high:
        job_list.append((i[0],i[1])) 

    return job_list 


# returns Top 4 study areas from the database info
def StudyAreaCount(self):
    
    
    model=Models.MyMongoDB()
    querycol=model.db
    querycol=querycol.diasporaList
    hum_col=querycol.find({'Occupation.Field-of-Study':'Humanities and Social Sciences'})
    count =0  
    for item in hum_col:                
        count+=1  
    hum_count=count 
    
    NS_col=querycol.find({'Occupation.Field-of-Study':'Natural Sciences'})
    count =0  
    for item in NS_col:                
        count+=1  
    NS_count=count 
    FS_col=querycol.find({'Occupation.Field-of-Study':'Formal Sciences'})
    count =0  
    for item in FS_col:                
        count+=1  
    FS_count=count 

    PAS_col=querycol.find({'Occupation.Field-of-Study':'Professions and Applied Sciences'})
    count =0  
    for item in PAS_col:                
        count+=1  
    PAS_count=count 
    
    oth_col=querycol.find({'Occupation.Field-of-Study':'Other'})
    count =0  
    for item in oth_col:                
        count+=1  
    oth_count=count 

    area_count={'Humanities and Social Sciences':hum_count,'Natural Sciences':NS_count,'Formal Sciences':FS_count,
    'Professions and Applied Sciences':PAS_count,'Other':oth_count}
    k = Counter(area_count) 
    area_list=[]
    
    # Finding 4 highest values 
    high = k.most_common(4)           
    for i in high:
        area_list.append((i[0],i[1])) 

    return area_list 




