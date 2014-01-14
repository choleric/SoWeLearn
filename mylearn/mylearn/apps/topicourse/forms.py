from django import forms
from .models import Topicourse

from mylearn.apps import errcode
from mylearn.apps.forms import convert_model_field_to_for_field


class TopicourseInfoForm(forms.ModelForm):
    formfield_callback = convert_model_field_to_for_field

    class Meta :
        model = Topicourse
        fields = ['topicourseTitle', 'topicourseContent',
                  'topicourseTag','topicourseType', 'topicourseLevel']