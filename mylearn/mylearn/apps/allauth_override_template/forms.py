from django import forms

from allauth.account.forms import SignupForm
from mylearn.apps.user_profile.models import User

class SignupFormAdd(forms.Form):
    userFirstName=forms.CharField(max_length=30,)
    userLastName=forms.CharField(max_length=30,)

    def save(self, user):
        pass



class SignupFormLearn(SignupForm):
    """
    This form is an adaptation of :class:`SignupForm` in order to include the two extra fields
    used in signing in: last name and first name
    """
    userFirstName=forms.CharField(max_length=30,)
    userLastName=forms.CharField(max_length=30,)

    def save(self):
        """ Save first and last name before falling back to parent signup form """
        userEmail = self.cleaned_data['email']
        userFirstName, userLastName = (self.cleaned_data['userFirstName'],self.cleaned_data['userLastName'],)
        User.user_signup(userEmail, userFirstName, userLastName)
        return super(SignupFormLearn, self).save()