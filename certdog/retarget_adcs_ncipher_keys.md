---
layout: default
title: Retarget ADCS nCipher Keys
parent: Certdog
nav_order: 57
---

# Retarget ADCS nCipher Keys to Certdog

If your microsoft CA is using an SafeNet nCipher HSM to store its keys. These can be migrated to certdog by following the steps below  

Essentially, the key is migrated from a the Microsoft application (mscapi/caping) to the pkcs11 application type, thus allowing the PKCS#11 interface (which certdog uses) to make use of the keys

<br>

Obtain the CA cert e.g. ``ca.cer``

Open a command prompt as Administrator and navigate to 

``C:\Program Files (x86)\nCipher\nfast\bin>``

From the prompt run:

``nfkminfo -k``

E.g.

```
C:\Program Files (x86)\nCipher\nfast\bin>nfkminfo -k

Key list - 27 keys
 AppName caping               Ident machine--d085239508f9d1890989497b38aef757494cf329
 AppName mscapi               Ident container-2c0afb5fd62d214dad1028bc6dfae81317d1b201
 AppName pkcs11               Ident uac2dca1b681e776095cd902c81fb8d1ec4cd9b5c6
 AppName pkcs11               Ident uc7c99e43e627c3a62933bc1c16f559db862978952-06c70f2b0fa50c3799809248ffd5fcf9a740b169
...
```

This displays the keys currently held on the HSM  

The *AppName* specifies what interface was used to create the keys. In the example above we see *caping*, *mscapi* and *pkcs11*  

ADCS keys are created using the *caping* application  

<br>

To find the actual keys that are associated with the CA certificate we use the nCipher command:

``pub key-find.exe`` 

passing it the CA certificate. It will then use the public key from the certificate to locate the keys held on the HSM

E.g. 

```
C:\Program Files (x86)\nCipher\nfast\bin>pubkey-find.exe c:\ca.cer
 input format cert
 nCore hash 6556fd4afee4c4db9c6d60e901b107bb34a8c82a

 name `Krestfield Root CA'
 appname caping
 ident machine--d085239508f9d1890989497b38aef757494cf329
```

We can see that a key has been located, called:

```
ident machine--d085239508f9d1890989497b38aef757494cf329
```

Which you will see matches an item in the list when we ran ``nfkminfo`` above

<br>

We now need to retarget this key so it is accessible via the pkcs11 interface, which is the interface Certdog uses. We will use the ``generate key.exe --retarget pkcs11`` command to create a copy of the key which will then be accessible via pkcs11:

```
C:\Program Files (x86)\nCipher\nfast\bin>generatekey.exe --retarget pkcs11
from-application: Source application? (caping, mscapi, pkcs11) [caping]
> 
```

For *from-application* enter ``caping``

```
> caping
```

We will now asked what *caping* key we wish to migrate. Note that if there is only one key that matches this application (which is often the case with a CA), it will be set as the default

```
from-ident: Source key identifier?
(machine--d085239508f9d1890989497b38aef757494cf329)
  [default machine--d085239508f9d1890989497b38aef757494cf329]
>
```

Just hit enter to accept the default. Otherwise enter the *ident* of the key we located when we ran ``pubkey-find.exe`` above (in the form: ``machine--d085239508f9d1890989497b38aef757494cf329``)  

<br>

Next we need to give the new key a name. This is the name Certdog will reference the key by in its configuration when we import it. So ensure that this is a unique name (e.g. you could add the time and/or date to the key name such as ``20220814_krestfield_root_ca``):

```
plainname: Key name? [] > 20220814_krestfield_root_ca
key generation parameters:
 operation         Operation to perform     retarget
 application       Application              pkcs11
 slot              Slot to read cards from  0
 verify            Verify security of key   yes
 from-application  Source application       caping
 from-ident        Source key identifier    machine--d085239508f9d1890989497b38aef757494cf329
 plainname         Key name                 20220814_krestfield_root_ca
```

A summary (as above) is displayed and you may then be prompted to enter your HSM passphrase (e.g. the operator smart card passphrase), depending on your HSM setup:

```
Loading `caocs':
 Module 1: 0 cards of 1 read
 Module 1 slot 0: `caocs' #2
 Module 1 slot 0:- passphrase supplied - reading card
Card reading complete.
```

The key will be retargeted and the new filename will be displayed:

```
Key successfully retargetted.
Path to key: C:\ProgramData\nCipher\Key Management Data\local\key_pkcs11_uc7c99e43e627c3a62933bc1c16f559db862978952-17af2072c8e48350d68ec693fa10f0700d7523d6
```

<br>

This key can now be imported into Certdog



