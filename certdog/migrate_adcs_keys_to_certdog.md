---
layout: default
title: Migrate ADCS Keys to Certdog
parent: Certdog
nav_order: 57
---

# Migrate ADCS Keys to Certdog



Keys stored on nCipher HSMs, in use by Microsoft CAs must first be migrated to formats certdog understands

https://download.primekey.com/docs/EJBCA-Enterprise/7_0_1/Migrating_RSA_Keon_CA_with_nCipher.html



Essentially, locate the private key:

```
C:\nfast\bin>pubkey-find.exe c:\kca.pem
input format cert
nCore hash d0196ea2e070315e9e162c28dcdc5a524bf6380d
unnamed
appname rsa-keon-ca-65
ident 1184659106609000
```

Where kca.pem is the CA certificate

You can also locate the public key:

```
C:\nfast\bin>pubkey-``find``.exe --augment c:\kca.pem
```

To translate for use by PKCS11

```
C:\nfast\bin>ckcerttool.exe -c oper -f c:\ca\kca.pem -k uc3126f2b3cf7d9d53e3ba27`
`8a081ef471644298f8-628484d430c6c0502fdb1a520fb84b9dc73c8372 -L kcaSign`
`Certificate found, processing...`
`Please enter the passphrase ``for` `”oper” token (No ``echo` `set``).`
`Passphrase:`
`Certificate successfully imported.`
`Run cklist to view your certificate object.`
`OK
```

