---
layout: default
title: EzSign Release Note
parent: EzSign
nav_order: 99
---

# RELEASE NOTE

### EzSign - Digital Signing Server



Documentation: [https://krestfield.github.io/docs/ezsign/ezsign.html](https://krestfield.github.io/docs/ezsign/ezsign.html)

Support: [support@krestfield.com](mailto:support@krestfield.com)

Web: [https://www.krestfield.com]


------------------------------------------------------------------------------
> Version: 4.3.0
> Release Date: 12 September  2024

Changes:
* Server can now be configured with a server side TLS certificate to secure communications from the client.
* Client can now be configured with a client-side TLS certificate to authenticate to the Server and client-side TLS can be enforced at the Server side.



------------------------------------------------------------------------------
> Version: 4.2.3
> Release Date: 12 April 2024

Changes:
* Thales payShield 10k support added including support for TLS.




------------------------------------------------------------------------------
> Version: 4.2.2
> Release Date: 11 December 2023

Changes:
* Update to relax the PKCS#7 signature's Encryption Algorithm checking, to allow sha256WithRSA etc. Extracting the signature part from this.



------------------------------------------------------------------------------
> Version: 4.2.1
> Release Date: 06 January 2023

Changes:
* Full support added for YubiHSM2
* Internal changes made to support Java 17 and later
* Several dependancies updated to latest versions, including Bouncy Castle, Google KMS and Log4j 
* Custom PKCS11 templates added to increase HSM support
* ezsign-manage improvements

Fixes:
* ezsign-manage could set the signing key ID on the wrong channel if the channels started with the same name

* Fix when attempt to get public key from HSM failed when importing a certificate

* Fix for public key comparison error (failure to import certificate)

* Fix for importing a certificate with the same key

* Translate keys temp directory naming fixed on Solaris

* ezsign-manage could set the signing key ID on the wrong channel if the channels started with the same name

* Fix when attempt to get public key from HSM failed when importing a certificate

* Fix for public key comparison error (failure to import certificate)

* Fix for importing a certificate with the same key

* Translate keys temp directory naming fixed on Solaris

  


------------------------------------------------------------------------------
> Version: 4.2.0
> Release Date:  06 June 2022

Changes:
* UPN added as option for Subject Alternative Names
* Added more direct integration methods
* Improved PKCS7 internal processing
* Added ContentSigner so external libraries can utilise EzSign for signing using their own libraries
* Removed internal (sun) classes
* Added saveObjectsToDisk channel property which allows objects to be stored in memory rather than written to disk, for use when integrating with the EzSign library directly

Fixes:
* None


------------------------------------------------------------------------------
> Version: 4.1.3
> Release Date: 04 February 2022

Changes:
* Google KMS now accepts JSON creds as a string, rather than as a file
* More information available if PKCS11 library cannot be loaded
* Updated nCipher support to accommodate the import of Microsoft CA keys
* More functions added to allow direct integration with the library allowing for external storing of keys and certificates

Fixes:
* Log4J version upped to 2.17.1
  
------------------------------------------------------------------------------
> Version: 4.1.2
> Release Date: 20 July 2020

Changes:
* Revocation checking updated to allow only checking of end-entity
* Relax path option added to OCSP revocation checking to support IdenTrust
* Any revocation checker added

Fixes:
* Added backwards compatibility for setting issuer DN in PKCS#7 in order
  to support Thales SafeSign
  
------------------------------------------------------------------------------
>  Version: 4.1.0
> Release Date: 30 June 2020

Changes:
* Support for Google KMS added
* Support for Azure Key Vault added

Fixes:
* None
  
------------------------------------------------------------------------------
> Version: 4.0.0
> Release Date: 6 May 2020

Changes:

* Elliptic curve (ECDSA) now supported
* SHA-3 hash algorithms now supported
* Support for Thales/Gemalto HSM on Demand added
* Support for Utimaco HSMs added
* Thales PayShield KeyBlock and LMK ID support added

Fixes:
* None
  
------------------------------------------------------------------------------
>  Version: 3.1.3
> Release Date: 2 Mar 2020

Changes:
* None

Fixes:
* Issue generating a CSR for PayShield using Java 8u161 and later resolved
  
------------------------------------------------------------------------------
>  Version: 3.1.2
> Release Date: 16 Sep 2019

Changes:
* None

Fixes:
* Importing existing keys from an nCipher HSM that had been generated using
    the Thales SafeSign tool failed

------------------------------------------------------------------------------
> Version: 3.1.1
> Release Date: 11 Mar 2019

Changes:
* Minor update to support Luna PKCS#11 HSM template

Fixes:
* None
  
------------------------------------------------------------------------------
> Version: 3.1.0
> Release Date: 21 Jan 2019

Changes:
* Support for AWS CloudHSM added
* Reliability enhancements to PKCS#11 interface
* Updated to use the latest dependencies
* Some security improvements
* Added Java 11 support

Fixes:
* Server would not start if OCSP signing key was not set
  
------------------------------------------------------------------------------
> Version: 3.0.0
> Release Date: 28 April 2018

Changes:
* Message and control comms between client and server can now be secured if the 
  client provides an authentication code and the same code is set on the server
* The Management Utility now has the ability to import existing keys from an HSM 
  including those previously managed by other systems such as Thales SafeSign
* The control server interface now starts before the main server and reports 
  "starting" whilst the server is in the startup phase
* Shutdown is now more graceful - stopping further messages, setting the status
  to "stopping" and then waiting for all processing to complete before 
  shutting down
* Master password can now be supplied via a file or system property as well as 
  via the command prompt
* Support for raw signature (PKCS#1) signatures added
* Support for AEP Keyper HSMs added
* Jar files now versioned
* Translate objects from current token password to new password added to the 
  Management Utility
* New option to switch off status control messages (to reduce logs filling up 
  when constantly monitoring)
* You can now decide whether to include signed attributes in a signature
  or not.  Previously, they were always included

Fixes:
* Several error messages clarified or corrected
* If two PKCS#11 objects had the same CK_ID obtaining the public key would fail
    when importing a certificate

------------------------------------------------------------------------------
> Version: 2.2.1
> Release Date: 14 September 2017

Changes:
* Added support for nCipher HSM module protection

Fixes:
* None
  
------------------------------------------------------------------------------
> Version: 2.2
> Release Date: 19 June 2017

Changes:
* Path check can now check weak signature hash separately from weak certificate hash
* Option added to ignore root certificate extension checks
* Added ability to specify a path check class for custom certificate path checking
* Management utility now displays whether a certificate is a root/intermediate or
  end-entity

Fixes:
* Management utility: The same token password was stored for all channels, now
  correctly stores per channel
* Corrected the properties spelling mistake, now server.ctrl.port from server.crtl.port

------------------------------------------------------------------------------
> Version: 2.1.1
> Release Date: 21 April 2017

Changes:
* None

Fixes:
* Minor update to client connection timings
  
------------------------------------------------------------------------------
> Version: 2.1
> Release Date: 1 April 2017

Changes:
* None

Fixes:
* If certificate did not contain key usage the error was reported as 
    unable to parse signature.  Now reports the correct error
* If content data was corrupt the error was reported as 34.  The correct
    error is now reported

------------------------------------------------------------------------------
> Version: 2.0
> Release Date: 24 March 2017

Changes:
* Symmetric encryption (AES) support added for PKCS#11 and Software tokens
* Basic Constraints checking now also checks the path length for any violation
* PKCS#11 operations can now run in parrallel, improving performance up to 10x
* ClientUtils methods expanded
* Updates to start/stop and management scripts
* Server properties can now be passed as system parameters
* Client server connectivity improved

Fixes:
* When two CA certificates had the same DN and issuer, path building occaisionally failed (when the wrong CA was selected and final validation failed)
  
------------------------------------------------------------------------------
> Version: 1.5
> Release Date: 26 January 2017

Changes:
* Transaction Id added to logs
* Added test certificates to initial setup
  

Fixes:
* None      
  
------------------------------------------------------------------------------
> Version: 1.4
> Release Date: 28 November 2016

Changes:
* Timeout added to client constructor
* OCSP caching added
* OCSP producedAt check added
* Optional certificate extension checks added (non repudiation, basic constraints)
* ClientUtils updated with more methods

Fixes:
* Re-enabled SSLv3 support as some OCSP servers are still at this level
* Fixed a path building error where intermediate certs would be removed from
  the path building process if not held locally 
  
------------------------------------------------------------------------------
> Version: 1.3
> Release Date: 24 October 2016

Changes:
* Logging enhanced to use Log4J2
* Upgraded server threading 
* PKCS#11 performance increased
* PKCS#11 auto-reconnection added
* Tested with Gemalto smartcards
* Deny weak hash option added
* OCSP timeout values are now configurable
* Generate random number function added    
  

Fixes:
* When control tool used to alter logging level, socket closed when under load
* PKCS#11 failed to locate a key when under load
* Server Manager failed to reload config when CSR generated
* Requested DN was reversed in the request
  
------------------------------------------------------------------------------
> Version: 1.2
> Release Date: 08 August 2016

Changes:
* Added management and control utilities
* Added further samples
  
------------------------------------------------------------------------------
> Version: 1.1
> Release Date: 8 March 2016

Changes:
* Added PKCS#11 support
* Added allow expired certs and CRLs
* Added OCSP signing
  
------------------------------------------------------------------------------
> Version: 1.0
> Release Date: 8 July 2015

Changes:
* Initial Release

  