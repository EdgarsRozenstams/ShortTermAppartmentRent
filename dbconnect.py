from pymongo import MongoClient

def Connect():
	client = MongoClient('mongodb+srv://C00195570:j264du@3rdyearproject-sams9.mongodb.net/admin')
	#client = MongoClient()	#loclhost
	db = client.TestDB
	return db

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
	
def updateUser(post):
	db = Connect()
	collection = db.TestColl
	#mycollection.update_one({'_id':mongo_id}, {"$set": post}, upsert=False)

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
	searchResults = list(db.TestProperties.find({ "Addres":location, "cost":{"$gte": minCost, "$lte": maxCost} , "Bedrooms":{"$gte": minBed, "$lte": maxBed} },{'_id':0}).sort("cost")) #session['searchProps'] = db.TestProperties.find( "Addres":location)
	return searchResults