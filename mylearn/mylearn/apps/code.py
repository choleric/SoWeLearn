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
SignupFailure = 1
UserExist = 2
DifferentPassword = 3
ChangePasswordFailure = 4
WrongOldPassword = 5
EmailNotRegistered = 6
ResetPasswordFailure = 7
ResetpasswordFromKeyCommonFailure = 8
ResetPasswordFromKeyBadToken = 9
InvalidConfirmationEmail = 10
SigninFailure = 11
SigninInvalidField = 12

SocialAccountSignupFailure = 1001
DuplicateEmailSocialAccount=1002
SocialConnectionFailed = 1003
SocialConnectionFailedNoPassword = 1004
SocialConnectionFailedNoVerifiedEmail = 1005
SocialAccountLoginCancelled = 1006
SocialAccountLoginFailed = 1011
SocialAccountAuthenticationFailure = 1012

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
profileUserIDInvalid = 101
profileSkypeIDInvalid = 102
profileQuoteInvalid = 103
profilelocationInvalid = 104
profileEduInvalid = 105
profileWorkInvalid = 106
profileTutorTopicsInvalid = 107
profileTutorHourlyRateInvalid = 108
