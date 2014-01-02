from django.views.generic.edit import BaseFormView
from django.views.generic import View
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.http import HttpResponseRedirect
from mylearn.apps import JsonResponse
from mylearn.apps import errcode

"""
any class-based view can inherit this class to get login support
"""
class LoginRequriedView(View):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request, 'user') or isinstance(request.user, AnonymousUser):
            return HttpResponseRedirect(settings.LOGIN_URL)
        # login validate and redirect to settings.LOGIN_URL
        return super(LoginRequriedView, self).dispatch(request, *args, **kwargs)


class LoginFreeView(View):
    pass


class UserRelatedFormView(LoginRequriedView, BaseFormView) :
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        data = form._meta.model.objects.get(userID = request.user.pk)
        return JsonResponse(errcode.SUCCESS, self.format_model(form, data))

    def format_model(self, form, data) :
        if not form._meta.fields :
            return data

        formatedData = {}
        for field in form._meta.fields :
            formatedData[field] = getattr(data, field, "default invalid value from baseviews")
        return formatedData
