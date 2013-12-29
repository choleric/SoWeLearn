from django.contrib import messages
from django.shortcuts import redirect

from allauth.utils import email_address_exists
from allauth.account import app_settings as account_settings
from allauth.account.utils import user_email
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from ... import settings
from ..response import JsonResponse
from .. import code

class SocialAccountAdapterLearn(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # If email is specified, check for duplicate and if so, no auto signup.
        auto_signup = app_settings.AUTO_SIGNUP
        if auto_signup:
            email = user_email(sociallogin.account.user)
            # Let's check if auto_signup is really possible...
            if email:
                if account_settings.UNIQUE_EMAIL:
                    if email_address_exists(email):
                        #Todo: modify request.
                        requenst = request
                        auto_signup = False
            elif app_settings.EMAIL_REQUIRED:
                # Nope, email is required and we don't have it yet...
                auto_signup = False
        return auto_signup