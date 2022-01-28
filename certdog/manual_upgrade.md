---
layout: default
title: Manually Upgrading
parent: Certdog
nav_order: 20
---

# Manually Upgrading Certdog

 <br>

To upgrade to a new version of Certdog you may 

* Simply uninstall the old and install the new version
  * This will not retain any settings - you will end up with a new, blank installation of the later version
  * This may be useful if you are building your configurations using automation and also do not need to retain any existing data (existing certificates)
  * This may also be the best option for test instances when you just want to dispose of the old versions

* Perform an in-place upgrade
  * This option overwrites the existing installation with the new files but retains all of the data and settings

<br>

## Option 1: Uninstall the old and Install the new version

Follow the guide [here](uninstalling.html) to uninstall your existing installation

If you wish to retain the data, in case of future use, follow the guide [here](backup.html) to backup

Follow the guide [here](installation.html) to install the new version

<br>

## Option 2: In Place Upgrade

### Overview

Essentially, we will backup the current installation then replace the following file and folder:

```
[certdog installation]\tomcat\webapps\certdog#api.war
[certdog installation]\tomcat\webapps\certdog#ui
```

With those from the new version's zip

<br>

**<u>STEP 1 - Stop Certdog</u>**

On Windows, open the services snapin and stop **Krestfield Certdog Service**

(On other OS's, either stop Tomcat or use the stop-certdog or stop-tomcat scripts)  



On Windows, open the services snapin and stop **Krestfield Certdog Database**

(On other OS's, stop mongo using the command line option ``db.shutdownServer()``or service options ``service mongod stop``) 

<br>

**<u>STEP 2 - Backup</u>** 

Backup the following folder:

```
[certdog installation]\tomcat\webapps
```

Also backup the database by following the guide [here](backup.html)

<br>

**<u>STEP 3 - Delete Existing Files</u>**

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

**<u>STEP - 4</u>**

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

**<u>STEP - 5</u>**

Start Certdog

<br>

### Verification and Rollback

Attempt to login as per normal to Certdog  

Confirm the version as follows:  

From the menu select **Settings** then choosing the **Settings** sub menu

The *System Information* should display:

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
