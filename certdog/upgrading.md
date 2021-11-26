---
layout: default
title: Windows Installation
parent: Certdog
nav_order: 20
---

# Upgrading Certdog

 

If you already have an instance of Certdog running and wish to upgrade to a later version, the following steps may be followed  

<br>

### Overview

Essentially, we will backup the current installation then replace the following

```
[certdog installation]\tomcat\webapps\certdog#api.war
[certdog installation]\tomcat\webapps\certdog#ui
```

From the new version's zip

<br>

### Steps

**<u>STEP 1 Stop Certdog</u>**

On Windows, open the services snapin and stop **Krestfield Certdog Service**

On other OS's, either stop Tomcat or use the stop-certdog or stop-tomcat scripts  



Stop the Database from running

On Windows, open the services snapin and stop **Krestfield Certdog Database**

On other OS's, stop mongo using the command line option ``db.shutdownServer()``or service options ``service mongod stop`` 

<br>

**<u>STEP 2 Backup</u>** 

Backup the following folder:

```
[certdog installation]\tomcat\webapps
```

Also backup the database by following the guide [here](backup.html)

<br>

**<u>STEP 3 Delete Existing Files</u>**

From your existing installation, navigate to:

```sh
[certdog installation]\tomcat\webapps
```

It should look like this

![File Structure](.\images\certdog_upgrade1.png)

Delete the following folders

```
.\certdog#api
.\certdog#ui
```

And delete the following file

```
certdog#api.war
```

<br>

**<u>STEP 4</u>**

Unzip the new version's media, navigate to this unzipped location here:

```
[new media location]\certdog\tomcat\webapps\
```

Copy the following folder:

```
.\certdog#ui
```

And the following file:

```
certdog#api.war
```

To your current installation here:

```
[certdog installation]\tomcat\webapps
```

<br>

**<u>STEP 5</u>**

Start Certdog

<br>

### Verification and Rollback

Attempt to login as per normal to Certdog  

Confirm the version: From the menu select Settings then choosing the Settings sub menu

The System Information should display:

* UI Version
* API Version

Verify these are as expected

<br>

If a rollback is required, perform the following:

* Stop Certdog

* Replace the following folder:

```
[certdog installation]\tomcat\webapps
```

* With the version backed up

* Restore the database as per the guide [here](backup.html)

* Start Certdog

