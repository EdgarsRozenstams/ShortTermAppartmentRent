from pymongo import MongoClient

def Connect():
	#client = MongoClient('mongodb+srv://C00195570:j264du@3rdyearproject-sams9.mongodb.net/admin')
	client = MongoClient()	
	db = client.TestDB
	return db

	
def registerUser(post):
	db = Connect()
	collection = db.TestColl
	collection.insert_one(post)
	
	
