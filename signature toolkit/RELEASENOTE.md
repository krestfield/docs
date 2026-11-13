---
layout: default
title: Release Note
parent: Signature Toolkit
nav_order: 1
---

# RELEASE NOTE

### Signature Toolkit  



Support: [support@krestfield.com](mailto:support@krestfield.com)

Web: [https://www.krestfield.com](https://www.krestfield.com)

---


> **Version 2.0.0**
> **Release Date**: 12th November 2026



**Updates**

* Added support for the post-quantum ML-DSA (FIPS 204) and SLH-DSA (FIPS 205) algorithms. Signatures and certificates using these algorithms can be viewed, verified and generated
* Now built on .NET 10. The .NET runtime is included in the installer, so the .NET Framework is no longer required
* New user interface, including a value preview pane, a detailed signature verification results window and a new certificate path display
* Signatures can now be generated using a certificate and key held in a PKCS#12 (.pfx / .p12) file, as well as from the Windows certificate store
* Added ECDSA and RSASSA-PSS signature generation, and a choice of binary (DER), PEM or Base64 output
* Detached signatures can be verified by supplying the signed content or its digest
* Signature verification now reports problems as well as the result. The signature algorithm identifier parameters are checked (NULL must be present for RSA and absent for ML-DSA, SLH-DSA and ECDSA), along with the signed attributes, the signer's certificate and weak algorithms. Where a signature is otherwise valid this is stated
* When a signature fails verification the reason is given together with the probable causes
* A verification report can be copied or saved for each signature
* The certificate path display shows whether each certificate came from the signature or from the Windows certificate store
* X.509 certificate files (.cer, .crt, .pem, .der) can be opened directly
* Timestamps, counter signatures, certificate extensions and public key details are now displayed
* The ASN.1 view is now built in and names the object identifiers it recognises
* New installer. Installing replaces any earlier version



**Fixes** 

* Signature generation corrected. Files are now signed exactly as stored on disk
* Viewing the signer certificate now works for all signers, not only the first
* Files containing duplicate certificates or CRLs, or a CRL with no next update time, now open correctly
* Signatures produced by some older signing products and smart cards, which previously failed to verify, are now verified
* A successful CRL signature verification is now reported
* Files are opened based on their content, whatever their file extension



**Changes**

* A signature whose certificate path is incomplete or untrusted is no longer reported as failing verification. The signature itself is verified, and the state of the certificate path is reported alongside as a warning
* Issuer certificates are no longer downloaded from AIA (Authority Information Access) locations when building certificate paths



---


> **Version 1.5.0**
> **Release Date**: 12th January 2024



**Updates**

* None
  



**Fixes** 

* ASN1 view failed if data was not imported as binary. Now works for Base64 and HEX



---


> **Version 1.4.0**
> **Release Date**: 23rd June 2022



**Updates**

* .NET Framework increased to 4.8
  



**Fixes** 

* Improved CSR generation



---


> **Version 1.3.9**
> **Release Date**: 10th February 2021



**Updates**

* .NET Framework increased to 4.7.2



**Fixes** 

* Corrected some signature parsing errors (where parsing would fail if some data items were not present)
* Corrected issue showing NULL when no key usage specified in a certificate
* Corrected an ASN1 generation issue - where this would fail if data had been pasted in 



---

> **Version 1.3.8**
> **Release Date**: 17th November 2016



**Updates**

* Some UI Updates

* Added export all certificates option

* Allowed URL encoded signatures to be imported

* Removed the license tool

  

**Fixes** 

* None



---

> **Version 1.3.6**
> **Release Date**: 30th November 2015



**Updates**

* First official release

  

**Fixes** 

* None



  <br>

