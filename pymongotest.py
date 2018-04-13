from dbconnect import Connect

client = Connect()

print(client.database_names())
#print(db.collection_names())

db = client.TestDB

print(db.collection_names())


#db = Connect()
#collection = db.TestCollection

#post = ({"Sucess":True})

#collection.insert_one(post)


#post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"]}

#posts = db.posts
#post_id = posts.insert_one(post).inserted_id


