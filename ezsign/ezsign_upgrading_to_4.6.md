---
layout: default
title: EzSign - Upgrading to 4.6
parent: EzSign
nav_order: 98
---

# Upgrading to EzSign 4.6

<br>

Version 4.6.0 makes signature verification and revocation checking follow the standards (RFC 5280 for certificates, RFC 6960 for OCSP) more closely. As a result, some signatures, certificates, CRLs or OCSP responses that were accepted before may now be refused. This page lists the issues you are most likely to see after upgrading, the error you will see, and what to do

Each new check can be switched off with a setting in the server properties file. Before switching a check off, consider why it failed: the check is there because accepting the certificate or response carries a risk. Switching a check off is a decision for your organisation. The risks of each are described in [Certificate Path Checking](ezsign_server.html#the-risks-of-relaxing-these-checks)

In the settings below, replace ``channel.1`` with the number of your channel

This page will be updated as more is learnt from upgrades

<br>

## Before upgrading

* **Replace the whole ``EzSignServer/lib`` folder** with the new one. Do not copy the new jars into the existing folder (see [Jar or class errors](#jar-or-class-errors) below)
* Keep a copy of your current properties file and ``lib`` folder, so you can go back if needed
* Test signature verification with a sample of your real signatures and certificates before upgrading production. Most of the issues below show up the first time a signature is verified

<br>

## Jar or class errors

**What you see** - errors such as these in the logs, often only when a particular operation is carried out:

```
java.lang.NoSuchMethodError: 'void com.krestfield.ezsign.KRevocationException.<init>(java.lang.String, com.krestfield.ezsign.KRevocationException$Reason)'
java.lang.NoClassDefFoundError: ...
```

or, from version 4.6.0, when the server starts:

```
ERROR Classpath conflict: com.krestfield.ezsign.KRevocationException is in 2 places (the copies differ): .../lib/ezsign-4.6.0.jar, .../lib/ezsign-client-4.4.0.jar. Either copy may be loaded, ...
```

**Why** - the server and Management Tool scripts load every jar in the ``lib`` folder. If a jar from the previous version is still there, or a jar has been copied in from elsewhere, the same class can be in two jars at different versions and either may be loaded. Older EzSign client jars contained classes with the same names as the server's, so a client jar in the server's ``lib`` folder causes exactly this

**What to do** - remove the out of date jar named in the error, or replace the ``lib`` folder with the one from the 4.6.0 release. The EzSign client jar is for client applications and is never needed in the server's ``lib`` folder

The Management Tool prints the same warning when it starts. From version 4.6.0 it also needs the ``ezsign-users`` jar, which is in the server's ``lib`` folder. If you run the Management Tool on another machine, copy the whole ``lib`` folder

To stop the server starting at all when there is a conflict, set:

```
server.failOnClasspathConflicts=true
```

<br>

## Signer certificates with the client authentication (or another non-signing) extended key usage

**What you see**

```
The signer certificate CN=... has the extended key usages [1.3.6.1.5.5.7.3.2], none of which is allowed for signing. Allowed are [...] (set with allowedExtendedKeyUsages). Set relaxExtendedKeyUsageChecks=true to allow this
```

**Why** - RFC 5280 (section 4.2.1.12) says that if a certificate has the extended key usage extension, it must only be used for the purposes listed. Client authentication (``1.3.6.1.5.5.7.3.2``) is for TLS client authentication, and server authentication (``1.3.6.1.5.5.7.3.1``) for TLS servers, not for signing. Some CAs issue certificates with only these purposes that are then used for signing (e.g. smart card certificates). Version 4.6.0 rejects them. Certificates without the extended key usage extension are not affected

The purposes accepted by default are: any extended key usage, email protection, code signing, document signing, Microsoft document signing and Adobe authentic documents trust

**What to do** - preferably, have the certificates reissued with a signing purpose. Otherwise, add the purpose to the accepted list. The setting **replaces** the default list, so include the defaults as well. For example, to also accept client authentication:

```
channel.1.verify.allowedExtendedKeyUsages=2.5.29.37.0,1.3.6.1.5.5.7.3.4,1.3.6.1.5.5.7.3.3,1.3.6.1.5.5.7.3.36,1.3.6.1.4.1.311.10.3.12,1.2.840.113583.1.1.5,1.3.6.1.5.5.7.3.2
```

Or, to accept any extended key usage (a warning is logged each time a certificate would have been rejected):

```
channel.1.verify.relaxExtendedKeyUsageChecks=true
```

See [Allowed extended key usages](ezsign_server.html#allowed-extended-key-usages)

<br>

## Certificates with a critical extension EzSign does not process

**What you see**

```
The certificate CN=... has the critical extension 1.3.6.1.4.1.12345.1, which is not supported. It can also be added to allowedCriticalExtensions. Set relaxCriticalExtensionChecks=true to allow this
```

**Why** - RFC 5280 (section 4.2) says a certificate with a critical extension that is not recognised must be rejected. A CA marks an extension critical when the certificate must not be used by software that does not understand it, e.g. policy constraints or a private extension. The root certificate is not checked

**What to do** - if you know the extension and it is safe to ignore, add its OID (shown in the error) to the list. This is the narrowest option:

```
channel.1.verify.allowedCriticalExtensions=1.3.6.1.4.1.12345.1
```

The extension is still not processed; the certificate is just no longer rejected for carrying it. To accept every unknown critical extension instead (a warning is logged each time):

```
channel.1.verify.relaxCriticalExtensionChecks=true
```

See [Allowed critical extensions](ezsign_server.html#allowed-critical-extensions)

<br>

## Certificates that break a CA's name constraints

**What you see**

```
The certificate CN=... breaks the name constraints of its issuing CA. ... Set relaxNameConstraints=true to allow this
```

**Why** - a CA certificate can restrict the names of the certificates below it (e.g. to one organisation's domain or directory names). Before 4.6.0 these restrictions were ignored. The subject name, email addresses and subject alternative names are now checked against them

**What to do** - check the certificate was issued correctly. To accept it anyway:

```
channel.1.verify.relaxNameConstraints=true
```

<br>

## A CA certificate used as the signer

**What you see**

```
The signer certificate CN=... is a CA certificate (basic constraints CA is true). Set relaxCaSignerCheck=true to allow this
```

**Why** - a CA key should only issue certificates and CRLs. Self-signed signer certificates are not affected

**What to do** - sign with an end-entity certificate. To accept it anyway:

```
channel.1.verify.relaxCaSignerCheck=true
```

<br>

## CRL problems

**A CRL issuer without the CRL Sign key usage**

```
The CRL issuer CN=... does not have the CRL sign key usage set. Set relaxCrlSignCheck=true to allow this
```

The certificate that signs a CRL must have the *CRL Sign* key usage (RFC 5280 section 4.2.1.3). To accept it anyway:

```
channel.1.revocationChecker.crl.relaxCrlSignCheck=true
```

**A CRL without a next update time**

```
The CRL issued by ... has no nextUpdate, so it cannot be checked as current
```

Without a next update time there is no way to tell a CRL is out of date, so it is refused. This cannot be switched off; the CA must issue CRLs with a next update time

**Expired CRLs refused when allowExpiredCrl is set**

```
CRL obtained was not valid.  It expired on ... Allow expired CRLs is true but the CRL expired outside of the allowed N days
```

Before 4.6.0, when ``allowExpiredCrl=true`` was set, **any** expired CRL was accepted, however long ago it expired, because of a bug in the check. ``allowExpiredCrlForDays`` is now applied correctly. If you see this error, the CRL has been out of date for longer than you allowed: fix the CRL publication, or (temporarily) increase the number of days

<br>

## OCSP problems

**Old OCSP responses without a next update time**

```
The OCSP response has no nextUpdate and its thisUpdate (...) is more than 60 minutes in the past. To change this set maxAgeWithoutNextUpdateMins
```

A response without a next update time was accepted at any age, so an old response could be replayed. It is now only accepted for 60 minutes after its ``thisUpdate`` time. If your OCSP responder returns cached responses without a next update time, increase the limit (or set 0 to accept any age, as before):

```
channel.1.revocationChecker.ocsp.maxAgeWithoutNextUpdateMins=240
```

**OCSP responses signed by a certificate that is not trusted**

```
Validation of the OCSP signer certificate failed as a valid issuer could not be found. The wrong certificate may be signing the response. ...
```

Before 4.6.0 a fallback accepted the OCSP signer certificate without checking it was trusted. This has been removed. The response must be signed by the CA that issued the certificate being checked, or by a certificate that CA issued (RFC 6960). If your responder's certificate is issued by another trusted CA (e.g. a root CA, as with some IdenTrust responders), set:

```
channel.1.revocationChecker.ocsp.relaxSigningPath=true
```

**ignoreSSLErrors now only applies to that channel**

Before 4.6.0, ``ignoreSSLErrors=true`` on an OCSP or CRL checker changed the TLS settings for the whole Java process, so it also (silently) applied to every other HTTPS connection, including other channels. It now only applies to that checker's own connections. If another channel's OCSP or CRL downloads start failing with TLS certificate errors after the upgrade, they were relying on this side effect: set ``ignoreSSLErrors`` on that channel too, or better, trust the server's certificate

<br>

## Signatures that are now refused

**Raw signatures using SHA-1 or MD5**

```
... is weak and has therefore been rejected.  To permit this algorithm set the denyWeakSignatureHash property to false
```

The hash used in raw RSA signatures was not checked before. It is now checked as for PKCS#7 signatures. To accept SHA-1 or MD5 signatures:

```
channel.1.verify.denyWeakSignatureHash=false
```

**PKCS#7 data with no signers**

```
The signature does not contain any signers
```

A PKCS#7 structure with no signers (such as a ``.p7b`` certificate bundle) was reported as a verified signature. It is now refused. This cannot be switched off

<br>

## Server and socket interface changes

These do not need any action, but may be noticed:

* **Messages are no longer logged by default** - ``server.logMessages`` now defaults to false (it was true). Set it to true if you relied on the messages being in the log. They can contain the data being signed or decrypted
* **Large messages are refused** - messages longer than ``server.maxMessageSize`` (64M characters, about 48MB of data) are refused with an error. Increase the setting if you send larger data
* **An empty allowed address list now allows every client** - if ``server.allowedSourceIpAddresses`` is present but empty, every client can connect (as when it is omitted). Before 4.6.0 an empty value refused every client. IPv6 addresses in the list now also work
* **Clients receive error replies** - some errors (e.g. a request that could not be parsed) used to close the connection without a reply. The client now receives the error. Existing clients handle this without changes

<br>

## Signatures created by 4.6.0

RSA signatures now include the NULL parameter in the signature algorithm, as RFC 3370 requires (it had been left out since an earlier change). All standard verifiers accept both forms, and EzSign continues to verify signatures created by earlier versions. No action is needed
