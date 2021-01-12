# Windows Installation

 

The following steps outline the steps required to install the EzCert on a single system

If the pre-requisites are in place, the entire installation should not take more than 10 minutes





### Pre-requisites

The system may be installed on the following operating systems:  


* Windows Server 2016

* Windows Server 2019

* Windows 10 [^1]



.NET 4.8 must be installed



You must have local Administrator privileges on the system




### 1.  Download the Installer

Download the zip file from here: 

https://krestfield.s3.eu-west-2.amazonaws.com/ezcert/v1.0.1/ezcert.zip  



### 1.1 Verify the download

To verify the downloaded file, perform the following operations:

Open a command prompt or PowerShell window and navigate to the download location e.g.

``C:\Users\myname\Downloads``

At the prompt type:

``certutil -hashfile ezcert.zip sha1``

Or, if you wish to produce the longer SHA-256 hash, type:

``certutil -hashfile ezcert.zip sha1``

E.g.

```powershell
C:\temp\downloads>certutil -hashfile ezcert.zip sha256
SHA256 hash of c:\Users\myname\Downloads\ezcert.zip:
7916f6ae820e6f491ba00c71fbd8f1f7c0e6fcf0447bb3e8cc57753238234b74
CertUtil: -hashfile command completed successfully.
```

Compare the hash value produced with the following checksums:

SHA1: ``143e93265c1d9dac7c8a58119d7dfad1eaff838b``

SHA256: ``7916f6ae820e6f491ba00c71fbd8f1f7c0e6fcf0447bb3e8cc57753238234b74``



### 1.2 Unzip

Unzip this to a location on the target machine. You may wish to create a folder beneath ``C:\Program Files`` such as:

``C:\Program Files\Krestfield``

But you can also create a folder anywhere on the file system

Unzip the contents of the download to this folder. This should result in a directory structure such as:

``C:\Program Files\Krestfield\ezcert``



Open a PowerShell prompt as **Administrator** and navigate to this folder e.g.

```powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\WINDOWS\system32> cd "C:\Program Files\Krestfield\ezcert"
PS C:\Program Files\Krestfield\ezcert>
```



Run ``dir`` and check the file structure looks something like the following:

```powershell
    Directory: C:\Program Files\Krestfield\EzCert


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        06/01/2021     17:46                bin
d-----        05/01/2021     16:01                config
d-----        08/01/2021     11:27                install
d-----        07/01/2021     15:22                java
d-----        06/01/2021     15:48                tomcat
```

If you don't see the ``install`` directory, the unzipping process may have failed. Check that you have the correct permissions, then delete the folder and attempt the unzip process again



### 2. Run the Installer

From the PowerShell prompt, navigate into the ``install`` directory and run the ``.\install.ps1`` script:

```powershell
PS C:\Program Files\Krestfield\ezcert> cd install
PS C:\Program Files\Krestfield\ezcert\install> .\install.ps1
```



The installer will start and display some initial information. e.g.

```powershell
Krestfield EzCert Setup Version 1.0
===================================

This script will install the EzCert system on this machine
...
```



Follow the instructions to install the system, noting the following:

1. In the first instance it is recommended that you install **al**l required components (including java and the database binaries). These files are installed in the local directory and if required, can easily be removed later
   

   I.e. when prompted with:

   ``Download java (y/n)? (Choose n if you have previously downloaded):``  
   Enter **y**   
   
   and when prompted with   
   
   ``Download the database binaries (y/n)? (Choose n if you have previously downloaded):``  
   
   Enter **y**
   
2. You will be prompted to enter details and passwords for several accounts, these are discussed in the section below

3. You will be asked what interface you wish the system to be available on and the current available IP Addresses (as configured on your system) will be listed

    For a production system you should have an IP Address available which will be targeted via a DNS entry. For an initial test system the local loopback address (127.0.0.1) can be used



There are many customisations and deployment options that can be applied including the separation of services across multiple machines, hosting on other containers, using shared databases and hosting fully or partially in the cloud. Contact support support@krestfield.com for more details



### 3. Verify the Installation

First, check the installation log files for any errors

* installlog.out
* installlog.txt

If no errors were shown during the installation these files should just contain audit information



From the PowerShell script, navigate to the ``..\bin`` folder and type ``.\is-db-running.ps1``:

```powershell
PS C:\Program Files\Krestfield\EzCert\install> cd ..\bin
PS C:\Program Files\Krestfield\EzCert\bin> .\is-db-running.ps1
Database is running
```

The message ``Database is running`` should be seen  

Then type, ``is-api-running.ps1``  

```powershell
PS C:\Program Files\Krestfield\EzCert\bin> .\is-api-running.ps1
Testing https://127.0.0.1/ezcert/api...
API is running
```

The message ``API is running`` should be seen  

If either the database or API are not running, see the Troubleshooting at the end of this document



Next, open a browser and navigate to ``https://[Your IP Address]/ezcert/ui``

Where ``[Your IP Address]`` is the address chosen during the installation e.g.

``https://127.0.0.1/ezcert/ui``

You should see a warning such as:

<img src=".\images\sslconnectionerror.png" alt="image-20210108155429427" style="zoom:67%;" />

This is because we have not yet configured a valid SSL certificate.  For now, click **Advanced** then click **Continue to 127.0.0.1 (unsafe)** 

You should see the login screen:

<img src=".\images\login.png" alt="image-20210108155637774" style="zoom:67%;" />

Enter the **username** and **password** for the First Admin User that you provided during the installation and click **Login**  

You should be logged in OK.  The initial view will be ***Certificates***, but at this stage there are none to show    

A successful login indicates that the installation was completed OK  



### 4. SSL Configuration

By default an a test SSL certificate protects the system using the default 127.0.0.1 IP address  

This certificate will not be trusted by your system. You will see warnings when accessing the application via browser and REST API calls may fail  

For test purposes you may continue to use the provided SSL certificate. To enable trust double click the following certificate:  

``[Install Dir]\config\sslcerts\dbssl_root.cer``  

in order to open it:

<img src=".\images\def_ssl_root.png" alt="image-20210108162250620" style="zoom:67%;" />

Click Install **Certificate**... and select **Current User**

<img src=".\images\root_cert_store.png" alt="image-20210108162426401" style="zoom:67%;" />

Select **Place all certificates in the following store** and browse to **Trusted Root Certification Authorities**, click **Next** and then **Finish**

<img src=".\images\import_root_warning.png" alt="image-20210108162618663" style="zoom:67%;" />

Click **Yes**

If you now close the browser, re-open and navigate to https://127.0.0.1/excert/ui the warnings should be gone

Note: This is a test certificate and should not be trusted in a production environment. You should still continue to create a valid SSL certificate as described [here](configure_server_ssl.html)



### Accounts and Passwords

During the installation you will be prompted for the following details:

* The Database User Admin Account
  * This is the main database administrator account and is used by the installer to create the other initial database accounts required by the system
  * You will not normally need to use this account on a day-to-day basis but you must retain the details (username as displayed and the password you enter)
  * If you wish to manually configure the database later (for example if all user accounts were lost), these credentials will be required
* First Admin User
  * This is the first user that will log into the system, as an administrator. This will normally be your account
  * As well as a username and password, you will be required to enter an email address. All EzCert user accounts require an associated email address to which notifications from the system may be sent
* Master Password
  * This account is used as the top level protection for other accounts. It is not stored in the clear on the system
  * You must enter this password when installing the Application Service
  * Once entered, it should not be required again for this system but should be stored securely. If you start the application manually (not via the windows service) or wish to host the application on another container (e.g. on a shared Tomcat service), this password will be required



### Windows Services

**Application Service**  

This service will be installed by the install script but can also be installed manually by running the .msi installer separately. This .msi installer is located here:   

`` [Install Folder]\install\bin\InstallEzCertService.msi``  

This service starts and stops the system  

  

**AD Certificate Services Agent**  

This service interfaces with your Microsoft ADCS instance.  More details on this service can be found [here](adcsdriver.html)  




### Trouble Shooting

If the installation has not started the services, this is normally associated with permissions issues. If any of the scripts failed to execute fully, the configuration may not be complete. In these cases it is often easier to delete the ``ezcert`` directory (where the files were unzipped) and attempt the installation again, checking the account being used has Administrator level permissions on the system  

Alternatively, you may try the following to attempt to start services manually and determine the cause of the issue:



Open the Windows Services snapin and search for the Krestfield EzCert Service:

<img src=".\images\ezcert_service.png" alt="image-20210108160848515" style="zoom:80%;" />

Attempt to restart this service and monitor to ensure it starts OK (press F5 to refresh the view). Note, it can take several seconds for the service to start-up 

Open the **Windows Event Viewer** and navigate to **Windows Logs** | **Application**

<img src=".\images\event_viewer_ezcertservice.png" alt="image-20210108161039972" style="zoom:80%;" />



Search for entries with Source = **Krestfield EzCert Service**

Check if there are any error entries that may indicate issues starting the system



If the service is still not operating, open a PowerShell script as an Administrator and navigate to the installation directory e.g.  

``C:\Program Files\Krestfield\ezcert``

Navigate to the **bin** directory and type, ``.\start-db.ps1``

You should see:

```powershell
Starting database...
DB Running OK
```

Then type ``.\start-tomcat.ps1``

You should see:

```powershell
Starting tomcat using:
Java: C:\temp\hash\java\jdk15\bin\java.exe

Retrieved master password from the cmmasterpassword environment variable OK

JRE_HOME=C:\temp\hash\java\jdk15
Starting C:\temp\ezcert\tomcat\bin\catalina.bat please wait...

Testing https://127.0.0.1/ezcert/api...
Application is running
```



But if there is an issue, you will see something like:

```powershell
Testing https://127.0.0.1/ezcert/api...
Unable to connect to the remote server
Not started yet...waiting...

Application failed to start. Check console.out and console.err for errors
```

Analyse the ``console.err`` and ``console.out`` files for any obvious errors. 






[^1]: Windows 10 can not host the ADCS Driver. This component must be installed on a Server based operating system. See the ADCS Driver documentation for more information
