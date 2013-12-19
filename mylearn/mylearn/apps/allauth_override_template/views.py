from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.http import HttpResponse
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin, LoginView,_ajax_response
from ..response import JsonResponse
from .. import code
# Create your views here.

class SignupViewLearn(SignupView,AjaxCapableProcessFormViewMixin):
    def form_invalid(self, form):
        #return HttpResponse(dict(form.errors.items()))
        data = dict(form.errors.items())
        return JsonResponse(code.SignupFailure, data)

signup_learn = SignupViewLearn.as_view()

class SigninViewLearn(LoginView):
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            response = self.form_valid(form)
            return _ajax_response(self.request, response, form=form)
        else:
            response = self.form_invalid(form)
            #TODO json
            return HttpResponse(response.context_data['form'].errors.items()[0][1])

signin_learn = SigninViewLearn.as_view()
