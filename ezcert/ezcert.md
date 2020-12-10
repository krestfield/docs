---
layout: default
title: EzCert
nav_order: 2
has_children: true
---
# EzCert

Making the issuance and management of certificates easy







## Features



### Support CAs

- Microsoft ADCS (Active Directory Certificate Services)
- Internal CA
- (DigiCert, EJBCA and others coming soon...)



### Interfaces

- Complete Restful API for all certificate management and administative operations
- PowerShell
- .NET Interface
- Java Interface



```java
EzCertClient client = new EzCertClient("127.0.0.1", "username", "password");
String b64CertData = client.requestCertP10(csr, "testca1");

```
