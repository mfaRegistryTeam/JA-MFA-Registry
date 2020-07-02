# Author : Shane Okukenu

from Keywords import Variables
from bson import ObjectId
from flask import Flask,request,session
import bcrypt,datetime,json,re
from _datetime import timedelta
from collections import Counter
from Models import Models
from Methods import EmailVerification
import threading




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
        threading.Timer(60.0, self.CleanUserList).start()        
        model=Models.MyMongoDB()  
        cur_date=datetime.datetime.now()
        fifteen_minutes_ago=cur_date-timedelta(minutes=5)   

        a=model.db.users.find().count()         
        if a >0 :
            model.db.users.remove({'Added':{'$lte':fifteen_minutes_ago},'Status':False})


    def AutoEmail(self):
        model=Models.MyMongoDB()
        cur_date=datetime.datetime.now()
        six_months_ago=cur_date-timedelta(weeks=26)
        four_days_ago=cur_date-timedelta(days=4)

      
        a=model.db.diasporaList.find({'Date-Last-Updated':{'$lte':six_months_ago},'Emailed_last':{'$lte':cur_date-four_days_ago}}).limit(5000)
        result=list(a)
        email_list=[]
        for x in result:
            b=x[Variables.databaseLabels().EmailAddress]
            email_list.append(b)

        for thisemail in email_list:             
            EmailVerification.EmailReminder(thisemail)
            model.db.diasporaList.update_one(
                    {Variables.databaseLabels().EmailAddress : thisemail},
                    {'$set':{'Emailed_last':cur_date}})


            
            
            


    def Indexing(self):
        model=Models.MyMongoDB()        
        #1
        model.db.diasporaList.createIndex( { 'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "LastNameCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #2
        model.db.diasporaList.createIndex( { 'Gender': 1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "GenderNamesCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #3
        model.db.diasporaList.createIndex( { 'Nationality':1 ,'Gender': 1,'Name.Last': 1, 'Name.First' : 1},
                                        { 'name': "NatGenderNamesNatCompIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #4       
        model.db.diasporaList.createIndex( { 'Classification': 1,'Nationality': 1, 'Name.Last' : 1,'Name.First':1 },
                                        { 'name': "ClassifactionCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #5                               
        model.db.diasporaList.createIndex( { 'Address.Country':1,'Classification': 1,'Nationality': 1,'Gender':1,'Name.Last': 1,
                                          'Name.First' : 1 },
                                        { 'name': "CountryAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        
        
        #6
        model.db.diasporaList.createIndex( { 'Occupation.Type':1,'Address.Country':1,'Classification': 1,'Nationality': 1,
                                          'Gender':1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "OccupationAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )      
        #7
        model.db.diasporaList.createIndex( { 'Occupation.Job-Class':1,'Occupation.Type':1,'Address.Country':1,'Classification': 1,'Nationality': 1,
                                          'Gender':1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "OccupationJobsAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )    
        #8
        model.db.diasporaList.createIndex( { 'Address-in-Barbados.Parish':1,'Destination-Address.Country':1,
                                          'Purpose-of-Travel':1,'Classification': 1,'Nationality': 1,
                                          'Gender':1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "AddressAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #9
        model.db.diasporaList.createIndex( { 'Destination-Address.Country':1,'Address-in-Barbados.Parish':1,'Purpose-of-Travel':1,
                                          'Classification': 1,'Nationality': 1,'Gender':1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "CitizenAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #10                          
        model.db.diasporaList.createIndex( { 'Purpose-of-Travel':1,'Destination-Address.Country':1,'Address-in-Barbados.Parish':1,
                                          'Classification': 1,'Nationality': 1,'Gender':1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "DestinationAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #11
        model.db.diasporaList.createIndex( { 'Residence-Abroad-Address.Country':1,'Areas-of-Interest':1,'Classification': 1,
                                          'Nationality': 1,'Gender':1,'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "ResidentAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )
        #12
        model.db.diasporaList.createIndex( { 'Areas-of-Interest-fr':1,'Classification': 1,'Nationality': 1,'Gender':1,
                                          'Name.Last': 1, 'Name.First' : 1 },
                                        { 'name': "AOIAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )      

        #13
        model.db.diasporaList.createIndex( { 'Knowledge-of-BB':1,'Classification': 1,'Nationality': 1,'Gender':1,'Name.Last': 1,
                                          'Name.First' : 1 },
                                        { 'name': "KBBAllCompoundIndex"},
                                        { 'collation': { 'locale': 'en', 'strength': 2 }},
                                        { 'background': True} )  

    
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
        dob_start_1=datetime.datetime(int(dob_start[0:4] ),int(dob_start[5:7]),int(dob_start[8:10]))

        dob_end=request.form.get('DOB_end')
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
        exp_dep_st=datetime.datetime(int(dep_date_start[0:4] ),int(dep_date_start[5:7]),int(dep_date_start[8:10]))

        dep_date_end=request.form.get('dep_date_end')
        exp_dep_end=datetime.datetime(int(dep_date_end[0:4] ),int(dep_date_end[5:7]),int(dep_date_end[8:10]))



        ret_date_start=request.form.get('ret_date_start')
        exp_ret_st=datetime.datetime(int(ret_date_start[0:4] ),int(ret_date_start[5:7]),int(ret_date_start[8:10]))

        ret_date_end=request.form.get('ret_date_end')
        exp_ret_end=datetime.datetime(int(ret_date_end[0:4] ),int(ret_date_end[5:7]),int(ret_date_end[8:10]))
        

            #resident overseas
        res_interests=request.form.get('interest_search')
        res_country=request.form.get('res_country_search')

            #friends barbados
        fr_interests=request.form.get('interestsfr_search')
        fr_country=request.form.get('countryfr_search')
        KnowledgeofBB=request.form.get('KBB_search')

        var_list=[lastname,firstname,gender,nationality,classification,country,occupation_type,job_class,
        address_parish,dest_country,purpose,res_country,fr_interests,KnowledgeofBB]

        key_list=[{'Name.Last':lastname},{'Name.First':firstname},{Variables.databaseLabels().Gender:gender},
        {Variables.databaseLabels().Nationality:nationality},{Variables.databaseLabels().Classification:classification},
        {'Address.Country':country},{'Occupation.Type':occupation_type},{'Occupation.Job-Class' : job_class},{'Address-in-Barbados.Parish':address_parish},
        {'Destination-Address.Country':dest_country},{Variables.databaseLabels().PurposeofTravel:purpose},
        {'Residence-Abroad-Address.Country':res_country},{Variables.databaseLabels().AreasofInterestFr:{'$all':fr_interests}},
        {Variables.databaseLabels().KnowledgeofBB:{'$all':KnowledgeofBB}}]

        query = []
        for i in var_list:
            if i is not None:
                query.append(key_list[i])

        if middlename is not None:
            query.append({'Name.Middle':middlename})

        if emailaddress is not None:
            query.append({'Email-Address':emailaddress})

        if dob_start_1 and dob_end_1 is not None:
            query.append({Variables.databaseLabels().DOB :{'$gte':dob_start_1,'$lte':dob_end_1}})

        if exp_dep_st and exp_dep_end is not None:
            query.append({Variables.databaseLabels().DepDate:{'$gte':exp_dep_st,'$lte':exp_dep_end}})

        if exp_ret_st and exp_ret_end is not None:
            query.append({Variables.databaseLabels().ReturnDate:{'$gte':exp_ret_st,'$lte':exp_ret_end}})

        if res_interests is not None:
            query.append({Variables.databaseLabels().AreasofInterest:{'$all':res_interests}})

        if study_field is not None:
            query.append({Variables.databaseLabels().FieldofStudy:study_field})

        if study_level is not None:
            query.append({Variables.databaseLabels().StudyLevel:study_level})

        if passportcountry is not None:
            query.append({Variables.databaseLabels().IssuedPassportCountry:passportcountry})

        

            
        # Each result represents a single person that is return from the query.
        # If 1 person is returned then as it stands the history of updates available for that person can be seen
        # using histlist from GetHistory() ordered by most recent first. Can see the logic in

        # If you trace and follow along I know you can see the logic

        result = list(model.db.diasporaList.find({'$and': query}).collation({'locale': "en", 'strength': 2}))

        histlist=AdminQuery.GetHistory(array_found=result)
        
        return (result, histlist)        

    

#Static Queries
    def DatabaseTotal(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a = model.db.diasporaList.count()
        return a
    
    def DatabaseFriendsBB(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a =model.db.diasporaList.find({'Classification':'Friend'}).collation({'locale': "en", 'strength': 2}).count()            
        return a

    def DatabaseCitizensTravellingBB(self):        
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a = model.db.diasporaList.find({'Classification':'CitizenTO'}).collation({'locale': "en", 'strength': 2}).count()            
        return a

    def DatabaseOverseasResidentBB(self):
       
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a =model.db.diasporaList.find({'Classification':'ResidentO'}).collation({'locale': "en", 'strength': 2}).count()            
        return a
    
    def NAmericaResidentBB(self):
        if 'adminuser' in session:           
            model=Models.MyMongoDB()
            a=model.db.diasporaList.find({'Classification':'ResidentO','Resident-Abroad-Address.Location.0':{'$gte':7,'$lte':84},
            'Resident-Abroad-Address.Location.1':{'$gte':-180,'$lte':-20}}).collation({'locale': "en", 'strength': 2}).count() 
                                  
        return a

    def EUResidentBB(self):
        if 'adminuser' in session:           
            model=Models.MyMongoDB()
            a=model.db.diasporaList.find({'Classification':'ResidentO','Resident-Abroad-Address.Location.0':{'$gte':35,'$lte':72},
            'Resident-Abroad-Address.Location.1':{'$gte':-25,'$lte':65}}).collation({'locale': "en", 'strength': 2}).count()                                   
        return a
    
    def AsiaResidentBB(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a=model.db.diasporaList.find({'Classification':'ResidentO','Resident-Abroad-Address.Location.0':{'$gte':-10,'$lte':80},
            'Resident-Abroad-Address.Location.1':{'$gte':-170,'$lte':25}}).collation({'locale': "en", 'strength': 2}).count() 
                                              
        return a
    
    def AfricaResidentBB(self):       
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a=model.db.diasporaList.find({'Classification':'ResidentO','Resident-Abroad-Address.Location.0':{'$gte':-37,'$lte':35},
            'Resident-Abroad-Address.Location.1':{'$gte':-17,'$lte':50}}).collation({'locale': "en", 'strength': 2}).count() 

        return a

    def SAmericaResidentBB(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a=model.db.diasporaList.find({'Classification':'ResidentO','Residence-Abroad-Address.Location.0':{'$gte':-55,'$lte':12},
            'Resident-Abroad-Address.Location.1':{'$gte':-81,'$lte':-35}}).collation({'locale': "en", 'strength': 2}).count() 
        return a

    #Takes string type of country name that matches the exact pattern in the html dropdown
    def CountryMarker(self,name):
        name = self.name
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            a=model.db.diasporaList.find({'Classification':'ResidentO','Residence-Abroad-Address.country_ro':name}).collation({'locale': "en", 'strength': 2}).count()
        return a

    #Returns documents updated by the user in the past week
    def WeeklyUpdated(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            cur_date=datetime.datetime.now()
            last_week=cur_date-timedelta(weeks=1)
            a=model.db.diasporaList.find({'Date-Last-Updated':{'$gte':last_week,'$lte':cur_date}}).sort({'Date-Last-Updated':-1}).limit(50)
        return a

    #Returns documents added ie registrations in the past week
    def WeeklyAdded(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            cur_date=datetime.datetime.now()
            last_week=cur_date-timedelta(weeks=1)
            a=model.db.diasporaList.find({'Date-Added':{'$gte':last_week,'$lte':cur_date}}).sort({'Date-Added':-1}).limit(50)
        return a

    #returns Top 4 interests of Residents overseas from the database info
    def InterestsCount(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            edu_count=model.db.diasporaList.find({'Areas-of-Interest':'Education'}).count()
            sprt_count=model.db.diasporaList.find({'Areas-of-Interest':'Sports'}).count()
            inv_count=model.db.diasporaList.find({'Areas-of-Interest':'Investment'}).count()
            med_count=model.db.diasporaList.find({'Areas-of-Interest':'Medical'}).count()
            vol_count=model.db.diasporaList.find({'Areas-of-Interest':'Volunteerism'}).count()
            re_count=model.db.diasporaList.find({'Areas-of-Interest':'Real-Estate'}).count()
            cult_count=model.db.diasporaList.find({'Areas-of-Interest':'Culture'}).count()
            gen_count=model.db.diasporaList.find({'Areas-of-Interest':'Geneology'}).count()
            oth_count=model.db.diasporaList.find({'Areas-of-Interest':'Other'}).count()

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
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            edu_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Education'}).count()
            sprt_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Sports'}).count()
            inv_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Investment'}).count()
            med_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Medical'}).count()
            vol_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Volunteerism'}).count()
            re_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Real-Estate'}).count()
            cult_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Culture'}).count()
            gen_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Geneology'}).count()
            oth_count=model.db.diasporaList.find({'Areas-of-Interest-fr':'Other'}).count()

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
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            adv_count=model.db.diasporaList.find({'Occupation.Job-Class':'Advertising,Promotions,Marketing'}).count()
            AE_count=model.db.diasporaList.find({'Occupation.Job-Class':'Architecture & Engineering'}).count()
            busin_count=model.db.diasporaList.find({'Occupation.Job-Class':'Business'}).count()
            edu_count=model.db.diasporaList.find({'Occupation.Job-Class':'Education'}).count()
            fin_count=model.db.diasporaList.find({'Occupation.Job-Class':'Finance'}).count()
            heal_count=model.db.diasporaList.find({'Occupation.Job-Class':'Healthcare'}).count()
            info_count=model.db.diasporaList.find({'Occupation.Job-Class':'Information Technology'}).count()
            math_count=model.db.diasporaList.find({'Occupation.Job-Class':'Mathematics'}).count()
            sci_count=model.db.diasporaList.find({'Occupation.Job-Class':'Science'}).count()
            soc_count=model.db.diasporaList.find({'Occupation.Job-Class':'Social Services'}).count()
            oth_count=model.db.diasporaList.find({'Occupation.Job-Class':'Other'}).count()

            job_dict={'Advertising,Promotions,Marketing':adv_count,'Architecture & Engineering':AE_count,'Business':busin_count,
            'Education':edu_count,'Finance':fin_count,'Healthcare':heal_count,'Information Technology':info_count,
            'Mathematics':math_count,'Science':sci_count,'Scoial Services':soc_count,'Other':oth_count}
            k = Counter(job_dict) 
            job_list=[]
            
            # Finding 4 highest values 
            high = k.most_common(4)           
            for i in high:
                job_list.append((i[0],i[1])) 

        return job_list 


# returns Top 4 study areas from the database info
    def StudyAreaCount(self):
        if 'adminuser' in session:
            model=Models.MyMongoDB()
            hum_count=model.db.diasporaList.find({'Occupation.Field-of-Study':'Humanities and Social Sciences'}).count()
            NS_count=model.db.diasporaList.find({'Occupation.Field-of-Study':'Natural Sciences'}).count()
            FS_count=model.db.diasporaList.find({'Occupation.Field-of-Study':'Formal Sciences'}).count()
            PAS_count=model.db.diasporaList.find({'Occupation.Field-of-Study':'Professions and Applied Sciences'}).count()
            oth_count=model.db.diasporaList.find({'Occupation.Field-of-Study':'Other'}).count()

            area_count={'Humanities and Social Sciences':hum_count,'Natural Sciences':NS_count,'Formal Sciences':FS_count,
            'Professions and Applied Sciences':PAS_count,'Other':oth_count}
            k = Counter(area_count) 
            area_list=[]
            
            # Finding 4 highest values 
            high = k.most_common(4)           
            for i in high:
                area_list.append((i[0],i[1])) 

        return area_list 


# ----------------Updating documents--------------------
# diasporaList.update({
#     'Author': 'Shane Okukenu'
#     }, {
#         '$set':{
#             'Author':'Shane Okukenu Updated'
#             }

#     },multi=False )
# ---------------------------------------------------------


# --------Deleting documents---[Delete_one or Delete_many]---

# diasporaList.Delete_one({
#     'Author': 'Shane Langley'
# })
# print(diasporaList.find({'Author': 'Shane Langley'}))

# ---------------------------------------------------------

# ----------------Searching---------------------
# cursor=diasporaList.find({
#     'Author': 'Shane Orion',
#     'Price' : {
#         '$gt':5000
#         }
# })
# for m in (cursor):
#     pprint.pprint(m)

# ---------------Aggregation--------------------

# print(list(diasporaList.aggregate([
#     {
#         '$group':{
#             '_id': '$author',
#             'Rating': {
#                 '$avg':'$rating'
#             }
#         }
#     }
# ])))

