from django import forms
from .models import TopicourseDiscussion

from mylearn.apps import errcode
from mylearn.apps.forms import convert_model_field_to_for_field

class TopicourseDiscussionForm(forms.ModelForm):
    formfield_callback = convert_model_field_to_for_field

    class Meta :
        model = TopicourseDiscussion
        fields = ['discussionTitle', 'discussionContent']