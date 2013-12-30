from django import forms

from models import UserPersonalProfile
from mylearn.apps import errcode

class UserQuoteForm(forms.Form):
    aboutUserQuote= forms.CharField(max_length=10)

    #def __unicode__(self):

class WorkAndEducationCredentialForm(forms.Form):
    userEducationCredential = forms.CharField()
    userWorkCredential = forms.CharField()

class LocationAndContactForm(forms.Form):
    userLocation = forms.CharField(required=False)
    userSkypeID = forms.CharField(required=False)

class TutorTuitionTopicsForm(forms.Form):
    tutorTuitionTopics = forms.CharField(required=False)  #should be chosen from predefined lists!

class TutorHourlyRateForm(forms.Form):
    tutorTuitionAverageHourlyRateMiddleSchool = forms.DecimalField(decimal_places=2,required=False)
    tutorTuitionAverageHourlyRateHighSchool = forms.DecimalField(decimal_places=2,required=False)
    tutorTuitionAverageHourlyRateCollege = forms.DecimalField(decimal_places=2,required=False)

class UserProfileForm(forms.ModelForm):
    userID = forms.IntegerField(
            required = False,
            error_messages={
        "required" : errcode.profileUserIDInvalid,
        "invalid" : errcode.profileUserIDInvalid,
        })
    skypeID = forms.CharField(
            required=False,
            error_messages={
        "invalid" : errcode.profileSkypeIDInvalid,
        })

    class Meta :
        model = UserPersonalProfile
        fields = ['skypeID']
