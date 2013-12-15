from django import forms

class UserQuoteForm(forms.Form):
    user_quote= forms.CharField(max_length=5)

    def clean_user_quote(self):
        user_quote = self.cleaned_data['user_quote']
        if len(user_quote) > 5:
            raise forms.ValidationError('too long quote')
        return user_quote

class WorkAndEducationCredentialForm(forms.Form):
    userEducationCredential = forms.CharField(required=False)
    userWorkCredential = forms.CharField(required=False)

class LocationAndContactForm(forms.Form):
    userLocation = forms.CharField(required=False)
    userSkypeID = forms.CharField(required=False)

class TutorTuitionTopicsForm(forms.Form):
    tutorTuitionTopics = forms.CharField(required=False)  #should be chosen from predefined lists!

class TutorHourlyRateForm(forms.Form):
    tutorTuitionAverageHourlyRateMiddleSchool = forms.DecimalField(decimal_places=2,required=False)
    tutorTuitionAverageHourlyRateHighSchool = forms.DecimalField(decimal_places=2,required=False)
    tutorTuitionAverageHourlyRateCollege = forms.DecimalField(decimal_places=2,required=False)