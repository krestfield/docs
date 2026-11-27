---
layout: default
title: EzSign - Alignment to ISO 27001
parent: EzSign
nav_order: 320
---

# EzSign Alignment to ISO 27001

<br>

ISO/IEC 27001 certifies an organisation's Information Security Management System (ISMS), not individual products. There is therefore no "ISO 27001 mode" in EzSign, and installing EzSign does not by itself make a system compliant

What EzSign does provide are the settings needed to meet the technical controls in Annex A of ISO/IEC 27001:2022 that apply to a signing and encryption service. This page lists those controls, the EzSign settings that support each one and the configuration we recommend

The final decisions (e.g. which networks may connect, how long logs are kept, how often passwords are changed) belong to your organisation and should follow your own policies and risk assessment

The settings below are in the server properties file. Replace ``channel.N`` with the number of your channel. For full details of each setting see [EzSign Properties](ezsign_properties.html)

Some settings are only available from version **4.6.0**. These are marked where they appear

<br>

## Summary

| Annex A Control | Title | How EzSign supports it |
| --------------- | ----- | ---------------------- |
| 8.24 | Use of cryptography | HSM and cloud KMS key storage, configurable algorithms, key sizes and hashes |
| 8.20, 8.21, 8.22 | Network security | Bind addresses, source IP allow lists, TLS on all interfaces |
| 5.15, 8.3 | Access control and information access restriction | Per-channel roles on the REST API, authentication codes, Control interface restrictions |
| 8.5 | Secure authentication | API tokens, TLS client certificates |
| 5.17 | Authentication information | Passwords encrypted with the master password, API tokens stored only as hashes |
| 8.2 | Privileged access rights | Master password, signed users file |
| 8.9 | Configuration management | Controlled properties and users files, signed users file |
| 8.15, 8.16 | Logging and monitoring | Log levels, REST request logging, Control status monitoring |
| 8.8 | Management of technical vulnerabilities | Security Advisories, supported Java versions |
| 8.13 | Information backup | Configuration backup, HSM key backup |
| 8.32 | Change management | Upgrade guidance, classpath checks |
| 8.11, 8.12 | Data masking and data leakage prevention | Message logging off by default |

Each control is described below

<br>

## 8.24 Use of Cryptography

**Store keys in hardware**

For production channels, keep signing and encryption keys in an HSM or cloud KMS rather than the software key store:

```
channel.N.tokenType=PKCS11
```

Supported token types are **PKCS11** (e.g. nCipher, Thales Luna, Utimaco, AWS CloudHSM), **PAYSHIELD**, **GOOGLEKMS** and **AZUREKEYVAULT**. See [HSM Support](hsm_support.html)

The **SOFTWARE** token type encrypts keys with AES but keeps them on disk. Use it only for testing or where your risk assessment accepts software key protection

If using Google KMS, create keys with HSM protection:

```
channel.N.token.googleKms.keyProtectionLevel=HSM
```

If using a PKCS#11 HSM, ``channel.N.token.useModuleProtection=true`` means no operator logon is needed to use the keys. Consider whether this is acceptable under your key management policy before enabling it

<br>

**Use current algorithms**

Set the algorithm and key size for each channel (see [EzSign Algorithms](ezsign-algorithms.html)) e.g.

```
channel.N.signature.algorithm=RSA
channel.N.signature.keySize=3072
channel.N.signature.hash=SHA256
```

We recommend:

* RSA keys of at least 2048 bits (3072 bits or more for keys with a long lifetime)
* ECDSA with the ``secp256r1`` curve or stronger
* ML-DSA (``ML-DSA-44``, ``ML-DSA-65`` or ``ML-DSA-87``) where post-quantum signatures are needed
* SHA-256 or stronger for the signature hash. Do not use **SHA1** for new signatures
* SHA-256 or stronger for signed OCSP requests (``channel.N.revocationChecker.ocsp.signatureHash``)

<br>

**Verify signatures fully**

Enable revocation checking on channels that verify signatures:

```
channel.N.revocationChecker.type=ANY
```

Avoid ``NONE`` in production. From version 4.6.0 certificate path checks follow RFC 5280 and RFC 6960 closely. Leave the ``relax...`` settings (e.g. ``channel.N.verify.relaxAllCertExtensionChecks``) at their default of **false** unless there is a documented reason. See [Certificate Path Checking](ezsign_server.html#the-risks-of-relaxing-these-checks)

Keep ``channel.N.revocationChecker.ocsp.ignoreSSLErrors`` and ``channel.N.revocationChecker.crl.ignoreSSLErrors`` set to **false**, so that revocation information is only fetched from trusted servers

<br>

## 8.20, 8.21, 8.22 Network Security

**Bind to specific interfaces**

By default EzSign listens on all interfaces. Bind each interface to the address it should be reached on:

```
server.bindIpAddress=10.100.15.32
server.restapi.bindIpAddress=10.100.15.32
server.ctrl.bindIpAddress=127.0.0.1
```

<br>

**Restrict which hosts can connect**

List the application servers that may connect. If these are omitted, any host can connect to the socket interface and the REST API:

```
server.allowedSourceIpAddresses=10.100.15.40,10.100.15.41
server.restapi.allowedSourceIpAddresses=10.100.15.40,10.100.15.41
server.ctrl.allowedSourceIpAddresses=127.0.0.1
```

Also restrict these ports with host or network firewalls, as a second layer

<br>

**Encrypt traffic**

Use TLS on every interface that crosses a network. For the socket interface:

```
server.useTls=true
server.useClientTls=true
server.tls.protocols=TLSv1.3,TLSv1.2
```

When ``server.useClientTls=true``, set ``tls.trustStore.filename`` to a trust store holding only the CA(s) that issue your client certificates. Otherwise Java's default ``cacerts`` is used and any certificate from a public CA would be accepted

For the REST API (version 4.6.0 and later), HTTPS is on by default. Leave it on:

```
server.restapi.useTls=true
server.restapi.tls.protocols=TLSv1.3,TLSv1.2
```

For a Thales payShield, enable TLS between EzSign and the HSM with ``channel.N.token.payShield.useTls=true``. See [payShield TLS Configuration](payshield_tls_configuration.html)

See [Configuring TLS](configuring_tls.html) for setting up the certificates

<br>

**Separate the service**

Place the EzSign Server and its HSMs on a network segment that only the applications that use them can reach. Use separate channels (each with its own keys) to keep different applications or data classifications apart

<br>

## 5.15, 8.3 Access Control and Information Access Restriction

**REST API**

Every REST API user is given roles, and each role grants operations on named channels only e.g.

```
"roles": {
  "finance-signer": ["sign:channel/FINANCE", "verify:channel/FINANCE"]
}
```

Grant each application only the operations and channels it needs. A user with no roles can authenticate but cannot do anything. See [REST API Users File](rest_api_users_properties.html)

<br>

**Socket interface**

Set an authentication code so that only clients holding it can use the server. Set it with the [Management Tool](ezsign_management_tool.html):

```
server.authCode=...
```

The client must pass the same code to the ``EzSignClient`` constructor. Without it, messages are sent in the clear

<br>

**Control interface**

The Control interface can pause, resume and stop the server. Bind it to ``127.0.0.1`` (or a management network), restrict it with ``server.ctrl.allowedSourceIpAddresses`` and set an authentication code:

```
server.ctrl.authCode=...
```

See [EzSign Control](ezsign_control.html)

<br>

## 8.5 Secure Authentication

For the REST API, prefer TLS client certificates over API tokens for system-to-system access:

```
server.restapi.tls.trustStore.filename=/opt/ezsign/client-ca.p12
server.restapi.tls.clientAuth=required
```

The REST API trust store should hold only the CA(s) that issue your client certificates. Java's ``cacerts`` file is never used for it

If API tokens are used, generate them with the Management Tool (they are 32 random bytes), give each system its own token and label it, so that one can be removed without affecting others

<br>

## 5.17 Authentication Information

* Set all passwords (master, token, key store and trust store) with the [Management Tool](ezsign_management_tool.html). They are stored in the properties file encrypted with the master password, not in the clear
* Use a strong, unique master password and keep it in your organisation's password vault
* Change passwords and API tokens in line with your password policy, and when someone who knew them leaves
* REST API tokens are stored only as SHA-256 hashes, and the Management Tool shows a new token only once. Store it securely when it is shown
* If proxy authentication is used for OCSP or CRL downloads, use a service account that has no other access

<br>

## 8.2 Privileged Access Rights

The master password allows all of the server's configuration to be changed. Limit it to the administrators who need it

From version 4.6.0, require the REST API users file to be signed by an admin key:

```
server.restapi.usersFile.signerCerts=/opt/ezsign/admin1.pem,/opt/ezsign/admin2.pem
```

Someone who can edit the users file then cannot give themselves access without an admin's private key. List at least two admin certificates so that the admin key can be changed without a break. See [Signing the Users File](ezsign_management_tool.html#signing-the-users-file)

Run the EzSign service under a dedicated service account with no interactive logon, rather than as root or an administrator

<br>

## 8.9 Configuration Management

* Treat the properties file, ``log4j2.xml``, the users file and its ``.sig`` file as controlled configuration items
* Restrict file permissions on these files and on ``keyStoreDir`` to the service account and administrators
* Keep a reviewed, versioned baseline of the configuration, and compare against it after changes
* Document any ``relax...`` setting that has been enabled, and why

<br>

## 8.15, 8.16 Logging and Monitoring

Set the log level to record errors, warnings and events:

```
log.level=3
```

Level **4** (debug) is useful for fault finding but produces a large volume of output. Return to level 3 afterwards. The level can be changed while the server runs using [EzSign Control](ezsign_control.html)

For the REST API, keep request logging on. One line is logged per request (user, operation, channel, result and time taken). Request bodies are never logged:

```
server.restapi.logRequests=true
```

Configure ``log4j2.xml`` to keep logs for the period your policy requires and to forward them to your SIEM. See [EzSign Server](ezsign_server.html). We suggest alerting on:

* Authentication failures and refused connections
* The users file being refused when it is loaded (e.g. an invalid signature)
* The server stopping, pausing or failing to reach its HSM
* Warnings that a relaxed check has accepted a certificate

Use the ``status`` action of EzSign Control for health monitoring. If this is polled often, ``server.ctrl.logStatusMessages=false`` stops it filling the logs

<br>

## 8.11, 8.12 Data Masking and Data Leakage Prevention

Message logging records the data being signed, encrypted or decrypted. Keep it off in production:

```
server.logMessages=false
```

This is the default from version 4.6.0 (before 4.6.0 it defaulted to **true**, so set it explicitly on older versions)

Set ``server.restapi.maxRequestSize`` to the largest request your applications need

<br>

## 8.8 Management of Technical Vulnerabilities

* Keep EzSign up to date. Release notes are in [RELEASENOTE](RELEASENOTE.html)
* Keep the Java runtime patched. See [EzSign Java Versions](ezsign_java_versions.html) for the supported versions
* Keep HSM firmware and client software patched, following your HSM vendor's guidance
* Check our [Security Advisories](../security/) for guidance on vulnerabilities that affect EzSign

<br>

## 8.13 Information Backup

* Back up the properties file, ``log4j2.xml``, the users file and its signature
* If using the software key store, back up ``keyStoreDir`` and protect the backup as you would the keys
* For HSM keys, use your HSM vendor's secure backup mechanism (e.g. nCipher Security World backups, Luna backup HSMs). Cloud KMS keys are protected by the provider
* Test restoring to a non-production server

<br>

## 8.32 Change Management

* Test configuration changes and upgrades on a non-production server first, using a sample of your real signatures and certificates
* When upgrading, replace the whole ``EzSignServer/lib`` folder. To stop the server starting if old jars are left behind (version 4.6.0 and later):

```
server.failOnClasspathConflicts=true
```

* See [Upgrading to 4.6](ezsign_upgrading_to_4.6.html) for the checks introduced in that version

<br>

## Checklist

A quick check of a production server:

| Check | Setting |
| ----- | ------- |
| Production keys are in an HSM or cloud KMS | ``channel.N.tokenType`` is not SOFTWARE |
| Signature hash is SHA-256 or stronger | ``channel.N.signature.hash`` |
| Revocation checking is on | ``channel.N.revocationChecker.type`` is not NONE |
| No relaxed checks without a documented reason | ``channel.N.verify.relax...`` are false |
| Interfaces bound to specific addresses | ``server.bindIpAddress``, ``server.restapi.bindIpAddress``, ``server.ctrl.bindIpAddress`` |
| Source IP allow lists set | ``server.allowedSourceIpAddresses``, ``server.restapi.allowedSourceIpAddresses``, ``server.ctrl.allowedSourceIpAddresses`` |
| TLS on the socket interface | ``server.useTls=true``, ``server.useClientTls=true`` |
| TLS on the REST API | ``server.restapi.useTls=true`` |
| Authentication codes set | ``server.authCode``, ``server.ctrl.authCode`` |
| REST API users file is signed | ``server.restapi.usersFile.signerCerts`` |
| Message logging is off | ``server.logMessages=false`` |
| Log level records events | ``log.level=3`` |
| Logs forwarded to SIEM | ``log4j2.xml`` |
| EzSign and Java are up to date | |

<br>

<hr>

Need more info? Contact us at [support@krestfield.com](mailto:support@krestfield.com)  

Or take a look at [our website](https://www.krestfield.com/ezsign)
