from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import FileField


class SignupFormAdd(forms.Form):
    userFirstName=forms.CharField(max_length=10)
    userLastName=forms.CharField(max_length=30)

    class Meta:
        model = get_user_model() # use this function for swapping user model

    def save(self, user):
        user.first_name = self.cleaned_data['userFirstName']
        user.last_name = self.cleaned_data['userLastName']
        user.save()