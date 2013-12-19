from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import View
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin
# Create your views here.

class SignupViewLearn(SignupView,AjaxCapableProcessFormViewMixin):
    def form_invalid(self, form):
        pass
        #return dict(form.errors.items())


signup_learn = SignupViewLearn.as_view()
