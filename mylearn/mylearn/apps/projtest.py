from django.test import TestCase
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.test.simple import DjangoTestSuiteRunner
from django.test.simple import dependency_ordered

class BaseTest(TestCase):
    pass
  
"""  
test utils
"""
class BaseTestUtil :  
    """  
    util for create user  
        params:  
            user: user model  
    """
    @staticmethod
    def create_user(**kwargs):  
        User = get_user_model()
        user = User.objects.create(**kwargs)

        pwdKey = 'password'
        if pwdKey in kwargs :
            user.set_password('password')
            user.save()

        return user

    @staticmethod
    def create_email(**kwargs) :
        return EmailAddress.objects.create(**kwargs)


"""
Test runner for project
not init db mongo because of the site framework hard code
1. default test runner will init every db in settings.DATABASES
2. site framework will save a Site object with id 1
3. mongodb Site object define an String Id and the test will break
"""
class ProjTestRunner(DjangoTestSuiteRunner) :

    def setup_databases(self, **kwargs):
        from django.db import connections, DEFAULT_DB_ALIAS

        # First pass -- work out which databases actually need to be created,
        # and which ones are test mirrors or duplicate entries in DATABASES
        mirrored_aliases = {}
        test_databases = {}
        dependencies = {}
        default_sig = connections[DEFAULT_DB_ALIAS].creation.test_db_signature()
        for alias in connections:
            connection = connections[alias]
            if connection.settings_dict['TEST_MIRROR']:
                # If the database is marked as a test mirror, save
                # the alias.
                mirrored_aliases[alias] = (
                    connection.settings_dict['TEST_MIRROR'])
            else:
                # Store a tuple with DB parameters that uniquely identify it.
                # If we have two aliases with the same values for that tuple,
                # we only need to create the test database once.
                item = test_databases.setdefault(
                    connection.creation.test_db_signature(),
                    (connection.settings_dict['NAME'], set())
                )
                item[1].add(alias)

                if 'TEST_DEPENDENCIES' in connection.settings_dict:
                    dependencies[alias] = (
                        connection.settings_dict['TEST_DEPENDENCIES'])
                else:
                    if alias != DEFAULT_DB_ALIAS and connection.creation.test_db_signature() != default_sig:
                        dependencies[alias] = connection.settings_dict.get(
                            'TEST_DEPENDENCIES', [DEFAULT_DB_ALIAS])

        # Second pass -- actually create the databases.
        old_names = []
        mirrors = []

        for signature, (db_name, aliases) in dependency_ordered(
            test_databases.items(), dependencies):
            test_db_name = None
            # Actually create the database for the first connection

            for alias in aliases:
                connection = connections[alias]
                # mongo db will not be init
                if "django_mongodb_engine" == connection.settings_dict['ENGINE'] :
                    continue
                if test_db_name is None:
                    test_db_name = connection.creation.create_test_db(
                            self.verbosity, autoclobber=not self.interactive)
                    destroy = True
                else:
                    connection.settings_dict['NAME'] = test_db_name
                    destroy = False
                old_names.append((connection, db_name, destroy))

        for alias, mirror_alias in mirrored_aliases.items():
            mirrors.append((alias, connections[alias].settings_dict['NAME']))
            connections[alias].settings_dict['NAME'] = (
                connections[mirror_alias].settings_dict['NAME'])

        return old_names, mirrors
