---
layout: default
title: EzSign - TLS Configuration
parent: EzSign
nav_order: 51
---

  

# TLS Configuration



Client-server communications between the EzSign Client and Server may be protected using TLS.

You can configure the EzSign Server with a server side certificate only or you may also, optionally configure two-way TLS where the client also authenticates to the server with a client side certificate.  



## Requirements

* For server side TLS you need a TLS certificate that includes the *Server Authentication* extended key usage.  The certificate should also have a SAN (Subject Alternative Name) for either the DNS name or IP Address relating to the server. For example, if the server is running at ``ezsign.server1.local`` then the certificate should have a DNS SAN of ``ezsign.server1.local``
* To add client side TLS you will also need a TLS certificate that includes the *Client Authentication* extended key usage 
* It is possible to use same certificate for both client and server side TLS, in this case the certificate must have both the *Client Authentication* and *Server Authentication* extended key usage
* The certificates can be packaged as either a PKCS12 or JKS file 
* Ideally, both the server and client side certificate are issued from the same CA. If this is not the case you may need to trust both CA chains as outlined in the [3. Configure the JRE's Trust](#3-configure-the-jre's-trust) below



## Server Side TLS Configuration

There are four things that must be done to implement server side TLS:

1. Create a JKS or PKCS12 keystore file containing the server-side certificate (and associated keys)  
2. Configure the server properties to use TLS and reference the JKS/PKCS12 keystore above
3. Configure the JRE (Java Runtime) to trust the server-side certificate
4. From within the application calling the EzSign Client, update the code to tell the client to use TLS

These steps are detailed below:



### 1. Create a Server JKS or PKCS12 file

Use *keytool* or similar to generate your CSR and obtain the server side TLS certificate for the server.  

When the CA issues the certificate, ensure that it meets the requirements as outlined in the [Requirements](#requirements) section above.



### 2. Configure the Server Properties

Obtain the following pieces of information:

* The full path to the PKCS12 or JKS file containing the server side TLS certificate
* The password used to protect the file
* Whether the file is a JKS or PKCS12



In the server properties file (e.g. ``ezsign.properties``), you must set the following properties:

* server.useTls
  * Set this to **true**
* tls.clientKeyStore.type
  * Set this to either **JKS** or **PKCS12** whether the file is JKS or PKCS12 formatted. 
* tls.clientKeyStore.filename
  * The *full path* to the JKS or PKCS12 file

For example: 

```properties
server.useTls=true
tls.clientKeyStore.type=jks
tls.clientKeyStore.filename=/opt/ezsign/keystores/ezsign_server.jks
```

Finally, run the *EzSign Management* utility, choosing the following option:

 ``15. Set TLS Client Keystore Password``. 

This will set the value for the password property, i.e.:

* tls.clientKeyStore.password
  * This is the encrypted keystore password

See the [Setting TLS Passwords](#setting-tls-passwords) section below for detailed steps on setting this password.  

The server properties file should now include entries such as the following:

```  properties
server.useTls=true
tls.clientKeyStore.type=JKS
tls.clientKeyStore.filename=/opt/ezsign/keystores/ezsign_server.jks
tls.clientKeyStore.password=CSMFimWkKvuIwfriyRvDzeNwthjH5gGxBWAiRWsL73xHZSkJaPXgCA==
```



After a restart the server will now only accept connections over TLS.  

You can confirm that the server is now providing a valid TLS certificate by using the ``openssl`` tool. See the [Validating the TLS Configuration](#validating-the-tls-configuration) section below for details how to do this.  

If any errors are seen during server start up or connection from the client, refer to the [Common TLS Configuration Errors](#common-tls-configuration-errors) section below.

Proceed to the next section.



### 3. Configure the JRE's Trust

You can add the trusted root (and any intermediate certificates), to the JRE's trusted store as follows.

1. Obtain the Root CA and any Intermediate CA certificates from the chain that issued the certificates e.g.
   1. root.cer
   2. ca.cer
2. Identify the java instance running the application that is using the EzSign Client and locate the *cacerts* file (e.g. ``C:\Program Files\java\jdk-18.0.1.1\lib\security\cacerts``)
3. Run the following keytool commands to import the root and optionally any intermediate certificates:


```shell
keytool -import -trustcacerts -alias krestfieldroot -file root.cer -keystore "C:\Program Files\java\jdk-18.0.1.1\lib\security\cacerts"

keytool -import -trustcacerts -alias krestfieldca -file ca.cer -keystore "C:\Program Files\java\jdk-18.0.1.1\lib\security\cacerts"
```

4. The default password for the keystore is usually ``changeit`` 
4. Identify the java instance running the EzSign Server and update its cacerts file in the same way





### 4. Code Client to use TLS

In order to update the client to use TLS, the ``useTls()`` option is required. E.g.

```java
 EzSignClient client = new EzSignClient("ezsign.server1.local", 5656)
     .useTls();
```

The client will now attempt to connect to the server using TLS.  



## Client Side TLS Configuration

Note that it is advisable to validate that the server side configuration is correct by following the steps in [Validating the TLS Configuration](#validating-the-tls-configuration) before proceeding to configure the client side.





There are three things that must be done to implement client side TLS:

1. Create a JKS or PKCS12 file containing the client-side certificate (and associated keys)  

2. Configure the server properties to require client side TLS

3. From within the application calling the EzSign Client, update the code to provide the Key Store containing the client side certificate

   

### 1. Create a Client JKS or PKCS12 file

Use *keytool* or similar to generate your CSR and obtain the client-side TLS certificate for the client. 

When the CA issues the certificate, ensure that it meets the requirements as outlined in the [Requirements](#requirements) section above for the client-side.



### 2. Configure the Server Properties

Add the following property to the server properties file:

```properties
server.useClientTls=true
```

This indicates to the server that any connecting client must authenticate with a client side TLS certificate.



### 3. Code Client to use Client TLS

In order to update the client to use client TLS, the ``useClientTls()`` option is required, in addition to the ``useTls()`` option.  

``useClientTls`` requires three parameters:

* ``clientKeystoreFilename`` - The Keystore Filename
  * This is the full path to the keystore file
* ``clientKeystorePassword`` - The Keystore Password
  * This is the password that protects the keystore file
* ``keyStoreType`` - The Keystore Type
  * This can be "JKS" or "PKCS12"




I.e.

```java
EzSignClient client = new EzSignClient(
    serverAddress, serverPort)
    .useTls()
    .useClientTls(keystoreFilename, keystorePassword, keystoreType);
```

E.g.

```java
EzSignClient client = new EzSignClient(
    "ezsign.server1.local", 5656)
    .useTls()
    .useClientTls("/opt/keystores/client.p12", "password", "PKCS12");
```

The client will now attempt to connect to the server using TLS and will now also provide the certificate supplied in the specified PKCS12 file.

 Refer to the [Common TLS Configuration Errors](#common-tls-configuration-errors) for details of common issues.







## Setting TLS Passwords

The Keystore TLS passwords (for either JKS or PKCS12 files) are encrypted in the properties file. To set these perform the following steps:

From the ``EzSignServer/bin`` directory run ``ezsign-manage`` utility:

```shell
  Krestfield EzSign Management
  ----------------------------

  The master password is required to manage the server

  Enter password:

  Krestfield EzSign Management
  ----------------------------

  1.  Set Passwords

  2.  Generate CSR
  3.  Import Certificate
  4.  Import Existing HSM Keys

  5.  Set Signing Key

  6.  Display Certificates
  7.  Display Certificates Details
  8.  Delete Certificate

  9.  Generate AES Key
  10. Display AES Keys
  11. Delete AES Key

  12. Translate Keystore Objects
  13. Display All Channel Objects
  14. Set Authentication Code

  15. Set TLS Client Keystore Password
  16. Set TLS Trust Keystore Password

  17. Exit
```

Enter the master password and choose option ``15. Set TLS Client Keystore Password``  

You will need to re-enter the master password and then to enter the *Keystore Password*.

```shell
  Command: 15

  You will now be asked to enter the Master Password
  Followed by the Client Keystore Password

  Master Password
  ---------------

  This is the password which is used to start the server
  It is used to encrypt other passwords (Token Passwords etc). It is not stored

 Enter Password:
Retype Password:

  Enter the Client Keystore Password
  ----------------------------------

  This is a password that protects the TLS Client Keystore.
  This is only required if you are utilising TLS.

 Enter Password:
Retype Password:

  A backup of the original has been saved to ..\config\ezsign.properties.2024.08.23.15.35
  Ready to update properties file ..\config\ezsign.properties with the new data

Proceed? (y/n): y

  The properties file ..\config\ezsign.properties has been updated successfully.
```

The properties file will be updated with the encrypted TLS Client Password and a backup saved in case you need to revert back.








## Validating the TLS Configuration

When server side TLS has been configured, re-start the server. On startup the following command can be used to confirm that the server is now using TLS and returning a TLS certificate:

This requires that *openssl* has been installed.

From a shell or command prompt, run the following command:

```shell
openssl s_client [EzSign Server Address or IP]:[Server Port]
```

E.g.

```shell
openssl s_client 127.0.0.1:5656
```



If setup has been successful, you should see something like the following:

```shell
CONNECTED(00000180)
Can't use SSL_get_servername
depth=2 C = GB, O = Krestfield, CN = Certdog Test Root
verify error:num=19:self-signed certificate in certificate chain
verify return:1
depth=2 C = GB, O = Krestfield, CN = Certdog Test Root
verify return:1
depth=1 C = GB, O = Krestfield, CN = Certdog Test Issuing CA
verify return:1
depth=0 CN = 127.0.0.1
verify return:1
---
Certificate chain
 0 s:CN = 127.0.0.1
   i:C = GB, O = Krestfield, CN = Certdog Test Issuing CA
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: Aug 22 10:13:32 2024 GMT; NotAfter: Aug 22 10:13:32 2025 GMT
 1 s:C = GB, O = Krestfield, CN = Certdog Test Issuing CA
   i:C = GB, O = Krestfield, CN = Certdog Test Root
   a:PKEY: rsaEncryption, 2048 (bit); sigalg: RSA-SHA256
   v:NotBefore: May  5 08:20:24 2023 GMT; NotAfter: May  3 08:20:24 2030 GMT
 2 s:C = GB, O = Krestfield, CN = Certdog Test Root
   i:C = GB, O = Krestfield, CN = Certdog Test Root
   a:PKEY: rsaEncryption, 4096 (bit); sigalg: RSA-SHA256
   v:NotBefore: May  5 08:11:09 2023 GMT; NotAfter: May  1 08:11:09 2038 GMT
---
Server certificate
-----BEGIN CERTIFICATE-----
MIIEOTCCAyGgAwIBAgIQMyRwNafeaU5bbdC+mtjpKzANBgkqhkiG9w0BAQsFADBE
MQswCQYDVQQGEwJHQjETMBEGA1UECgwKS3Jlc3RmaWVsZDEgMB4GA1UEAwwXQ2Vy
dGRvZyBUZXN0IElzc3VpbmcgQ0EwHhcNMjQwODIyMTAxMzMyWhcNMjUwODIyMTAx
...
+rWcZt/Hoyr/kbmArZpmAzukOPiThjpbSTmsfnsS7wi9RBaQBbg/tfMqfe7Md66X
u75sxg6470BYMNMLxTlnKPUK68Q1cJ5QgbytpaQD1RV0toiNRmZk8j919ncyP49J
awbadh/VgeyBc5RQ3FL1ywumL/Ja9uvx5KbSLkESVzDaLykseOJDqoREK0G6f/Jg
NlV94RXdTC79kmbC+R2YLAeeowDfc7kyEaljzFY=
-----END CERTIFICATE-----
subject=CN = 127.0.0.1
issuer=C = GB, O = Krestfield, CN = Certdog Test Issuing CA
---
...
```

Ensure you see the ``Server certificate`` and the details (e.g. the ``subject``) match what you expect.



If you see output such as the following:

```
CONNECTED(00000188)
Can't use SSL_get_servername
54A80000:error:0A000410:SSL routines:ssl3_read_bytes:sslv3 alert handshake failure:ssl\record\rec_layer_s3.c:1584:SSL alert number 40
---
no peer certificate available
---
No client certificate CA names sent
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 243 bytes and written 297 bytes
Verification: OK
---
New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384
Secure Renegotiation IS NOT supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
Early data was not sent
Verify return code: 0 (ok)
---
```

i.e.

```
no peer certificate available
```

Then there was no valid TLS found



## Common TLS Configuration Errors



### Client Error Messages

```
There was an error connecting to the EzSign server. Ensure the server is running on host 127.0.0.1 and listening on port 5656 and there is connectivity between this client and the server. If auth code is in use, check both the client and server are using the same code. PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

The key part here is:

```
PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

Which indicates that the correct root and intermediate certificates have not been added to the JRE trust store correctly. Check the steps outlined in step 3 of the [Server Side TLS Configuration](#server-side-tls-configuration) section



If the error message contains:

```
Received fatal alert: handshake_failure
```

Confirm that the server contains a valid server-side TLS certificate. You can view the contents of a JKS file by running the following command:

```shell
keytool -list -v -keystore keystorename.jks
```

In the EzSign Server logs, you may also see an entry such as:

```
2024-08-29 15:43:56.289 [pool-2-thread-1] ERROR EzSignServerLog - Failed to process message from client as there was a TLS error. Error Details: No available authentication scheme
```



If the error message contains:

```
Remote host terminated the handshake
```

This indicates that the client is attempting to use TLS but the server is not configured to use it. Check that ``server.useTls=true`` is present in the server properties file.



If the error message  contains:

```
Response received from the server was not valid
```

This indicates that the server is configured for TLS but the client is not. Ensure the client is using the ``useTls()`` option when being created.



If the error message  contains:

```
Error Details: Received fatal alert: bad_certificate
```

This indicates that the server is expecting a client side TLS certificate but none (or an invalid certificate) was provided by the client. Ensure the client is accessing a PKCS12 or JKS file with the correct client-side TLS certificate and is using the ``useClientTls()`` option when created.





### Server Error Messages

If the following is seen in the Server logs:

```
2024-08-23 08:44:04.856 [pool-2-thread-1] ERROR EzSignServerLog - Failed to process message from client as there was a TLS error. Error Details: Empty client certificate chain
```

It could be that the server does not trust the client-side TLS certificate provided by the client. Ensure the ``cacerts`` file for the JRE running the server includes the full chain (root and ca certificates) of the client TLS certificate.



If your client TLS certificate does not have the correct Client Authentication enhanced key usage, you will see an error as follows:

```
2024-08-23 09:04:40.279 [pool-2-thread-1] ERROR EzSignServerLog - Failed to process message from client as there was a TLS error. Error Details: Extended key usage does not permit use for TLS client authentication
```

To resolve, re-issue the client TLS certificate with the correct enhanced key usage.

