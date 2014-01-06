from django import forms

from mongodbforms import DocumentForm, EmbeddedDocumentForm

from models import UserPersonalProfile, UserEducationCredential, UserWorkCredential

class UserProfileForm(DocumentForm) :

    class Meta :
        document = UserPersonalProfile
        fields = ['userSkypeID', 'aboutUserQuote', 'userLocation']

class TutorProfileForm(DocumentForm):

    class Meta :
        document = UserPersonalProfile
        fields = ['userSkypeID', 'aboutUserQuote', 'userLocation',
                  'tutorTuitionTopics',
                  'tutorMiddleSchoolHourlyRate',
                  'tutorHighSchoolHourlyRate',
                  'tutorCollegeHourlyRate',
                  ]

class UserEducationForm(EmbeddedDocumentForm):

    class Meta :
        document = UserEducationCredential
        embedded_field_name = 'userEducationCredential'

        fields = ['userEducationInfo']

class UserWorkForm(EmbeddedDocumentForm):

    class Meta :
        document = UserWorkCredential
        embedded_field_name = 'userworCredential'
        fields = ['userWorkInfo']