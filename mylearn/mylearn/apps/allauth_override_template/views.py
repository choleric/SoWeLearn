from django.shortcuts import render
from allauth.account.views import SignupView
from forms import SignupFormLearn
# Create your views here.

class SignupViewLearn(SignupView):
    form_class = SignupFormLearn

signup_learn = SignupViewLearn.as_view() #Instantiate the class, this is the view function in URLConf