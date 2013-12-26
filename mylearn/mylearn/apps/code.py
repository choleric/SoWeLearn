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
# app customize codes
