import re
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
        for k,v in data.iteritems():
            v=re.split('<li>',re.split('</li>',str(v))[0])[1]
            data[k]=v
        if "email" in data and data["email"]=="A user is already registered with this e-mail address.":
                return JsonResponse(code.UserExist)
        elif "__all__" in data and data["__all__"]=="You must type the same password each time.":
            return JsonResponse(code.DifferentPassword)
        else:
            dataList = []
            for k in data.keys():
                dataList.append(k)
            errorList = ["email","password1","password2","userFirstName","userLastName"]
            overlapList = list(set(dataList)&set(errorList))
            errorData=[]
            for i,v in enumerate(errorList):
                if v in overlapList:
                    errorData.append(i)
            return JsonResponse(code.SignupFailure, errorData)

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