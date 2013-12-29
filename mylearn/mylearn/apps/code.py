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
SocialConnectionFailed = 1002
SocialConnectionFailedNoPassword = 1003
SocialConnectionFailedNoVerifiedEmail = 1004
SocialAccountLoginCancelled = 1005
SocialAccountLoginFailed = 1011

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
SigninFormField = ['login', 'password']
