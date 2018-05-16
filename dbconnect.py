import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint


def Connect():
    client = MongoClient('mongodb+srv://C00195570'
                         ':j264du@3rdyearproject-sams9.mongodb.net/admin')
    db = client.Rent
    return db


# for login
def getUserDetails(email):
    db = Connect()
    users = db.Users
    for itm in users.find({"email": email}, {'_id': 0}):
        return itm


def getUserId(email):
    db = Connect()
    users = db.Users
    for itm in users.find({"email": email}):
        userid = itm.get('_id')
        return str(userid)


def getUserProps(user):
    db = Connect()
    collection = db.Props
    properties = list(collection.find({"User": user}, {'_id': 0}))
    return properties


def getAllProps():
    db = Connect()
    collection = db.Props
    properties = list(collection.find())
    return properties


# for property page
def getProperty(id):
    db = Connect()
    collection = db.Props
    prop = collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
    return prop


def getOwner(id):
    db = Connect()
    users = db.Users
    owner = users.find_one({"_id": ObjectId(id)}, {"_id": 0})
    return owner


def registerUser(post):
    db = Connect()
    collection = db.Users
    collection.insert_one(post)


def registerProperty(post):
    db = Connect()
    collection = db.Props
    collection.insert_one(post)


def updateUser(post, userId):
    db = Connect()
    collection = db.Users
    ConvertedId = ObjectId(userId)

    # check for existing emails, cant have 2 emails of the same type.

    collection.update_one({"_id": ConvertedId},
                          {"$set":
                          {"name": post.get("name"),
                           "surname": post.get("surname"),
                           "email": post.get("email"),
                           "phone": post.get("phone")}},
                          psert=False)


def Search(location, minCost, maxCost, minBed, maxBed):
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
    searchResults = list(db.Props.find({"county": location, "cost":
                                       {"$gte": minCost,
                                        "$lte": maxCost},
                                        "Bedrooms": {"$gte": minBed,
                                                     "$lte": maxBed}},
                                       {"_id": 0}).sort("cost"))
    return searchResults
