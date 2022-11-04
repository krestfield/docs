---
layout: default
title: OCSP
parent: Certdog
nav_order: 212
---
# OCSP

> From version: 1.8.0

<br>

Certdog provides OCSP services for local CAs  

When creating a Local CA, if you check the **Create OCSP Server** option an OCSP server will be created and configured  

By default the OCSP server will be located at the following URL

```
http://[server name]/certdog/ocsp
```

This is the value that should be added as the AIA OCSP Location for certificates issued from the CA. This value will be populated when you select the *Create OCSP Server* option  

When an OCSP server is created in this way the following are automatically generated:

* An OCSP Server. You can view configured servers from the Local CAs - OCSP Servers menu item
* A Certificate Profile. This profile will be configured to issue OCSP signing certificates
* A Certificate Issuer. This will combine the profile above with the local CA - so that the CA is able to issue OCSP signing certificates
* A User and a Team. The user will be a member of the team and the team will only have permissions to request certificates from the Certificate Issuer mentioned above. The user account will be used by the OCSP server to authenticate to Certdog and request a signing certificate

With the above items in place an OCSP server will automatically obtain a signing certificate from the CA. This certificate will be auto-renewed  

If you wish to create an OCSP server manually, or alter the default settings. Navigate to the **Local CAs, OCSP Servers** menu item. Click **Add New OCSP Server** to create a new server from scratch, or select an existing item and select **View/Edit**  

<br>

### OCSP Server Settings

The following settings are available for each OCSP Server

<br>

* Server Name
  * This is simply the OCSP Server name. It can be changed without affecting any functionality
  
* Enabled
  * If not enabled the OCSP server will not process any OCSP requests. Unauthorized will be returned
  
* For Local CA
  * This is the CA this OCSP Responder is connected with. The status (revoked or good etc.) of certificates issued from this CA will be returned by this responder
  

<br>

<u>Signing Certificate Renewal Details</u>

This section contains details about the OCSP signing certificate, including where to obtain it from, what to name it and when to renew

* URL
  * This is the Certdog API URL that the OCSP server will use to request certificates. It will be of the form ``https://[certdog server]/certdog/api`` 

* Certdog Username

  * This is the username of the account that has permissions to request the OCSP signing certificate. If the OCSP was created automatically this user account would have been generated for you. If you wish to configure this yourself, use an account that has permissions on the Certificate Issuer which will provide the correct OCSP Signing certificates

* Certdog Password

  * This is the password associated with the account name mentioned above

* Certificate Issuer

  * This is the Certificate Issuer. If the OCSP was created automatically this issuer would have been generated for you. If you wish to create this yourself, the issuer must be associated with the same CA that this responder is serving and be configured with an OCSP compliant Certificate Profile

* Bypass Issuer Check
  * By default the Certificate Issuer must be associated with the same CA as set for Local CA i.e. you obtain an OCSP signing certificate from the CA whose status is being provided by the OCSP server. In some cases you may want to issue an OCSP signing certificate from another CA or the root CA. If this option is checked it will then allow these configurations
* Signing Cert DN

  * If you wish for the OCSP Signing certificate to have a specific DN, you may set it here. If this is left empty a default DN will be created of the form: ``CN=OCSPServer-[CA Name]-[ID]``

* Renew at
  * This is the percentage of life remaining on the OCSP Signing certificate at which it will be renewed. For example, if you set this to 50. When the current signing cert has 50% of its lifetime remaining, it will be renewed. 
* Current Signing Certificate
  * This provides a link to the current OCSP signing certificate in use

* Renew Certificate
  * If this option is checked, the current OCSP signing certificate will be renewed at the next expiry check (which by default is every minute) whether it is currently expiring or not. Check this option if you have made changes to the certificate details such as Certificate Issuer or Signing Cert DN and wish to force a renewal 


<br>

<u>Key Store and Signing Algorithm Details</u>

* Key Store
  * This is the Key Store where the responder will store its own signing keys. By default the same Key Store as used by the CA is selected, but another can be configured
* Algorithm
  * The algorithm that will be used to sign OCSP responses (this also dictates what algorithm the signing certificate will use)
* Key Size
  * The key size of the signing certificate if RSA is selected as the Algorithm
* Curve
  * The ECC curve. If ECDSA is selected as the Algorithm

* Hash Algorithm
  * This is the hash algorithm that will be used when signing OCSP responses and not the algorithm that will be included in the signing certificate (as this is dictated by the issuing CA). Some systems require a specific hashing algorithm to be configured

<br>

<u>Other Settings</u>

* Respect Number Once
  * If this is checked, if a Number Once value is provided in the OCSP request, that same value will be returned in the response. This option is often employed by clients to ensure that the OCSP response is freshly generated

* Requests must be signed
  * If this option is checked then OCSP requests must be signed and will be rejected (with an Unauthorized response) otherwise

* Next Update Period
  * This is the time that will be added to the *Produced At* period of the OCSP response, and is essentially the validity of the response

* Time Skew
  * If there are any clock deviations between clients and the OCSP Server, you may set this value to allow a time skew (in seconds). E.g. if you set this value to 5 then the produced at date of the OCSP response will be NOW minus 5 seconds and the response's expiry date (Next Update) will be EXPIRY TIME plus 5 seconds


<br>

### Operational Notes

Although they run on the same server by default, OCSP Servers run independently of Certdog. This is to allow for the OCSP Server to run on a separate machine to the Certdog instances. E.g. you may wish to run your OCSP servers in a more accessible environment and load-balance

It is for this reason that the Certdog URL, Username and Password need to be set above - as the Certdog instance providing the certificates may not always be on the same machine

<br>

### OCSP Certificate Profile

If you wish to create your own Certificate Profile for an OCSP server you must configure the following:

* Key Usage
  * This must include the **digital signature** key usage
* Enhanced Key Usage
  * This must include the **OCSP Signing** option

Optionally, you may set Include **OCSP No Check**. This indicates to the client that the OCSP signing certificate itself should not be OCSP checked. If this is not set, then the client may then carry out an additional OCSP check on the OCSP signing certificate itself
