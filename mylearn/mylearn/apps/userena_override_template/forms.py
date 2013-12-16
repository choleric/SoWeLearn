from django import forms

from userena import settings as userena_settings
from userena.models import UserenaSignup
from userena.utils import get_profile_model, get_user_model
from userena.forms import SignupForm

class SignupFormLearn(SignupFormOnlyEmail):
    """
    This form is an adaptation of :class:`SignupFormOnlyEmail` in order to include the two extra fields
    used in signing in: last name and first name

    """
    userFirstName=forms.CharField(max_length=30,)
    userLastName=forms.CharField(max_length=30,)

    def save(self):
        """ Save first and last name before falling back to parent signup form """
        userFirstName, userLastName = (self.cleaned_data['userFirstName'],self.cleaned_data['userLastName'],)
        #new_user = UserenaSignup.objects.
        return super(SignupFormLearn, self).save()