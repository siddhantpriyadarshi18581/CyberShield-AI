from pymongo import MongoClient

def save_to_mongodb(result_dict):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['phishing_database']
    collection = db['phishing_urls']

    # Insert the result_dict into the collection
    collection.insert_one(result_dict)
    client.close()