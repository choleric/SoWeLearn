from django import forms

from mongodbforms import DocumentForm

from models import UserPersonalProfile

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
