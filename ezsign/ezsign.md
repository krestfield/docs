---
layout: default
title: EzSign
nav_order: 2
has_children: true
---
# EzSign

<br>

The Krestfield EzSign suite enables applications to quickly generate and verify digital signatures or encrypt and decrypt data without the need for complex programming	

It provides the following key features:

<br>
### Compliant Signature Generation and Verification

The server produces PKCS#7 compliant signatures (RSA or Elliptic Curve), which include signed attributes and the certificate chain. The SHA-1, SHA-2 and SHA-3 suite of digest algorithms are supported

The server performs full signature validation including path building and revocation checking, supporting both CRL and OCSP revocation checking

OCSP validation also supports the signing of OCSP requests and the inclusion of the correct Service Locator extension for use with the IdenTrust OCSP four corner model

Support for proxies to access CRL and OCSP servers is also supported, including proxies requiring authentication

<br>

### AES Encryption and Decryption

AES keys of 128, 196 or 256 bits can be generated for encryption/decryption purposes. Data is encrypted using CBC (Cipher Block Chaining) and a random IV (Initialisation Vector) is generated for each and every encryption operation, ensuring the data is secured to the maximum level

<br>

### Multi Token Support

The server supports several mechanisms for secure key storage, including:

* Cloud Based HSMs (including AWS Cloud HSM, Google KMS and the Thales DPoD Cloud HSM)

* PKCS#11 based HSMs (such as the nCipher and Thales/Gemalto Luna range)

* Thales PayShield HSMs (including the 10k)

* Software
  * For testing or applications that do not require hardware key protection, a software key store may be used. Keys and certificates are AES encrypted

<br>
### Java based

The server is completely java based, and supports Java versions 8 onwards

<br>

### Simple Client API

A thin java or .NET client is available with a simple interface to the server enabling rapid integration. You can start to generate signatures by writing only two lines of code

<br>

### Multi-Channel

The server provides key separation and the ability to support different configuration options per channel e.g. one channel can use a software key store whilst another makes use of an HSM, all from the same server

The number of channels is not limited (technically or by license)

<br>

<br>

## Technical Specifications

Signature Formats:

* Raw Signatures

* PKCS#7 Signatures

  

Algorithms:

* RSA
* ECDSA
* AES
* SHA-2 and SHA-3 algorithms



Interfaces

* REST API
* .NET
* Java



HSM Support

* nCipher
* Thales Luna
* Utimaco
* AWS CloudHSM
* Azure KeyVault
* Google KMS
* Thales PayShield

<hr>

Need more info? Contact us at [support@krestfield.com](mailto:support@krestfield.com)  

Or take a look at [our website](https://www.krestfield.com/ezsign-tool)

