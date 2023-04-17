---
layout: default
title: EzSign - HSM Support
parent: EzSign
nav_order: 40
---



# EzSign Key Store and HSM Support

> From version 4.2.1

Note: For previous versions contact [support](mailto:support@krestfield.com)



EzSign supports the following HSMs and Key Stores:



### Via the PKCS#11 Interface

The following HSMs are supported via the [pkcs#11](http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/os/pkcs11-base-v2.40-os.html) interface. You must set the corresponding ``model`` property (as indicated below) for the specific HSM

- EnTrust nCipher nShield range
  - ``token.pkcs11.model=NCipher``

    *Tested: nShield Connect 500+, nShield Edge*

- Thales Luna range
  - ``token.pkcs11.model=Luna``

    *Tested: Luna 6*

- Utimaco
  - ``token.pkcs11.model=Utimaco``

    *Tested: Utimaco simulator*

- Thales DPoD Cloud HSM
  - ``token.pkcs11.model=Luna``

    *Tested: Latest cloud HSM*

- AWS CloudHSM
  - ``token.pkcs11.model=AWSCloudHSM``

    *Tested: Latest cloud HSM*

- Yubi HSM 2

  - ``token.pkcs11.model=YubiHsm``

    *Tested: YubiHSM 2 FIPS*




### Bespoke Interfaces

- Google KMS

  - Configured via the ``token.googleKms`` properties 

- Azure KeyVault

  - Configured via the ``token.azureKeyVault`` properties  

- Thales PayShield 9000 - *Deprecated*

  - Configured via the ``token.hsm9000`` properties

    *Tested: PayShield 9000*
    
    

Refer to the installation and configuration guide for details on configuring EzSign for these key stores

Note that the tested instances are confirmed. Backwards compatibility should be maintained by the vendors for the PKCS#11 interface for later versions



#### Thales PayShield Additional Notes

Support for PayShield may be removed in future releases. Contact [support](mailto:support@krestfield.com) for more information

PayShields may require additional licenses to support the RSA system. Specific commands must be enabled on the HSM - including ``EI`` and ``EW``
