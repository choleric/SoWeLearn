from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import View
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin
# Create your views here.

class SignupViewLearn(AjaxCapableProcessFormViewMixin,SignupView):
    dispatch= View.dispatch


signup_learn = SignupViewLearn.as_view()