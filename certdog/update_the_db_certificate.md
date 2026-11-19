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

Note: If the database is remaining on the same server as the certdog services and the database network interface is still bound to 127.0.0.1 e.g. ``.\certdog\mongodb\bin\mongod.cfg`` includes:

```
net:
   bindIp: 127.0.0.1
```

Then the database cannot be accessed externally and no traffic to the database will leave the local network stack.

In this case there is not real requirement to implement TLS. However, it is configured by default as an added layer of protection and to avoid an alteration to the bindIp value that would allow the database to be externally available. The default configuration would prevent this.

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

<u>Subject Alternative Names</u>

For the Subject Alternative Names, add the [Database Server FQDN] as a DNS entry and any other DNS or IP Address entries as required. 

If you will continue to access the database locally at ``127.0.0.1`` ensure that is added as a **IP Address SAN**

<br>

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

Next open the Services snapin and stop the services in this order:

1. Krestfield Adcs Driver
2. Krestfield Certdog Service
3. Krestfield Certdog Database

Then starting in this order:

1. Krestfield Certdog Database
2. Krestfield Certdog Service
3. Krestfield Adcs Driver

<br>

**STEP 3: Configure the SSL Certificate on the Database**

If using the ADCS Driver (i.e. interfacing to Microsoft CAs), ensure that the root and intermediate CA certificates that issued the new database certificate have been imported into the Windows store.

You can obtain these by navigating to the issued certificate in STEP 1 and choosing the **Actions** - **Go To Issuer** option. Then downloading the certificates (ensuring you download all CA certificates, including the root) and importing into the Intermediate or Trusted Roots store (depending whether the certificate is a root CA or not). 

<br>

<br>

## Troubleshooting

To confirm that an issue is certificate related, you may first disable TLS (temporarily), to ensure that without any certificates the connection to the database is OK. See [Disable TLS](#disable-tls) below.

<br>

**The database certificate has expired**

If the database certificate has expired, the Krestfield Certdog Database service will not start and ``mongod.log`` will contain:

```
"s":"F",  "c":"NETWORK",  "id":50755, ... "msg":"The provided SSL certificate is expired or not yet valid."
```

The certdog logs (``[certdog install]\logs\certdog.log``) will show ``CertificateExpiredException: NotAfter: <date>``, giving the date the certificate expired.

As certdog needs the database to issue a new certificate, first [Disable TLS](#disable-tls), start certdog and issue the new certificate, then re-enable TLS as described in [Re-enable TLS](#re-enable-tls).

<br>

If the service does not start. Attempt a restart again ensuring that the stop and start order is carried out correctly.

<br>

Next, analyse the following log file:

```
C:\certdog\tomcat\logs\catalina.YYYY-MM-DD.log
```

(Where YYYY-MM-DD is the timestamp when the log was created).

Search for: ``PKIX path building failed``

A full log entry containing this string will look like this:

```
Caused by: com.mongodb.MongoTimeoutException: Timed out while waiting for a server that matches ReadPreferenceServerSelector{readPreference=primary}. Client view of cluster state is {type=UNKNOWN, servers=[{address=127.0.0.1:27017, type=UNKNOWN, state=CONNECTING, exception={com.mongodb.MongoSocketWriteException: Exception sending message}, caused by {javax.net.ssl.SSLHandshakeException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target}, caused by {sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target}, caused by {sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target}}]
```

The key part here is:

```
PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

And indicates that the certdog service does not trust the DB TLS certificate.

This may be because it was not imported correctly, is not being referenced by the database correctly or does not have the correct attributes. We can check all of these manually next:

<br>

<u>Verify the certificate</u>

From certdog locate the TLS certificate that was issued in STEP 1 above and view the details:

<img src="./images/image-20251010120953588.png" alt="image-20251010120953588" style="zoom:80%;" />

- The Subject DN should be the FQDN of the server. E.g. SERVER1.krestfield.local
- The Key Usages should include Digital Signature and Key Encipherment
- The EKU (Extended Key Usages) should include Server Authentication
- The SANs (Subject Alternative Names) should include:
  - IP:127.0.0.1 - if you are accessing from the same machine
  - DNS: [Server FQDN] - this should be the same as the Subject DN
  - You may have additional entries

Open 

```
.\certdog\config\application.properties
```

And locate the line starting with ``spring.data.mongodb.uri`` E.g.

```
spring.data.mongodb.uri=mongodb://certmanuser:eZAqMcOcVu58RLdoyBb9@127.0.0.1/certman?tls=true
```

Ensure that whatever DNS name or IP address appears after the @ symbol is included in the certificate as a DNS or IP SAN. E.g. in this case ``127.0.0.1`` appears after the @ symbol and we have an IP SAN of 127.0.0.1, which is correct.



Under **Technical Details**, ensure that the Certificate ID is the one that was specified to the script above.

<br>

<u>Confirm certificate has been imported into the database</u>

Open a browser and navigate to:

https://127.0.0.1:27017

Note: That if your database is not listening on 127.0.0.1 port 27017 enter the correct IP address (or FQDN) and port. To verify what these values should be analyse the file here:

```
.\certdog\mongodb\bin\mongod.cfg
```

Which will have values under the ``net:`` heading, as follows:

```
net:
   bindIp: 127.0.0.1
   port: 27017
```

The browser should navigate to the address and may show a security warning. From the browser, inspect the certificate protecting this TLS end point. It should match that as generated in STEP 1 above.

<br>

<u>Confirm certificate has been imported into the JKS store</u>

Navigate to:

```
.\certdog\config\sslcerts
```

And enter the following command:

```
..\..\java\bin\keytool.exe -list -keystore dbssltrust.jks -storepass temp1234! | findstr certdog
```

You should see several occurrences named certdogN (e.g. certdog1, certdog2 etc):

```
certdog
certdog1, 10 Oct 2025, trustedCertEntry,
certdog2, 10 Oct 2025, trustedCertEntry,
certdogtlsroot, 10 Oct 2025, trustedCertEntry,
```

Verify each of the certificates using the following command - providing the certdog aliases with the ``-alias`` switch:

```
..\..\java\bin\keytool.exe -list -v -alias certdog1 -keystore dbssltrust.jks -storepass temp1234!
```

These certificates (certdog1 and certdog2) should be the chain certificates. That is the root and intermediate(s).

Verify these are present and as expected. I.e. examine the issuers for the certificate created in STEP 1 above within certdog, comparing the Issuers and Serial Numbers.

<br>

When running the command above the only output is the following:

```
certdogtlsroot, 10 Oct 2025, trustedCertEntry,
```

This indicates that the new CA certificates have not been imported correctly. Try re-running the ``set-dbsslcert.ps1`` script again, or import manually as described below.

<br>

<u>Manually Add to JKS Store</u>

In certdog, navigate to the certificate issued in STEP 1 above. Under Actions, click Go To Issuer. Then, once the page takes you to the issuer (CA) certificate, click Download Options and Certificate (.cer). 

If this is not a Root CA certificate, click on Actions - Go To Issuer again and repeat until you have downloaded all CA certificates including the root.

For each of these certificates, run the following command:

```
..\..\java\bin\keytool.exe -importcert -trustcacerts -alias <alias> -file <ca-cert-file> -keystore dbssltrust.jks
```

Providing an alias (which can be anything that will help identify the certificate) and the certificate file e.g. certdogca1.cer.

<br>

Once any changes have been made ensure that services are restarted.

<br>

## Disable TLS

TLS on the database can be disabled temporarily. For example:

- The database TLS certificate (``[certdog install]\config\sslcerts\dbssl.pem``) has **expired**, so the database will not start. As certdog needs the database to issue a replacement certificate, disabling TLS lets you start certdog, issue the new certificate (STEP 1 above), then re-enable TLS
- To confirm whether an issue is certificate related

If the database is bound to ``127.0.0.1`` only (the default - see the note at the top of this page), running without TLS for a short time is low risk as the database cannot be reached from outside the server.

<br>

**The following changes are required. If any one of them is missed, the database, the certdog service or the ADCS Driver will not start or connect:**

1. Comment out the ``tls:`` section in ``mongod.cfg``
2. Comment out the ``clusterAuthMode: x509`` line in ``mongod.cfg``
3. Remove ``?tls=true`` from the database URI in ``application.properties``
4. If the ADCS Driver is installed (i.e. you issue certificates from Microsoft CAs), run ``configure-adcs-service.ps1`` so that the driver uses the new (non-TLS) database URI. Restarting the driver service on its own is **not** enough

<br>

### 1. Stop the services

Open the Services snapin and stop the services in this order:

1. Krestfield Adcs Driver
2. Krestfield Certdog Service
3. Krestfield Certdog Database

<br>

### 2. Edit mongod.cfg

First take a backup, then edit the following file:

```
[certdog install]\mongodb\bin\mongod.cfg
```

Make the following changes, using the ``#`` character at the start of each line:

- Comment out the ``tls:`` line **and every line below it** that belongs to that section (``mode``, ``certificateKeyFile``, ``CAFile`` if present and ``allowConnectionsWithoutCertificates``)
- Comment out the ``clusterAuthMode: x509`` line under ``security:`` (if present)
- Do **not** comment out the ``security:`` or ``authorization: "enabled"`` lines. Certdog still logs in to the database with a username and password, so authorization must stay enabled

The file should then look similar to this. Your paths may differ and your file may contain other lines - leave any other lines as they are:

```
systemLog:
   destination: file
   path: C:\certdog\mongodb\mongod.log
   logAppend: true
storage:
   dbPath: C:\certdog\mongodb\dbfiles
processManagement:
   pidFilePath: C:\certdog\mongodb\mongod.pid 
net:
   bindIp: 127.0.0.1
   port: 27017
#   tls:
#        mode: requireTLS
#        certificateKeyFile: C:\certdog\mongodb\..\config\sslcerts\dbssl.pem
#        CAFile: C:\certdog\mongodb\..\config\sslcerts\dbssl_root.pem
#        allowConnectionsWithoutCertificates: true
setParameter:
   enableLocalhostAuthBypass: false
replication:
   replSetName: replocal
security:
   authorization: "enabled"
#   clusterAuthMode: x509
```

Save the file.

<br>

**Why clusterAuthMode must also be commented out**

``clusterAuthMode: x509`` tells the database to authenticate replica set members using their TLS certificates. This requires TLS to be enabled. If TLS is disabled but this line is left in place, the database will refuse to start.

In this case the database may stop before it opens its log file, so **nothing new is written to** ``mongod.log``. The Services snapin will simply report:

```
Windows could not start the Krestfield Certdog Database service on Local Computer.
Error 1053: The service did not respond to the start or control request in a timely fashion.
```

Running the database from a console (see [Check the database starts](#check-the-database-starts) below) will display the actual error.

<br>

**Notes on editing mongod.cfg**

This file is in YAML format, which is strict about layout:

- Use spaces only. Never use tab characters
- Do not change the indentation of any lines you are not commenting out
- Save the file in UTF-8 (or ANSI) format, not Unicode

Older installations may not have the ``CAFile`` or ``clusterAuthMode`` lines. If they are not present, there is nothing to change for them.

<br>

### 3. Check the database starts

Before starting the Windows service, start the database from a console. Any error will then be displayed on screen.

Ensure the **Krestfield Certdog Database** service is stopped, then open a PowerShell window as Administrator and run:

```powershell
cd [certdog install]\mongodb\bin
.\mongod.exe --config .\mongod.cfg
```

As the database logs to a file, very little (or nothing) is displayed when it starts successfully. The command keeps running until you stop it.

- **If the command keeps running**, the database has started OK. Leave it running and carry out the checks below from a second PowerShell window. Then press **Ctrl+C** to stop it
- **If the command exits straight away**, the database has failed to start. Note the error that is displayed and check the [log entries](#log-entries-to-look-for) below

<br>

<u>Check the database is listening</u>

In a second PowerShell window, run:

```powershell
Test-NetConnection 127.0.0.1 -Port 27017
```

The output should include:

```
TcpTestSucceeded : True
```

(If your database uses a different address or port, use the values from the ``net:`` section of ``mongod.cfg``.)

<br>

<u>Check the database is accepting connections without TLS</u>

If ``mongosh.exe`` is present in ``[certdog install]\mongodb\bin``, you can connect using the same credentials as certdog. Copy the URI from the ``spring.data.mongodb.uri`` line in ``application.properties`` (without ``?tls=true``) and run:

```powershell
cd [certdog install]\mongodb\bin
.\mongosh.exe "mongodb://certmanuser:<password>@127.0.0.1/certman" --eval "db.runCommand({ping: 1})"
```

The output should include:

```
{ ok: 1 }
```

This confirms that the database is running without TLS and that the certdog credentials are accepted.

<br>

<u>Check the database log</u>

Open ``[certdog install]\mongodb\mongod.log`` (the path is set by ``systemLog: path:`` in ``mongod.cfg``) and look at the most recent entries. You can do this from PowerShell:

```powershell
Get-Content "C:\certdog\mongodb\mongod.log" -Tail 50
```

A successful start includes an entry such as:

```
{"t":{"$date":"..."},"s":"I",  "c":"NETWORK",  "id":23016,   "ctx":"listener","msg":"Waiting for connections","attr":{"port":27017,"ssl":"off"}}
```

``"ssl":"off"`` confirms that TLS is now disabled.

See [Log entries to look for](#log-entries-to-look-for) below for the entries that indicate a problem.

Once the checks are complete, stop the console database with **Ctrl+C**.

<br>

### 4. Edit application.properties

First take a backup, then edit the following file:

```
[certdog install]\config\application.properties
```

Locate the ``spring.data.mongodb.uri`` line and remove the ``?tls=true`` part from the end. E.g. the line will look like this:

```
spring.data.mongodb.uri=mongodb://certmanuser:eZAqMcOcVu58RLdoyBb9@127.0.0.1/certman?tls=true
```

After editing, like this:

```
spring.data.mongodb.uri=mongodb://certmanuser:eZAqMcOcVu58RLdoyBb9@127.0.0.1/certman
```

Change nothing else on this line. If the URI has other options after the ``?`` (e.g. ``?tls=true&replicaSet=replocal``), remove only ``tls=true`` and keep the other options.

Save the file.

<br>

### 5. Start the database and certdog services

Start the services in this order:

1. Krestfield Certdog Database
2. Krestfield Certdog Service

The certdog service can take a few minutes to start fully.

Then check that:

- Both services show as **Running** in the Services snapin
- You can log in to certdog from a browser
- The latest entries in ``[certdog install]\logs\certdog.log`` and ``[certdog install]\tomcat\logs\catalina.YYYY-MM-DD.log`` do not contain ``MongoTimeoutException`` or ``Timed out while waiting for a server``

<br>

### 6. Update the ADCS Driver

**This step is only required if the ADCS Driver (Krestfield Adcs Driver service) is installed.**

The ADCS Driver does not read ``application.properties`` when it starts. The database URI is passed to the driver when it is configured, and the driver stores it securely. If the driver is simply restarted it will continue to use the old URI (ending ``?tls=true``) and will fail to connect to the database.

To pass the new URI to the driver, open a PowerShell window as Administrator and run the ``configure-adcs-service.ps1`` script **from the install directory**:

```powershell
cd [certdog install]\install
.\configure-adcs-service.ps1
```

The script:

- Reads the ``spring.data.mongodb.uri`` value from ``..\config\application.properties``. This is why it must be run from the ``install`` directory, and after ``application.properties`` has been edited (step 4)
- Stops the Krestfield Adcs Driver service (if it is running) and starts it again, passing it the new URI

If the script cannot find ``application.properties`` (e.g. because it was run from a different directory), it will ask you to enter the full database URL. In that case, enter the ``spring.data.mongodb.uri`` value from ``application.properties``, without ``?tls=true``.

When successful, the script displays:

```
Service started OK
```

Then check that:

- The **Krestfield Adcs Driver** service shows as **Running** in the Services snapin
- In certdog, under **Administration > Agents**, the agent for this server is listed and approved. If it shows as un-approved, approve it and re-select it as a *Permitted Agent* on each Microsoft CA Certificate Issuer, as described in [Registering the Service](adcsdriver.html#registering-the-service)
- A test certificate can be issued from a Microsoft CA

See [ADCS Driver](adcsdriver.html#registering-the-service) for more details on this script.

<br>

### Log entries to look for

The tables below list the entries most commonly seen in each log, and what they mean.

<u>Database log: [certdog install]\mongodb\mongod.log</u>

To list only errors (``"s":"E"``) and fatal errors (``"s":"F"``), run:

```powershell
Select-String -Path "C:\certdog\mongodb\mongod.log" -Pattern '"s":"F"','"s":"E"' | Select-Object -Last 20
```

| Entry | Meaning |
| --- | --- |
| ``"msg":"Waiting for connections"`` with ``"ssl":"off"`` | The database started OK without TLS |
| ``"msg":"Waiting for connections"`` with ``"ssl":"on"`` | The database started OK but TLS is still enabled. Check the ``tls:`` section in ``mongod.cfg`` is fully commented out and that you edited the file used by the service |
| ``"msg":"The provided SSL certificate is expired or not yet valid."`` | TLS is still enabled and the certificate has expired. The ``tls:`` section has not been commented out (or a different ``mongod.cfg`` is being used) |
| ``"codeName":"InvalidSSLConfiguration"`` | TLS is enabled but the certificate file cannot be read. See [Database Fails to Start after SSL Configuration](errors%20v%20solutions.html) |
| No new entries after a failed start | The database stopped before opening its log, usually because of a configuration error. Check that ``clusterAuthMode: x509`` is commented out and that the file has no tabs or indentation errors. Run the database from a console (step 3) to see the error |

<br>

<u>Certdog logs: [certdog install]\logs\certdog.log and [certdog install]\tomcat\logs\catalina.YYYY-MM-DD.log</u>

All of the following appear inside a ``Timed out while waiting for a server`` message. The ``caused by`` part shows the reason:

| Entry | Meaning |
| --- | --- |
| ``java.net.ConnectException: Connection refused`` | The database is not running. Check the database first (step 3) |
| ``CertificateExpiredException: NotAfter: ...`` or ``(certificate_expired)`` | Certdog connected using TLS and the database certificate has expired. The date shown is when the certificate expired |
| ``SSLHandshakeException`` (any other reason) | Certdog is still trying to connect using TLS. Check ``?tls=true`` has been removed from ``application.properties`` |
| ``PKIX path building failed`` | TLS is enabled and certdog does not trust the database certificate. See [Troubleshooting](#troubleshooting) above |
| ``Exception authenticating`` or ``Authentication failed`` | The database is running, but the username or password in the URI is wrong. Check the ``spring.data.mongodb.uri`` line was not changed apart from removing ``?tls=true`` |

<br>

<u>ADCS Driver</u>

If ``configure-adcs-service.ps1`` reports ``Unable to start the service``, or the agent does not appear in certdog:

- Check the Windows **Application** event log for errors from the ADCS Driver
- For more detail, enable the driver's file log by setting the ``ADCS_DRIVER_FILE_LOGGING`` environment variable to ``true`` and restarting the Krestfield Adcs Driver service. The log is written to ``C:\ProgramData\Krestfield\AdcsAgent\log.txt``. See [Additional File Logging](adcsdriver.html#additional-file-logging). Switch this logging off again afterwards as the file will keep growing

The most common cause is that the driver is still using the old URI. Re-run ``configure-adcs-service.ps1`` from the ``install`` directory, after checking ``application.properties`` has been updated.

<br>

### Re-enable TLS

Once certdog is running without TLS, issue the new database certificate and switch the database, certdog and the ADCS Driver back to TLS.

<br>

<u>1. Issue and install the new certificate</u>

Follow STEP 1 at the top of this page to issue the new certificate from certdog, then run ``set-dbsslcert.ps1`` as described in STEP 2.

``set-dbsslcert.ps1`` only updates the certificate files (``dbssl.pem``, ``dbssl_root.pem`` and ``dbssltrust.jks`` in ``[certdog install]\config\sslcerts``). It does not change ``mongod.cfg`` or ``application.properties``, and the new certificate is not used until TLS is re-enabled below. You do not need to restart the services when the script prompts you to. Continue with the next steps instead.

If you use the ADCS Driver, also import the root and intermediate CA certificates that issued the new certificate into the Windows certificate stores, as described in STEP 3. The ADCS Driver will not be able to connect to the database over TLS if it does not trust the new certificate.

<br>

<u>2. Stop the services</u>

Stop the services in this order:

1. Krestfield Adcs Driver
2. Krestfield Certdog Service
3. Krestfield Certdog Database

<br>

<u>3. Restore mongod.cfg</u>

Restore your backup of ``[certdog install]\mongodb\bin\mongod.cfg``, or remove the ``#`` characters added in step 2 of [Disable TLS](#disable-tls). Ensure that:

- The ``tls:`` section is restored (``tls:``, ``mode``, ``certificateKeyFile``, ``CAFile`` if present and ``allowConnectionsWithoutCertificates``)
- The ``clusterAuthMode: x509`` line is restored under ``security:``
- The indentation matches the original file and no tab characters have been added

<br>

<u>4. Restore application.properties</u>

Restore your backup of ``[certdog install]\config\application.properties``, or add ``?tls=true`` back to the end of the ``spring.data.mongodb.uri`` line. E.g.:

```
spring.data.mongodb.uri=mongodb://certmanuser:eZAqMcOcVu58RLdoyBb9@127.0.0.1/certman?tls=true
```

<br>

<u>5. Check the database starts with TLS</u>

As in step 3 of [Disable TLS](#disable-tls), you can first start the database from a console (``.\mongod.exe --config .\mongod.cfg`` from ``[certdog install]\mongodb\bin``) to confirm it starts, then press **Ctrl+C**.

``mongod.log`` should now contain ``"msg":"Waiting for connections"`` with ``"ssl":"on"``. You can also browse to ``https://127.0.0.1:27017`` and check that the certificate shown is the new one (see [Troubleshooting](#troubleshooting)).

<br>

<u>6. Start the database and certdog services</u>

Start the services in this order:

1. Krestfield Certdog Database
2. Krestfield Certdog Service

Check you can log in to certdog. If the certdog service does not start, search ``catalina.YYYY-MM-DD.log`` and ``certdog.log`` for ``PKIX path building failed`` and see [Troubleshooting](#troubleshooting) above.

<br>

<u>7. Update the ADCS Driver</u>

If the ADCS Driver is installed, run ``configure-adcs-service.ps1`` again, so that the driver uses the TLS URI (ending ``?tls=true``):

```powershell
cd [certdog install]\install
.\configure-adcs-service.ps1
```

This also starts the Krestfield Adcs Driver service. Check the service is running, the agent is approved under **Administration > Agents** and that a test certificate can be issued from a Microsoft CA. If the driver cannot connect, check that the CA certificates were imported into the Windows stores (step 1 above) and see the [ADCS Driver](#log-entries-to-look-for) log checks above.

<br>

To avoid the database certificate expiring unexpectedly in future, note its expiry date. You may also want to choose a longer validity period for the new certificate.
