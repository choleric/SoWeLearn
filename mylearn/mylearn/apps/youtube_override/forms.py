from django import forms
from .models import VideoTopicourse

from mylearn.apps import errcode

class YoutubeMetadataForm(forms.ModelForm):
    class Meta :
        model = VideoTopicourse
        #do we need access_control here?
        fields = ['access_control']

        err_maps = {'access_control' :  errcode.youtubeVideoAccessInvalid}
