from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

from allauth.account import signals
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin, LoginView,_ajax_response, PasswordChangeView, \
    PasswordResetView, \
    LogoutView

from ..response import JsonResponse
from .. import code
# Create your views here.


class SignupViewLearn(SignupView,AjaxCapableProcessFormViewMixin):

    def form_invalid(self, form):
        #return HttpResponse(dict(form.errors.items()))
        data = dict(form.errors.items())
        if "email" in data and data["email"]==["A user is already registered with this e-mail address."]:
                return JsonResponse(code.UserExist)
        elif "__all__" in data and data["__all__"]==["You must type the same password each time."]:
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

class PasswordChangeViewLearn(PasswordChangeView):
    def form_invalid(self, form):
        data = dict(form.errors.items())
        if "oldpassword" in data and data["oldpassword"]==["Please type your current password."]:
            return JsonResponse(code.WrongOldPassword)
        elif "password2" in data and data["password2"]==["You must type the same password each time."]:
            return JsonResponse(code.DifferentPassword)
        else:
            dataList = []
            for k in data.keys():
                dataList.append(k)
            errorList = ["oldpassword","password1","password2"]
            overlapList = list(set(dataList)&set(errorList))
            errorData=[]
            for i,v in enumerate(errorList):
                if v in overlapList:
                    errorData.append(i)
            return JsonResponse(code.ChangePasswordFailure, errorData)

    def form_valid(self, form):
        form.save()
        signals.password_changed.send(sender=self.request.user.__class__,
                                      request=self.request,
                                      user=self.request.user)
        return JsonResponse(code.SUCCESS)

password_change_learn = login_required(PasswordChangeViewLearn.as_view())

class PasswordResetViewLearn(PasswordResetView):
    def form_invalid(self,form):
        data = dict(form.errors.items())
        if "email" in data and data["email"]==["The e-mail address is not assigned to any user account"]:
            return JsonResponse(code.EmailNotRegistered)
        else:
            return JsonResponse(code.ResetPasswordFailure)

password_reset_learn = PasswordResetViewLearn.as_view()


class SignOutView(LogoutView) :
    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            self.logout()
        redirectURL = self.get_redirect_url()
        return JsonResponse(code.SUCCESS, redirectURL, isHTMLEncode=False)


    def logout(self):
        auth_logout(self.request)

signout_learn = SignOutView.as_view()
