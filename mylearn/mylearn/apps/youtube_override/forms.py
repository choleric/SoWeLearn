from django import forms
from django_youtube.models import Video

from mylearn.apps import errcode

class YoutubeMetadataForm(forms.ModelForm):
    class Meta :
        model = Video
        #do we need access_control here?
        fields = ['title', 'description', 'keywords', 'access_control']

        err_maps = {'title': errcode.youtubeVideoTitleInvalid,
                    'description':  errcode.youtubeVideoDescriptionInvalid,
                    'keywords':  errcode.youtubeVideoKeywordsInvalid,
                    'access_control' :  errcode.youtubeVideoAccessInvalid}
