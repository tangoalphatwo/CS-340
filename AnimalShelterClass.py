from pymongo import MongoClient
from bson.objectid import ObjectId
import json

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections. 
        self.client = MongoClient('mongodb://%s:%s@localhost:38426/AAC' % (username, password))
        self.database = self.client['AAC']
        
# Method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            # Insert the data, and return true if successful.
            self.database.animals.insert_one(data)  # data should be dictionary   
            return True
        else:
            # Data was invalid.
            raise Exception("Nothing to save, because data parameter is empty")
            return False

# Method to implement the R in CRUD.
    def read(self, data):
        if data is not None:
            # Return all records that match.
            return list(self.database.animals.find(data, {'_id':False}))
        else:
            # Data was invalid.
            raise Exception("Nothing to search, because data parameter is empty")
            return False

# Method to implement the U in CRUD.
    def update(self, search, data):
        if data is not None:
            # Update the chosen data in the animal database.
            updateRecord = self.database.animals.update_many(search, data)
            oldFor = json.dumps(search) # json.dumps converts library to string for outputting readability
            newFor = json.dumps(data)
            pStr = 'The data ' + oldFor + ' was successfully changed to ' + newFor
            return pStr
        else:
            # Data is invalid.
            raise Exception("Nothing to update, because data parameter is empty")
            return False
    
# Method to implement the D in CRUD.
    def delete(self, data):
        if data is not None:
            # Delete the specified data in the animal database.
            self.database.animals.delete_many(data)
            delDataFor = json.dumps(data)
            pStr = 'The data ' + delDataFor + ' was successfully deleted.'
            return pStr
        else:
            # Data is invalid
            raise Exception("Nothing to delete, because data parameter is empty")
            return False

#title = __name__
#print(title)