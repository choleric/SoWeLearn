from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import ensure_csrf_cookie

from allauth.account.adapter import get_adapter
from allauth.account.views import SignupView, AjaxCapableProcessFormViewMixin, LoginView, PasswordChangeView, \
    PasswordResetView, PasswordResetFromKeyView, \
    LogoutView, ConfirmEmailView

from ... import settings
from ..response import JsonResponse
from mylearn.apps import errcode
# Create your views here.


class SignupViewLearn(SignupView,AjaxCapableProcessFormViewMixin):

    def form_invalid(self, form):
        #return HttpResponse(dict(form.errors.items()))
        data = dict(form.errors.items())
        if "email" in data and data["email"]==["A user is already registered with this e-mail address."]:
                return JsonResponse(errcode.UserExist)
        elif "__all__" in data and data["__all__"]==["You must type the same password each time."]:
            return JsonResponse(errcode.DifferentPassword)
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
            return JsonResponse(errcode.SignupFailure, errorData)

signup_learn = ensure_csrf_cookie(SignupViewLearn.as_view())

class ConfirmEmailViewLearn(ConfirmEmailView):

    def get(self, *args, **kwargs):
        try:
            self.object = self.get_object()
            if settings.ACCOUNT_CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return JsonResponse(errcode.InvalidConfirmationEmail)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        get_adapter().add_message(self.request,
                                  messages.SUCCESS,
                                  'account/messages/email_confirmed.txt',
                                  {'email': confirmation.email_address.email})
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)

confirm_email_learn = ensure_csrf_cookie(ConfirmEmailViewLearn.as_view())


class SigninViewLearn(LoginView):
    def form_invalid(self, form):
        data = dict(form.errors.items())
        #
        if '__all__' in data or len(data) < 1:
            return JsonResponse(errcode.SigninFailure)
        else:
            errorData = []
            # don't care the detail, it's enough to treat all kinds of errors as SigninInvalidField?
            if 'login' in data:
                errorData.append(errcode.SigninFormField.index('login'))
            if 'password' in data:
                errorData.append(errcode.SigninFormField.index('password'))
            return JsonResponse(errcode.SigninInvalidField, errorData)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

signin_learn = ensure_csrf_cookie(SigninViewLearn.as_view())

class PasswordChangeViewLearn(PasswordChangeView):
    def form_invalid(self, form):
        data = dict(form.errors.items())
        if "oldpassword" in data and data["oldpassword"]==["Please type your current password."]:
            return JsonResponse(errcode.WrongOldPassword)
        elif "password2" in data and data["password2"]==["You must type the same password each time."]:
            return JsonResponse(errcode.DifferentPassword)
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
            return JsonResponse(errcode.ChangePasswordFailure, errorData)

password_change_learn = ensure_csrf_cookie(login_required(PasswordChangeViewLearn.as_view()))

class PasswordResetViewLearn(PasswordResetView):
    def form_invalid(self,form):
        data = dict(form.errors.items())
        if "email" in data and data["email"]==["The e-mail address is not assigned to any user account"]:
            return JsonResponse(errcode.EmailNotRegistered)
        else:
            return JsonResponse(errcode.ResetPasswordFailure)

password_reset_learn = ensure_csrf_cookie(PasswordResetViewLearn.as_view())

class PasswordResetFromKeyViewLearn(PasswordResetFromKeyView):
    def form_invalid(self,form):
        data = dict(form.errors.items())
        if "password2" in data and data["password2"]==["You must type the same password each time."]:
            return JsonResponse(errcode.DifferentPassword)
        else:
            return JsonResponse(errcode.ResetpasswordFromKeyCommonFailure)

    def _response_bad_token(self, request, uidb36, key, **kwargs):
        return JsonResponse(errcode.ResetPasswordFromKeyBadToken)

password_reset_from_key_learn = ensure_csrf_cookie(PasswordResetFromKeyViewLearn.as_view())


class SignOutView(LogoutView) :
    def logout(self):
        auth_logout(self.request)

signout_learn = SignOutView.as_view()
