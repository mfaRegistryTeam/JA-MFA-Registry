# Author : Shane Okukenu

from Keywords import Variables
from bson import ObjectId
from flask import Flask,request
import bcrypt,datetime
from Models import Models


class SiteQuery:
    def __init__(self):
       pass

    
    
    def find_existing_user(self):
        model=Models.MyMongoDB()
        userList = model.db.users
        a = userList.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email')})
        #using username to find document for testing purposes
        return a

    def find_existing_user2(self):
        model=Models.MyMongoDB()
        userList = model.db.users
        a = userList.find_one({Variables.databaseLabels().EmailAddress:request.form.get('email')})
        #using username to find document for testing purposes
        return a

    def find_admin(self):
        model=Models.MyMongoDB()
        adminList = model.db.user_admin
        a = adminList.find_one({Variables.databaseLabels().Username: request.form.get('username'),
        Variables.databaseLabels().EmailAddress:request.form.get('email')})
        #using username and email to find document for testing purposes
        return a


class AdminQuery:
    def __init__(self):
        pass
    
    def FindDocument(self):
        firstname=request.form.get('firstname-search')
        middlename=request.form.get('middlename-search')
        lastname=request.form.get('lastname-search')
        bbid=request.form.get('BBID-search')
        email=request.form.get('email-search')
        phonenumber=request.form.get('phone-search')
        dob=request.form.get('dob-search')
        gender=request.form.get('gender-search')
        city_town=request.form.get('city-town-search')
        address=request.form.get('address-search')

        model=Models.MyMongoDB()
        diasporaList = model.db.diasporaList
        if firstname is not None:
            diasporaList.create_index([
                (Variables.databaseLabels.BarbadosID, 1)],
                unique=True,
                background=True
            
            )
      


    # db.collection.createIndex( { user: 1, title: 1, Bank: 1 }, {unique:true} )

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"  


# member={
#     'Author' : 'Shane Okukenu',
#     'Topic' : 'This is a Test',
#     'Price' :  96,
#     'Rating' : '5'
# }

# arr_members=[
# {
#     'Author' : 'Shane Orion',
#     'Topic' : 'This is a Test',
#     'Price' :  794196,
#     'Rating' : '5691'
# },
# {
#     'Author' : 'Shane Langley',
#     'Topic' : 'This is a Test',
#     'Price' :  85296,
#     'Rating' : '5461'
# },
# {
#     'Author' : 'Shawn Smith',
#     'Topic' : 'This is a Test',
#     'Price' :  9646,
#     'Rating' : '5854'
# },
# {
#     'Author' : 'Shane Oconnor',
#     'Topic' : 'This is a Test',
#     'Price' :  986,
#     'Rating' : '589'
# },
# ]

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

# ---------------Insertion---------------------------------

# result=diasporaList.insert_one(member)
# results=diasporaList.insert_many(arr_members)

# for ObjectId in results.inserted_ids:
#     print("Member Added. The member id is "+str( ObjectId) )


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

# --------------Indexing--------------------------------

# diasporaList.create_index(
#     [('Price', 1)],
#     unique=True)

# ------------------------------------------------------    
    