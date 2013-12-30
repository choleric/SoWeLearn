"""
auto route to mongo based on class
read config from settings.DBROUTER_APP_CONFIG and route db operation
"""
from django.conf import settings

DATABASES_APP_FILTER_KEY = "APPS"

class DBRouter(object) :
    def routeDBOperation(self, app_label) :
        for db, config in settings.DATABASES.iteritems() :
            if DATABASES_APP_FILTER_KEY not in config :
                continue
            if app_label in config[DATABASES_APP_FILTER_KEY] :
                return db
        return "default"

    def db_for_read(self, model, **hints):
        return self.routeDBOperation(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)
