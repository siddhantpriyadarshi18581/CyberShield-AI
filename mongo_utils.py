from pymongo import MongoClient

def put_to_mongodb(email_dict):

    client = MongoClient('mongodb://localhost:27017/')
    emails_db= client['emails_database']
    collection_2 = emails_db['lemmatizer_collection']

    collection_2.insert_one(email_dict)
    client.close()