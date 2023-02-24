from pymongo import MongoClient

# client = MongoClient(port=27017)
# DB = client['subscription-bot']
client = MongoClient("mongodb+srv://wongjapan:bHmTQzOWMMwbYWyj@cluster0.tdy1g8j.mongodb.net/?retryWrites=true&w=majority")
DB = client.test