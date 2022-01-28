---
layout: default
title: Add Databases Indexes
parent: Certdog
nav_order: 300
---

# Add Database Indexes



From certdog version 1.6, the required indexes are applied to the database at install  

However, if you are running a previous version of certdog (or have upgraded from a previous version), your database will not have the latest indexes configured  

For low numbers of certificates (less than 5000) this should not effect performance. But if you are experiencing slow certificate searches you may perform the following steps to apply indexes  

<br>

### Option 1: Automatic Update (if you have upgraded to version 1.6 or above)

Open a PowerShell window as Administrator and navigate to:

```powershell
[Certdog Installation]\install
```

Run the following script:

```powershell
.\add-db-indexes.ps1
```

This script essentially carries out the manual steps detailed below

<br>

### Option 2: Manually Applying Indexes

Stop the **Krestfield Certdog Service**

Backup the ``mongod.cfg`` file located here:

```powershell
[Certdog Installation]\mongodb\bin\mongod.cfg
```

Now open the ``mongod.cfg`` file and comment out the following lines:

```ini
replication:
   replSetName: replocal
```

By adding a ``#`` to the start of these lines e.g.:

```ini
...
setParameter:
   enableLocalhostAuthBypass: false
#replication:
#   replSetName: replocal
security:
   authorization: "enabled"
...
```

Save the ``mongod.cfg`` file

Start the **Krestfield Certdog Service**

<br>

Open either a PowerShell or cmd prompt as Administrator and navigate to:

```powershell
[Certdog Installation]\mongodb\bin
```

Run

```
.\mongo.exe -tls -tlsAllowInvalidCertificates
```

To start the mongodb prompt. You should see something like this:

```powershell
PS C:\certdog\mongodb\bin> .\mongo.exe -tls -tlsAllowInvalidCertificates
MongoDB shell version v4.4.1
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("fee1c275-867b-4558-a33a-cb1ff824b9de") }
MongoDB server version: 4.4.1
>
```

At the mongo prompt type the following commands:

```powershell
use certman
```
Locate the *password* from your ``.\config\application.properties`` file. It will be contained in a string such as:
```powershell
spring.data.mongodb.uri=mongodb://certmanuser:abcd1234@127.0.0.1/certman?tls=true
```
In this example, the password required is ``abcd1234``. Yours will be set to a random string

Using this password, run the following command to authenticate to the database

```powershell
db.auth("certmanuser", "abcd1234")
```

Now create the indexes buy running the following commands

```powershell
db.certificates.createIndex({'validFrom' : 1})
db.certificates.createIndex({'validTo' : 1})
```

Then just type exit to end the session

```
exit
```

*See the Full Output below for an example*

<br>

Next stop the **Krestfield Certdog Service**

Either replace the ``mongod.cfg`` file with the backed up version or just uncomment the lines commented out above

Start the **Krestfield Certdog Service**

<br>

### Other Options

When using the mongo shell, you can view current indexes and drop them if required. For example, to view indexes use the following command:

```powershell
> db.certificates.getIndexes()
[
        {
                "v" : 2,
                "key" : {
                        "_id" : 1
                },
                "name" : "_id_"
        },
        {
                "v" : 2,
                "key" : {
                        "validFrom" : 1
                },
                "name" : "validFrom_1"
        },
        {
                "v" : 2,
                "key" : {
                        "validTo" : 1
                },
                "name" : "validTo_1"
        }
]
```

And to drop all indexes (this will not drop the default *_id* index - only those we have previously manually applied):

```powershell
> db.certificates.dropIndexes("*")
{
        "nIndexesWas" : 3,
        "msg" : "non-_id indexes dropped for collection",
        "ok" : 1
}
```

<br>

#### Full Output

```powershell
PS C:\certdog\mongodb\bin> .\mongo.exe -tls -tlsAllowInvalidCertificates
MongoDB shell version v4.4.1
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("fee1c275-867b-4558-a33a-cb1ff824b9de") }
MongoDB server version: 4.4.1
> use certman
switched to db certman
> db.auth("certmanuser", "abcd1234")
1
> db.certificates.createIndex({'validFrom' : 1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 1,
        "numIndexesAfter" : 2,
        "ok" : 1
}
> db.certificates.createIndex({'validTo' : 1})
{
        "createdCollectionAutomatically" : false,
        "numIndexesBefore" : 2,
        "numIndexesAfter" : 3,
        "ok" : 1
}
> exit
bye
```





