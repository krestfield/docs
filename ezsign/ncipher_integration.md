---
layout: default
title: nCipher HSM - Integration
parent: EzSign
nav_order: 24
---



# EzSign: nCipher HSM - Integration



EzSign can make use of any HSM that supports the PKCS#11 interface.  The steps to configure EzSign for use with an HSM are simple and are outlined below but before any configuration takes place, the following pre-requisites must be in place: 

- The HSM must be networked, configured and the Security World must be loaded
- The local HSM client software must be installed and the HSM must be enrolled
- Any passwords (such as the operator card set password) must be available

 To confirm that the server can see and communicate with the HSM run the enquiry command e.g. 

```bash
C:\nCipher\nfast\bin\enquiry.exe
```

This will output details about the HSM, card sets and the status

 

### EzSign Server Configuration

Edit the ``server.properties`` file and add a new channel as shown below:  

```properties
channel.1.name=CHANNELNAME
channel.1.enabled=true
channel.1.tokenType=PKCS11
channel.1.token.password=
channel.1.token.pkcs11.library=C:/nCipher/nfast/toolkits/pkcs11/cknfast-64.dll
channel.1.token.pkcs11.slot=1
channel.1.signature.hash=SHA256
channel.1.signature.includeCerts=ALLEXCEPTROOT
channel.1.signature.includeContent=false
channel.1.signature.keyId=
channel.1.revocationChecker.type=NONE
channel.1.verify.nonRepudiationRequired=true
channel.1.verify.denyWeakHash=false
channel.1.verify.relaxAllCertExtensionChecks=true
```

The key points to note are:  

The channel number (e.g. channel.**1**) increments for every channel, so if you have any previous channels configured (which you wish to retain) then the number should be incremented (e.g. if you had settings for channel.1 already, then these settings would all start channel.**2**)  

The ``tokenType`` is **PKCS11** 

The ``token.password`` value should be blank for now, as we will set this later  

The value for ``token.pkcs11.library`` should be the **PKCS#11 library**.  You should reference the 32 or 64 bit versions depending on the host system  

The value for ``token.pkcs11.slot`` depends on how your HSM has been setup.  Usually the module is at slot 0, and operator card sets at slot 1, 2...etc.  Usually slot 1 refers to the operator card set if only one has been created  

Other options can be altered as required  

 

### Configure Passwords

Next start the EzSign Management utility

```bash
ezsign-manage.bat [properties file]
```

Enter the master password and choose option

```bash
1. Set Passwords
```

Follow the prompts which require you to set the master password again, then the token password.  In this instance the token password will be the HSM password.  If an operator card set has been created this will be the passphrase associated with that card set (set when the card set is created)  

The utility will prompt to save the updated file  

This will result in the ``token.password`` setting being populated with the encrypted password  

Exit the utility  

 

### Generate CSR

When ready to generate a CSR, start the Management utility and choose option 

```bash
2. Generate a CSR
```

This will be the same process as when software CSRs are generated.  Note, that the token password will be the operator card set password for the HSM  

Once the CSR has been generated, send this to the CA and obtain the certificates as .cer files.  Obtain the entire chain (issued end-entity certificate plus any intermediates and the root).  Import via the Management utility using option 4  

When the end-entity certificate has been imported you will be prompted whether you wish to set this as the signing key.  Choose yes, and the properties file will be updated, populating the ``signature.keyId`` value  

 

### Run the Server

Assuming all steps were successful and the HSM is operational the server can now be started and signing operations should use the key generated on the HSM