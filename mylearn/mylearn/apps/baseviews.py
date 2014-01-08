from django.views.generic.edit import BaseFormView
from django.views.generic import View
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.http import HttpResponseRedirect

from mongoengine import EmbeddedDocument
from mongoengine.fields import ListField

from mylearn.apps import JsonResponse
from mylearn.apps import errcode
from mylearn.apps.user_profile.models import UserPersonalProfile

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

    def from_object_to_dict(self, obj, include_fields = [], exclude_fields = []):
        '''
        This method returns all non-none values from db according to the defined fields constraint.
        "obj" is the model object containing the expected data
        fields defined should be the name of the fields that is not embedded document field.
        '''
        if include_fields!= []:
            self.fields = include_fields
        else:
            #all the fields in the object model, including embedded fields
            self.fields = self._get_all_field_name(obj)

        return self._get_non_empty_field(obj, self.fields, exclude_fields)

    def _get_non_empty_field(self, obj, include_fields, exclude_fields):
        ret = {}
        for field, typ in obj._fields.iteritems():
            # if the field is a ListField
            if isinstance(typ, ListField):
                list_field = []
                listData = getattr(obj, field)
                if listData != []:
                    for item in listData:
                        # If the item of the field is embedded document
                        if isinstance(item, EmbeddedDocument):
                            list_field.append(
                                self._get_non_empty_field(item, include_fields, exclude_fields))
                        else:
                            list_field.append(item)
                    ret[field] = list_field
            # if the field is not a list field
            else:
                if (field not in include_fields) or (field in exclude_fields):
                    continue

                else:
                    data = getattr(obj, field, "default invalid value from baseviews")
                    if data != None:
                        ret[field] = data
        return ret

    def _get_all_field_name(self,obj):
        # I think this is very inefficient!
        field_names = []
        for field, typ in obj._fields.iteritems():
            # if the field is a ListField
            if isinstance(typ, ListField):
                listData = getattr(obj, field)
                if listData != []:
                    if isinstance(listData[0], EmbeddedDocument):
                        list = self._get_all_field_name(listData[0])
                        for item in list:
                            field_names.append(item)
        for item in obj._fields_ordered:
            field_names.append(item)
        return field_names

    def pre_validation_for_list(self, request, max_length, obj, list_field = None):
        length_exceeded = False
        # Cheapest solution: the requested position exceed the max_length
        if 'position' in request.POST:
            position = int(request.POST['position'])
            if position > max_length:
                length_exceeded = True
                return length_exceeded

        # When position parameter is not available in request, get the list_field length in db
        # This is mostly likely a malicious request
        if list_field == None :
            for field, typ in obj._fields.iteritems():
                if isinstance(typ, ListField):
                    list_field = field
        length = len(getattr(obj, list_field))
        if length >= max_length:
            length_exceeded = True
            return length_exceeded

        try:
            # The position from request might be wrong
            if position > length:
                del request.POST['position']
        except NameError:
            pass
        return length_exceeded

