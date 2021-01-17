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
from pprint import pprint

class MyMongoDB:
    def __init__(self):
        self._client = MongoClient('localhost', 27017)
        # self._client = MongoClient("mongodb://heroku_qc5l7qqd:or7uuplla29cvq7u647oo7ooap@ds163905.mlab.com:63905/heroku_qc5l7qqd?retryWrites=false")
        self.db = self._client[Variables.siteLabels.DatabaseName]     

class DatabaseStruct:
    def __init__(self):
        pass                   

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
                'Added': timestamp              
                })            
    
    def InsertAdmin(self): 
        model=MyMongoDB()
        user_admin=model.db.user_admin
        password=request.form.get('password')     
        hashpass=bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt() )
        if user_admin.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email'),Variables.databaseLabels().Username:request.form.get('username')}) is None:
            user_admin.insert_one({
                Variables.databaseLabels().Username :request.form.get('username'),
                Variables.databaseLabels().EmailAddress :request.form.get('email'),
                Variables.databaseLabels().Logged:False,
                Variables.databaseLabels().Password: hashpass,
                
         }) 

    def InsertFormData(self):
        model=MyMongoDB()      
        Firstname=request.form.get('first_name')
        Middlename=request.form.get('middle_name')
        Lastname= request.form.get('last_name')

        Gender=request.form.get('gender')   

        dob_string=request.form.get('DOB')
        if dob_string=='':
            dob_string='1900-01-01'
        DOB = datetime.datetime(int(dob_string[0:4]),int(dob_string[5:7]),int(dob_string[8:10]))

        MaritalStatus= request.form.get('marital_status')

        Streetjm=request.form.get('street_jm')
        CityorTownjm=request.form.get('city_town_jm')
        Parishjm= request.form.get('parish_jm')

        CountryofBirth = request.form.get('country_of_birth')
        JaPassportNumber=request.form.get('ja_passport_num')
        OtherNationality=request.form.get('other_nation')
        OtherPassportNumber=request.form.get('passport_num')
          
        Landline= request.form.get('landline')           
        WhatsappNumber= request.form.get('whatsapp_num')
        OtherContacts= request.form.get('other_contact')
        
        OccupationType = request.form.get('occupation')
        StudyDetails=request.form.get('study_details')        
        InstitutionAddress=request.form.get('edu_addr')        
        
        JobClass=request.form.get('job_class')
        Jobtitle = request.form.get('job_title')        
        WorkplaceDetails = request.form.get('workplace_details')

        Other=request.form.get('other')

        EmergencyConFirstname= request.form.get('emerg_firstname')
        EmergencyConLastname= request.form.get('emerg_lastname')
        EmergencyConRel= request.form.get('emerg_rel')
        EmergencyConPhone= request.form.get('emerg_phone')
        EmergencyConEmail= request.form.get('emerg_email')

        EmergencyConFirstname2= request.form.get('emerg_firstname2')
        EmergencyConLastname2= request.form.get('emerg_lastname2')
        EmergencyConRel2= request.form.get('emerg_rel2')
        EmergencyConPhone2= request.form.get('emerg_phone2')
        EmergencyConEmail2= request.form.get('emerg_email2')        

        PurposeofTravel=request.form.get('radio') 
        POTdescription=request.form.get('POT_des')

        dept_string=request.form.get('dept_date')
        return_string=request.form.get('ret_date')

        if dept_string is '':
            dept_string='1900-01-01'
        if return_string is '':
            return_string='1900-01-01'       

        expected_departure = datetime.datetime(int(dept_string[0:4] ),int(dept_string[5:7]),int(dept_string[8:10]))
        expected_return = datetime.datetime(int(return_string[0:4] ),int(return_string[5:7]),int(return_string[8:10]))  
      
        AmountofStops=request.form.get('amountStop')            

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

                    Variables.databaseLabels().Gender:Gender , 
                    Variables.databaseLabels().DOB: DOB,
                    Variables.databaseLabels().CountryofBirth:CountryofBirth, 
                    Variables.databaseLabels().JaPassportNumber: JaPassportNumber,
                    Variables.databaseLabels().OtherNationality: OtherNationality,
                    Variables.databaseLabels().OtherPassportNumber:OtherPassportNumber,
                    Variables.databaseLabels().MaritalStatus:MaritalStatus,

                    Variables.databaseLabels().Landline: Landline,             
                    Variables.databaseLabels().WhatsappNumber: WhatsappNumber,
                    Variables.databaseLabels().OtherContacts: OtherContacts,

                    Variables.databaseLabels().JamaicaAddress:{
                        Variables.databaseLabels().Street:Streetjm,
                        Variables.databaseLabels().CityorTown:CityorTownjm,
                        Variables.databaseLabels().Parish: Parishjm
                        }, 
                    Variables.databaseLabels().Occupation:{
                        Variables.databaseLabels().Type: OccupationType,
                        Variables.databaseLabels().StudyDetails: StudyDetails,                        
                        Variables.databaseLabels().InstitutionAddress: InstitutionAddress,                        

                        Variables.databaseLabels().JobClass: JobClass,
                        Variables.databaseLabels().Jobtitle: Jobtitle,
                        Variables.databaseLabels().WorkplaceDetails: WorkplaceDetails,
                        Variables.databaseLabels().Other: Other           
                        },                     
                    Variables.databaseLabels().EmergDetails:{
                        Variables.databaseLabels().EmergencyConFirstname: EmergencyConFirstname,
                        Variables.databaseLabels().EmergencyConLastname: EmergencyConLastname,
                        Variables.databaseLabels().EmergencyConRel: EmergencyConRel,
                        Variables.databaseLabels().EmergencyConPhone: EmergencyConPhone,
                        Variables.databaseLabels().EmergencyConEmail: EmergencyConEmail,

                        Variables.databaseLabels().EmergencyConFirstname2: EmergencyConFirstname2,
                        Variables.databaseLabels().EmergencyConLastname2: EmergencyConLastname2,
                        Variables.databaseLabels().EmergencyConRel2: EmergencyConRel2,
                        Variables.databaseLabels().EmergencyConPhone2: EmergencyConPhone2,
                        Variables.databaseLabels().EmergencyConEmail2: EmergencyConEmail2 

                        },               

                    #Travel Details Entry
                    Variables.databaseLabels().PurposeofTravel: PurposeofTravel,
                    Variables.databaseLabels().POTdescription:  POTdescription,                    

                    Variables.databaseLabels().TravelDates:{    
                        Variables.databaseLabels().DepDate: expected_departure,
                        Variables.databaseLabels().ReturnDate: expected_return
                        }, 

                    Variables.databaseLabels.AmountStops:AmountofStops,

                    # Single Selection

                    Variables.databaseLabels.CountryOne:{
                        Variables.databaseLabels().Duration:request.form.get('duration_1'),
                        Variables.databaseLabels().AirportCountry:request.form.get('airport_country_1'),
                        Variables.databaseLabels().QuickDetails:request.form.get('airport_details_1'),
                        Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_1'),  
                        Variables.databaseLabels().Street:request.form.get('short_ext_street_1'),
                        Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_1'),
                        Variables.databaseLabels().State: request.form.get('short_ext_state_1'),
                        Variables.databaseLabels().ExtDetails:request.form.get('quick_details_1')
                                   
                        },
                    #Multi Selection 2+
                Variables.databaseLabels().TwoCountries:{
                    Variables.databaseLabels.CountryOne_Multi:{
                        Variables.databaseLabels().Duration:request.form.get('duration_2_1'),
                        Variables.databaseLabels().AirportCountry:request.form.get('airport_country_2_1'),
                        Variables.databaseLabels().QuickDetails:request.form.get('airport_details_2_1'),
                        Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_2_1'),  
                        Variables.databaseLabels().Street:request.form.get('short_ext_street_2_1'),
                        Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_2_1'),
                        Variables.databaseLabels().State: request.form.get('short_ext_state_2_1'),
                        Variables.databaseLabels().ExtDetails:request.form.get('quick_details_2_1')
            
                        },
                    Variables.databaseLabels.CountryTwo:{
                        Variables.databaseLabels().Duration:request.form.get('duration_2_2'),
                        Variables.databaseLabels().AirportCountry:request.form.get('airport_country_2_2'),
                        Variables.databaseLabels().QuickDetails:request.form.get('airport_details_2_2'),
                        Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_2_2'),  
                        Variables.databaseLabels().Street:request.form.get('short_ext_street_2_2'),
                        Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_2_2'),
                        Variables.databaseLabels().State: request.form.get('short_ext_state_2_2'),
                        Variables.databaseLabels().ExtDetails:request.form.get('quick_details_2_2')
              
                        }
                    },
                    Variables.databaseLabels().ThreeCountries:{
                        Variables.databaseLabels.CountryOne_Multi:{
                            Variables.databaseLabels().Duration:request.form.get('duration_3_1'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_3_1'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_3_1'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_3_1'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_3_1'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_3_1'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_3_1'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_3_1')              
                            },
                        Variables.databaseLabels.CountryTwo:{
                            Variables.databaseLabels().Duration:request.form.get('duration_3_2'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_3_2'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_3_2'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_3_2'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_3_2'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_3_2'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_3_2'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_3_2')              
                            },
                        Variables.databaseLabels.CountryThree:{
                            Variables.databaseLabels().Duration:request.form.get('duration_3_3'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_3_3'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_3_3'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_3_3'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_3_3'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_3_3'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_3_3'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_3_3')             
                            }
                    },
                    Variables.databaseLabels().FourCountries:{
                        Variables.databaseLabels.CountryOne_Multi:{
                            Variables.databaseLabels().Duration:request.form.get('duration_4_1'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_4_1'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_4_1'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_4_1'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_4_1'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_4_1'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_4_1'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_4_1')             
                            },
                        Variables.databaseLabels.CountryTwo:{
                            Variables.databaseLabels().Duration:request.form.get('duration_4_2'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_4_2'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_4_2'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_4_2'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_4_2'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_4_2'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_4_2'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_4_2')           
                            },
                        Variables.databaseLabels.CountryThree:{
                            Variables.databaseLabels().Duration:request.form.get('duration_4_3'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_4_3'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_4_3'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_4_3'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_4_3'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_4_3'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_4_3'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_4_3')      
                            },
                         Variables.databaseLabels.CountryFour:{
                            Variables.databaseLabels().Duration:request.form.get('duration_4_4'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_4_4'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_4_4'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_4_4'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_4_4'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_4_4'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_4_4'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_4_4')         
                            }
                    },
                    Variables.databaseLabels().FiveCountries:{
                        Variables.databaseLabels.CountryOne_Multi:{
                            Variables.databaseLabels().Duration:request.form.get('duration_5_1'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_5_1'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_5_1'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_5_1'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_5_1'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_5_1'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_5_1'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_5_1')           
                            },
                        Variables.databaseLabels.CountryTwo:{
                            Variables.databaseLabels().Duration:request.form.get('duration_5_2'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_5_2'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_5_2'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_5_2'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_5_2'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_5_2'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_5_2'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_5_2')              
                            },
                        Variables.databaseLabels.CountryThree:{
                            Variables.databaseLabels().Duration:request.form.get('duration_5_3'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_5_3'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_5_3'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_5_3'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_5_3'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_5_3'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_5_3'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_5_3')              
                            },
                         Variables.databaseLabels.CountryFour:{
                            Variables.databaseLabels().Duration:request.form.get('duration_5_4'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_5_4'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_5_4'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_5_4'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_5_4'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_5_4'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_5_4'),                            
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_5_4')             
                            },
                         Variables.databaseLabels.CountryFive:{
                            Variables.databaseLabels().Duration:request.form.get('duration_5_5'),
                            Variables.databaseLabels().AirportCountry:request.form.get('airport_country_5_5'),
                            Variables.databaseLabels().QuickDetails:request.form.get('airport_details_5_5'),
                            Variables.databaseLabels().ShortExCountry: request.form.get('short_ext_country_5_5'),  
                            Variables.databaseLabels().Street:request.form.get('short_ext_street_5_5'),
                            Variables.databaseLabels().CityorTown:request.form.get('short_ext_city_5_5'),
                            Variables.databaseLabels().State: request.form.get('short_ext_state_5_5'),
                            Variables.databaseLabels().ExtDetails:request.form.get('quick_details_5_5')             
                            }
                    },                 
                    'Emailed_last':timestamp,
                    Variables.databaseLabels().DateRegistered: timestamp,
                    Variables.databaseLabels().LastUpdated:timestamp,                           
                                        
            }
            
            )
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
    def UpdateFormData(self):   
        model=MyMongoDB()        
        diasporaList=model.db.diasporaList        
        diasporaList.delete_one({Variables.databaseLabels.EmailAddress:session['email']})  
        
        database= DatabaseStruct()
        database.InsertFormData()       
        
    
    def AdminDeleteFormData(self,email): 
        model=MyMongoDB()        
        diasporaList=model.db.diasporaList        
        diasporaList.delete_one({Variables.databaseLabels.EmailAddress:email})  
              
        
    def AdminViewFormData(self,email): 
        model=MyMongoDB()
        result=model.db.diasporaList.find_one({Variables.databaseLabels().EmailAddress:email})     
    # Pulling information stored in date to be able to display it on page

        var_list=[]

        Email_Address_0= result[Variables.databaseLabels.EmailAddress]

    #Add to list
    # 0
        var_list.append(Email_Address_0)  
        
    #Name Section
        Name=result[Variables.databaseLabels.Name]

        First_Name_1=Name[Variables.databaseLabels.Firstname]
        Middle_Name_2=Name[Variables.databaseLabels.Middlename]        
        Last_Name_3=Name[Variables.databaseLabels.Lastname]

    #Add to list
        # 1,2,3
        var_list.extend([First_Name_1,Middle_Name_2,Last_Name_3]) 

    #Personal Info
        Gender_4= result[Variables.databaseLabels.Gender]
        Date_of_Birth_5 = str(result[Variables.databaseLabels().DOB])
        Country_of_Birth_6=result[Variables.databaseLabels().CountryofBirth]

        JaPassportNumber_7=result[Variables.databaseLabels().JaPassportNumber]
        OtherNationality_8=result[Variables.databaseLabels().OtherNationality]
        OtherPassportNumber_9=result[Variables.databaseLabels().OtherPassportNumber]
        Landline_10=result[Variables.databaseLabels().Landline]           
        WhatsappNumber_11=result[Variables.databaseLabels().WhatsappNumber]
        MaritalStatus_12=result[Variables.databaseLabels().MaritalStatus]

        #Add to list
        # 4,5,6,7,8,9,10,11,12
        var_list.extend([Gender_4,Date_of_Birth_5,Country_of_Birth_6,JaPassportNumber_7,OtherNationality_8,OtherPassportNumber_9,Landline_10,WhatsappNumber_11,MaritalStatus_12])         

        #Address section          
        Jamaica_Address=result[Variables.databaseLabels().JamaicaAddress]

        JamaicaStreet_13=Jamaica_Address[Variables.databaseLabels().Street]
        JamaicaCity_14=Jamaica_Address[Variables.databaseLabels().CityorTown]
        JamaicaParish_15=Jamaica_Address[Variables.databaseLabels().Parish]

        #Add to list   
        # 13,14,15
        var_list.extend([JamaicaStreet_13,JamaicaCity_14,JamaicaParish_15])      

            #Emergency Contact Section              
        EmergContDetails=result[Variables.databaseLabels().EmergDetails]

        Emergfname_16=EmergContDetails[Variables.databaseLabels().EmergencyConFirstname]
        Emerglname_17=EmergContDetails[Variables.databaseLabels().EmergencyConLastname]
        Emergrel_18=EmergContDetails[Variables.databaseLabels().EmergencyConRel]
        Emergpnum_19= EmergContDetails[Variables.databaseLabels().EmergencyConPhone]
        Emergemail_20=EmergContDetails[Variables.databaseLabels().EmergencyConEmail]  

        Emergfname2_21=EmergContDetails[Variables.databaseLabels().EmergencyConFirstname2]
        Emerglname2_22=EmergContDetails[Variables.databaseLabels().EmergencyConLastname2]
        Emergrel2_23=EmergContDetails[Variables.databaseLabels().EmergencyConRel2]
        Emergpnum2_24= EmergContDetails[Variables.databaseLabels().EmergencyConPhone2]
        Emergemail2_25=EmergContDetails[Variables.databaseLabels().EmergencyConEmail2]  

        #Add to list
        # 16, 17, 18, 19, 20
        var_list.extend([Emergfname_16, Emerglname_17,Emergrel_18,Emergpnum_19,Emergemail_20])
        # 21, 22, 23, 24, 25
        var_list.extend([Emergfname2_21, Emerglname2_22,Emergrel2_23,Emergpnum2_24,Emergemail2_25])

    #Occupation Section
        Occupation_Details=result[Variables.databaseLabels().Occupation]

        Occupation_Type_26=Occupation_Details[Variables.databaseLabels().Type]
        StudyDetails_27=Occupation_Details[Variables.databaseLabels().StudyDetails]
        InstitutionAddress_28=Occupation_Details[Variables.databaseLabels().InstitutionAddress]
          

        Job_Class_29=Occupation_Details[Variables.databaseLabels().JobClass]
        Job_Title_30=Occupation_Details[Variables.databaseLabels().Jobtitle]
        WorkplaceDetails_31=Occupation_Details[Variables.databaseLabels().WorkplaceDetails] 

        Other_Details_32=Occupation_Details[Variables.databaseLabels().Other]

        #Add to list
        
        var_list.extend([Occupation_Type_26,StudyDetails_27,InstitutionAddress_28,Job_Class_29,Job_Title_30,WorkplaceDetails_31,Other_Details_32])

    #Citizen Travelling Overseas Section

        Citizen_POT_33 = result[Variables.databaseLabels().PurposeofTravel]
        Citizen_POT_Desc_34=result[Variables.databaseLabels().POTdescription]

    #Add to list 33, 34
        var_list.extend([Citizen_POT_33,Citizen_POT_Desc_34])

    #Travel Dates Section
        TravelDetails=result[Variables.databaseLabels().TravelDates]

        Expected_Depature_35=str(TravelDetails[Variables.databaseLabels().DepDate])
        Expected_ReturnDate_36=str(TravelDetails[Variables.databaseLabels().ReturnDate])

        #Add to list  35, 36
        var_list.extend([Expected_Depature_35,Expected_ReturnDate_36])

    #Amount of  stops in trip
        Amount_Stops_37=result[Variables.databaseLabels().AmountStops]

        #Add to list  37
        var_list.extend([Amount_Stops_37])

    #One Single Country selected
        Single_Country=result[Variables.databaseLabels().CountryOne]
        Duration_1_38=Single_Country[Variables.databaseLabels().Duration]
        Airport_Country_1_39=Single_Country[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_1_40=Single_Country[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_1_41=Single_Country[Variables.databaseLabels().ShortExCountry]
        Dest_Street_1_42=Single_Country[Variables.databaseLabels().Street]
        Dest_City_1_43=Single_Country[Variables.databaseLabels().CityorTown]
        Dest_State_1_44=Single_Country[Variables.databaseLabels().State]
        ExtDetails_1_45=Single_Country[Variables.databaseLabels().ExtDetails]
        

        #Add to list 38, 39, 40, 41, 42, 43, 44, 45
        var_list.extend([Duration_1_38,Airport_Country_1_39,Emergency_Quick_1_40,ShortEx_Country_1_41,Dest_Street_1_42,Dest_City_1_43,Dest_State_1_44,ExtDetails_1_45])     


        
        #Two Countries selected
            #FIRST
        CountryTwo=result[Variables.databaseLabels().TwoCountries]
        Single_Country_2_1=CountryTwo[Variables.databaseLabels().CountryOne_Multi]
        Duration_2_1_46=Single_Country_2_1[Variables.databaseLabels().Duration]
        Airport_Country_2_1_47=Single_Country_2_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_2_1_48=Single_Country_2_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_2_1_49=Single_Country_2_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_2_1_50=Single_Country_2_1[Variables.databaseLabels().Street]
        Dest_City_2_1_51=Single_Country_2_1[Variables.databaseLabels().CityorTown]
        Dest_State_2_1_52=Single_Country_2_1[Variables.databaseLabels().State]
        ExtDetails_2_1_53=Single_Country_2_1[Variables.databaseLabels().ExtDetails]
        
            #SECOND
        
        Single_Country_2_2=CountryTwo[Variables.databaseLabels().CountryTwo]
        Duration_2_2_54=Single_Country_2_2[Variables.databaseLabels().Duration]
        Airport_Country_2_2_55=Single_Country_2_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_2_2_56=Single_Country_2_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_2_2_57=Single_Country_2_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_2_2_58=Single_Country_2_2[Variables.databaseLabels().Street]
        Dest_City_2_2_59=Single_Country_2_2[Variables.databaseLabels().CityorTown]
        Dest_State_2_2_60=Single_Country_2_2[Variables.databaseLabels().State]
        ExtDetails_2_2_61=Single_Country_2_2[Variables.databaseLabels().ExtDetails]

        #Add to list
        var_list.extend([Duration_2_1_46,Airport_Country_2_1_47,Emergency_Quick_2_1_48,ShortEx_Country_2_1_49,Dest_Street_2_1_50,Dest_City_2_1_51,Dest_State_2_1_52,ExtDetails_2_1_53])
        
        var_list.extend([Duration_2_2_54,Airport_Country_2_2_55,Emergency_Quick_2_2_56,ShortEx_Country_2_2_57,Dest_Street_2_2_58,Dest_City_2_2_59,Dest_State_2_2_60,ExtDetails_2_2_61])


        #Three Countries Selected       
            #FIRST
        CountryThree=result[Variables.databaseLabels().ThreeCountries]
        Single_Country_3_1=CountryThree[Variables.databaseLabels().CountryOne_Multi]
        Duration_3_1_62=Single_Country_3_1[Variables.databaseLabels().Duration]
        Airport_Country_3_1_63=Single_Country_3_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_3_1_64=Single_Country_3_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_3_1_65=Single_Country_3_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_3_1_66=Single_Country_3_1[Variables.databaseLabels().Street]
        Dest_City_3_1_67=Single_Country_3_1[Variables.databaseLabels().CityorTown]
        Dest_State_3_1_68=Single_Country_3_1[Variables.databaseLabels().State]
        ExtDetails_3_1_69=Single_Country_3_1[Variables.databaseLabels().ExtDetails]

            #SECOND
        
        Single_Country_3_2=CountryThree[Variables.databaseLabels().CountryTwo]
        Duration_3_2_70=Single_Country_3_2[Variables.databaseLabels().Duration]
        Airport_Country_3_2_71=Single_Country_3_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_3_2_72=Single_Country_3_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_3_2_73=Single_Country_3_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_3_2_74=Single_Country_3_2[Variables.databaseLabels().Street]
        Dest_City_3_2_75=Single_Country_3_2[Variables.databaseLabels().CityorTown]
        Dest_State_3_2_76=Single_Country_3_2[Variables.databaseLabels().State]
        ExtDetails_3_2_77=Single_Country_3_2[Variables.databaseLabels().ExtDetails]

        #THIRD
        
        Single_Country_3_3=CountryThree[Variables.databaseLabels().CountryThree]
        Duration_3_3_78=Single_Country_3_3[Variables.databaseLabels().Duration]
        Airport_Country_3_3_79=Single_Country_3_3[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_3_3_80=Single_Country_3_3[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_3_3_81=Single_Country_3_3[Variables.databaseLabels().ShortExCountry]
        Dest_Street_3_3_82=Single_Country_3_3[Variables.databaseLabels().Street]
        Dest_City_3_3_83=Single_Country_3_3[Variables.databaseLabels().CityorTown]
        Dest_State_3_3_84=Single_Country_3_3[Variables.databaseLabels().State]
        ExtDetails_3_3_85=Single_Country_3_3[Variables.databaseLabels().ExtDetails]

        #Add to list
        var_list.extend([Duration_3_1_62,Airport_Country_3_1_63,Emergency_Quick_3_1_64,ShortEx_Country_3_1_65,Dest_Street_3_1_66,Dest_City_3_1_67,Dest_State_3_1_68,ExtDetails_3_1_69])
        
        var_list.extend([Duration_3_2_70,Airport_Country_3_2_71,Emergency_Quick_3_2_72,ShortEx_Country_3_2_73,Dest_Street_3_2_74,Dest_City_3_2_75,Dest_State_3_2_76,ExtDetails_3_2_77])
        
        var_list.extend([Duration_3_3_78,Airport_Country_3_3_79,Emergency_Quick_3_3_80,ShortEx_Country_3_3_81,Dest_Street_3_3_82,Dest_City_3_3_83,Dest_State_3_3_84,ExtDetails_3_3_85])
        
        #Four Countries Selected       
            #FIRST
        CountryFour=result[Variables.databaseLabels().FourCountries]
        Single_Country_4_1=CountryFour[Variables.databaseLabels().CountryOne_Multi]
        Duration_4_1_86=Single_Country_4_1[Variables.databaseLabels().Duration]
        Airport_Country_4_1_87=Single_Country_4_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_1_88=Single_Country_4_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_1_89=Single_Country_4_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_1_90=Single_Country_4_1[Variables.databaseLabels().Street]
        Dest_City_4_1_91=Single_Country_4_1[Variables.databaseLabels().CityorTown]
        Dest_State_4_1_92=Single_Country_4_1[Variables.databaseLabels().State]
        ExtDetails_4_1_93=Single_Country_4_1[Variables.databaseLabels().ExtDetails]        
        #SECOND
        
        Single_Country_4_2=CountryFour[Variables.databaseLabels().CountryTwo]
        Duration_4_2_94=Single_Country_4_2[Variables.databaseLabels().Duration]
        Airport_Country_4_2_95=Single_Country_4_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_2_96=Single_Country_4_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_2_97=Single_Country_4_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_2_98=Single_Country_4_2[Variables.databaseLabels().Street]
        Dest_City_4_2_99=Single_Country_4_2[Variables.databaseLabels().CityorTown]
        Dest_State_4_2_100=Single_Country_4_2[Variables.databaseLabels().State]
        ExtDetails_4_2_101=Single_Country_4_2[Variables.databaseLabels().ExtDetails]

        #THIRD
        
        Single_Country_4_3=CountryFour[Variables.databaseLabels().CountryThree]
        Duration_4_3_102=Single_Country_4_3[Variables.databaseLabels().Duration]
        Airport_Country_4_3_103=Single_Country_4_3[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_3_104=Single_Country_4_3[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_3_105=Single_Country_4_3[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_3_106=Single_Country_4_3[Variables.databaseLabels().Street]
        Dest_City_4_3_107=Single_Country_4_3[Variables.databaseLabels().CityorTown]
        Dest_State_4_3_108=Single_Country_4_3[Variables.databaseLabels().State]
        ExtDetails_4_3_109=Single_Country_4_3[Variables.databaseLabels().ExtDetails]
            #FOURTH
        
        Single_Country_4_4=CountryFour[Variables.databaseLabels().CountryFour]
        Duration_4_4_110=Single_Country_4_4[Variables.databaseLabels().Duration]
        Airport_Country_4_4_111=Single_Country_4_4[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_4_112=Single_Country_4_4[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_4_113=Single_Country_4_4[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_4_114=Single_Country_4_4[Variables.databaseLabels().Street]
        Dest_City_4_4_115=Single_Country_4_4[Variables.databaseLabels().CityorTown]
        Dest_State_4_4_116=Single_Country_4_4[Variables.databaseLabels().State]
        ExtDetails_4_4_117=Single_Country_4_4[Variables.databaseLabels().ExtDetails]

        #Add to list
        var_list.extend([Duration_4_1_86,Airport_Country_4_1_87,Emergency_Quick_4_1_88,ShortEx_Country_4_1_89,Dest_Street_4_1_90,Dest_City_4_1_91,Dest_State_4_1_92,ExtDetails_4_1_93])
        
        var_list.extend([Duration_4_2_94,Airport_Country_4_2_95,Emergency_Quick_4_2_96,ShortEx_Country_4_2_97,Dest_Street_4_2_98,Dest_City_4_2_99,Dest_State_4_2_100,ExtDetails_4_2_101])
        
        var_list.extend([Duration_4_3_102,Airport_Country_4_3_103,Emergency_Quick_4_3_104,ShortEx_Country_4_3_105,Dest_Street_4_3_106,Dest_City_4_3_107,Dest_State_4_3_108,ExtDetails_4_3_109])
        
        var_list.extend([Duration_4_4_110,Airport_Country_4_4_111,Emergency_Quick_4_4_112,ShortEx_Country_4_4_113,Dest_Street_4_4_114,Dest_City_4_4_115,Dest_State_4_4_116,ExtDetails_4_4_117])

        #Five Countries Selected       
            #FIRST
        CountryFive=result[Variables.databaseLabels().FiveCountries]
        Single_Country_5_1=CountryFive[Variables.databaseLabels().CountryOne_Multi]
        Duration_5_1_118=Single_Country_5_1[Variables.databaseLabels().Duration]
        Airport_Country_5_1_119=Single_Country_5_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_1_120=Single_Country_5_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_1_121=Single_Country_5_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_1_122=Single_Country_5_1[Variables.databaseLabels().Street]
        Dest_City_5_1_123=Single_Country_5_1[Variables.databaseLabels().CityorTown]
        Dest_State_5_1_124=Single_Country_5_1[Variables.databaseLabels().State]
        ExtDetails_5_1_125=Single_Country_5_1[Variables.databaseLabels().ExtDetails]        
        #SECOND
        
        Single_Country_5_2=CountryFive[Variables.databaseLabels().CountryTwo]
        Duration_5_2_126=Single_Country_5_2[Variables.databaseLabels().Duration]
        Airport_Country_5_2_127=Single_Country_5_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_2_128=Single_Country_5_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_2_129=Single_Country_5_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_2_130=Single_Country_5_2[Variables.databaseLabels().Street]
        Dest_City_5_2_131=Single_Country_5_2[Variables.databaseLabels().CityorTown]
        Dest_State_5_2_132=Single_Country_5_2[Variables.databaseLabels().State]
        ExtDetails_5_2_133=Single_Country_5_2[Variables.databaseLabels().ExtDetails]         

        #THIRD
        
        Single_Country_5_3=CountryFive[Variables.databaseLabels().CountryThree]
        Duration_5_3_134=Single_Country_5_3[Variables.databaseLabels().Duration]
        Airport_Country_5_3_135=Single_Country_5_3[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_3_136=Single_Country_5_3[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_3_137=Single_Country_5_3[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_3_138=Single_Country_5_3[Variables.databaseLabels().Street]
        Dest_City_5_3_139=Single_Country_5_3[Variables.databaseLabels().CityorTown]
        Dest_State_5_3_140=Single_Country_5_3[Variables.databaseLabels().State]
        ExtDetails_5_3_141=Single_Country_5_3[Variables.databaseLabels().ExtDetails]
            #FOURTH
        
        Single_Country_5_4=CountryFive[Variables.databaseLabels().CountryFour]
        Duration_5_4_142=Single_Country_5_4[Variables.databaseLabels().Duration]
        Airport_Country_5_4_143=Single_Country_5_4[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_4_144=Single_Country_5_4[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_4_145=Single_Country_5_4[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_4_146=Single_Country_5_4[Variables.databaseLabels().Street]
        Dest_City_5_4_147=Single_Country_5_4[Variables.databaseLabels().CityorTown]
        Dest_State_5_4_148=Single_Country_5_4[Variables.databaseLabels().State]
        ExtDetails_5_4_149=Single_Country_5_4[Variables.databaseLabels().ExtDetails]
            #FIFTH
        
        Single_Country_5_5=CountryFive[Variables.databaseLabels().CountryFive]
        Duration_5_5_150=Single_Country_5_5[Variables.databaseLabels().Duration]
        Airport_Country_5_5_151=Single_Country_5_5[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_5_152=Single_Country_5_5[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_5_153=Single_Country_5_5[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_5_154=Single_Country_5_5[Variables.databaseLabels().Street]
        Dest_City_5_5_155=Single_Country_5_5[Variables.databaseLabels().CityorTown]
        Dest_State_5_5_156=Single_Country_5_5[Variables.databaseLabels().State]
        ExtDetails_5_5_157=Single_Country_5_5[Variables.databaseLabels().ExtDetails]
        
        #Add to list
        var_list.extend([Duration_5_1_118,Airport_Country_5_1_119,Emergency_Quick_5_1_120,ShortEx_Country_5_1_121,Dest_Street_5_1_122,Dest_City_5_1_123,Dest_State_5_1_124,ExtDetails_5_1_125])
        
        var_list.extend([Duration_5_2_126,Airport_Country_5_2_127,Emergency_Quick_5_2_128,ShortEx_Country_5_2_129,Dest_Street_5_2_130,Dest_City_5_2_131,Dest_State_5_2_132,ExtDetails_5_2_133])
        
        var_list.extend([Duration_5_3_134,Airport_Country_5_3_135,Emergency_Quick_5_3_136,ShortEx_Country_5_3_137,Dest_Street_5_3_138,Dest_City_5_3_139,Dest_State_5_3_140,ExtDetails_5_3_141])
        
        var_list.extend([Duration_5_4_142,Airport_Country_5_4_143,Emergency_Quick_5_4_144,ShortEx_Country_5_4_145,Dest_Street_5_4_146,Dest_City_5_4_147,Dest_State_5_4_148,ExtDetails_5_4_149])
        
        var_list.extend([Duration_5_5_150,Airport_Country_5_5_151,Emergency_Quick_5_5_152,ShortEx_Country_5_5_153,Dest_Street_5_5_154,Dest_City_5_5_155,Dest_State_5_5_156,ExtDetails_5_5_157])
        
        Date_Added_158= str(result[Variables.databaseLabels().DateRegistered])
        Last_Updated_159 = str(result[Variables.databaseLabels().LastUpdated])  

        #Add to list    
        var_list.extend([Date_Added_158,Last_Updated_159])       
        
        
        
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
    # 0
        var_list.append(Email_Address)  
        
    #Name Section
        Name=result[Variables.databaseLabels.Name]

        First_Name=Name[Variables.databaseLabels.Firstname]
        Middle_Name=Name[Variables.databaseLabels.Middlename]        
        Last_Name=Name[Variables.databaseLabels.Lastname]

    #Add to list
        # 1,2,3
        var_list.extend([First_Name,Middle_Name,Last_Name]) 

    #Personal Info
        Gender= result[Variables.databaseLabels.Gender]
        Date_of_Birth = str(result[Variables.databaseLabels().DOB])
        
        Country_of_Birth=result[Variables.databaseLabels().CountryofBirth]
        PPnum=result[Variables.databaseLabels().JaPassportNumber]
        
        OtherNationality=result[Variables.databaseLabels().OtherNationality]
        OtherPassportNumber=result[Variables.databaseLabels().OtherPassportNumber]
        
        Landline=result[Variables.databaseLabels().Landline]           
        WhatsappNumber=result[Variables.databaseLabels().WhatsappNumber]
        MaritalStatus=result[Variables.databaseLabels().MaritalStatus]

        #Add to list
        # 4,5,6,7,8,9,10,11,12
        var_list.extend([Gender,Date_of_Birth,Country_of_Birth,PPnum,OtherNationality,OtherPassportNumber,Landline,WhatsappNumber,MaritalStatus])         

        #Address section          
        Jamaica_Address=result[Variables.databaseLabels().JamaicaAddress]

        JamaicaStreet=Jamaica_Address[Variables.databaseLabels().Street]
        JamaicaCity=Jamaica_Address[Variables.databaseLabels().CityorTown]
        JamaicaParish=Jamaica_Address[Variables.databaseLabels().Parish]

        #Add to list   
        # 13,14,15
        var_list.extend([JamaicaStreet,JamaicaCity,JamaicaParish])      

            #Emergency Contact Section              
        EmergContDetails=result[Variables.databaseLabels().EmergDetails]

        Emergfname=EmergContDetails[Variables.databaseLabels().EmergencyConFirstname]
        Emerglname=EmergContDetails[Variables.databaseLabels().EmergencyConLastname]
        Emergrel=EmergContDetails[Variables.databaseLabels().EmergencyConRel]
        Emergpnum= EmergContDetails[Variables.databaseLabels().EmergencyConPhone]
        Emergemail=EmergContDetails[Variables.databaseLabels().EmergencyConEmail]  

        Emergfname2=EmergContDetails[Variables.databaseLabels().EmergencyConFirstname2]
        Emerglname2=EmergContDetails[Variables.databaseLabels().EmergencyConLastname2]
        Emergrel2=EmergContDetails[Variables.databaseLabels().EmergencyConRel2]
        Emergpnum2= EmergContDetails[Variables.databaseLabels().EmergencyConPhone2]
        Emergemail2=EmergContDetails[Variables.databaseLabels().EmergencyConEmail2]  

        #Add to list
        # 16, 17, 18, 19, 20
        var_list.extend([Emergfname, Emerglname,Emergrel,Emergpnum,Emergemail])
        # 21, 22, 23, 24, 25
        var_list.extend([Emergfname2, Emerglname2,Emergrel2,Emergpnum2,Emergemail2])

    #Occupation Section
        Occupation_Details=result[Variables.databaseLabels().Occupation]

        Occupation_Type=Occupation_Details[Variables.databaseLabels().Type]
        InstitutionAddress=Occupation_Details[Variables.databaseLabels().InstitutionAddress]
        StudyDetails=Occupation_Details[Variables.databaseLabels().StudyDetails]  

        Job_Class=Occupation_Details[Variables.databaseLabels().JobClass]
        Job_Title=Occupation_Details[Variables.databaseLabels().Jobtitle]
        WorkplaceDetails=Occupation_Details[Variables.databaseLabels().WorkplaceDetails] 

        Other_Details=Occupation_Details[Variables.databaseLabels().Other]

        #Add to list
        # 26, 27, 28, 29, 30, 31, 32
        var_list.extend([Occupation_Type,StudyDetails,InstitutionAddress,Job_Class,Job_Title,WorkplaceDetails,Other_Details])

    #Citizen Travelling Overseas Section

        Citizen_POT = result[Variables.databaseLabels().PurposeofTravel]
        Citizen_POT_Desc=result[Variables.databaseLabels().POTdescription]

    #Add to list 33, 34
        var_list.extend([Citizen_POT,Citizen_POT_Desc])

    #Travel Dates Section
        TravelDetails=result[Variables.databaseLabels().TravelDates]

        Expected_Depature=str(TravelDetails[Variables.databaseLabels().DepDate])
        Expected_ReturnDate=str(TravelDetails[Variables.databaseLabels().ReturnDate])

        #Add to list  35, 36
        var_list.extend([Expected_Depature,Expected_ReturnDate])

    #Amount of  stops in trip
        Amount_Stops=result[Variables.databaseLabels().AmountStops]

        #Add to list  37
        var_list.extend([Amount_Stops])

    #One Single Country selected
        Single_Country=result[Variables.databaseLabels().CountryOne]
        Duration_1=Single_Country[Variables.databaseLabels().Duration]
        Airport_Country_1=Single_Country[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_1=Single_Country[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_1=Single_Country[Variables.databaseLabels().ShortExCountry]
        Dest_Street_1=Single_Country[Variables.databaseLabels().Street]
        Dest_City_1=Single_Country[Variables.databaseLabels().CityorTown]
        Dest_State_1=Single_Country[Variables.databaseLabels().State]
        ExtDetails_1=Single_Country[Variables.databaseLabels().ExtDetails]
        

        #Add to list 38, 39, 40, 41, 42, 43, 44, 45
        var_list.extend([Duration_1,Airport_Country_1,Emergency_Quick_1,ShortEx_Country_1,Dest_Street_1,Dest_City_1,Dest_State_1,ExtDetails_1])     


        
        #Two Countries selected
            #FIRST
        CountryTwo=result[Variables.databaseLabels().TwoCountries]
        Single_Country_2_1=CountryTwo[Variables.databaseLabels().CountryOne_Multi]
        Duration_2_1=Single_Country_2_1[Variables.databaseLabels().Duration]
        Airport_Country_2_1=Single_Country_2_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_2_1=Single_Country_2_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_2_1=Single_Country_2_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_2_1=Single_Country_2_1[Variables.databaseLabels().Street]
        Dest_City_2_1=Single_Country_2_1[Variables.databaseLabels().CityorTown]
        Dest_State_2_1=Single_Country_2_1[Variables.databaseLabels().State]
        ExtDetails_2_1=Single_Country_2_1[Variables.databaseLabels().ExtDetails]
        
            #SECOND
        
        Single_Country_2_2=CountryTwo[Variables.databaseLabels().CountryTwo]
        Duration_2_2=Single_Country_2_2[Variables.databaseLabels().Duration]
        Airport_Country_2_2=Single_Country_2_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_2_2=Single_Country_2_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_2_2=Single_Country_2_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_2_2=Single_Country_2_2[Variables.databaseLabels().Street]
        Dest_City_2_2=Single_Country_2_2[Variables.databaseLabels().CityorTown]
        Dest_State_2_2=Single_Country_2_2[Variables.databaseLabels().State]
        ExtDetails_2_2=Single_Country_2_2[Variables.databaseLabels().ExtDetails]

        #Add to list
        var_list.extend([Duration_2_1,Airport_Country_2_1,Emergency_Quick_2_1,ShortEx_Country_2_1,Dest_Street_2_1,Dest_City_2_1,Dest_State_2_1,ExtDetails_2_1])
        var_list.extend([Duration_2_2,Airport_Country_2_2,Emergency_Quick_2_2,ShortEx_Country_2_2,Dest_Street_2_2,Dest_City_2_2,Dest_State_2_2,ExtDetails_2_2])


        #Three Countries Selected       
            #FIRST
        CountryThree=result[Variables.databaseLabels().ThreeCountries]
        Single_Country_3_1=CountryThree[Variables.databaseLabels().CountryOne_Multi]
        Duration_3_1=Single_Country_3_1[Variables.databaseLabels().Duration]
        Airport_Country_3_1=Single_Country_3_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_3_1=Single_Country_3_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_3_1=Single_Country_3_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_3_1=Single_Country_3_1[Variables.databaseLabels().Street]
        Dest_City_3_1=Single_Country_3_1[Variables.databaseLabels().CityorTown]
        Dest_State_3_1=Single_Country_3_1[Variables.databaseLabels().State]
        ExtDetails_3_1=Single_Country_3_1[Variables.databaseLabels().ExtDetails]

            #SECOND
        
        Single_Country_3_2=CountryThree[Variables.databaseLabels().CountryTwo]
        Duration_3_2=Single_Country_3_2[Variables.databaseLabels().Duration]
        Airport_Country_3_2=Single_Country_3_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_3_2=Single_Country_3_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_3_2=Single_Country_3_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_3_2=Single_Country_3_2[Variables.databaseLabels().Street]
        Dest_City_3_2=Single_Country_3_2[Variables.databaseLabels().CityorTown]
        Dest_State_3_2=Single_Country_3_2[Variables.databaseLabels().State]
        ExtDetails_3_2=Single_Country_3_2[Variables.databaseLabels().ExtDetails]

        #THIRD
        
        Single_Country_3_3=CountryThree[Variables.databaseLabels().CountryThree]
        Duration_3_3=Single_Country_3_3[Variables.databaseLabels().Duration]
        Airport_Country_3_3=Single_Country_3_3[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_3_3=Single_Country_3_3[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_3_3=Single_Country_3_3[Variables.databaseLabels().ShortExCountry]
        Dest_Street_3_3=Single_Country_3_3[Variables.databaseLabels().Street]
        Dest_City_3_3=Single_Country_3_3[Variables.databaseLabels().CityorTown]
        Dest_State_3_3=Single_Country_3_3[Variables.databaseLabels().State]
        ExtDetails_3_3=Single_Country_3_3[Variables.databaseLabels().ExtDetails]

        #Add to list
        var_list.extend([Duration_3_1,Airport_Country_3_1,Emergency_Quick_3_1,ShortEx_Country_3_1,Dest_Street_3_1,Dest_City_3_1,Dest_State_3_1,ExtDetails_3_1])
        var_list.extend([Duration_3_2,Airport_Country_3_2,Emergency_Quick_3_2,ShortEx_Country_3_2,Dest_Street_3_2,Dest_City_3_2,Dest_State_3_2,ExtDetails_3_2])
        var_list.extend([Duration_3_3,Airport_Country_3_3,Emergency_Quick_3_3,ShortEx_Country_3_3,Dest_Street_3_3,Dest_City_3_3,Dest_State_3_3,ExtDetails_3_3])
        
        #Four Countries Selected       
            #FIRST
        CountryFour=result[Variables.databaseLabels().FourCountries]
        Single_Country_4_1=CountryFour[Variables.databaseLabels().CountryOne_Multi]
        Duration_4_1=Single_Country_4_1[Variables.databaseLabels().Duration]
        Airport_Country_4_1=Single_Country_4_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_1=Single_Country_4_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_1=Single_Country_4_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_1=Single_Country_4_1[Variables.databaseLabels().Street]
        Dest_City_4_1=Single_Country_4_1[Variables.databaseLabels().CityorTown]
        Dest_State_4_1=Single_Country_4_1[Variables.databaseLabels().State]
        ExtDetails_4_1=Single_Country_4_1[Variables.databaseLabels().ExtDetails]        
        #SECOND
        
        Single_Country_4_2=CountryFour[Variables.databaseLabels().CountryTwo]
        Duration_4_2=Single_Country_4_2[Variables.databaseLabels().Duration]
        Airport_Country_4_2=Single_Country_4_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_2=Single_Country_4_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_2=Single_Country_4_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_2=Single_Country_4_2[Variables.databaseLabels().Street]
        Dest_City_4_2=Single_Country_4_2[Variables.databaseLabels().CityorTown]
        Dest_State_4_2=Single_Country_4_2[Variables.databaseLabels().State]
        ExtDetails_4_2=Single_Country_4_2[Variables.databaseLabels().ExtDetails]

        #THIRD
        
        Single_Country_4_3=CountryFour[Variables.databaseLabels().CountryThree]
        Duration_4_3=Single_Country_4_3[Variables.databaseLabels().Duration]
        Airport_Country_4_3=Single_Country_4_3[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_3=Single_Country_4_3[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_3=Single_Country_4_3[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_3=Single_Country_4_3[Variables.databaseLabels().Street]
        Dest_City_4_3=Single_Country_4_3[Variables.databaseLabels().CityorTown]
        Dest_State_4_3=Single_Country_4_3[Variables.databaseLabels().State]
        ExtDetails_4_3=Single_Country_4_3[Variables.databaseLabels().ExtDetails]
            #FOURTH
        
        Single_Country_4_4=CountryFour[Variables.databaseLabels().CountryFour]
        Duration_4_4=Single_Country_4_4[Variables.databaseLabels().Duration]
        Airport_Country_4_4=Single_Country_4_4[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_4_4=Single_Country_4_4[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_4_4=Single_Country_4_4[Variables.databaseLabels().ShortExCountry]
        Dest_Street_4_4=Single_Country_4_4[Variables.databaseLabels().Street]
        Dest_City_4_4=Single_Country_4_4[Variables.databaseLabels().CityorTown]
        Dest_State_4_4=Single_Country_4_4[Variables.databaseLabels().State]
        ExtDetails_4_4=Single_Country_4_4[Variables.databaseLabels().ExtDetails]

        #Add to list
        var_list.extend([Duration_4_1,Airport_Country_4_1,Emergency_Quick_4_1,ShortEx_Country_4_1,Dest_Street_4_1,Dest_City_4_1,Dest_State_4_1,ExtDetails_4_1])
        var_list.extend([Duration_4_2,Airport_Country_4_2,Emergency_Quick_4_2,ShortEx_Country_4_2,Dest_Street_4_2,Dest_City_4_2,Dest_State_4_2,ExtDetails_4_2])
        var_list.extend([Duration_4_3,Airport_Country_4_3,Emergency_Quick_4_3,ShortEx_Country_4_3,Dest_Street_4_3,Dest_City_4_3,Dest_State_4_3,ExtDetails_4_3])
        var_list.extend([Duration_4_4,Airport_Country_4_4,Emergency_Quick_4_4,ShortEx_Country_4_4,Dest_Street_4_4,Dest_City_4_4,Dest_State_4_4,ExtDetails_4_4])

        #Five Countries Selected       
            #FIRST
        CountryFive=result[Variables.databaseLabels().FiveCountries]
        Single_Country_5_1=CountryFive[Variables.databaseLabels().CountryOne_Multi]
        Duration_5_1=Single_Country_5_1[Variables.databaseLabels().Duration]
        Airport_Country_5_1=Single_Country_5_1[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_1=Single_Country_5_1[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_1=Single_Country_5_1[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_1=Single_Country_5_1[Variables.databaseLabels().Street]
        Dest_City_5_1=Single_Country_5_1[Variables.databaseLabels().CityorTown]
        Dest_State_5_1=Single_Country_5_1[Variables.databaseLabels().State]
        ExtDetails_5_1=Single_Country_5_1[Variables.databaseLabels().ExtDetails]        
        #SECOND
        
        Single_Country_5_2=CountryFive[Variables.databaseLabels().CountryTwo]
        Duration_5_2=Single_Country_5_2[Variables.databaseLabels().Duration]
        Airport_Country_5_2=Single_Country_5_2[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_2=Single_Country_5_2[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_2=Single_Country_5_2[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_2=Single_Country_5_2[Variables.databaseLabels().Street]
        Dest_City_5_2=Single_Country_5_2[Variables.databaseLabels().CityorTown]
        Dest_State_5_2=Single_Country_5_2[Variables.databaseLabels().State]
        ExtDetails_5_2=Single_Country_5_2[Variables.databaseLabels().ExtDetails]         

        #THIRD
        
        Single_Country_5_3=CountryFive[Variables.databaseLabels().CountryThree]
        Duration_5_3=Single_Country_5_3[Variables.databaseLabels().Duration]
        Airport_Country_5_3=Single_Country_5_3[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_3=Single_Country_5_3[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_3=Single_Country_5_3[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_3=Single_Country_5_3[Variables.databaseLabels().Street]
        Dest_City_5_3=Single_Country_5_3[Variables.databaseLabels().CityorTown]
        Dest_State_5_3=Single_Country_5_3[Variables.databaseLabels().State]
        ExtDetails_5_3=Single_Country_5_3[Variables.databaseLabels().ExtDetails]
            #FOURTH
        
        Single_Country_5_4=CountryFive[Variables.databaseLabels().CountryFour]
        Duration_5_4=Single_Country_5_4[Variables.databaseLabels().Duration]
        Airport_Country_5_4=Single_Country_5_4[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_4=Single_Country_5_4[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_4=Single_Country_5_4[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_4=Single_Country_5_4[Variables.databaseLabels().Street]
        Dest_City_5_4=Single_Country_5_4[Variables.databaseLabels().CityorTown]
        Dest_State_5_4=Single_Country_5_4[Variables.databaseLabels().State]
        ExtDetails_5_4=Single_Country_5_4[Variables.databaseLabels().ExtDetails]
            #FIFTH
        
        Single_Country_5_5=CountryFive[Variables.databaseLabels().CountryFive]
        Duration_5_5=Single_Country_5_5[Variables.databaseLabels().Duration]
        Airport_Country_5_5=Single_Country_5_5[Variables.databaseLabels().AirportCountry]
        Emergency_Quick_5_5=Single_Country_5_5[Variables.databaseLabels().QuickDetails]
        ShortEx_Country_5_5=Single_Country_5_5[Variables.databaseLabels().ShortExCountry]
        Dest_Street_5_5=Single_Country_5_5[Variables.databaseLabels().Street]
        Dest_City_5_5=Single_Country_5_5[Variables.databaseLabels().CityorTown]
        Dest_State_5_5=Single_Country_5_5[Variables.databaseLabels().State]
        ExtDetails_5_5=Single_Country_5_5[Variables.databaseLabels().ExtDetails]
        
        #Add to list
        var_list.extend([Duration_5_1,Airport_Country_5_1,Emergency_Quick_5_1,ShortEx_Country_5_1,Dest_Street_5_1,Dest_City_5_1,Dest_State_5_1,ExtDetails_5_1])
        var_list.extend([Duration_5_2,Airport_Country_5_2,Emergency_Quick_5_2,ShortEx_Country_5_2,Dest_Street_5_2,Dest_City_5_2,Dest_State_5_2,ExtDetails_5_2])
        var_list.extend([Duration_5_3,Airport_Country_5_3,Emergency_Quick_5_3,ShortEx_Country_5_3,Dest_Street_5_3,Dest_City_5_3,Dest_State_5_3,ExtDetails_5_3])
        var_list.extend([Duration_5_4,Airport_Country_5_4,Emergency_Quick_5_4,ShortEx_Country_5_4,Dest_Street_5_4,Dest_City_5_4,Dest_State_5_4,ExtDetails_5_4])
        var_list.extend([Duration_5_5,Airport_Country_5_5,Emergency_Quick_5_5,ShortEx_Country_5_5,Dest_Street_5_5,Dest_City_5_5,Dest_State_5_5,ExtDetails_5_5])
        
        Date_Added= str(result[Variables.databaseLabels().DateRegistered])
        Last_Updated = str(result[Variables.databaseLabels().LastUpdated])  

        #Add to list    
        var_list.extend([Date_Added,Last_Updated])        

        return var_list



        
        