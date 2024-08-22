---
layout: default
title: EzSign - payShield TLS Configuration
parent: EzSign
nav_order: 51
---

  

# payShield 10k TLS Configuration



## Overview

Setting up TLS on the payShield requires both *server* AND *client* authentication i.e. you cannot just configure the HSM to have a server side TLS certificate - you also require a client side certificate.  

EzSign requires the client side certificate to be provided as a PKCS#12 or JKS file. EzSign must also trust the server side certificate installed on the payShield.  

The following is an example on how to configure this. Note that it is always advisable to follow the vendor specific documentation. The details given here are as a guide only. 



The high-level steps are:

1. Generate a CSR on the payShield
2. Issue a server side certificate from this CSR
3. Issue a client side certificate and obtain as a PKCS#12
4. Import the certificates onto the payShield and configure for TLS
5. Configure EzSign to use TLS

  

The following guide (available from Thales) may also be followed: **payShield TLS Host Port V3_5-6-23.pdf**

Although any CA can be used (it doesn't have to be an OpenSSL CA as specified in that tech note).

  

#### Step 1: Generate a CSR

Login to the **payShield Manager** with all required smartcards.

Set the state to **Secure**.

Start the **Virtual Console** .

Run the **SG** command to generate a CSR as follows:

```
Secure> SG <Return>
Please enter the Subject Information for the Certificate Request:
Country Name (2 letter code) []: GB <Return>
State or Province Name (full name) []: Chelsea <Return>
Locality Name (eg, city) []: London <Return>
Organization Name (eg, company) []: Krestfield <Return>
Organizational Unit Name (eg, section) []: Operations <Return>
Common Name (e.g. server FQDN or YOUR name) []: HSM-0001
<Return>
Email Address []: support@krestfield.com <Return>
Select key type:
1 - RSA
2 - ECDSA P-256
3 - ECDSA P-384
4 - ECDSA P-521
Type [4]: 1 <Return>
Generating key pair ......................+++
.......+++
DONE
Do you wish to save to a file [Y/N]: N <Return>
-----BEGIN CERTIFICATE REQUEST-----
MIIC2TCCAcECAQAwgZMxCzAJBgNVBAYTAlVLMRcwFQYDVQQIEw5HcmVhdGVyIExv
bmRvbjEPMA0GA1UEBxMGTG9uZG9uMREwDwYDVQQKEwhCYW5rIFhZWjETMBEGA1UE
CxMKT3BlcmF0aW9uczERMA8GA1UEAxMISFNNLTAwMDIxHzAdBgkqhkiG9w0BCQEW
EGJpbGxAYmFua3h5ei5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIB
AQC+JhIisca5k7l5YIRNcDcq/QMb3jHzhQIbME4O9zDhTtmINFM7YrvZ6N2Sy1TU
za1cPf9JKR2X5D3ukaICtkTwxArj1WRnU2UnINTYeO0RWeBaouxO4ijSvzx5mCCg
RtcSQDK748+0xgWlZezkKkv+akOh4vYPdiOKx47wiS7UAENBaQI14C5cbnj6JMLe
f3hmzQzzu3vACAIDbuQXZ5A7w7ecGLSLahjEyx1H7PXpLnul2lPRlBcemVdqHi8f
dfXTAKE1RrKSrvU22sOn6uQLGFRTseIuC4tFvtZNJRHAtqCYpabV4vrBmNQDaw8W
p2FFu+e71ybqsLY0R5xt7ZABAgMBAAGgADANBgkqhkiG9w0BAQUFAAOCAQEAvVzS
iy5gJkAjUdqaBjr5MUoAXvk15fEg6gO+SV39X3mSsQklQdoHwFSNgOUWYHkTKPvN
vZnCxMlUK2nBhlu2Xz44yC/U7+E7FsaQz2nXrNx/gF3SY/a/ODA+Y9iSERIpwRCM
9CKapYONeBHqK/NIcgTOZ3SMsC9JXsvtxPyQ7vmbu4a/JpMantWfcLCA+z6i+S+H
WavGnPVGt9ERD5Cij7B6qSbbrkn+xoJARIGsXhbVQmdSxR8I8HUAQDYV+2VJo3bA
ct9ubVjaw2SSiQZp9xB7BOJjk/NQrTk5gG3BkDI/Ukp9A9s7YoW1oMY8YdIg/YRo
Y+LI5trvXN73V2X0Ow==
-----END CERTIFICATE REQUEST-----
Secure>
```

If you choose **Y** to save the CSR to a filename, you will be prompted to enter a USB disk (FAT32 formatted) into the rear of the HSM and a file with the name specified will be saved there. If you choose **N** the CSR will be displayed on the screen and you can just copy and paste into a local file.



#### Step 2: Issuing a server side certificate from this CSR

You can follow the **payShield TLS Host Port V3_5-6-23.pdf** guide to create an openSSL CA but we created a Root CA in certdog and configured a Cert Issuer (that included this CA and a client/server SSL profile).

The CSR generated above was then issued from this Root CA and named **payshield1.crt**. 

Also download the root CA certificate. This was named **root.crt**.



#### Step 3: Issuing a client side certificate and obtaining as a PKCS#12

From the same payShield Cert Issuer in Certdog, issue a client certificate with details such as: ``CN=payshieldclient,O=Krestfield,ST=Kensington,L=London,O=Engineering,C=GB``

And download this as a PKCS#12 named **payshieldclient.p12**. Also download the certificate itself and name **payshieldclient.crt**.



#### Step 4: Importing these certificates onto the HSM

Whatever method is chosen, the Thales guide says that the certificates must be imported in this order:

1. The CA Certificate (**root.crt**)
2. The server certificate (**payshield1.crt**)
3. The client certificate (**payshieldclient.crt**)

You can either, start the Console (or Virtual Console) and import these certificates using the **SI** command or use the payShield manager.

If using the SI command the certificates need to be copied to a FAT32 formatted USB drive which has been inserted into the HSM's rear USB port.

The command is then run as follows:

```
Secure> SI <Return>
Select File
1 – root.crt
2 – payshield1.crt
3 - payshieldclient.crt
File: 1 <Return>
Imported Trusted CA Certificate
Issued to: Krestfield, Issued by: Krestfield
Validity : April 9 10:59:22 2024 GMT to May 7 10:59:22 2034 GMT
Unique ID: 9C8FC713FAA31010 - AC03FAD5 (Root)
Do you wish to import another certificate? Y <Return>
```

...and do this for all three certificates. Once the final certificate has been imported you should see a message such as ``Chain of Trust validated``.



Or do this via the **payShield Manager**, as follows:

Navigate to **Configuration** > **Host Settings** and choose the **TLS** tab. Click **Enable TLS** (if this option is not available you are not in Secure state).

Click **Import Host TLS Certificate** and import in the order mentioned above.

Note that after each and every import the **payShield Manager** has to be restarted and you have to re-login again.

Once all installed you will see the certificate chain as follows (when you next login):

```
Subject: payShield1
    subject: payshieldclient
        subject: PayShield Root
```



You can check that the server side certificate is working as expected using using openssl, as follows:

```
openssl s_client -connect 192.168.0.211:2500
```

This should show the server certificate. You can also verify the client authentication part. Refer to the Thales guide: **payShield TLS Host Port V3_5-6-23.pdf** for more info.



### Trusting SSL Certificates

When you configure TLS, EzSign must trust the configured  TLS certificate. If this is not the case you will receive an error such as: 

```
...Token Exception: Failed to connect to HSM at IP Address/server: 192.168.0.211 port: 2500. Error: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

You can configure this trust on either of the following ways:



#### Option 1: Add the CA certificate to Java's cacerts trust store

Locate the cacerts file location for the version of java being used to run EzSign. If using the bundled version, this will be located at:

```
[EzSign Install Dir]/java/jdk-17.0.2/lib/security/cacerts
```

Otherwise, this file is normally located within the ``/lib/security`` folder of the java instance.

Run the following command to import the Root CA certificate:

```
keytool -import -trustcacerts -alias root -file root.cer -keystore cacerts
```

Supplying the password of ``changeit`` (unless this has previously been altered).

There is no need to set the EzSign ``tls.trustStore`` settings in this instance.



#### Option 2: Create a custom trust store file

Obtain all the CA certificates in the chain as files (e.g. **root.crt**)

Run the following command to import the root:

```shell
keytool -import -trustcacerts -alias root -file root.crt -keystore payshield.jks
```

You will be asked for a password and whether you want to trust this certificate. Enter a password (this will be required in the configuration later) and answer **YES**.

If there are also intermediate CA certificates in your chain, run the following to import those certificates:

```shell
keytool -import -trustcacerts -alias ca -file ca.cer -keystore payshield.jks
```

Entering the password again.

The EzSign ``tls.trustStore`` settings must be configured to reference this key store (see below).



### Configuring EzSign

The following properties must apply when TLS is used: ``payShield.useTls``

This indicates whether to secure the link to the HSM with TLS or not.

E.g.

```properties
channel.1.token.payShield.useTls=true
```

Also ensure that the port (``payShield.port``) has been updated as TLS uses a different port to non-TLS traffic (**2500** by default).

When *useTls* is set to **true** the following global options will also be required to specify the client TLS certificate:

* tls.clientKeyStore.type

* tls.clientKeyStore.filename

* tls.clientKeyStore.password

For example:

```properties
tls.clientKeyStore.type=pkcs12
tls.clientKeyStore.filename=/opt/payshield/payshieldclient.p12
tls.clientKeyStore.password=zijFhJ+BMAO8B3bYw9XD0AZlOYt4eYACY4zW9UXtZk2EC7hl+dgevA==
```

Where the password provided is the password for the specified PKCS12 file, as generated above.  

Note that ``tls.clientKeyStore.password`` must be set via the Management Utility. Run EzSign Manage and selecting the **Set TLS Client Keystore Password** option.



If using a custom trust store the following properties need to be set:

* tls.trustStore.type
* tls.trustStore.filename
* tls.trustStore.password

For example:

```properties
tls.trustStore.type=jks
tls.trustStore.filename=/opt/payshield/payshield.jks
tls.trustStore.password=igjFhJ+H0MAO8bYw9XD0AZlOYt4eYACY4zW9UXt542EC7hl+egevV==
```

Where the password provided is the password for the custom trust store JKS file, as generated above.  

Note that ``tls.trustStore.password`` must be set via the Management Utility. Run EzSign Manage and selecting the **Set TLS Trust Keystore Password** option.



When all items are configured, restart the EzSign daemon. Refer to [payShield 10k Support](payshield10k_support.html) for more information on setup and troubleshooting.

