---
layout: default
title: OCSP for SafeSign
parent: Certdog
nav_order: 213
---

# Configuring OCSP for SafeSign/Safetronic

> From version 1.8.0

<br>

## Overview

Safetronic is often configured to use an IdenTrust OCSP Revocation Checker  

IdenTrust use a 4-corner model which effectively means a relying party sends all OCSP requests to the same OCSP responder address (the one associated with your OCSP signing certificate) and the OCSP server redirects these requests to the Responder responsible. Rather than the standard approach where OCSP requests are sent to the responsible responder directly

OCSP requests must also be signed and the responder associated with the CA that issued this certificate validates that signature  

The combination of this is that only IdenTrust customers that are in possession of a valid OCSP signing certificate may make OCSP revocation checks  

Another deviation is that OCSP server signing certificates are issued from the Root CA  

This extra complexity means some additional configuration needs to be made in certdog to cater for this

<br>

### Configuration Steps

This is assuming a typical three tier PKI (Root CA, Intermediate CA and End-Entity certificates) with CAs and OCSP responders all hosted in certdog



In certdog you should have the two CAs configured e.g.:

* Root CA

* Issuing CA

For each of these, you may just check the **Create OCSP Server** option when configuring as this will create OCSP Servers and other required artefacts (Certificate Issuer, User etc.). But you can also create from scratch if preferred

<br>

Once created, the OCSP servers for these CAs should be configured as follows:

<hr>

<u>Root CA OCSP Server</u>

If you let certdog create this automatically, the following will all be configured by default:

* **Local CA** should refer to the Root CA

* **Certificate Issuer** should refer to a Certificate Issuer that uses the Root CA and an OCSP compliant Certificate Profile

An OCSP compliant Certificate Profile should include:

- **Digital Signature** Key Usage
- **OCSP Signing** Enhanced Key Usage
- **Include OCSP No Check** should be enabled

It's lifetime can be whatever you choose (certdog will handle the renewal of these certificates anyway)



Items that may need to be updated:

**Signing Cert DN**: You can leave this empty but specifying a DN may provide more meaningful information e.g. CN=Root OCSP Server 1, O=Organisation, C=GB

If using older versions of Safetronic, set the **Hash Algorithm** to **SHA1**. Older versions mandate this hash algorithm for OCSP responses

Set **Requests must be Signed** to **True**

**Next Update Period** should be **5 minutes** or less

<hr>

<u>Issuing CA OCSP Server</u>

The following should be configured:

* **Local CA** should refer to the Issuing CA

* **Certificate Issuer** should refer to a Certificate Issuer that uses the **Root CA** and an OCSP compliant Certificate Profile that has **Include OCSP No Check** set to **false**
  * To make this change from the defaults, edit the *Certificate Issuer* referenced and set the **Local CA Configuration** item to the **Root CA**. This is required as all OCSP signing certificates are issued from the Root CA
  * Note the *Certificate Profile* name then edit that profile ensuring that **Include OCSP No Check** is disabled. This is required so that this OCSP signing certificate will also be checked for revocation
  * Go back to the Issuing CA OCSP Server by choosing **Edit/View** and check the **Bypass Issuer Check** option. If this is not checked, next time any changes are made to the OCSP server you will receive an error (as by default the signing certificate should be issued from the associated CA - not the Root CA)  



You may also again, update the **Signing Cert DN** and if using older versions of Safetronic, also set the **Hash Algorithm** to **SHA1**

Set **Requests must be Signed** to **True**

**Next Update Period** should be **5 minutes** or less

<hr>

<br>

Once the changes have been made you may force the OCSP signing certificates to be renewed by checking the **Renew Certificate** option in the OCSP configuration

<br>

## Other Considerations

IdenTrust also host OCSP servers at https addresses (rather than the standard http). If you must replicate this, perform the following steps

From your certdog installation, locate the ``.\tomcat\crlwebapps`` folder and move the certdog.war file to the ``.\tomcat\webapps`` folder  

The OCSP services will then be available via the same https address  



