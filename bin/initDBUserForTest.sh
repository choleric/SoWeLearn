#!/bin/bash


#
declare -a all_users=( 'mc' 'zw' 'ls' 'xg' )

db_name='mylearn'

echo "db.dropDatabase()" | mongo $db_name

table_name='user'
for username in ${all_users[@]}
do
    echo "$username"
    echo "use $db_name
db.$table_name.save({'userEmail': '$username', 'userName': '$username'})" | mongo

done


table_name='user_personal_profile'
for userid in ${all_users[@]}
do
    echo "use $db_name
    db.$table_name.save({'userEmail': '$userid', 'userSkypeID': '${userid}_001', 'aboutUserQuote': '$userid quote', 'userEducationCredential' : [{'_cls':'UserEducationCredential', 'IsVerified':false, 'verifiedTimeStamp': NumberLong(1000), 'verifiedStaffId':NumberLong(1), 'userEducationInfo': '${userid}_school'}],\
        'userWorkCredential': [{'_cls':'UserWorkCredential', 'IsVerified':false, 'verifiedTimeStamp': NumberLong(1000), 'verifiedStaffId':NumberLong(1), 'userWorkInfo': '$userid txt'}], 'userLocation': '$userid location'})" | mongo
done
