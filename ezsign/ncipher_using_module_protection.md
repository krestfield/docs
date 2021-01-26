---
layout: default
title: nCipher HSM - Using Module Protection
parent: EzSign
nav_order: 25
---



# EzSign: nCipher HSM - Using Module Protection



nCipher HSMs support Module protection as well as Operator Card Set protection  

The latter involves creating an Operator Card Set and assigning a Passphrase to the cards.  Objects stored on the HSM are then protected by the Module as well as this Card Set and applications that wish to make use of these objects not only must have access to the HSM but must also supply the Operator Card Set Passphrase  

Thus, access to objects such as private keys require the user to be logged on to the HSM, providing the Passphrase before access is granted  

If Module only protection is used then objects are still stored protected by the module's internal master keys, but can be accessed by any application (that has access to the HSM) without the need to log on to the HSM with a passphrase  

Within EzSign, the Operator Card Set Passphrase is provided as the Token Password.  This is encrypted by the Master Password.  The server may be started by supplying the Master Password but sensitive operations such as CSR generation and the import of certificates require that the Token password is also entered.  This prevents operational staff (responsible for managing the server) from also having the ability to perform sensitive operations.  Another team (e.g. Security) can own the Token/Operator Cardset password.  It is therefore, recommended that an Operator Card Set be created when using nCipher HSMs  

However, if other security controls are in place which restrict an application's access to an HSM and there is no need to restrict the operational user from performing sensitive operations, then Module-Only protection can be enabled as follows:  

 

### Edit the EzSign Server Configuration

The server properties file must be updated for the channel that wishes to make use of Module protection only.  The following property must be set:

```properties
  channel.N.token.useModuleProtection=true
```

Where 'N' is the channel number e.g.

```properties
  channel.1.token.useModuleProtection=true
```

 

### Run the Server

The server can be started in the normal way but on starting the following warning will be output to the logs:

```verilog
2020-09-14 10:06:26.085 [main] WARN  EzSignLog - Module protection is enabled.  This means that no password is required to access the keys on the Token/HSM.  Ensure that other sufficient security controls are in place to prevent unauthorised access
```



 Note that although the Token Password is no longer used to log in to the HSM, it is still required. It will still be used to encrypt other information relating to the HSM

  

### Viewing Object's Protection Level

To verify what protection each object within the HSM is under, from the nFast bin directory, run the following command:

```bash
  nfkminfo -l
```

 This will display all items (together with the label) sorted by protection e.g.:

```bash
Keys with module protection:
key_pkcs11_ua114f29785ea013fd5eca7e6cd7614c796bc24a06 `15e7f5e09ff2030'
key_pkcs11_ua1df56ecd5514769c92c361e2e3c799745bfd0b96 `nopassword'

...

Keys protected by cardsets:
key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-0317f899c8a6737e8506278850b57bf1b7b29e9e `OTP_SEED_SYM_KEY'
key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-49b37b070741ea08fccdafffcd3298e01306806e `15ab7ef2ff43176'
```



...