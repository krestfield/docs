---
layout: default
title: Available Parameters
parent: Certdog
nav_order: 1003
---

# Available Parameters

<br>

Workflows can execute scripts and pass parameters

Emails and Webhooks can also be passed parameters

These available parameters are listed below

(Note: All parameters are passed as strings)

<br>

* [CERTID]
  * The internal ID of the certificate
  * This uniquely identifies the certificate within the system, enabling other systems to make calls (e.g. using the REST API), specifying this ID to retrieve the certificate
* [CERTISSUER]
  * The name of the [Certificate Issuer](certificate_issuers.html)
  * This indicates what issuer provided the certificate e.g. TLS Certificates
* [CERTCSRB64]
  * A base64 string containing the CSR (PKCS#10) data
  * This can be used to parse the request before allowing issuance
* [CERTURL]
  * The full URL that will take a user to the certificate in the Console
  * E.g. if included in an email will provide a link for the user to click
* [CERTRENEWURL]
  * The URL that will take a user to the renewal page for the certificate
  * As above, can be included in emails to take the user to the renewal page
* [VALIDFROM]
  * The valid from date in the format: YYYY-MM-DD HH:MM:SS (e.g. 2026-05-15 13:04:44)
* [VALIDTO]
  * The valid to date in the format: YYYY-MM-DD HH:MM:SS (e.g. 2031-02-11 15:01:34)
* [SERIALNUM]
  * The serial number of the certificate
* [DAYSTOEXPIRY]
  * The number of days until the certificate expires
* [OWNERUSERNAME]
  * The username of the owner of the certificate
  * This may be the internal username, but if Active Directory or Azure Entra ID may be the UPN (e.g. fred.bloggs@certdog.com)
* [OWNEREMAIL]
  * The email associated with the user
* [CERTDATA]
  * The certificate data in PEM format (including header and footer)
  * This data can be set within emails but should not be passed as a parameter to scripts (use [CERTDATAB64] instead)

* [CERTDATAB64]
  * A one line string containing the certificate binary data encoded as base 64 (not including any headers or footers)
  * This data can safety be passed to scripts
  
* [CERTSUBJECT]
  * The DN of the certificate e.g. ``CN=Server Cert,O=Certdog,C=GB``

<br>
