from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.http import HttpResponse
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin
from ..response import JsonResponse
from .. import code
# Create your views here.

class SignupViewLearn(SignupView,AjaxCapableProcessFormViewMixin):
    def form_invalid(self, form):
        #return HttpResponse(dict(form.errors.items()))
        rawdata = dict(form.errors.items())
        for k,v in rawdata:

        return JsonResponse(code.SignupFailure, data)

signup_learn = SignupViewLearn.as_view()
