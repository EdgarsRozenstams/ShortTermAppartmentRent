import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

def Connect():
	client = MongoClient('mongodb+srv://C00195570:j264du@3rdyearproject-sams9.mongodb.net/admin')
	#client = MongoClient()	#loclhost
	db = client.TestDB
	return db

def getUserDetails(email):
    db = Connect()
    users = db.TestColl
    #userData = users.find_one({"email": email},{'_id': 0}) #strips the _id as the obj type has problems ,{'_id': 0}

    for itm in users.find({"email":email},{'_id': 0}):
        return itm

def getUserId(email):
    db = Connect()
    users = db.TestColl
    print('getId')

    for itm in users.find({"email":email}):
        userid = itm.get('_id')
        #return userid
        return str(userid)

def getUserProps(user):
	db = Connect()
	collection = db.TestProperties
	properties = list(collection.find({"User": user},{'_id': 0}))	
	return properties

def getAllProps():
	db = Connect()
	collection = db.TestProperties
	properties = list(collection.find())
	return properties
	
def registerUser(post):
	db = Connect()
	collection = db.TestColl
	collection.insert_one(post)
	
def registerProperty(post):
	db = Connect()
	collection = db.TestProperties
	collection.insert_one(post)
	
def updateUser(post, userId):
	db = Connect()
	collection = db.TestColl
	
	mycollection.update_one({'_id':userId}, {"$set": post}, upsert=False)

def Search(location,minCost,maxCost,minBed,maxBed):
	
	if minCost == "":
		minCost = 0
	else:
		minCost = int(minCost)

	if maxCost == "":
		maxCost = 99999
	else:
		maxCost = int(maxCost)

	if minBed == "":
		minBed = 0
	else:
		minBed = int(minBed)

	if maxBed == "":
		maxBed = 99999
	else:
		maxBed = int(maxBed)
		
	db = Connect()
	searchResults = list(db.TestProperties.find({ "county":location, "cost":{"$gte": minCost, "$lte": maxCost} , "Bedrooms":{"$gte": minBed, "$lte": maxBed} },{'_id':0}).sort("cost")) #session['searchProps'] = db.TestProperties.find( "Addres":location)
	return searchResults