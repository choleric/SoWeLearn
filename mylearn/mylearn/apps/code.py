"""
This file contains response codes.
"""

# generic codes

"""
operation success
"""
SUCCESS = 0x0

"""
operation error
"""
#General erros 2-100
ListMaxLengthExceeded = 2

# below is error code for user authentication system 200-300
SignupFailure = 201
UserExist = 202
DifferentPassword = 203
ChangePasswordFailure = 204
WrongOldPassword = 205
EmailNotRegistered = 206
ResetPasswordFailure = 207
ResetpasswordFromKeyCommonFailure = 208
ResetPasswordFromKeyBadToken = 209
InvalidConfirmationEmail = 210
SigninFailure = 211
SigninInvalidField = 212

# below is error code for user social login system 300-400
SocialAccountSignupFailure = 301
DuplicateEmailSocialAccount=302
SocialConnectionFailed = 303
SocialConnectionFailedNoPassword = 304
SocialConnectionFailedNoVerifiedEmail = 305
SocialAccountLoginCancelled = 306
SocialAccountLoginFailed = 311
SocialAccountAuthenticationFailure = 312

# app customize codes

AllAuthErrorMessageMap = {
 'This field is required.' : SigninInvalidField,
 'Enter a valid email address.' : SigninInvalidField,
'Your account has no password set up.': SocialConnectionFailedNoPassword,
'Your account has no verified e-mail address.' : SocialConnectionFailedNoVerifiedEmail,
}

#
# we will refer this when returning error to frontend
# every field has a number: 0,1,2,3....
SignupFormField = ['email', 'password1', 'password2', 'userFirstName' 'userLastName']
SigninFormField = ['login', 'password']


# below is error code for user_profile, from 100 - 200
profileUnknown = 100
personalProfileInvalid = 101
profileSkypeIDInvalid = 102
profileQuoteInvalid = 103
profilelocationInvalid = 104
profileEduInvalid = 105
profielEduEntryNotExist = 106
profileWorkInvalid = 107
profileWorkEntryNotExist = 108
UserNotVerifiedAsTutor = 109
TutorProfileUnknown = 110
TutorProfileFormInvalid = 111
profileTutorTopicsInvalid = 112
middleSchoolHourlyRateInvalid = 113
highSchoolHourlyRateInvalid =114
collegeHourlyRateInvalid = 115
