from django.contrib import messages
from django.shortcuts import redirect

from allauth.utils import email_address_exists
from allauth.account import app_settings as account_settings
from allauth.account.utils import user_email
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from ... import settings
from ..response import JsonResponse
from mylearn.apps import errcode

class DuplicateEmail(Exception):
    pass

class ImmediateHttpResponse(Exception):
    """
    This exception is used to interrupt the flow of processing to immediately
    return a custom HttpResponse.
    """
    def __init__(self, response):
        self.response = response

class SocialAccountAdapterLearn(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # If email is specified, check for duplicate and if so, no auto signup.
        auto_signup = app_settings.AUTO_SIGNUP
        if auto_signup:
            email = user_email(sociallogin.account.user)
            # Let's check if auto_signup is really possible...
            try:
                if email:
                    if account_settings.UNIQUE_EMAIL:
                        if email_address_exists(email):
                            state = email_address_exists(email)
                            auto_signup = False
                            raise DuplicateEmail
                elif app_settings.EMAIL_REQUIRED:
                    # Nope, email is required and we don't have it yet...
                    auto_signup = False
            except DuplicateEmail:
                return auto_signup
        return auto_signup