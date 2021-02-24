---
layout: default
title: What Version of Certdog
parent: certdog
nav_order: Certdog
---

# What Version of Certdog am I Running



### UI and API Versions

From the main user interface, when logged in you will see the version displayed in the footer:

<img src=".\images\footer.png" alt="image-20210111165711454" style="zoom: 80%;" />

To obtain further details, select **Management > Settings** from the menu. System Information will be displayed as follows:

<img src=".\images\system_info.png" alt="image-20210111165904651" style="zoom:80%;" />



### Database Version

Open a PowerShell window as Administrator and navigate to your installation folder  

Navigate into the ``mongodb\bin`` folder

Start the mongo shell by typing ``.\mongo.exe -tls`` (Note: If your database SSL certificate is not trusted by the system you will need to run: ``.\mongo.exe -tls -tlsAllowInvalidCertificates``)

Once the shell has connected, type ``db.version()`` and press **Enter**:

```powershell
PS C:\Program Files\Krestfield\certdog\mongodb\bin> .\mongo.exe -tls -tlsAllowInvalidCertificates
MongoDB shell version v4.4.1
connecting to: mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("2fe5acd6-b1a7-4246-aa85-8877bfce36a4") }
MongoDB server version: 4.4.1
replocal:PRIMARY> db.version()
4.4.1
replocal:PRIMARY>
```

This will display the database version. In the example above this is **4.4.1**



### ADCS Agent Version



