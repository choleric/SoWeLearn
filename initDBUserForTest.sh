#!/bin/sh

echo "use user;
db.user_profile.insert({'user_email': 'mc', 'user_name': 'mc', 'userPersonalProfile':{'aboutUserQuote': 'walk my road', 'userEducationCredentials': 'high school', 'userWorkCredentials': 'txt', 'userLocation': 'sz'}})" | mongo
echo "use user;
db.user_profile.insert({'user_email': 'ls', 'user_name': 'ls', 'userPersonalProfile':{'aboutUserQuote': 'walk my road', 'userEducationCredentials': 'high school', 'userWorkCredentials': 'txt', 'userLocation': 'sz'}})" | mongo
echo "use user;
db.user_profile.insert({'user_email': 'xxg', 'user_name': 'xxg', 'userPersonalProfile':{'aboutUserQuote': 'walk my road', 'userEducationCredentials': 'high school', 'userWorkCredentials': 'txt', 'userLocation': 'sz'}})" | mongo
