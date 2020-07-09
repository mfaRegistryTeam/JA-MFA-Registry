# Author: Shane Okukenu 

from Keywords import Variables
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson import ObjectId
from flask import Flask,request,session
from Methods import Queries
from Keywords import Variables
import bcrypt,datetime,json
from datetime import timedelta
from flask.helpers import flash
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import datetime


class User:
    def __init__(self, username,password,email):
        self.username = username
        self.password = password
        self.email = email


    def get_account_details(self):        
        return[self.username,self.password,self.email]


class MyMongoDB:
    def __init__(self):
        # self._client = MongoClient('localhost', 27017)
        self._client = MongoClient("mongodb://heroku_qc5l7qqd:or7uuplla29cvq7u647oo7ooap@ds163905.mlab.com:63905/heroku_qc5l7qqd?retryWrites=false")
        self.db = self._client[Variables.siteLabels.DatabaseName]
        


class DatabaseStruct:
    def __init__(self):
        pass   

    def InsertHistory(self):
        #The function logic is important here this function inserts and maintains
        # the history list as per prescribed

        model=MyMongoDB()
        r=Queries.SiteQuery().find_existing_registered
        q=Queries.SiteQuery().find_existing_history
        s=Queries.SiteQuery().find_existing_user
        
        HistoryList=[]
        if r and s and q is not None:
            history=model.Historical

            history.create_index( [(Variables.databaseLabels().EmailAddress, 1)],
                                           name= "UniqueEmailIndex",
                                           background=True,
                                           unique= True)
            result=list(r)
            #list hold no more than 3 elements
            if len(q[Variables.databaseLabels().History])>3:
                history.update_one(
                {Variables.databaseLabels().EmailAddress : session['email']},
                                
                {'$pop':{Variables.databaseLabels().History:-1    }}) 

            # as time goes on the latest 3 versions of a users information will be stored.
            if len(q[Variables.databaseLabels().History])<=3:
                history.update_one(
                {Variables.databaseLabels().EmailAddress : session['email']},
                                
                {'$push':{
                    Variables.databaseLabels().History:{
                        '$each': result,
                        '$sort': {Variables.databaseLabels().LastUpdated : -1 }             
                    
                    }
                     
                    } 
                })          

    def InsertUser(self,email,password,username):

        hashpass=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt() )
        model=MyMongoDB()
        users=model.db.users
        timestamp = datetime.datetime.now() 

        if users.find_one({Variables.databaseLabels().EmailAddress:email}) is None:
            users.insert_one({
                Variables.databaseLabels().Username : username,
                Variables.databaseLabels().Password: hashpass,
                Variables.databaseLabels().EmailAddress :email,
                'Status':False,
                'Added': timestamp              
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

        if user_admin.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email')}) is None:
            user_admin.insert_one({
                Variables.databaseLabels().Username :request.form.get('username'),
                Variables.databaseLabels().EmailAddress :request.form.get('email'),
                Variables.databaseLabels().Password: hashpass,
                Variables.databaseLabels().Permissions:permission_set 
         })              


    def InsertFormData(self):
        model=MyMongoDB()
       
        dob_string=request.form.get('DOB')
        if dob_string=='':
            dob_string='1900-01-01'
        DOB = datetime.datetime(int(dob_string[0:4]),int(dob_string[5:7]),int(dob_string[8:10]))


        geolocator = Nominatim(user_agent="Barbados")
        country_ro=request.form.get('country_ro')      
        if country_ro =='' or None:
            latitude=None
            longitude=None
        else:
            try:
                location = geolocator.geocode(country_ro,timeout=16000) 
                latitude=location.latitude
                longitude=location.longitude  
            except GeocoderTimedOut as e:    
                print("Error: geocode failed on input %s with message %s"%(country_ro,e.message))
                #redirect to another page?
                pass               

        Firstname=request.form.get('first_name')
        Middlename=request.form.get('middle_name')
        Lastname= request.form.get('last_name')      
        Nationality = request.form.get('nationality')
        Type= request.form.get('occupation')
        EducationalInst=request.form.get('edu_inst')
        
        Other=request.form.get('other')
        Jobtitle = request.form.get('job_title')
        JobClass=request.form.get('job_class')
        Workplace = request.form.get('workplace_name')
        PassportNumber=request.form.get('passport_num')
        IssuedPassportCountry=request.form.get('pp_country')
        WeChatID= request.form.get('we_chat')           
        PhoneNumber= request.form.get('phone_num')
        Street1=request.form.get('street')
        CityorTown1= request.form.get('city_town')
        Country1=request.form.get('country')


        if Firstname  is None or '':
            Firstname =None        
        if Middlename is None or '':
            Middlename =None 
        if Lastname is None or '':
            Lastname =None       
        if Nationality is None:
            Nationality=None

        if Type is "Student" or'Employed' or 'Other':
            # if FieldofStudy == None or "None":
            #     FieldofStudy=None     

            if EducationalInst is None or "":
                EducationalInst=None
       
            # if Jobtitle is None or "":
            #     Jobtitle=None
            # if JobClass == "None":
            #     JobClass=None
            # if Workplace is None or "":
            #     Workplace=None

            # if Other is None or "":
            #     Other=None 
     
        if PassportNumber is None or "":
            PassportNumber=None
        if IssuedPassportCountry is None or "":
            IssuedPassportCountry=None   

        if Street1 is None or "":
            Street1=None
        if CityorTown1 is None or "":
            CityorTown1=None
        if Country1 is None or "":   
            Country1=None                    
                   

        classification=request.form.get('classification')
        POTdescription=request.form.get('POT_des')
        PurposeofTravel=request.form.get('radio') 

        Streetbb=request.form.get('street_bb')
        CityorTownbb=request.form.get('city_town_bb')
        Parishbb= request.form.get('parish_bb')            
    
        Streetab=request.form.get('street_abroad')
        CityorTownab=request.form.get('city_town_abroad')
        Stateab= request.form.get('state_abroad')
        CountryAbroad= request.form.get('country_abroad')
        
        dept_string=request.form.get('dept_date')
        return_string=request.form.get('ret_date')

        if dept_string is '':
            dept_string='1900-01-01'
        if return_string is '':
            return_string='1900-01-01'       

        expected_departure = datetime.datetime(int(dept_string[0:4] ),int(dept_string[5:7]),int(dept_string[8:10]))
        expected_return = datetime.datetime(int(return_string[0:4] ),int(return_string[5:7]),int(return_string[8:10]))          
            
        
        EmergencyConFirstname= request.form.get('emerg_firstname')
        EmergencyConLastname= request.form.get('emerg_lastname')
        EmergencyConPhone= request.form.get('emerg_phone')
        EmergencyConEmail= request.form.get('emerg_email')
        EmergencyConRel= request.form.get('emerg_rel')                 
                    

        EmergencyConFirstname_ab= request.form.get('firstname_ab')
        EmergencyConLastname_ab= request.form.get('lastname_ab')
        EmergencyConPhone_ab= request.form.get('emerg_phone_ab')
        EmergencyConEmail_ab= request.form.get('emerg_email_ab')
        EmergencyConRel_ab= request.form.get('emerg_rel_ab')                 
                    
        
       
        residential_abroad=request.form.get('residential_abroad')
        mobile_abroad=request.form.get('mobile_abroad')
        WA_abroad=request.form.get('WA_abroad')
        WeChatAB= request.form.get('we_chat_ab')
        AbroadEmail= request.form.get('abroad_email')

        ResidentialRes=request.form.get('residential_ro')
        MobileRes=request.form.get('mobile_ro')
        WhatsappRes=request.form.get('WA_ro') 
        Street=request.form.get('street_ro'),
        State= request.form.get('state_ro'),
        CityorTown= request.form.get('city_town_ro')

        AOI=request.form.getlist('AOI')  
        KBB=request.form.getlist('KBB')
        AOI_fr=request.form.getlist('AOI_fr')

        if classification=="CitizenTO" or 'ResidentO' or'Friend':
            var_list=[PurposeofTravel,POTdescription,CountryAbroad,Streetbb,CityorTownbb,Parishbb,Streetab,CityorTownab,
            Stateab,EmergencyConFirstname_ab,EmergencyConLastname_ab,EmergencyConPhone_ab,EmergencyConEmail_ab,
            EmergencyConRel_ab,residential_abroad,mobile_abroad,WA_abroad,WeChatAB,AbroadEmail,ResidentialRes,MobileRes,WhatsappRes,Street,State,CityorTown]              
            for var in var_list:
                if var is None or '' or "None":
                    var=None

            l=[AOI,KBB,AOI_fr]
            for y in l:
                if y is [] or None:
                    AOI=None
                    AOI_fr=None
                    KBB=None 

        col = MyMongoDB()
        timestamp = datetime.datetime.now() 
        diasporaList=col.db.diasporaList
        if diasporaList.find_one({Variables.databaseLabels().EmailAddress:session['email']}) is None:

            diasporaList.insert_one(
                {
                    Variables.databaseLabels().EmailAddress : session['email'],
                    Variables.databaseLabels().Name:{
                        Variables.databaseLabels().Firstname: Firstname,
                        Variables.databaseLabels().Middlename: Middlename,
                        Variables.databaseLabels().Lastname: Lastname
                        },       

                    Variables.databaseLabels().Gender: request.form.get('gender'), 
                    Variables.databaseLabels().DOB: DOB,
                    Variables.databaseLabels().Nationality:Nationality, 
                    Variables.databaseLabels().Occupation:{
                        Variables.databaseLabels().Type: Type,
                        Variables.databaseLabels().FieldofStudy: request.form.get('field'),
                        Variables.databaseLabels().StudyLevel: request.form.get('field_study_level'),
                        Variables.databaseLabels().EducationalInst: EducationalInst,
                        Variables.databaseLabels().Other: Other,

                        Variables.databaseLabels().JobClass: JobClass,
                        Variables.databaseLabels().Jobtitle: Jobtitle,
                        Variables.databaseLabels().Workplace: Workplace                 
                        },

                    Variables.databaseLabels().PassportNumber: PassportNumber,
                    Variables.databaseLabels().IssuedPassportCountry: IssuedPassportCountry,
                    Variables.databaseLabels().WeChatID: WeChatID,             
                    Variables.databaseLabels().PhoneNumber: PhoneNumber,
                    Variables.databaseLabels().Address:{
                        Variables.databaseLabels().Street:Street1,
                        Variables.databaseLabels().CityorTown: CityorTown1,
                        Variables.databaseLabels().Country:Country1
                        },
                    Variables.databaseLabels().EmergDetails:{
                        Variables.databaseLabels().EmergencyConFirstname: EmergencyConFirstname,
                        Variables.databaseLabels().EmergencyConLastname: EmergencyConLastname,
                        Variables.databaseLabels().EmergencyConRel: EmergencyConRel,
                        Variables.databaseLabels().EmergencyConPhone: EmergencyConPhone,
                        Variables.databaseLabels().EmergencyConEmail: EmergencyConEmail                                     
                        },

                    Variables.databaseLabels().Classification: classification,

#Citizen travelling abroad
                    Variables.databaseLabels().PurposeofTravel: PurposeofTravel,
                    Variables.databaseLabels().POTdescription:  POTdescription,
                    Variables.databaseLabels().BarbadosAddress:{
                        Variables.databaseLabels().Street:Streetbb,
                        Variables.databaseLabels().CityorTown:CityorTownbb,
                        Variables.databaseLabels().Parish: Parishbb
                        },  
                                
                    Variables.databaseLabels().AddressAbroad:{
                        Variables.databaseLabels().Street:Streetab,
                        Variables.databaseLabels().CityorTown:CityorTownab,
                        Variables.databaseLabels().State: Stateab,
                        Variables.databaseLabels().CountryAbroad: CountryAbroad
                        },  

                    Variables.databaseLabels().EmergDetailsAbroad:{
                        Variables.databaseLabels().EmergencyConFirstname: EmergencyConFirstname_ab,
                        Variables.databaseLabels().EmergencyConLastname: EmergencyConLastname_ab,
                        Variables.databaseLabels().EmergencyConPhone: EmergencyConPhone_ab,
                        Variables.databaseLabels().EmergencyConEmail: EmergencyConEmail_ab,
                        Variables.databaseLabels().EmergencyConRel: EmergencyConRel_ab                
                        },

                    Variables.databaseLabels().TravelDates:{                    
                        Variables.databaseLabels().DepDate: expected_departure,
                        Variables.databaseLabels().ReturnDate: expected_return
                        },     

                    Variables.databaseLabels().PhoneNumberAbroad:[
                        {Variables.databaseLabels().ResidentialAbroad:residential_abroad},
                        {Variables.databaseLabels().MobileAbroad:mobile_abroad},
                        {Variables.databaseLabels().WhatsappAbroad:WA_abroad}],
                    Variables.databaseLabels().WeChatAB: WeChatAB,
                    Variables.databaseLabels().AbroadEmail: AbroadEmail,
               
#Residents Overseas

                    Variables.databaseLabels().ResidenceAbroadDetails:{
                        Variables.databaseLabels().Street:Street,
                        Variables.databaseLabels().State: State,
                        Variables.databaseLabels().CityorTown: CityorTown,
                        Variables.databaseLabels().Country:country_ro,
                        Variables.databaseLabels().Location: [latitude, longitude]   
                        },
                    Variables.databaseLabels().ResidentsAbroadPhone:[
                        {Variables.databaseLabels().ResidentialRes:ResidentialRes},
                        {Variables.databaseLabels().MobileRes:MobileRes},
                        {Variables.databaseLabels().WhatsappRes:WhatsappRes}],    

                     Variables.databaseLabels().AreasofInterest:AOI,               

#Friends of Barbados                   
                    Variables.databaseLabels().KnowledgeofBB:KBB,
                    Variables.databaseLabels().AreasofInterestFr:AOI_fr,

                    Variables.databaseLabels().DateAdded : timestamp,
                    Variables.databaseLabels().LastUpdated:timestamp,
                    'Emailed_last': timestamp
                                        })  

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

    def UpdateFormData(self):   
        model=MyMongoDB()

        dob_string=request.form.get('DOB')
        dept_string=request.form.get('dept_date')
        return_string=request.form.get('ret_date')

        AOI=request.form.getlist('AOI')  
        KBB=request.form.getlist('KBB')
        AOI_fr=request.form.getlist('AOI_fr')

        if dob_string=='':
            dob_string='1900-01-01'
        DOB = datetime.datetime(int(dob_string[0:4] ),int(dob_string[5:7]),int(dob_string[8:10]))

        

        if dept_string is'' :
            dept_string ='1900-01-01'
        expected_departure = datetime.datetime(int(dept_string[0:4] ),int(dept_string[5:7]),int(dept_string[8:10]))

        if return_string is'' :
            return_string ='1900-01-01'
        expected_return = datetime.datetime(int(return_string[0:4] ),int(return_string[5:7]),int(return_string[8:10]))
        
        

           
        updatedtimestamp = datetime.datetime.now() 
        

       # hashpass=bcrypt.hashpw(request.form.get('password').encode('UTF-8'), bcrypt.gensalt() )
        col = MyMongoDB()
        diasporaList=col.db.diasporaList
        if diasporaList.find_one({Variables.databaseLabels().EmailAddress:session['email']}) is not None:

            if request.form.get('Firstname') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Name.First':request.form.get('Firstname')}})
            
            if request.form.get('Middlename') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Name.Middle':request.form.get('Middlename')}})

            if request.form.get('Lastname') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Name.Last':request.form.get('Lastname')}})

            if request.form.get('Gender') is not None:
                  diasporaList.update_one(
                     {Variables.databaseLabels().EmailAddress : session['email']},
                     {'$set':{Variables.databaseLabels().Gender:request.form.get('Gender')}})

            if dob_string  !='1900-01-01':
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().DOB:DOB}})

            if request.form.get('occupation') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Type':request.form.get('occupation')}})

            if request.form.get('field') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Field-of-Study':request.form.get('field')}})

            if request.form.get('field_study_level') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Level':request.form.get('field_study_level')}})

            if request.form.get('edu_inst') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Educational-Institution':request.form.get('edu_inst')}})

            if request.form.get('job_class') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Job-Class':request.form.get('job_class')}})


            if request.form.get('Jobtitle') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Job-Title':request.form.get('Jobtitle')}})

            if request.form.get('Workplacename') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Occupation.Workplace-Name':request.form.get('Workplacename')}})

            if request.form.get('OcpOther') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().Other : session['email']},
                    {'$set':{'Occupation.Other':request.form.get('OcpOther')}})


            if  request.form.get('PassportNumber') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().PassportNumber: request.form.get('PassportNumber')}})

            if  request.form.get('pp_country') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().IssuedPassportCountry: request.form.get('pp_country')}})                

            if request.form.get('nationality') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().Nationality:request.form.get('nationality')}})

            if request.form.get('WeChat') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().WeChatID:request.form.get('WeChat')}})

            if request.form.get('PhoneNumber') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().PhoneNumber:request.form.get('PhoneNumber')}})

            if request.form.get('Street') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address.Street':request.form.get('Street')}})

            if request.form.get('parish') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address.State':request.form.get('parish')}})

            if request.form.get('CityorTown') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address.City/Town':request.form.get('CityorTown')}})

            if request.form.get('country') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address.Country':request.form.get('country')}})

            if request.form.get('EmergencyConFirstname') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Details.Firstname':request.form.get('EmergencyConFirstname')}})

            if request.form.get('EmergencyConLastname') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Details.Lastname':request.form.get('EmergencyConLastname')}})

            if request.form.get('EmergencyConRel') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Details.Relationship':request.form.get('EmergencyConRel')}})

            if request.form.get('EmergencyConPhone') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Details.Phone':request.form.get('EmergencyConPhone')}})

            if request.form.get('EmergencyConEmail') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Details.Email':request.form.get('EmergencyConEmail')}})

            if  request.form.get('classification') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().Classification : request.form.get('classification')}})  

        #Citizen Travelling

            if  request.form.get('radio') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().PurposeofTravel : request.form.get('radio')}})  

            if   request.form.get('POT_des') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().POTdescription :  request.form.get('POT_des')}})                    
                                

            if request.form.get('street_bb') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address-in-Barbados.Street':request.form.get('street_bb')}})            

            if request.form.get('city_town_bb') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address-in-Barbados.City/Town':request.form.get('city_town_bb')}})

            if request.form.get('parish_bb') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Address-in-Barbados.Parish':request.form.get('parish_bb')}})        

            if request.form.get('street_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Destination-Address.Street':request.form.get('street_abroad')}})    
               
            if request.form.get('city_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Destination-Address.City/Town':request.form.get('city_abroad')}}) 

            if request.form.get('state_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Destination-Address.State':request.form.get('state_abroad')}})

            if request.form.get('country_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Destination-Address.Country':request.form.get('country_abroad')}})

            if request.form.get('EmergencyConFirstnameab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Abroad.Firstname':request.form.get('EmergencyConFirstnameab')}})

            if request.form.get('EmergencyConLastnameab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Abroad.Lastname':request.form.get('EmergencyConLastnameab')}})
            
            if request.form.get('EmergencyConPhoneab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Abroad.Phone':request.form.get('EmergencyConPhoneab')}})

            if request.form.get('EmergencyConEmailab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Abroad.Email':request.form.get('EmergencyConEmailab')}})

            if request.form.get('EmergencyConRelab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Emergency-Contact-Abroad.Relationship':request.form.get('EmergencyConRelab')}})

            if dept_string != '1900-01-01':
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Travel-Date-Details.Expected-DepDate':expected_departure}})

            if return_string !='1900-01-01':
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Travel-Date-Details.Expected-ReturnDate':expected_return}})

                    
            if request.form.get('ResPhoneNumberAbroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Phone-Number-Abroad.0.Residential-Phone-Abroad':request.form.get('ResPhoneNumberAbroad')}})

            if request.form.get('ResMobileAbroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Phone-Number-Abroad.1.Mobile-Abroad':request.form.get('ResMobileAbroad')}})


            if request.form.get('ResWhatsappAbroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Phone-Number-Abroad.2.Whatsapp-Abroad':request.form.get('ResWhatsappAbroad')}})

#########################################################################################
            if request.form.get('ResWechatAB') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().AbroadPhone:request.form.get('ResWechatAB')}})
#####################################################################################################

            if request.form.get('AbroadEmail') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().AbroadEmail:request.form.get('AbroadEmail')}})              

     #Residents Overseas

            if request.form.get('resstreet_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residence-Abroad-Address.Street':request.form.get('resstreet_abroad')}})

            if request.form.get('resstate_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residence-Abroad-Address.State':request.form.get('resstate_abroad')}})

            if request.form.get('rescity_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residence-Abroad-Address.City/Town':request.form.get('rescity_abroad')}})

        #     country_ro=request.form.get('country_ro')
        # geolocator = Nominatim(user_agent="Barbados-MFA")
        # if country_ro is not None:
        #     try:
        #         location = geolocator.geocode(country_ro,timeout=15000)   
        #     except GeocoderTimedOut as e:
        #         print("Error: geocode failed on input %s with message %s"%(country,e.message))
        #         pass  
            geolocator = Nominatim(user_agent="Barbados")
            country_ro=request.form.get('country_ro')  
            if country_ro =='' or None :
                    diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residence-Abroad-Address.Country':country_ro}})
                    latitude=None
                    longitude=None
                                        
                    diasporaList.update_one(
                        {Variables.databaseLabels().EmailAddress : session['email']},
                        {'$set':{'Residence-Abroad-Address.Location.0':latitude}})

                    diasporaList.update_one(
                        {Variables.databaseLabels().EmailAddress : session['email']},
                        {'$set':{'Residence-Abroad-Address.Location.1':longitude}}) 
            else:
                try:
                    location = geolocator.geocode(country_ro,timeout=16000) 
                    diasporaList.update_one(
                        {Variables.databaseLabels().EmailAddress : session['email']},
                        {'$set':{'Residence-Abroad-Address.Location.0':latitude}})

                    diasporaList.update_one(
                        {Variables.databaseLabels().EmailAddress : session['email']},
                        {'$set':{'Residence-Abroad-Address.Location.1':longitude}})                                            
                except GeocoderTimedOut as e:    
                    print("Error: geocode failed on input %s with message %s"%(country_ro,e.message))
                    #redirect to another page?
                    pass         
            
           

            if request.form.get('ResidentialPhoneNumberAbroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residents-Abroad-Phone.0.Residential-Phone-Abroad':request.form.get('ResidentialPhoneNumberAbroad')}})

            if request.form.get('MobilePhoneNumberAbroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residents-Abroad-Phone.1.Mobile-Res':request.form.getlist('MobilePhoneNumberAbroad')}})

            if request.form.get('ResidentialWhatsappAbroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{'Residents-Abroad-Phone.2.Whatsapp-Res':request.form.getlist('ResidentialWhatsappAbroad')}})

            if request.form.getlist('AOI') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().AreasofInterest:AOI}})

 #Friends of Barbados            

            if request.form.getlist('KBB') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().KnowledgeofBB:KBB}})
            
            if request.form.getlist('AOI_fr') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : session['email']},
                    {'$set':{Variables.databaseLabels().AreasofInterestFr:AOI_fr}}) 

            diasporaList.update_one(
                {Variables.databaseLabels().EmailAddress : session['email']},
                {'$set':{Variables.databaseLabels().LastUpdated:updatedtimestamp}})




        # Each time there is an update this call takes a snapshot of the current document to be stored 
        # then the update is made after. 

        # Date Added never changes but Last Date Updated does.Tht is what is used to sort them
        #DatabaseStruct.InsertHistory()
    
#         dob_string=request.form.get('DOB')
#         dept_string=request.form.get('dept_date')
#         return_string=request.form.get('ret_date')

#         DOB = datetime.datetime(int(dob_string[0:4] ),int(dob_string[5:7]),int(dob_string[8:10]))
#         expected_departure = datetime.datetime(int(dept_string[0:4] ),int(dept_string[5:7]),int(dept_string[8:10]))
#         expected_return = datetime.datetime(int(return_string[0:4] ),int(return_string[5:7]),int(return_string[8:10]))
        
#         country=request.form.get('country_ro')
#         geolocator = Nominatim(user_agent="Barbados-MFA")
#         if country is not None:
#             try:
#                 location = geolocator.geocode(country,timeout=15000)   
#             except GeocoderTimedOut as e:
#                 print("Error: geocode failed on input %s with message %s"%(country,e.message))
#                 pass  

           
#         updatedtimestamp = datetime.datetime.now() 
        

#         hashpass=bcrypt.hashpw(request.form.get('password').encode('UTF-8'), bcrypt.gensalt() )
#         col = MyMongoDB()
#         diasporaList=col.db.diasporaList
#         if diasporaList.find_one({Variables.databaseLabels().EmailAddress:session['email']}) is not None:

#             if request.form.get('first_name') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Name.First':request.form.get('first_name')}})
            
#             if request.form.get('middle_name') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Name.Middle':request.form.get('middle_name')}})

#             if request.form.get('last_name') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Name.Last':request.form.get('last_name')}})

#             # if request.form.get('gender') is not None:
#             #     diasporaList.update_one(
#             #         {Variables.databaseLabels().EmailAddress : session['email']},
#             #         {'$set':{Variables.databaseLabels().Gender:request.form.get('gender')}})

#             if DOB is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().DOB:DOB}})

#             if request.form.get('occupation') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Type':request.form.get('occupation')}})

#             if request.form.get('field_study') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Field-of-Study':request.form.get('field_study')}})

#             if request.form.get('field_study_level') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Level':request.form.get('field_study_level')}})

#             if request.form.get('edu_inst') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Educational-Institution':request.form.get('edu_inst')}})

#             if request.form.get('job_class') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Job-Class':request.form.get('job_class')}})


#             if request.form.get('job_title') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Job-Title':request.form.get('job_title')}})

#             if request.form.get('workplace_name') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Occupation.Workplace-Name':request.form.get('workplace_name')}})

            

#             if  request.form.get('passport_num') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().PassportNumber: request.form.get('passport_num')}})

#             if  request.form.get('pp_country') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().IssuedPassportCountry: request.form.get('pp_country')}})                

#             if request.form.get('nationality') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().Nationality:request.form.get('nationality')}})

#             if request.form.get('we_chat') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().WeChatID:request.form.get('we_chat')}})

#             if request.form.get('phone_num') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().PhoneNumber:request.form.get('phone_num')}})

#             if request.form.get('street') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address.Street':request.form.get('street')}})

#             if request.form.get('parish') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address.State':request.form.get('parish')}})

#             if request.form.get('city_town') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address.City/Town':request.form.get('city_town')}})

#             if request.form.get('country') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address.Country':request.form.get('country')}})

#             if request.form.get('emerg_firstname') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Details.Firstname':request.form.get('emerg_firstname')}})

#             if request.form.get('emerg_lastname') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Details.Lastname':request.form.get('emerg_lastname')}})

#             if request.form.get('emerg_rel') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Details.Relationship':request.form.get('emerg_rel')}})

#             if request.form.get('emerg_phone') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Details.Phone':request.form.get('emerg_phone')}})

#             if request.form.get('emerg_email') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Details.Email':request.form.get('emerg_email')}})

#             if  request.form.get('classification') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().Classification : request.form.get('classification')}})  

#         #Citizen Travelling

#             if  request.form.get('radio') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().PurposeofTravel : request.form.get('radio')}})  

#             if   request.form.get('POT_des') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().POTdescription :  request.form.get('POT_des')}})                    
                                

#             if request.form.get('street_bb') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address-in-Barbados.Street':request.form.get('street_bb')}})            

#             if request.form.get('city_town_bb') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address-in-Barbados.City/Town':request.form.get('city_town_bb')}})

#             if request.form.get('parish_bb') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Address-in-Barbados.Parish':request.form.get('parish_bb')}})        

#             if request.form.get('street_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Destination-Address.Street':request.form.get('street_abroad')}})    
               
#             if request.form.get('city_town_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Destination-Address.City/Town':request.form.get('city_town_abroad')}}) 

#             if request.form.get('state_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Destination-Address.State':request.form.get('state_abroad')}})

#             if request.form.get('country_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Destination-Address.Country':request.form.get('country_abroad')}})

#             if request.form.get('firstname_ab') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Abroad.Firstname':request.form.get('firstname_ab')}})

#             if request.form.get('lastname_ab') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Abroad.Lastname':request.form.get('lastname_ab')}})
            
#             if request.form.get('emerg_phone_ab') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Abroad.Phone':request.form.get('emerg_phone_ab')}})

#             if request.form.get('emerg_email_ab') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Abroad.Email':request.form.get('emerg_email_ab')}})

#             if request.form.get('emerg_rel_ab') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Emergency-Contact-Abroad.Relationship':request.form.get('emerg_rel_ab')}})

#             if expected_departure is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Travel-Date-Details.Expected-DepDate':expected_departure}})

#             if expected_return is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Travel-Date-Details.Expected-ReturnDate':expected_return}})

                    
#             if request.form.get('residential_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Phone-Number-Abroad.Residential-Phone-Abroad':request.form.get('residential_abroad')}})

#             if request.form.get('mobile_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Phone-Number-Abroad.Mobile-Abroad':request.form.get('mobile_abroad')}})


#             if request.form.get('WA_abroad') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Phone-Number-Abroad.Whatsapp-Abroad':request.form.get('WA_abroad')}})


#             if request.form.get('abroad_phone') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().AbroadPhone:request.form.get('abroad_phone')}})


#             if request.form.get('abroad_email') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().AbroadEmail:request.form.get('abroad_email')}})              

#      #Residents Overseas

#             if request.form.get('street_ro') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residence-Abroad-Address.Street':request.form.get('street_ro')}})

#             if request.form.get('state_ro') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residence-Abroad-Address.State':request.form.get('state_ro')}})

#             if request.form.get('city_town_ro') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residence-Abroad-Address.City/Town':request.form.get('city_town_ro')}})

#             if country is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residence-Abroad-Address.Country':country}})

#             if location is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residence-Abroad-Address.Location.0':location.latitude}})

#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residence-Abroad-Address.Location.1':location.longitude}})

#             if request.form.get('residential_ro') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residents-Abroad-Phone.Residential-Phone-Abroad':request.form.get('residential_ro')}})

#             if request.form.get('mobile_ro') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residents-Abroad-Phone.Mobile-Res':request.form.get('mobile_ro')}})

#             if request.form.get('WA_ro') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{'Residents-Abroad-Phone.Whatsapp-Res':request.form.get('WA_ro')}})

#             if request.form.getlist('AOI') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().AreasofInterest:request.form.get('AOI')}})

#  #Friends of Barbados            

#             if request.form.getlist('KBB') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().KnowledgeofBB:request.form.get('KBB')}})
            
#             if request.form.getlist('AOI_fr') is not None:
#                 diasporaList.update_one(
#                     {Variables.databaseLabels().EmailAddress : session['email']},
#                     {'$set':{Variables.databaseLabels().AreasofInterest:request.form.get('AOI_fr')}}) 

#             diasporaList.update_one(
#                 {Variables.databaseLabels().EmailAddress : session['email']},
#                 {'$set':{Variables.databaseLabels().LastUpdated:updatedtimestamp}})


    def AdminViewFormData(self,email):   
        model=MyMongoDB()
        
        registeredList = model.db.diasporaList
        result = registeredList.find_one({Variables.databaseLabels().EmailAddress:email})
        # Pulling information stored in date to be able to display it on page

        var_list=[]

        Email_Address= result[Variables.databaseLabels.EmailAddress]

    #Add to list
        var_list.append(Email_Address)  

        
#Name Section
        Name=result[Variables.databaseLabels.Name]

        First_Name=Name[Variables.databaseLabels.Firstname]
        Middle_Name=Name[Variables.databaseLabels.Middlename]        
        Last_Name=Name[Variables.databaseLabels.Lastname]

    #Add to list
        var_list.extend([First_Name,Middle_Name,Last_Name])

#Personal Info
        Gender= result[Variables.databaseLabels.Gender]
        Date_of_Birth = str(result[Variables.databaseLabels().DOB])
        Country_of_Birth=result[Variables.databaseLabels().Nationality]

        PPnum=result[Variables.databaseLabels().PassportNumber]
        IssuedPassportCountry=result[Variables.databaseLabels().IssuedPassportCountry]
        WeChatID=result[Variables.databaseLabels().WeChatID]           
        PhoneNum=result[Variables.databaseLabels().PhoneNumber]

        #Add to list
        var_list.extend([Gender,Date_of_Birth,Country_of_Birth,PPnum,IssuedPassportCountry,WeChatID,PhoneNum])

         

        #Address section          
        Address_Details=result[Variables.databaseLabels().Address]

        Address_Street=Address_Details[Variables.databaseLabels().Street]
        Address_City=Address_Details[Variables.databaseLabels().CityorTown]
        Address_Country=Address_Details[Variables.databaseLabels().Country]

        #Add to list
        var_list.extend([Address_Street,Address_City,Address_Country])

          #Emergency Contact Section              
        EmergContDetails=result[Variables.databaseLabels().EmergDetails]

        Emergfname=EmergContDetails[Variables.databaseLabels().EmergencyConFirstname]
        Emerglname=EmergContDetails[Variables.databaseLabels().EmergencyConLastname]
        Emergrel=EmergContDetails[Variables.databaseLabels().EmergencyConRel]
        Emergpnum= EmergContDetails[Variables.databaseLabels().EmergencyConPhone]
        Emergemail=EmergContDetails[Variables.databaseLabels().EmergencyConEmail]                    

        Classification=result[Variables.databaseLabels().Classification]

        #Add to list
        var_list.extend([Emergfname, Emerglname,Emergrel,Emergpnum,Emergemail,Classification])

#Occupation Section
        Occupation_Details=result[Variables.databaseLabels().Occupation]

        Occupation_Type=Occupation_Details[Variables.databaseLabels().Type]
        Education_Field=Occupation_Details[Variables.databaseLabels().FieldofStudy]
        Education_Level=Occupation_Details[Variables.databaseLabels().StudyLevel]
        Education_Inst=Occupation_Details[Variables.databaseLabels().EducationalInst]
        Other_Details=Occupation_Details[Variables.databaseLabels().Other]
        Job_Class=Occupation_Details[Variables.databaseLabels().JobClass]
        Job_Title=Occupation_Details[Variables.databaseLabels().Jobtitle]
        Workplace=Occupation_Details[Variables.databaseLabels().Workplace] 

        #Add to list
        var_list.extend([Occupation_Type,Education_Field,Education_Level,Education_Inst,Other_Details,Job_Class,
        Job_Title,Workplace])

#Citizen Travelling Overseas Section

        Citizen_POT = result[Variables.databaseLabels().PurposeofTravel]
        Citizen_POT_Desc=result[Variables.databaseLabels().POTdescription]

        var_list.extend([Citizen_POT,Citizen_POT_Desc])

        #Citizen Travelling Barbadian Address Information
        Barbados_Address=result[Variables.databaseLabels().BarbadosAddress]

        BarbadosStreet=Barbados_Address[Variables.databaseLabels().Street]
        BarbadosCity=Barbados_Address[Variables.databaseLabels().CityorTown]
        BarbadosParish=Barbados_Address[Variables.databaseLabels().Parish]

        #Add to list   
        var_list.extend([ BarbadosStreet,BarbadosCity,BarbadosParish]) 
        
         

        #Citizen Travelling Destination Address Section
        DestAddress=result[Variables.databaseLabels().AddressAbroad]

        Dest_st=DestAddress[Variables.databaseLabels().Street]
        Dest_city=DestAddress[Variables.databaseLabels().CityorTown]
        Dest_state=DestAddress[Variables.databaseLabels().State]
        Dest_country=DestAddress[Variables.databaseLabels().CountryAbroad]

        #Add to list
        var_list.extend([Dest_st,Dest_city,Dest_state,Dest_country])
                      
        #Citizen Travelling Emergency Contact Information
        EContAbroad=result[Variables.databaseLabels().EmergDetailsAbroad]

        EContfname=EContAbroad[Variables.databaseLabels().EmergencyConFirstname]
        EContlname=EContAbroad[Variables.databaseLabels().EmergencyConLastname]
        EContpnum=EContAbroad[Variables.databaseLabels().EmergencyConPhone]
        EContemail=EContAbroad[Variables.databaseLabels().EmergencyConEmail]
        EContrel=EContAbroad[Variables.databaseLabels().EmergencyConRel] 

        #Add to List         
        var_list.extend([EContfname,EContlname,EContpnum,EContemail,EContrel]) 
                    
        #Travel Dates Section
        TravelDetails=result[Variables.databaseLabels().TravelDates]

        Expected_Depature=str(TravelDetails[Variables.databaseLabels().DepDate])
        Expected_ReturnDate=str(TravelDetails[Variables.databaseLabels().ReturnDate])

        #Add to list  
        var_list.extend([Expected_Depature,Expected_ReturnDate])
                   
        #Citizen Travelling Phone Section
        Phones_Abroad=result[Variables.databaseLabels().PhoneNumberAbroad]
            
        CitizenAb_Phone=Phones_Abroad[0][Variables.databaseLabels().ResidentialAbroad]
        CitizenAb_Mobile=Phones_Abroad[1][Variables.databaseLabels().MobileAbroad]
        CitizenAb_WA=Phones_Abroad[2][Variables.databaseLabels().WhatsappAbroad]

        CitizenAb_Wechat=result[Variables.databaseLabels().WeChatAB]
        CitizenAb_email=result[Variables.databaseLabels().AbroadEmail]

        #Add to list
        var_list.extend([CitizenAb_Phone,CitizenAb_Mobile,CitizenAb_WA,CitizenAb_Wechat,CitizenAb_email])


        
#Resident Overseas Address
        Res_Overseas_Details=result[Variables.databaseLabels().ResidenceAbroadDetails]

        Res_Overseas_Street=Res_Overseas_Details[Variables.databaseLabels().Street]
        Res_Overseas_State=Res_Overseas_Details[Variables.databaseLabels().State]
        Res_Overseas_City=Res_Overseas_Details[Variables.databaseLabels().CityorTown]
        Res_Overseas_Country=Res_Overseas_Details[Variables.databaseLabels().Country]

        #Resident Overseas Phone Details
        Res_Overseas_Phones=result[Variables.databaseLabels().ResidentsAbroadPhone]

        Resident_Phone=Res_Overseas_Phones[0][Variables.databaseLabels().ResidentialRes]
        Resident_Mobile=Res_Overseas_Phones[1][Variables.databaseLabels().MobileRes]
        Resident_WA=Res_Overseas_Phones[2][Variables.databaseLabels().WhatsappRes]

        #Resident Overseas Areas of Interest
        AOI_Res=result[Variables.databaseLabels().AreasofInterest]

        #Add to list
        var_list.extend([Res_Overseas_Street,Res_Overseas_State,Res_Overseas_City,Res_Overseas_Country,Resident_Phone,
        Resident_Mobile,Resident_WA,AOI_Res])

#Friends of Barbados                    
        KBB_fr=result[Variables.databaseLabels().KnowledgeofBB]
        AOI_fr=result[Variables.databaseLabels().AreasofInterestFr]

        #Add to list
        var_list.extend([KBB_fr, AOI_fr]) 

      
        Date_Added= str(result[Variables.databaseLabels().DateAdded])
        Last_Updated = str(result[Variables.databaseLabels().LastUpdated])  

        #Add to list    
        var_list.extend([Date_Added,Last_Updated])

        return var_list

 #####################################################################################################
    def ViewFormData(self):   
        model=MyMongoDB()
        
        r=Queries.SiteQuery()
        result=r.find_existing_registered()   

        # Pulling information stored in date to be able to display it on page

        var_list=[]

        Email_Address= result[Variables.databaseLabels.EmailAddress]

    #Add to list
        var_list.append(Email_Address)  

        
#Name Section
        Name=result[Variables.databaseLabels.Name]

        First_Name=Name[Variables.databaseLabels.Firstname]
        Middle_Name=Name[Variables.databaseLabels.Middlename]        
        Last_Name=Name[Variables.databaseLabels.Lastname]

    #Add to list
        var_list.extend([First_Name,Middle_Name,Last_Name])

#Personal Info
        Gender= result[Variables.databaseLabels.Gender]
        Date_of_Birth = str(result[Variables.databaseLabels().DOB])
        Country_of_Birth=result[Variables.databaseLabels().Nationality]

        PPnum=result[Variables.databaseLabels().PassportNumber]
        IssuedPassportCountry=result[Variables.databaseLabels().IssuedPassportCountry]
        WeChatID=result[Variables.databaseLabels().WeChatID]           
        PhoneNum=result[Variables.databaseLabels().PhoneNumber]

        #Add to list
        var_list.extend([Gender,Date_of_Birth,Country_of_Birth,PPnum,IssuedPassportCountry,WeChatID,PhoneNum])

         

        #Address section          
        Address_Details=result[Variables.databaseLabels().Address]

        Address_Street=Address_Details[Variables.databaseLabels().Street]
        Address_City=Address_Details[Variables.databaseLabels().CityorTown]
        Address_Country=Address_Details[Variables.databaseLabels().Country]

        #Add to list
        var_list.extend([Address_Street,Address_City,Address_Country])

          #Emergency Contact Section              
        EmergContDetails=result[Variables.databaseLabels().EmergDetails]

        Emergfname=EmergContDetails[Variables.databaseLabels().EmergencyConFirstname]
        Emerglname=EmergContDetails[Variables.databaseLabels().EmergencyConLastname]
        Emergrel=EmergContDetails[Variables.databaseLabels().EmergencyConRel]
        Emergpnum= EmergContDetails[Variables.databaseLabels().EmergencyConPhone]
        Emergemail=EmergContDetails[Variables.databaseLabels().EmergencyConEmail]                    

        Classification=result[Variables.databaseLabels().Classification]

        #Add to list
        var_list.extend([Emergfname, Emerglname,Emergrel,Emergpnum,Emergemail,Classification])

#Occupation Section
        Occupation_Details=result[Variables.databaseLabels().Occupation]

        Occupation_Type=Occupation_Details[Variables.databaseLabels().Type]
        Education_Field=Occupation_Details[Variables.databaseLabels().FieldofStudy]
        Education_Level=Occupation_Details[Variables.databaseLabels().StudyLevel]
        Education_Inst=Occupation_Details[Variables.databaseLabels().EducationalInst]
        Other_Details=Occupation_Details[Variables.databaseLabels().Other]
        Job_Class=Occupation_Details[Variables.databaseLabels().JobClass]
        Job_Title=Occupation_Details[Variables.databaseLabels().Jobtitle]
        Workplace=Occupation_Details[Variables.databaseLabels().Workplace] 

        #Add to list
        var_list.extend([Occupation_Type,Education_Field,Education_Level,Education_Inst,Other_Details,Job_Class,
        Job_Title,Workplace])

#Citizen Travelling Overseas Section

        Citizen_POT = result[Variables.databaseLabels().PurposeofTravel]
        Citizen_POT_Desc=result[Variables.databaseLabels().POTdescription]

        var_list.extend([Citizen_POT,Citizen_POT_Desc])

        #Citizen Travelling Barbadian Address Information
        Barbados_Address=result[Variables.databaseLabels().BarbadosAddress]

        BarbadosStreet=Barbados_Address[Variables.databaseLabels().Street]
        BarbadosCity=Barbados_Address[Variables.databaseLabels().CityorTown]
        BarbadosParish=Barbados_Address[Variables.databaseLabels().Parish]

        #Add to list   
        var_list.extend([ BarbadosStreet,BarbadosCity,BarbadosParish]) 
        
         

        #Citizen Travelling Destination Address Section
        DestAddress=result[Variables.databaseLabels().AddressAbroad]

        Dest_st=DestAddress[Variables.databaseLabels().Street]
        Dest_city=DestAddress[Variables.databaseLabels().CityorTown]
        Dest_state=DestAddress[Variables.databaseLabels().State]
        Dest_country=DestAddress[Variables.databaseLabels().CountryAbroad]

        #Add to list
        var_list.extend([Dest_st,Dest_city,Dest_state,Dest_country])
                      
        #Citizen Travelling Emergency Contact Information
        EContAbroad=result[Variables.databaseLabels().EmergDetailsAbroad]

        EContfname=EContAbroad[Variables.databaseLabels().EmergencyConFirstname]
        EContlname=EContAbroad[Variables.databaseLabels().EmergencyConLastname]
        EContpnum=EContAbroad[Variables.databaseLabels().EmergencyConPhone]
        EContemail=EContAbroad[Variables.databaseLabels().EmergencyConEmail]
        EContrel=EContAbroad[Variables.databaseLabels().EmergencyConRel] 

        #Add to List         
        var_list.extend([EContfname,EContlname,EContpnum,EContemail,EContrel]) 
                    
        #Travel Dates Section
        TravelDetails=result[Variables.databaseLabels().TravelDates]

        Expected_Depature=str(TravelDetails[Variables.databaseLabels().DepDate])
        Expected_ReturnDate=str(TravelDetails[Variables.databaseLabels().ReturnDate])

        #Add to list  
        var_list.extend([Expected_Depature,Expected_ReturnDate])
                   
        #Citizen Travelling Phone Section
        Phones_Abroad=result[Variables.databaseLabels().PhoneNumberAbroad]
            
        CitizenAb_Phone=Phones_Abroad[0][Variables.databaseLabels().ResidentialAbroad]
        CitizenAb_Mobile=Phones_Abroad[1][Variables.databaseLabels().MobileAbroad]
        CitizenAb_WA=Phones_Abroad[2][Variables.databaseLabels().WhatsappAbroad]

        CitizenAb_Wechat=result[Variables.databaseLabels().WeChatAB]
        CitizenAb_email=result[Variables.databaseLabels().AbroadEmail]

        #Add to list
        var_list.extend([CitizenAb_Phone,CitizenAb_Mobile,CitizenAb_WA,CitizenAb_Wechat,CitizenAb_email])


        
#Resident Overseas Address
        Res_Overseas_Details=result[Variables.databaseLabels().ResidenceAbroadDetails]

        Res_Overseas_Street=Res_Overseas_Details[Variables.databaseLabels().Street]
        Res_Overseas_State=Res_Overseas_Details[Variables.databaseLabels().State]
        Res_Overseas_City=Res_Overseas_Details[Variables.databaseLabels().CityorTown]
        Res_Overseas_Country=Res_Overseas_Details[Variables.databaseLabels().Country]

        #Resident Overseas Phone Details
        Res_Overseas_Phones=result[Variables.databaseLabels().ResidentsAbroadPhone]

        Resident_Phone=Res_Overseas_Phones[0][Variables.databaseLabels().ResidentialRes]
        Resident_Mobile=Res_Overseas_Phones[1][Variables.databaseLabels().MobileRes]
        Resident_WA=Res_Overseas_Phones[2][Variables.databaseLabels().WhatsappRes]

        #Resident Overseas Areas of Interest
        AOI_Res=result[Variables.databaseLabels().AreasofInterest]

        #Add to list
        var_list.extend([Res_Overseas_Street,Res_Overseas_State,Res_Overseas_City,Res_Overseas_Country,Resident_Phone,
        Resident_Mobile,Resident_WA,AOI_Res])

#Friends of Barbados                    
        KBB_fr=result[Variables.databaseLabels().KnowledgeofBB]
        AOI_fr=result[Variables.databaseLabels().AreasofInterestFr]

        #Add to list
        var_list.extend([KBB_fr, AOI_fr]) 

      
        Date_Added= str(result[Variables.databaseLabels().DateAdded])
        Last_Updated = str(result[Variables.databaseLabels().LastUpdated])  

        #Add to list    
        var_list.extend([Date_Added,Last_Updated])

        return var_list


################################################################################################


class Noticeboard: 
    def __init__(self): 
        pass

        
        