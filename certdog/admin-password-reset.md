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

<u>For Microsoft Windows Deployments</u>

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

Copy this value e.g. copy and paste into a text document for the time being, as we will need it in the steps below

<br>

Next, navigate to:

```
[certdog install]\mongodb\bin
```

And start the database shell by typing:

```
.\mongo.exe -tls
```

Note: For the free version the ``-tls`` may not be required

If this fails, try running the following:

```
.\mongo.exe -tls -tlsAllowInvalidCertificates
```



<u>For Linux Deployments</u>

Type:

```
.\mongosh
```

In the following steps. use the following hashed password:

```
$2a$10$GNiVPV88Zb/HKOt3NSnACufrPt4cj7XhpTB7oTkeRRnZQwbAMBeO.
```



<u>All Deployments</u>

Authenticate against the admin database:

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
db.users.updateOne({username:"admin"}, {$set:{ enabled:true, nextAllowedLogonTime:NumberLong("0"), password:"$2a$10$rPSQZhmM2wlTA6Ke29I85e14Q7GgXDX8iq2DNoDLI2GcqsbwcITVq"}})
```

Exit from the shell by typing ``exit``  

You should now be able to login using the new password  

For Linux deployments, login with a password of ``password`` and immediately change via the UI

<br>

### Complete Output

<u>Windows Deployments</u>

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

[
  {
    _id: ObjectId('664767e1c9fc372734a26a13'),
    email: 'certdog@example.com',
    username: 'admin',
    password: '$2a$10$KPF5U6zb.eYBo.6enTaT2ODg10r5ISnTdWmeidgVa0eG4EjGV/6wW',
    group: 'ADMIN',
    enabled: true,
    teamsIds: [ '664767e1c9fc372734a26a14' ],
    numFailedLoginAttempts: 0,
    nextAllowedLogonTime: Long('0'),
    accountType: 0,
    lastLoginTime: ISODate('2024-05-23T16:20:13.397Z'),
    lastLoginIpAddress: '127.0.0.1',
    mustChangePassword: false,
    _class: 'com.krestfield.pki.certman.model.users.CertManUser'
  }
]

replocal:PRIMARY> db.users.updateOne({username:"admin"}, {$set:{ enabled:true, nextAllowedLogonTime:NumberLong("0"), password:"$2a$10$qWAWK96LjEXsftZDsQ4DdOXe3deZNfsV645OuyI2utC7d01UId6nC"}})

{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 0,
  upsertedCount: 0
}

replocal:PRIMARY> exit
bye
```

<u>Linux Deployments</u>

```sh
krestfield@debian $ mongosh
Current Mongosh Log ID:	6650531891ea0a0fdea26a12
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.6
Using MongoDB:		7.0.9
Using Mongosh:		2.2.6

For mongosh info see: https://docs.mongodb.com/mongodb-shell/

test> use admin
switched to db admin

admin> db.auth("certmanadmin")
Enter password
********************{ ok: 1 }

admin> use certman
switched to db certman

certman> db.users.find({username:"admin"})

[
  {
    _id: ObjectId('664767e1c9fc372734a26a13'),
    email: 'certdog@example.com',
    username: 'admin',
    password: '$2a$10$KPF5U6zb.eYBo.6enTaT2ODg10r5ISnTdWmeidgVa0eG4EjGV/6wW',
    group: 'ADMIN',
    enabled: true,
    teamsIds: [ '664767e1c9fc372734a26a14' ],
    numFailedLoginAttempts: 0,
    nextAllowedLogonTime: Long('0'),
    accountType: 0,
    lastLoginTime: ISODate('2024-05-23T16:20:13.397Z'),
    lastLoginIpAddress: '127.0.0.1',
    mustChangePassword: false,
    _class: 'com.krestfield.pki.certman.model.users.CertManUser'
  }
]

certman> db.users.updateOne({username:"admin"}, {$set:{enabled:true, nextAllowedLogonTime:NumberLong("0"), password:"$2a$10$rPSQZhmM2wlTA6Ke29I85e14Q7GgXDX8iq2DNoDLI2GcqsbwcITVq"}})

{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 0,
  upsertedCount: 0
}

certman> exit
```

