---
layout: default
title: Administrator Password Reset
parent: Certdog
nav_order: 100
---
# Administrator Password Reset

<br>

If an administrator password has been lost or forgotten, another administrator can still login to certdog and reset the password  

However, if no administrators are able to login then their password may be reset by following the instructions below  

<br>

### Pre-Requisites

This process requires access to the host machine where the database is running  

You must also have the database administrator password. This is the password that would have been set during the installation step  *Database User Admin Account Setup*. The username for this account is ``certmanadmin``  

If you have also lost this password and you have a support agreement in place, contact [support](mailto:support@krestfield.com)

<br>

### Steps

Create the hashed password by navigating to:   

```
[certdog install]\install\bin
```

Run the following command, where ``[password]`` is the new password to be set for the account:  

```
java -jar SetDatabasePassword-1.0.jar h [password]
```

This will output the hashed version of the password:

```
$2a$10$rPSQZhmM2wlTA6Ke29I85e14Q7GgXDX8iq2DNoDLI2GcqsbwcITVq
```

Copy this value e.g. copy and paste into a text document for the time being, as will need it in the steps below

<br>

Next navigate to:

```
[certdog install]\mongodb\bin
```

And start the database shell by typing:

```
mongo
```

Now we authenticate against the admin database:

```
use admin
db.auth("certmanadmin")
```

Enter the password for the ``certmanadmin`` user  

Next, we change to the ``certman`` database and locate the account we want to reset the password for. In the example below we are searching for the user whose username is ``admin``

```
use certman
db.users.find({username:"admin"})
```

You can skip this step - but this will confirm the account is present  

Now we will update the password for this user by providing the hashed password from above in the following command:

```
db.users.updateOne({username:"admin"}, {$set:{ enabled:true, nextAllowedLogonTime:NumberLong(0), password:"$2a$10$rPSQZhmM2wlTA6Ke29I85e14Q7GgXDX8iq2DNoDLI2GcqsbwcITVq"}})
```

Exit from the shell by typing ``exit``  

You should now be able to login using the new password  

<br>

### Complete Output

```powershell
C:\certdog\install\bin>java -jar SetDatabasePassword-1.0.jar h Password1234!!
$2a$10$qWAWK96LjEXsftZDsQ4DdOXe3deZNfsV645OuyI2utC7d01UId6nC

C:\certdog\install\bin>cd ..\..\mongodb\bin

C:\certdog\mongodb\bin>mongo
MongoDB shell version v4.4.1
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("efc2c2a9-7cc8-47af-9fd9-343921ecf7ce") }
MongoDB server version: 4.4.1
replocal:PRIMARY> use admin
switched to db admin
replocal:PRIMARY> db.auth("certmanadmin")
Enter password:
1
replocal:PRIMARY> use certman
switched to db certman
replocal:PRIMARY> db.users.find({username:"admin"})
{ "_id" : ObjectId("6221f83e1e2f9ad7dd70cf56"), "email" : "admin@ased.com", "username" : "admin", "password" : "$2a$10$VEsIyJlN5MiZoXLsEe7GEesJuRDD9YhmymmKlERAq778mZaq5JOuG", "group" : "ADMIN", "enabled" : true, "teamsIds" : [ "6221f840876a2b78f10dd5c7" ], "numFailedLoginAttempts" : 0, "userMessage" : "Account access has been delayed as there were too many failed login attempts", "nextAllowedLogonTime" : NumberLong(0), "_class" : "com.krestfield.pki.certman.model.users.CertManUser" }
replocal:PRIMARY> db.users.updateOne({username:"admin"}, {$set:{ enabled:true, nextAllowedLogonTime:NumberLong(0), password:"$2a$10$qWAWK96LjEXsftZDsQ4DdOXe3deZNfsV645OuyI2utC7d01UId6nC"}})
{ "acknowledged" : true, "matchedCount" : 1, "modifiedCount" : 1 }
replocal:PRIMARY> exit
bye
```

