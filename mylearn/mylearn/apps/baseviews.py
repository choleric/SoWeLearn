from django.views.generic.edit import BaseFormView
from mylearn.apps import JsonResponse
from mylearn.apps import errcode

class UserRelatedFormView(BaseFormView) :
    def get_form_kwargs(self):
        postData = self.request.POST.copy()
        postData["userID"] = self.request.user.pk
        self.request.POST = postData
        return super(UserRelatedFormView, self).get_form_kwargs()

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ins = form._meta.model.objects.get(userID = request.user.pk)
        return JsonResponse(errcode.SUCCESS, ins)


