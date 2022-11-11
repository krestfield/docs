---
layout: default
title: Adding Additional Servers
parent: Certdog
nav_order: 131
---

# Adding Additional Servers



You may add additional servers to the base configuration for redundancy or load-balancing  

The Certdog architecture essentially consists of Certdog Servers (offering API and UI access) and a database  

The database may be replicated to provide redundancy or you may simply add additional Certdog servers to point to the same database. For example, you may have a large server hosting the database and simply wish to add additional Certdog servers that are accessible from other networks  

<br>

### Add Additional Certdog Servers

To add an additional Certdog server you must first have configured the database with a TLS certificate which is associated with the server the database is hosted on. This is required as the default certificate is tied to localhost (127.0.0.1) so will not be accepted by a remote server  

To do this, [follow the instructions here](update_the_db_certificate.html)

<br>

**Backup**

We will be making some changes to configuration files, so backup the following folder and file:

```
[certdog install]\config
[certdog install]\mongodb\bin\mongod.cfg
```

<br>

**Update Database Configuration**

On the main server we need to update the database configuration so it listens on a specific (or all interfaces) as by default it will be listening on 127.0.0.1  

To do this open 

```
[certdog install]\mongodb\bin\mongod.cfg
```

And update the following entry:

```
net:
   bindIp: 127.0.0.1
```

So that bindIp references a specific IP Address (the interface other servers will be connecting to) or set to ``0.0.0.0`` which means the database will be available on all interfaces (127.0.0.1 and any other IP Addresses that are configured on the server). If you set this value to a specific IP Address you will also have to update the following file:

```
[certdog install]\config\application.properties
```

And change ``127.0.0.1`` in the following line, to be the new IP Address. E.g. if you set ``bindIp`` to ``10.15.37.5`` then you need to update the line from this:

```
spring.data.mongodb.uri=mongodb://certmanuser:kFW8PypSqTF10cr9Z@127.0.0.1/certman?tls=true
```

To this:

```
spring.data.mongodb.uri=mongodb://certmanuser:kFW8PypSqTF10cr9Z@10.15.37.5/certman?tls=true
```

Note: You do not have to do this if you set ``bindIp to 0.0.0.0`` as this will include ``127.0.0.1``

<br>

**Check Firewall**

From any additional servers, check you can access the primary server over port ``27017``. On Windows this can be checked by opening a Command Prompt and typing the following

```
telnet [primary hostname or IP Address] 27017
```

And ensuring it connects. If it doesn't check the primary server's firewall settings - to allow incoming connections over port ``27017`` and that the additional servers are also allowing outgoing connections to the same

<br>

**Configure Additional Server**

On the second (or additional) server, install Certdog as normal or you may simply copy the entire certdog installation file from the primary server to this secondary  

If a database is running on this server, stop the *Krestfield Certdog Service* service  

Update the following file

```
[certdog install]\config\application.properties
```

And set the value for ``spring.data.mongodb.uri`` to reference the primary server. For example, by default this file may look like this

```
spring.data.mongodb.uri=mongodb://certmanuser:kFW8PypSqTF10cr9Z@127.0.0.1/certman?tls=true
```

I.e. the ``127.0.0.1`` part indicates that the Certdog server is connecting to the database on the localhost. Update this to point to the primary server e.g.

```
spring.data.mongodb.uri=mongodb://certmanuser:kFW8PypSqTF10cr9Z@10.15.37.5/certman?tls=true
```

Or if using the FQDN:

```
spring.data.mongodb.uri=mongodb://certmanuser:kFW8PypSqTF10cr9Z@server1.certdog.local/certman?tls=true
```

<br>

Now restart the Krestfield Certdog Service and ensure it starts OK and you are able to login etc. Once logged in, confirm that a change made on the primary server (e.g. issuing a certificate or adding a user) is seen on the secondary. This will confirm that both servers are using the same database

<br>

### Replicate the Database

The mongo DB can be replicated across several nodes. To do this, we simply copy the configuration across to the new server, install the DB as a service there, then back on the original server configure these new servers as additional nodes  

Connectivity from the original server to the new server(s) over port 27017 is required for this to operate  

<br>

From your current installation copy the following folder:

```
[certdog install]\mongodb
```

To the server(s) where you wish to replicate the database to. This may be the same server as configured above, or it could be a different server

<br>

Open a command prompt (or shell) and navigate to:

```
[certdog install]\mongodb\bin
```

Type the following:

```
mongod.exe --install --config .\mongod.cfg --serviceName "CertdogDB" --serviceDisplayName "Krestfield Certdog Database" --serviceDescription "The certdog database"
```

Open the Services snapin and start the **Krestfield Certdog Database**

<br>

Back on the original server, remove authorisation whilst we configure the replica set

Edit the following file:

```
[certdog install]\mongodb\bin\mongod.cfg
```

(On Linux this file will be located here ``/etc/mongod.cfg``)

Commenting out the following lines (with the ``#`` character) and saving:

```
#security:
#   authorization: "enabled"
```

Note: You will need sudo permissions to action this on Linux

<br>

Next start the mongo DB shell:

```
[certdog install]\mongodb\bin\mongo
```

For Linux use ``mongosh``

View the current settings by typing:

```
rs.conf()
```

Which should display something like the following:

```
{
        "_id" : "replocal",
        "version" : 1,
        "term" : 14,
        "protocolVersion" : NumberLong(1),
        "writeConcernMajorityJournalDefault" : true,
        "members" : [
                {
                        "_id" : 0,
                        "host" : "127.0.0.1:27017",
                        "arbiterOnly" : false,
                        "buildIndexes" : true,
                        "hidden" : false,
                        "priority" : 1,
                        "tags" : {

                        },
                        "slaveDelay" : NumberLong(0),
                        "votes" : 1
                }
        ],
        "settings" : {
                "chainingAllowed" : true,
                "heartbeatIntervalMillis" : 2000,
                "heartbeatTimeoutSecs" : 10,
                "electionTimeoutMillis" : 10000,
                "catchUpTimeoutMillis" : -1,
                "catchUpTakeoverDelayMillis" : 30000,
                "getLastErrorModes" : {

                },
                "getLastErrorDefaults" : {
                        "w" : 1,
                        "wtimeout" : 0
                },
                "replicaSetId" : ObjectId("62cfc2873221819903d25325")
        }
}
```

Now add the new server(s) by typing:

```
rs.add("newserver:27017")
```

Where ``newserver`` is the hostname or IP address of the new server  

Do this for all additional servers

You should see

```
{"ok" : 1}
```

If the setup was successful. If not, analyse the error message and verify that you have connectivity between the original server and new server over port 27017



