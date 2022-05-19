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

<br>

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

<br>

### ADCS Agent Version

From *Add or remove program*s, search for **Certdog** under *Apps & features*  

 Click on the **Certdog ADCS Driver** and the version should be displayed  

Alternatively, from a PowerShell window, type the following:  

```
Get-WmiObject Win32_Product | select Name,Version
```

Which should then display something like the following:  

```
Name                                                           Version
----                                                           -------
Certdog ADCS Driver                                            1.5.0
Microsoft Visual C++ 2019 X64 Additional Runtime - 14.28.29325 14.28.29325
Microsoft Visual C++ 2019 X64 Minimum Runtime - 14.28.29325    14.28.29325
Certdog Service                                                1.3.0
```



