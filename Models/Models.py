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
        self._client = MongoClient('mongodb://heroku_qc5l7qqd:or7uuplla29cvq7u647oo7ooap@ds163905.mlab.com:63905/heroku_qc5l7qqd?retryWrites=false')
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

            history.createIndex( {Variables.databaseLabels().EmailAddress: 1 },
                                          {'name': "UniqueEmailIndex"},
                                          {'background':True},
                                          {'unique': True})
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

#Friends of Barbados
                    Variables.databaseLabels().AreasofInterest:AOI,
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
        # Each time there is an update this call takes a snapshot of the current document to be stored 
        # then the update is made after. 

        # Date Added never changes but Last Date Updated does.Tht is what is used to sort them
        DatabaseStruct.InsertHistory()
    
        dob_string=request.form.get('DOB')
        dept_string=request.form.get('dept_date')
        return_string=request.form.get('ret_date')

        DOB = datetime.datetime(int(dob_string[0:4] ),int(dob_string[5:7]),int(dob_string[8:10]))
        expected_departure = datetime.datetime(int(dept_string[0:4] ),int(dept_string[5:7]),int(dept_string[8:10]))
        expected_return = datetime.datetime(int(return_string[0:4] ),int(return_string[5:7]),int(return_string[8:10]))
        
        country=request.form.get('country_ro')
        geolocator = Nominatim(user_agent="Barbados-MFA")
        if country is not None:
            try:
                location = geolocator.geocode(country,timeout=15000)   
            except GeocoderTimedOut as e:
                print("Error: geocode failed on input %s with message %s"%(country,e.message))
                pass  

           
        updatedtimestamp = datetime.datetime.now() 
        

        hashpass=bcrypt.hashpw(request.form.get('password').encode('UTF-8'), bcrypt.gensalt() )
        col = MyMongoDB()
        diasporaList=col.db.diasporaList
        if diasporaList.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email')}) is not None:

            if request.form.get('first_name') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Name.First':request.form.get('first_name')}})
            
            if request.form.get('middle_name') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Name.Middle':request.form.get('middle_name')}})

            if request.form.get('last_name') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Name.Last':request.form.get('last_name')}})

            # if request.form.get('gender') is not None:
            #     diasporaList.update_one(
            #         {Variables.databaseLabels().EmailAddress : request.form.get('email')},
            #         {'$set':{Variables.databaseLabels().Gender:request.form.get('gender')}})

            if DOB is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().DOB:DOB}})

            if request.form.get('occupation') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Type':request.form.get('occupation')}})

            if request.form.get('field_study') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Field-of-Study':request.form.get('field_study')}})

            if request.form.get('field_study_level') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Level':request.form.get('field_study_level')}})

            if request.form.get('edu_inst') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Educational-Institution':request.form.get('edu_inst')}})

            if request.form.get('job_class') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Job-Class':request.form.get('job_class')}})


            if request.form.get('job_title') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Job-Title':request.form.get('job_title')}})

            if request.form.get('workplace_name') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Occupation.Workplace-Name':request.form.get('workplace_name')}})

            

            if  request.form.get('passport_num') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().PassportNumber: request.form.get('passport_num')}})

            if  request.form.get('pp_country') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().IssuedPassportCountry: request.form.get('pp_country')}})                

            if request.form.get('nationality') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().Nationality:request.form.get('nationality')}})

            if request.form.get('we_chat') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().WeChatID:request.form.get('we_chat')}})

            if request.form.get('phone_num') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().PhoneNumber:request.form.get('phone_num')}})

            if request.form.get('street') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address.Street':request.form.get('street')}})

            if request.form.get('parish') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address.State':request.form.get('parish')}})

            if request.form.get('city_town') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address.City/Town':request.form.get('city_town')}})

            if request.form.get('country') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address.Country':request.form.get('country')}})

            if request.form.get('emerg_firstname') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Details.Firstname':request.form.get('emerg_firstname')}})

            if request.form.get('emerg_lastname') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Details.Lastname':request.form.get('emerg_lastname')}})

            if request.form.get('emerg_rel') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Details.Relationship':request.form.get('emerg_rel')}})

            if request.form.get('emerg_phone') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Details.Phone':request.form.get('emerg_phone')}})

            if request.form.get('emerg_email') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Details.Email':request.form.get('emerg_email')}})

            if  request.form.get('classification') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().Classification : request.form.get('classification')}})  

        #Citizen Travelling

            if  request.form.get('radio') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().PurposeofTravel : request.form.get('radio')}})  

            if   request.form.get('POT_des') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().POTdescription :  request.form.get('POT_des')}})                    
                                

            if request.form.get('street_bb') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address-in-Barbados.Street':request.form.get('street_bb')}})            

            if request.form.get('city_town_bb') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address-in-Barbados.City/Town':request.form.get('city_town_bb')}})

            if request.form.get('parish_bb') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Address-in-Barbados.Parish':request.form.get('parish_bb')}})        

            if request.form.get('street_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Destination-Address.Street':request.form.get('street_abroad')}})    
               
            if request.form.get('city_town_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Destination-Address.City/Town':request.form.get('city_town_abroad')}}) 

            if request.form.get('state_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Destination-Address.State':request.form.get('state_abroad')}})

            if request.form.get('country_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Destination-Address.Country':request.form.get('country_abroad')}})

            if request.form.get('firstname_ab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Abroad.Firstname':request.form.get('firstname_ab')}})

            if request.form.get('lastname_ab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Abroad.Lastname':request.form.get('lastname_ab')}})
            
            if request.form.get('emerg_phone_ab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Abroad.Phone':request.form.get('emerg_phone_ab')}})

            if request.form.get('emerg_email_ab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Abroad.Email':request.form.get('emerg_email_ab')}})

            if request.form.get('emerg_rel_ab') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Emergency-Contact-Abroad.Relationship':request.form.get('emerg_rel_ab')}})

            if expected_departure is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Travel-Date-Details.Expected-DepDate':expected_departure}})

            if expected_return is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Travel-Date-Details.Expected-ReturnDate':expected_return}})

                    
            if request.form.get('residential_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Phone-Number-Abroad.Residential-Phone-Abroad':request.form.get('residential_abroad')}})

            if request.form.get('mobile_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Phone-Number-Abroad.Mobile-Abroad':request.form.get('mobile_abroad')}})


            if request.form.get('WA_abroad') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Phone-Number-Abroad.Whatsapp-Abroad':request.form.get('WA_abroad')}})


            if request.form.get('abroad_phone') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().AbroadPhone:request.form.get('abroad_phone')}})


            if request.form.get('abroad_email') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().AbroadEmail:request.form.get('abroad_email')}})              

     #Residents Overseas

            if request.form.get('street_ro') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residence-Abroad-Address.Street':request.form.get('street_ro')}})

            if request.form.get('state_ro') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residence-Abroad-Address.State':request.form.get('state_ro')}})

            if request.form.get('city_town_ro') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residence-Abroad-Address.City/Town':request.form.get('city_town_ro')}})

            if country is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residence-Abroad-Address.Country':country}})

            if location is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residence-Abroad-Address.Location.0':location.latitude}})

                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residence-Abroad-Address.Location.1':location.longitude}})

            if request.form.get('residential_ro') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residents-Abroad-Phone.Residential-Phone-Abroad':request.form.get('residential_ro')}})

            if request.form.get('mobile_ro') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residents-Abroad-Phone.Mobile-Res':request.form.get('mobile_ro')}})

            if request.form.get('WA_ro') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{'Residents-Abroad-Phone.Whatsapp-Res':request.form.get('WA_ro')}})

            if request.form.getlist('AOI') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().AreasofInterest:request.form.get('AOI')}})

 #Friends of Barbados            

            if request.form.getlist('KBB') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().KnowledgeofBB:request.form.get('KBB')}})
            
            if request.form.getlist('AOI_fr') is not None:
                diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                    {'$set':{Variables.databaseLabels().AreasofInterest:request.form.get('AOI_fr')}}) 

            diasporaList.update_one(
                {Variables.databaseLabels().EmailAddress : request.form.get('email')},
                {'$set':{Variables.databaseLabels().LastUpdated:updatedtimestamp}})
 

class Noticeboard: 
    def __init__(self): 
        pass

        
        