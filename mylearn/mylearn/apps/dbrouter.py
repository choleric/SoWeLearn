"""
auto route to mongo based on class
"""
from mongoengine.base import BaseDocument


# these values must be the values in settings.DATABASES
MONGODB_NAME = 'mongodb'
DEFAULT_NAME = 'default'


class DBRouter(object) :
    MONGODB_APP_SET = set(['site', 'user_profile'])

    def isAppUsingMongo(self, app_label) :
        return app_label in self.MONGODB_APP_SET

    def db_for_read(self, model, **hints):
        if self.isAppUsingMongo(model._meta.app_label) :
            return MONGODB_NAME
        return DEFAULT_NAME

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)
