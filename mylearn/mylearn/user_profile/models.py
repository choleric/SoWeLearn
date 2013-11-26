from django.db import models
import pymongo

# Create your models here.

class User():
    def get_user(self, user_email):
        client = pymongo.MongoClient("localhost", 27017)
        mydb = client.user
        user_info = mydb.user_profile.find_one({'user_email': user_email})
        client.close()
        return user_info

    def add_user(self, **kwargs):
        client = pymongo.MongoClient("localhost", 27017)
        mydb = client.user
        mydb.user_profile.save(kwargs)
        client.close()
        return True


