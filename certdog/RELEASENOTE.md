---
layout: default
title: Release Note
parent: Certdog
nav_order: 10000
---

# RELEASE NOTE

### Certdog - Certificate Management and Automation System



Documentation: [https://krestfield.github.io/docs/certdog/certdog.html](https://krestfield.github.io/docs/certdog/certdog.html)

Support: [support@krestfield.com](mailto:support@krestfield.com)

Web: [https://www.krestfield.com](https://www.krestfield.com)



> **Version 1.6.0**
> **Release Date**: 31 January 2022
>
> **Updates**

* Certificate details now displays: key size (or curve name), thumbprint, policies, AIA and CDPs

* Revoked certificates are now displayed with a red outline

* Credentials cannot be deleted if in use

* When installing, the port can now be specified as well as the listening IP address

* CRLs are now hosted on an http site by default (previously they were https by default)

* Certificate search now retains number of certificates to display

* Additional email addresses can be added for cert issued and expiry reminder emails

* Emails can be suppressed for individual teams

* Saved searches are now available via a drop down and the search is executed as selected

* DN can now be entered as components (CN, O, OU etc.)

* Email sending can be switched off per server (in the case of multiple servers running)

* Admin users can navigate to team and user details from detailed certificate view

* Can now control access via IP address (including ranges and wildcards) per team

* Existing CA imports via PFX/P12 improved

* Microsoft CA certificate import improved and now stores template with certs when imported

* More efficient handling for large numbers of certificates (20k+)

  **Security Updates**:

  * Log4j2 version upped to 2.17.1
  * User disable and delay added for failed login attempts

  

**Fixes** 

* When Active selected in search - all certificates were returned
* If a CA P12 import password used the '£' character import failed. This was due to encoding in the PowerShell module
* The Certdog service failed to locate the API location on some installations (requiring a workaround) 
* P12 Import occasionally failed when mapping to a Key Store that had non-ASCII passwords 
* Once a Local CA is using a Key Store, the password could still be changed - this is now prevented
* Import Cert for a user (not admin) would produce an unauthorised response
* ADCS driver required a credential with local logon. This is no longer needed



---



> **Version 1.5.0**
> **Release Date**: 15 November 2021
>
> **Updates**

* The CA keys and certificates from existing ADCS (Microsoft CA) instances can now be migrated to Certdog, Including CAs using nCipher HSMs
* Local CAs can now be configured with specific Path Length constraints
* Local CA Cert Profiles now support the Basic Constraints extension
* Local CA and Cert Profiles now include the Certificate Policies extension
* A Sub CA CSR can now be generated for signing from an external CA
* Local CA CDP and CRL locations are now pre-populated
* The issuer certificate can now also be downloaded separately
* Certificate Profiles now have drop-down helpers - to select the most common key-usages etc. for a particular certificate type
* Certificate owners and teams can be changed via the UI
* Certificates can now be renewed rather than having to issue new
* Renewal URLs can now be included in expiry reminder and cert issued emails
* Filtered logs can now be downloaded
* Expiry monitoring can be disabled for a specific certificate
* My Issuers added - where users can obtain CA certs for the issuers they are permitted to use

**Fixes** 

* Cert chain (p7b) now also includes the end-entity certificate
* Unchecking all key usages in a Certificate Profile was not permitted. Now allowed
* If a certificate had no team an error was sometimes thrown when searching for certificates
* Certificate default search was set to not default when saved. Setting now retained



---




> **Version 1.4.1**
> **Release Date**: 6 August 2021
>
> **Updates**

* Logging can now also be directed to any log4j2 supported appender
* Force delete of key stores and local CAs added

**Fixes** 

* None




---




> **Version 1.4.0**
> **Release Date**: 19 July 2021
>
> **Updates**

* Local CAs can now utilise the follow key stores:
  * PKCS#11
    * including Thales Luna, AWS CloudHSM and Utimaco
  * Azure Key Vault
  * Google KMS
  * PKCS#12 (Software)
* Key stores, issuers and local CAs can now be recovered if accidentally deleted

**Fixes** 

* None




---




> **Version 1.3.0**
> **Release Date**: 17 June 2021
>
> **Updates**

* You can now build a hierarchy of Local CAs - with any path length
* Local CAs now produce CRLs
* Local CAs now include AIA and CDP extensions
* Certificates can be deleted from the Console
* Email reminders may be switched off for specific certificates
* Certificates can now be imported
* Other CAs can now be imported as a Local CA if provided as a PKCS#12
* OCSP No Check extension now available in cert profiles

**Fixes** 

* If email server settings were incorrect there would be a delay in obtaining a certificate (whilst the connection timed out). Emails are now sent in a separate queue




---




> **Version 1.2.0**
>
> **Release Date**: 25 March 2021
>
> **Updates**

* Users are now associated with teams
* Administrators can decided whether users see own certs, team certs all all of them
* Database is now installed as a service

**Fixes**

* Logout would log out all sessions from the same IP
* Key retention could not be set to zero




---




> **Version 1.1.0**
>
> **Release Date**: 15thFebruary 2021
>
> **Updates**:

* Support for PrimeKey's EJBCA Added
* Private Keys can now be stored for a configurable length of time
* There is now the ability to download a certificate in JKS and PEM formats, as well as PKCS#12
* Emails can now include a link to the certificate
* Extra information can now be stored with a certificate
* Additional emails can be set for a certificate so that those recipients are also emailed regarding issuance and expiry
* Certificate search improvements. More options available and searches can be stored and retrieved
* Teams are now supported. Users can be added to many teams. New Certificate Issuers can be automatically added to specific teams
* There are now two types of credential - username and password or just password

**Fixes**:

* CSR is now accepted even if it does not contain the correct PEM headers
* Corrected a bug in the email sending logic




---




> **Version 1.0.0**
>
> **Release Date**: 22 January 2021
>
> **Updates**: Initial Release
