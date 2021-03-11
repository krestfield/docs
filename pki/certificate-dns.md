---
layout: default
title: Certificate DNs
parent: General PKI
nav_order: 41
---

# Certificate DNs



DNs (Distinguished Names) and their comparison (or lookup) often causes confusion as there are cases where DNs are in fact equal, when they look different  

It’s best to start with an explanation of what a DN really is:  

So, a DN is not stored in a certificate as a string (in the form CN=Name, O=Organisation), although it is usually displayed this way when viewing. A DN is actually a data structure which includes a list of OIDs (Object Identifiers) and values. An OID takes the form:

  **A.B.C....n**  (i.e. a series of integers separated by dots)

e.g.

  **1.3.6.14.324.2**  

and is used to uniquely identify an object  

In the case of certificate DNs this will identify whether the data refers to *Common Name*, *Organisational Unit*, *Country* etc. For more information on OIDs see: https://en.wikipedia.org/wiki/Object_identifier  

The value associated with the OID is usually in a string format, although there are several formats such as PrintableString and UTF8String  

 Therefore, a DN may contain a list of OIDs against PrintableStrings such as:  

> 2.5.4.3=User One

> 2.5.6.5=Engineering

> 2.5.6.4=Krestfield Ltd

> 2.5.6.2=GB

 Which refers to: 

| **OID** | **Field Name**      | **Usually Represented As** | **Value**      |
| ------- | ------------------- | -------------------------- | -------------- |
| 2.5.4.3 | Common Name         | CN                         | User One       |
| 2.5.6.5 | Organisational Unit | OU                         | Engineering    |
| 2.5.6.4 | Organisation        | O                          | Krestfield Ltd |
| 2.5.6.2 | Country             | C                          | GB             |

 Now, this could be displayed as the following string:

   **CN=User One, OU=Engineering, O=Krestfield Ltd, C=GB**



How do we know that 2.5.4.3 should be displayed as CN though? Well, there are some specifications indicating how to represent these OIDs. It turns out a DN originates from X500 LDAP specifications such as this one:

X500 User Schema for LDAPv3: [https://www.ietf.org/rfc/rfc2256.txt](https://www.ietf.org/rfc/rfc2256.txt)

Which links several of the OID values to string representations



There is also a specification detailing specifically how DNs should be represented as strings:

LDAP String Representation of DNs: [https://tools.ietf.org/html/rfc2253  ](https://tools.ietf.org/html/rfc2253)



So pretty well worked out? Not really. These specifications do not cover every OID value available to use within a DN (in theory you can use any), nor do they infer that the string representations should be formatted strictly (e.g. spaces after a comma or not). What they give are details on how to represent an encoded DN as a String  

What this means is that this DN:

  **CN=User One, OU=Engineering, O=Krestfield Ltd, C=GB**

 Is actually the same as this DN:

  **CN=User One,OU=Engineering,O=Krestfield Ltd,C=GB**

i.e. no spaces after the commas



And, if you start to include other less common fields, such as *email*.  Then this DN:  

  **CN=User One, E=[userone@krestfield.com](mailto:userone@krestfield.com), O=Krestfield Ltd, S=London, C=GB**

Could also be represented as:

  **CN=User One,EMAIL=[userone@krestfield.com](mailto:userone@krestfield.com),O=Krestfield Ltd,ST=London,C=GB**



These DNs are the same, in that their base representation (the list of OIDs against values) is the same. It is just their formatted string representations that are different  

 It is for this reason, that if any checking on a certificate DN is done (e.g. to check that it is registered on a system etc.) the following should be noted:

* Avoid performing a straight string comparison on DNs

* If you must perform a DN string comparison, ensure that the code which extracts the DN from the certificate being registered is the same which performs the comparison later. This way the string representation will be the same (as the same code would have parsed the data and produced the string)

* Do not allow users to type or paste in the DN from say, the certificate viewed in Microsoft. The best way to register such details would be to extract the DN from the certificate itself (e.g. by allowing a certificate to be uploaded so that the same code can be used to extract the DN as a string)

* Use the Krestfield method: dnsAreEquivalent included in KCertUtils in the Client Utilities when comparing DNs as strings

 

Note: That the correct way to uniquely reference a certificate is using its *serial number* and *issuer DN* – not subject DN. Also there are other certificate fields which are also available to reference a certificate such as the thumbprint (a hash over the certificate data), the public key, subject key identifier etc. I.e. use decimal or byte values when possible rather than strings  

More details about the certificate profile is included in this specification: X509 Certificate and CRL Profile https://www.ietf.org/rfc/rfc5280.txt