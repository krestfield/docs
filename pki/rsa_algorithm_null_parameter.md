---
layout: default
title: RSA - missing your NULLs
parent: General PKI
nav_order: 61
---

# RSA - missing your NULLs

It is not uncomment to see interoperability issues when two more more systems are trying to integrate using digital signatures.  The formats used in PKI are often old and obscure (e.g. PKCS standards and ASN1 encoding) but have to be followed precisely - else things fail.  If not followed to the letter, signatures that look good and are verified on one system OK, are rejected on another  

A common issue is failing to include a NULL parameter within the digest information of an RSA signature. This is required as mentioned in RFC 3279 (See [Snippet from RFC 3279](#snippet-from-rfc-3279) below)  

Essentially the Digest Information for an RSA signature contains the identifier of a hash algorithm as well as the hash over the data (the hash being generated using that specified algorithm)  

The hash identifier is given in the form of an OID (Object Identifier) and for SHA-256 this is: ``2.16.840.1.101.3.4.2.1`` and the hash as an octet string. The ASN1 form for the algorithm identifier also allows for a parameter to be provided. RFC 2313 states:  

```
For these object identifiers, the parameters field of the digestAlgorithm value should be NULL
```

<br>

What you should end up with in ASN1 is something like the following:

```
   0 30   49: SEQUENCE {
   2 30   13:   SEQUENCE {
   4 06    9:     OBJECT IDENTIFIER '2 16 840 1 101 3 4 2 1'
  15 05    0:     NULL
            :     }
  17 04   32:   OCTET STRING
            :     22 D4 A7 6A 85 AF 92 15 FA 9A 71 D0 C6 2F CF 93
            :     B3 F9 FC DA B6 29 E5 97 B5 B5 FF 0C 1B 79 BB E3
            :   }
```

Where your algorithm OID is specified as ``2.16.840.1.101.3.4.2.1`` we can see that ``NULL`` is specified as the parameter and the OCTET STRING contains our 32 byte SHA-2 hash over the data

If you omit the NULL, your ASN1 will look like the following:

```
   0 30   47: SEQUENCE {
   2 30   11:   SEQUENCE {
   4 06    9:     OBJECT IDENTIFIER '2 16 840 1 101 3 4 2 1'
            :     }
  15 04   32:   OCTET STRING
            :     22 D4 A7 6A 85 AF 92 15 FA 9A 71 D0 C6 2F CF 93
            :     B3 F9 FC DA B6 29 E5 97 B5 B5 FF 0C 1B 79 BB E3
            :   }
```

i.e. the NULL part is missing

From a code perspective, using BouncyCastle libraries the correct form to obtain the Algorithm Identifier would be:

```
AlgorithmIdentifier algId = new AlgorithmIdentifier(algorithmOid, DERNull.INSTANCE);
```

But as the ``DerNull.INSTANCE`` parameter is optional, often it is missed, as follows:

```
AlgorithmIdentifier algId = new AlgorithmIdentifier(algorithmOid);
```

Resulting in an incorrectly specified Digest Information

<br>

Why does this matter? You may ask. I mean the hash has been identified correctly (by the OID) and the hash is the same - it should still work right?

Well, the wording in the RFCs referenced are: 

* SHALL - which in RFC world (see RFC 2119) is the same as MUST, and 
* SHOULD which means RECOMMENDED (there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications must be understood and carefully weighed before choosing a different course)

Which essentially mean it is often implemented as expected and will reject signatures that do not include it. As mentioned at the start - these standards need to be followed precisely to ensure interoperability.  This is the rule and so it is best to follow it 



### Snippet from RFC 3279

>   The signature algorithm with MD2 and the RSA encryption algorithm is
>    defined in PKCS #1 [RFC 2313].  As defined in PKCS #1 [RFC 2313], the
>    ASN.1 OID used to identify this signature algorithm is:

      md2WithRSAEncryption OBJECT IDENTIFIER  ::=  {
          iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
          pkcs-1(1) 2  }

>   The signature algorithm with MD5 and the RSA encryption algorithm is
>    defined in PKCS #1 [RFC 2313].  As defined in PKCS #1 [RFC 2313], the
>    ASN.1 OID used to identify this signature algorithm is:

      md5WithRSAEncryption OBJECT IDENTIFIER  ::=  {
          iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
          pkcs-1(1) 4  }

>    The ASN.1 object identifier used to identify this signature algorithm
>    is:

      sha-1WithRSAEncryption OBJECT IDENTIFIER  ::=  {
          iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1)
          pkcs-1(1) 5  }

>   When any of these three OIDs appears within the ASN.1 type
>    AlgorithmIdentifier, the parameters component of that type SHALL be
>    the ASN.1 type NULL.

