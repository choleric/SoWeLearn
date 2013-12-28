import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.core import mail
from django.conf import settings
from django.contrib.sites.models import Site
from django.test import Client
from django.utils.timezone import now

from allauth.account.forms import SignupForm
from allauth.account.models import EmailConfirmation


from .forms import SignupFormAdd
from ..projtest import BaseTest
from ..projtest import BaseTestUtil
from .. import code

User = get_user_model()

# Create your tests here.
class UserAllAuthTestCase(BaseTest):
    def setUp(self):
        if 'allauth.socialaccount' in settings.INSTALLED_APPS:
                    # Otherwise ImproperlyConfigured exceptions may occur
                    from allauth.socialaccount.models import SocialApp
                    sa = SocialApp.objects.create(name='testfb',
                                                  provider='facebook')
                    sa.sites.add(Site.objects.get_current())