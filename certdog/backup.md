---
layout: default
title: Backup
parent: Certdog
nav_order: 30
---

# Backup



The certdog architecture means that the majority of data is stored within the database with very few static configuration options being stored outside of the database



### Database

This is the main area for backup  

The database should be backed up regularly

Essentially the database files are stored here :

``[certdog installation]\mongodb\dbfiles``

And it is these files that must regularly be backed up

If the server's files system (where certdog is running) is also backed up, ensure this folder is included in that backup

<br>

<u>Manual Backup</u>

* Open the Services snapin, and locate the **Krestfield Certdog Database** service

* Stop the service

* Take a copy of the folder located here:

​        ``[certdog installation]\mongodb\dbfiles``

​		and save to a backup location

* Start the service

<br>

<u>Manual Restore</u>

* Open the Services snapin, and locate the **Krestfield Certdog Database** service

* Stop the service

* Move the following folder to  a backup location (in case you need to revert back):

​        ``[certdog installation]\mongodb\dbfiles``

* Copy the folder from the backup to ``[certdog installation]\mongodb\dbfiles``
* Start the service

<br>

This will restore the database to the state when the backup was taken and overwrite any changes that would have been made since then. A more granular approach can achieved using the mongodump and mongorestore tools

<br>



<u>Using mongodump and mongorestore</u>

You may download and install the mongodb Database Tools as per [this guide ](https://docs.mongodb.com/database-tools/installation/installation/)

Then use ``mongodump`` and ``mongorestore`` options to backup and restore  

Refer to the mongodb documentation for full details, but the certdog database may be backed up by using a command such as the following:

```sh
mongodump --db certman --username certmanuser --password [db password] --archive=c:\dbbackups\bk1.zip --gzip --ssl --tlsInsecure
```

The ``--db certman --username certmanuser`` are the default values for the database. The password for ``certmanuser `` can be obtained from your ``.\config\application.properties`` file

In this example, the entire database contents will be stored to the ``bk1.zip`` file which is zipped due to the ``--gzip`` switch (leave out the ``--gzip`` switch to prevent compression)  

Note that if the command is run again with the same archive name - the previous archive will be overwritten. Hence, to retain multiple copies, use unique names

In production TLS is used to secure the link to the database, if using the free version of certdog you should omit the ``--ssl --tlsInsecure`` switches e.g.

```sh
mongodump --db certman --username certmanuser --password [db password] --archive=c:\dbbackups\bk1.zip --gzip
```

<br>

To restore, the ``mongorestore`` command is used.  As for ``mongodump``, there are many options but two approaches are discussed here:

* Restore only deleted items
  * This will leave new and changed records in place but will import records that have been deleted since the backup was taken
  * This option would be useful if CAs, Key Stores or Certificates had been inadvertently deleted
* Restore the entire database and overwrite
  * This option drops the database and recovers from the backup
  * This option is useful if you wish to revert back to the database at the point the backup was taken. New and changed items will be removed and reverted to their state at the backup point

<br>

To restore only deleted items a command such as the following may be used:

```sh
mongorestore --db certman --username certmanuser --password [db password] --gzip --archive=c:\dbbackups\bk1.zip --ssl --tlsInsecure
```

For the free version the TLS options may be omitted e.g.

```sh
mongorestore --db certman --username certmanuser --password [db password] --gzip --archive=c:\dbbackups\bk1.zip
```

<br>

To restore the entire database and overwrite:

```sh
mongorestore --db certman --username certmanuser --password [db password] --gzip --archive=c:\dbbackups\bk1.zip --ssl --tlsInsecure --drop
```

I.e. the ``--drop`` switch has been added

<br>

### Application Configuration

Within your certdog installation, there is a folder named

```sh
[certdog installation]\config
```

This folder contains some static configuration data (such as the database URL to use) and some TLS certificates  

You should backup this folder but these settings will change infrequently and so only need backing up after initial setup and whenever a change is made (to the application TLS certificates or database location)  

If you carry out a machine or image backup, these settings will be retained together with that data anyway



### Logs

Logs that are written to the database will be backed up with the database  

However, there are also the following file logs:

<u>log4j2 Logs</u>

If the log4j2 default settings are in use then the following folder will contain text based logs

```sh
[certdog installation]\logs
```

This will contain a current file log named ``certdog.log`` as well as folders containing the previous days archived logs

The majority of the entries in these logs are duplicates of the database logs. These logs will contain additional information (such as debug or low-level output not written to the database)

All events are always stored to the database

<br>

<u>Container Logs</u>

The host container (Tomcat) also produces log files. By default these will be located here:  

```sh
[certdog installation]\tomcat\logs
```

These logs contain debug or system level entries relevant to the container

<br>

If any snapshot or system level backup is already being performed, this location should be included in those backups. Otherwise, if these logs also need to be retained ensure these locations are included in your backup plan

