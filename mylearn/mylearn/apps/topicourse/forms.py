from django import forms

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
        fields = ['topicourseID','topiquizAnswer','topiquizExplanation']