---
layout: default
title: Upgrading The Database
parent: Certdog
nav_order: 11
---

# Upgrading the Certdog Database

DO NOT PERFORM THIS STEP ON VERSIONS 1.17 OR LATER

Contact [Krestfield Support](mailto:support@krestfield.com) if you are unsure whether this step needs to be carried out

<br>

These instructions relate to versions 1.16 and earlier and result in a newer database being installed

These steps MUST be carried out before upgrading from version 1.16 as all future versions utilise the later database formats

<br>

### Pre-requisites

You will need the database admin password. This is the password that was entered when the server was first installed.

<br>

The database must use a TLS connection. Note that, for free versions before 1.16, TLS was not enabled by default on the database

To enable TLS, stop the *Krestfield CertDog Service*, then edit ``[CERTDOG INSTALL]\config\application.properties``. At the top of the file, add ``?tls=true`` to the end of the ``spring.data.mongodb.uri``. For example, if you have:

```
spring.data.mongodb.uri=mongodb://certmanuser:1TPEwGJ2h1CBcoG0suUX@127.0.0.1/certman
```

Update so it looks like this:

```
spring.data.mongodb.uri=mongodb://certmanuser:1TPEwGJ2h1CBcoG0suUX@127.0.0.1/certman?tls=true
```

<br>

Next edit ``[CERTDOG INSTALL]\mongodb\bin\mongod.cfg`` adding the following to the ``net`` section:

```
tls:	
	mode: requireTLS
	certificateKeyFile: C:\certdog\mongodb\..\config\sslcerts\dbssl.pem
	allowConnectionsWithoutCertificates: true
```

E.g. if you have:

```
...
net:
   bindIp: 127.0.0.1
   port: 27017
setParameter:
   enableLocalhostAuthBypass: false
...   
```

It would become:

```
net:
   bindIp: 127.0.0.1
   port: 27017
   tls:
      mode: requireTLS
      certificateKeyFile: C:\certdog\mongodb\..\config\sslcerts\dbssl.pem
      allowConnectionsWithoutCertificates: true
setParameter:
   enableLocalhostAuthBypass: false
```

Ensuring that your path names are correct. E.g. in this example we use ``c:\certdog`` as the default installation. Update appropriately

Verify the server still starts and operates after these changes have been made

<br>

### Backup

Open the services snapin and stop the following services:

* Krestfield Cerdog Service
* Krestfield Cerdog Database

![Certdog Services](.\images\upgrade_services.png)

(To open the services snapin - click **Start**, type **services** and select the **Services App**)

<br>

Backup the current installation by copying the entire install folder. E.g. if the installation resides at ``c:\certdog`` copy (or zip up) the entire folder

<br>

### Upgrade the database

Open a PowerShell window as administrator

Navigate to ``[CERT DOG INSTALL]\install`` e.g.  ``C:\certdog\install`` and run:

```
.\upgrade-db.ps1
```

This script will ask for the database admin password

<br>

**<u>Note</u>**

The script is unaware of what updates have been made to the TLS certificates. It replaces them all with versions it knows will operate correctly.  

If you have have made changes to your TLS certificates - server or database, they are copied to: ``.\certdog\config\sslcerts.bak[TIMESTAMP]`` e.g. ``.\certdog\config\sslcerts.bak.20260226-1012`` and they must then be manually coped back to the ``.\sslcerts`` folder 

<br>

### Troubleshooting

If you see an error such as

```
Database dump failed. Exiting.
```

Verify that the admin password for the database is correct

Verify that you meet the pre-requisites mentioned at the top of this page

<br>

The script outputs the following files:

* upgradedblog.txt

* upgradedblog.out

Any errors during the process will be available in these files

<br>

If the upgrade does fail and cannot be recovered, rollback the installation by stopping the services and re-instating the backed up files. Once restored, re-start the services
