from django.views.generic.edit import BaseFormView
from mylearn.apps import JsonResponse
from mylearn.apps import errcode

class UserRelatedFormView(BaseFormView) :
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
