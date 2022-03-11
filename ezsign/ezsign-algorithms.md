---
layout: default
title: EzSign Algorithms
parent: EzSign
nav_order: 96
---


# EzSign Algorithms



The available algorithms in EzSign are:

* RSA

  * This is the default and implements the RSA algorithm

* ECDSA

  * This is the elliptic curve digital signature algorithm
  

  


Algorithms are configured using the following property:

```
channel.N.signature.algorithm
```

E.g.

```
channel.N.signature.algorithm=RSA
```

<br>

If RSA is specified as the algorithm them the key size (in bits) must also be specified. This is done using the following property:

```
channel.N.signature.keySize
```

E.g.

```
channel.N.signature.keySize=2048
```

<br>

If ECDSA is chosen then the curve must also be specified using the following property:

```
channel.N.signature.ecc.curve
```

E.g.

```
channel.N.signature.ecc.curve=secp256r1
```

<br>

This algorithm specified is the one that will used whenever EzSign has to generate a key and perform a signing operation with that key  

For example, if RSA is chosen and a key size of 2048, then when a CSR is generated a 2048 bit RSA key pair will be generated  

When a request for a signature is received the private RSA key will be used to generate an RSA ECB PKCS1 encoded signature

