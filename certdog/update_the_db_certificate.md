---
layout: default
title: Updating the Database SSL Certificate
parent: Certdog
nav_order: 130
---

# Updating the Database SSL Certificate



A default database certificate is provided with the installation which protects the local database traffic  

This certificate is bound to the 127.0.0.1 IP address  

If you wish to cluster the database, or access it from another certdog installation then this certificate will need to be updated so that it is correctly associated with the host server  

<br>

### Steps

**STEP 1: Issue a new Certificate from Certdog**

Ensure you have a certificate profile (or template) that can issue an SSL/TLS certificate

Issue a certificate with the following details:

``CN=[Database Server FQDN]``

Where ``[Database Server FQDN]`` is the full qualified domain name of the server where the database resides

E.g.

``CN=server1.certdog.local``

You may add other fields if required (``O, OU, C`` etc.)

For the Subject Alternative Names, also add the server's FQDN and any other DNS or IP Address entries as required. For example, if you will continue to access the database locally at ``127.0.0.1`` ensure that is added as a IP Address SAN

Issue the certificate then click **More** to view all the certificate details. At the bottom of the view, click **Technical Details**:

<img src=".\images\cert-id.png" alt="Cert ID" style="zoom: 50%;" />

Click on the value displayed next to **Certificate ID**. This will copy the value to the clipboard. You will need this value in the next steps

<br>

**STEP 2: Configure the SSL Certificate on the Database**

On the server where the Certdog database is running (or the server you wish to be the primary node, if using database replication), open a PowerShell window as Administrator  

Navigate to ``[Certdog Install]\bin`` e.g. ``c:\certdog\bin``

Run the ``set-dbsslcert.ps1`` script, as shown below. You will need the certificate ID obtained in Step 1 as well as a credential that will login to Certdog to obtain the certificate that was issued in Step 1

```powershell
PS E:\certdog\bin> .\set-dbsslcert.ps1

Database SSL Configuration
--------------------------

This script will configure the provided certificate as the databases TLS certificate
Run this script to renew or replace the database TLS certificate

You will need the ID of the certificate (issued from Certdog) to successfully run this script
You can obtain this ID by vewing the certificate details in Certdog. Under Technical details
click the value beside Certificate ID to copy this ID to the clipboard
See: https://krestfield.github.io/docs/certdog/update_the_db_certificate.html for more details

Please enter the certificate ID (as obtained from Certdog): 62bec5d554122f00f090fe81

You must now enter credentials for Certdog
These credentials will be used to obtain the certificate from Certdog
Username: user@certdog.local
Password: **********
Attempting login at: https://127.0.0.1/certdog/api
Authenticated OK
Adding alias certdog1 to ..\config\sslcerts\dbssltrust.jks
Certificate was added to keystore
Adding alias certdog2 to ..\config\sslcerts\dbssltrust.jks
Certificate was added to keystore

You must restart the Krestfield Certdog Database and the Krestfield Certdog Service
for these changes to take effect
```

<br>

Next open the Services snapin and restart the following services:

* Krestfield Certdog Database

* Krestfield Certdog Service

In that order



