from django import forms

from mongodbforms import DocumentForm, EmbeddedDocumentForm

from models import UserPersonalProfile, UserEducationCredential, UserWorkCredential
from mylearn.apps import errcode

class UserProfileForm(DocumentForm) :

    class Meta :
        document = UserPersonalProfile
        fields = ['userSkypeID', 'aboutUserQuote', 'userLocation']
        err_maps = {'userSkypeID': errcode.profileSkypeIDInvalid,
                    'aboutUserQuote': errcode.profileQuoteInvalid,
                    'userLocation': errcode.profilelocationInvalid,
                    '__all__': errcode.personalProfileInvalid}

class TutorProfileForm(DocumentForm):

    class Meta :
        document = UserPersonalProfile
        fields = ['tutorTuitionTopics',
                  'tutorMiddleSchoolHourlyRate',
                  'tutorHighSchoolHourlyRate',
                  'tutorCollegeHourlyRate',
                  ]
        err_maps = {'tutorTuitionTopics': errcode.profileTutorTopicsInvalid,
                    'tutorMiddleSchoolHourlyRate': errcode.middleSchoolHourlyRateInvalid,
                    'tutorHighSchoolHourlyRate': errcode.highSchoolHourlyRateInvalid,
                    'tutorCollegeHourlyRate': errcode.collegeHourlyRateInvalid,
                    '__all__': errcode.TutorProfileFormInvalid}

class UserEducationForm(EmbeddedDocumentForm):

    class Meta :
        document = UserEducationCredential
        embedded_field_name = 'userEducationCredential'

        fields = ['userEducationInfo']

class UserWorkForm(EmbeddedDocumentForm):

    class Meta :
        document = UserWorkCredential
        embedded_field_name = 'userWorkCredential'
        fields = ['userWorkInfo']

    #def clean_