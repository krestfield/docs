---
layout: default
title: Certdog Errors and Solutions
parent: Certdog
nav_order: 2000
---

# Certdog Errors and Solutions

<br>

The following contains some common errors that may be experienced when using Certdog together with their solutions  
<br>
<br>

### There are no CA issuers that can process a request. This may be because you do not have permissions on any of the configured CA issuers

<u>Error Details</u>

When you navigate to Request by CSR or DN this message appears and you are unable to see any CA Issuers  

<u>Solution</u>

This is because the Team(s) you are a member of have not been assigned any permissions on CA Issuers. To rectify, first click on the top right *user* icon and select **Profile** under *My Account*  

The Team(s) you are a member of will be highlighted. Note these teams  

Next click on **Teams** from the menu, select one of the Teams you noted above and click **View/Edit**  

Next to *Permitted Certificate Issuers*, select the issuers that you wish this team to have permissions to obtain certificates from. As you are a member of this team you will also be provided with these permissions  

Re-attempt the certificate issuance



<hr>

### A CSR generator must be configured before you can request a certificate from a DN

<u>Error</u>

When navigating to Request - DN, this error is presented  

Solution  

If you want to request a certificate by only supplying the DN, Certdog must also create the CSR (Certificate Signing Request) on your behalf. In order to do this a CSR Generator is required  

To create a new CSR generator follow the steps outlined [here](create_csr_generator.html)



<hr>

### Credential fails when attempting to obtain templates or certificates from a Microsoft CA (ADCS)

<u>Error</u>

A credential is configured but when attempting to obtain templates or a certificate the following is seen:

```
The request to obtain the templates from the CA agent failed. Reason: There was an error obtaining the templates from the CA. Check the CA details are correct - they should be in the format 'hostname\ca name' as returned in the Config entry when certutils is run. Details (Logon failure: the user has not been granted the requested logon type at this computer)
```

Or

```
The request to obtain the certificate failed. Reason: Failed to process request. Logon failure: the user has not been granted the requested logon type at this computer
```

The important part being:

```
Logon failure: the user has not been granted the requested logon type at this computer
```

<u>Solution</u>

A service account should be used as a credential when accessing the Microsoft CA. The credential should be configured with the *Deny logon locally* and the *Logon as a service* user right assignments. If either *Deny logon locally* or *Logon as a service* are not set, this error will occur

You may run ``rsop.msc`` to obtain the local policy settings and check the assignments for the group that the user is a member of

Arrange for the correct permissions and assignments to be added to the user. See [here](https://krestfield.github.io/docs/certdog/configure_logon_as_a_service.html) for information on how to configure the account correctly   

You may also try running the ADCS Agent service under this account and setting the credential in the Microsoft Certificate Issuer to be *No Credential (use local agent account)*. See [here](adcsdriver.html) for more details  



<hr>

### Login screen runs slow

On some virtual machines that have limited graphics processing power or that may have 3d acceleration switched off, the login screen can appear to run slow

<u>Error</u>

Login screen slow to respond

<u>Solution</u>

This is due to the login screen background. This can be removed as follows:

* Stop the Krestfield Certdog Service

* Delete (or move to a backup location if still required) the following file:

```
[certdog install]\tomcat\webapps\certdog#ui\background.mp4
```

* Start the Krestfield Certdog Service

If your browser is still showing the background this will be because of the browser cache. Try closing the browser or performing a full refresh (e.g. CTRL-F5 on Chrome)



<hr>

### Cannot stop Krestfield CertDog Service

<u>Error</u>

Windows could not stop the Krestfield CertDog Service service on Local Computer.

Error 1061: The service cannot accept control messages at this time

<u>Solution</u>

Open a PowerShell window as Administrator and navigate to: ``[certdog install]\bin``  

Run ``.\stop-tomcat.ps1``

Next, open task manager, click on the Services tab and locate **Krestfield Certdog Service**

Right click and select **Go to details**

Click **certman-service.exe** and click **End task**



<hr>

### The request to obtain the certificate failed. Reason: Failed to process request. Index was outside the bounds of the array

<u>Error Details</u>

Applicable to versions up until version 1.6 only

If running the Krestfield ADCS Service under a specific Service Account and you have set the Microsoft CA Issuer in Certdog to use No Credential. You may see this error when requesting a certificate

<u>Solution</u>

Set the Krestfield ADCS Service to run under the Local System account and set the service account (that has permissions on the CA) as a Credential in Certdog. For your Microsoft Certificate Issuer - select this credential



<hr>


### Creating a CA using an AWS CloudHSM Key Store fails

<u>Error Details</u>

The AWS CloudHSM client has been configured on the machine and a key store configured in Certdog. When attempting to create a new CA, you see the following error:

```
There was an error creating the new CA. There was an error whilst creating the root CA: Signing Exception: There was an error generating the raw signature. Signing Exception: Signing error. Signing Exception: There was an error signing the data: CKR_FUNCTION_FAILED
```

Checking the CloudHSM log (on windows the default location is here ``C:\Program Files\Amazon\CloudHSM\cloudhsm-pkcs11.log.[timestamp]``)  you see errors such as:

```
2022-05-26T07:53:48.054Z ERROR [3908] ThreadId(3) [cloudhsm_pkcs11::sign::rsa_pkcs] Key 1310835 does not meet the availability requirements - The key must be available on at least 2 HSMs before being used.
2022-05-26T07:53:48.054Z ERROR [3908] ThreadId(3) [cloudhsm_pkcs11::sign::C_SignInit] C_SignInit failed, returning 0x00000006
```

Then this is due to the default availability requirements being enabled on the CloudHSM client. Which (as the error message above indicates) requires that the key be available on at least 2 HSMs before being used  

If you only have a single HSM configured this will never be the case

<u>Solution</u>

Switch off the key availability check as follows



For Windows:

Open a command prompt, as Administrator. Navigate to the bin directory (as below) and then run the following command:

```
C:\Program Files\Amazon\CloudHSM\bin>configure-pkcs11.exe --disable-key-availability-check
```

Restart the Certdog service



For Linux, from a shell run the following:

```
sudo /opt/cloudhsm/bin/configure-pkcs11 --disable-key-availability-check
```

Restart the Tomcat service



<hr/>

### The Krestfield CertDog Service doesn't start

<u>Error Details</u>

The following message is seen whilst attempting to manually start the service

```
The Krestfield CertDog Service service on Local Computer started and then stopped. Some services stop automatically if they are not in use by other services or programs.
```

<u>Solution</u>

Check the windows Event Log and navigate to Windows Logs, Application

If you locate event ID 7172 with the following message:

```
Unable to start the system. No master password has been set. Run the set master password script
```

Open a PowerShell window as Administrator and navigate to ``[certdog installation]\install`` e.g. ``c:\certdog\install``

Run the following command

```
.\start-certdog-service.ps1
```

When prompted enter the Master Secret/Password. This is the passphrase that would have initially been saved to ``MasterSecret.txt`` at installation



<hr/>

### Database Fails to Start after SSL Configuration

<u>Error Details</u>

The Krestfield Certdog Database service fails to start  

This can happen after the database SSL certificate has been renewed

Checking the log file here ``[certdog install]\mongodb\mongod.log`` there is an ``InvalidSSLConfiguration`` error, with message ``Failed to find PEM blob header`` e,g,:

```
{"t":{"$date":"2022-06-30T17:44:09.963+00:00"},"s":"F",  "c":"CONTROL",  "id":20574,   "ctx":"main","msg":"Error during global initialization","attr":{"error":{"code":140,"codeName":"InvalidSSLConfiguration","errmsg":"Failed to find PEM blob header: -----BEGIN CERTIFICATE-----"}}}
```

<u>Solution</u>

The database is very sensitive to file formats. If the certificate PEM file (``[certdog install]\config\sslcerts\dbssl.pem``) was saved as UNICODE, the database will not read it correctly. Open the certificate file and save as UTF-8 using a suitable text editor



<hr/>

### Get "CA does not have any certificates configured" when requesting a certificate

<u>Error Details</u>

The error message ``Error Generating Certificate``, ``Unable to process certificate request as the CA specified: IssuingCA1 does not have any certificates configured``   is displayed when attempting to request a certificate from a Microsoft CA  

Checking the log you see an entry such as:

```
There was an error whilst attempting to retrieve the CA certificates from the CA. Unable to obtain certificates from the CA. CCertAdmin::GetCAProperty: Access is denied. 0x80070005 (WIN32: 5 ERROR_ACCESS_DENIED)
```

which is reported from the agent when the Certificate Issuer is configured



<u>Solution</u>

This is a permissions issue. The account used by the agent does not have the correct permissions on the CA. To rectify, follow the guide here: https://krestfield.github.io/docs/pki/setting_adcs_template_permissions.html and also ensure that the account has **Issue and Manage Certificates** and **Request Certificates** permissions on the CA itself (managed via Properties)

One the permissions have been updated, delete the issuer and re-create. Check the logs for errors



<hr/>

### Using a PKCS11 token gives CKR_TOKEN_NOT_PRESENT or CKR_DEVICE_REMOVED

<u>Error Details</u>

After creating a PKCS11 Key Store, attempting to create a CA gives an error stating CKR_TOKEN_NOT_PRESENT e.g.

```
There was an error initialising: Token Exception: PKCS#11 Token: Unable to login to Token. CKR_DEVICE_REMOVED
```





<u>Solution</u>

This usually means that the hardware device (e.g. HSM) is not currently online or may not been configured correctly for this server  

Start the server (or re-connect)  

Run the vendor tools to confirm the device has been configured correctly and allows this client (where Certdog is running) to access it. Also ensure that the PKCS11 interface has been configured  

Ensure any environment variables have been set e.g. for Utimaco the ``CS_PKCS11_R3_CFG`` environment variable must be set. If you set this ensure you restart the services to pick up the change

If after making changes the error still occurs, stop and start the Krestfield CertDog Service as underlying processes can cache failed attempts and this cache can only be cleared via a restart



<hr/>

### DN Restrictions do not restriction wildards in Common Name

<u>Error Details</u>

Configure a DN restriction to Deny Wilcard Domains but domains such as *.org.com are still permitted in the Common Name (CN) field

<u>Solution</u>

Domains are not restricted in the Common Name field as this field is not checked to validate domains (for TLS certificates), rather this processing is carried out on the Subject Alternative Name extension

The CA Browser Forum Baseline Requirements have required the presence of the Subject Alternative Name extension since 2012, and use of the subject common name was deprecated in RFC 2818


<hr/>

### Cannot add wildcard IP Address to SAN

<u>Error Details</u>

Attempting to add a wildcard IP address to a SAN (such as \*.168.100.57) gives an error such as ``IP Address is invalid``  

It is neither possible to restrict wildcarded IP Addresses from the DN Restrictions

<u>Solution</u>

IP Addresses must be specified explicitly and cannot contain a wildcard  

RFC2818 states

```
In some cases, the URI is specified as an IP address rather than a 
hostname. In this case, the iPAddress subjectAltName must be present  
in the certificate and must exactly match the IP in the URI.
```

Note RFC6125 mentions that IP Addresses are out of scope as they are not reliable identifiers for application services

It is recommended that DNS domain names are used in place of IP addresses  

