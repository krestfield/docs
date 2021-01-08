# Configuring the Server's SSL Certificates

 

Once installed, the system will be configured with a default SSL certificate  

This certificate is issued under a test CA with the subject ``CN=127.0.0.1``  

With this certificate in place, you will see errors such as:









Download the zip file and unzip to a location e.g. ``c:\program files\krestfield\ezcert``

Open a command prompt as administrator and navigate to c:\certman\installers

Type install.ps1 (or something)

[this runs: msiexec.exe /l*v mdbinstall.log /qb /i mongodb-windows-x86_64-4.4.1-signed.msi ADDLOCAL="ServerNoService,Client" INSTALLLOCATION="C:\krestfieldcertman\mongodb"]

 

Install the database

If you have an instance of MongoDB already installed (or available as Atlas) skip this step

Double click mongodb-windows-x86_64-4.4.1-signed.msi

Select the option to install as a Windows Service

Set the location for the database files. Note, the installation reserves a folder for the database files ([install location]\database) which can be used

 

If the Mongo Compass window appears at the end of the installation, close it

 

### Configure the Database

Open a command prompt as administrator

Navigate to the mongodb installation bin folder e.g. C:\Program Files\MongoDB\Server\4.4\bin

Type mongo and press Enter

At the mongo shell, type:

mongo 127.0.0.1/admin [certman install location]\createadmin.js

e.g.

mongo 127.0.0.1/admin “c:\certman\createadmin.js”

and press Enter

At the prompt 

Enter password:

Enter a strong password. This is the main user admin account for the database

 

At the prompt, type:

​        net stop mongodb

 

C:\WINDOWS\system32>net stop mongodb

The MongoDB Server (MongoDB) service is stopping.

The MongoDB Server (MongoDB) service was stopped successfully.

 

 

Now open a text editor as administrator and edit C:\Program Files\MongoDB\Server\4.4\bin\mongod.cfg

 

 