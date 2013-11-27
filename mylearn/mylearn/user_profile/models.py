from django.db import models
import pymongo
from mongoengine import *
#connect('user')

# Create your models here.

class userPersonalProfile(EmbeddedDocument):
    aboutUserQuote = StringField(max_length=120)
    userEducationCredentials = StringField(max_length=120)
    userWorkCredentials = StringField(max_length=120)
    userLocation = StringField(max_length=120)

class user(Document):
    user_email = StringField(max_length=120, required=True)
    user_name = StringField(max_length=50)
    userPersonalProfile=EmbeddedDocumentField(userPersonalProfile)

class UserOld():
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

