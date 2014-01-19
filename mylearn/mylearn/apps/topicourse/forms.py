from django import forms
from django.core.exceptions import ValidationError

from .models import Topicourse, Topiquiz
from mylearn.apps import errcode
from mylearn.apps.forms import convert_model_field_to_for_field, AutoCreateUpdateModelForm


class TopicourseInfoForm(AutoCreateUpdateModelForm):
    formfield_callback = convert_model_field_to_for_field

    class Meta :
        model = Topicourse
        fields = ['topicourseTitle', 'topicourseContent',
                  'topicourseTag','topicourseType', 'topicourseLevel']


class TopiquizTorFForm(AutoCreateUpdateModelForm):
    formfield_callback = convert_model_field_to_for_field

    class Meta :
        model = Topiquiz
        fields = ['topicourseID','topiquizOption','topiquizAnswer','topiquizExplanation']

    def clean_topiquizAnswer(self):
        data = self.cleaned_data['topiquizAnswer']

        if data=="0" or data=="1":
            return data
        else:
            raise ValidationError(
                str(errcode.topiquizAnswerInvalid),
                code='invalid',
            )
class TopiquizSingleChoice(AutoCreateUpdateModelForm):
    formfield_callback = convert_model_field_to_for_field

    class Meta :
        model = Topiquiz
        fields = ['topicourseID','topiquizOption','topiquizAnswer','topiquizExplanation']

    def clean_topiquizAnswer(self):
        data = self.cleaned_data['topiquizAnswer']
        correctList = ['0','1','2','3','4']
        if data in correctList:
            return data
        else:
            raise ValidationError(
                str(errcode.topiquizAnswerInvalid),
                code='invalid',
            )

class TopiquizMultipleChoice(AutoCreateUpdateModelForm):
    formfield_callback = convert_model_field_to_for_field

    class Meta :
        model = Topiquiz
        fields = ['topicourseID','topiquizOption','topiquizAnswer','topiquizExplanation']

    def clean_topiquizAnswer(self):
        data = self.cleaned_data['topiquizAnswer']
        dataList=data.split(',')
        correctList = ['0','1','2','3','4']
        for item in dataList:
            if item not in correctList:
                raise ValidationError(
                    str(errcode.topiquizAnswerInvalid),
                    code='invalid',
                )
        return data
