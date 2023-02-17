---
layout: default
title: Certificate Issuers
parent: Certdog
nav_order: 69
---

# Certificate Issuers



Certificate Issuers are a combination of 

* A Certificate Authority

* A Certificate Profile (called a Certificate Template in Microsoft AD CS) 

* And *optionally*, [DN Restrictions](dn_restrictions.html)



Certificate Issuers enable you to combine these items in order to make certificate issuance simpler and to control what types of certificates can be issued  

For example, you could create a Certificate Issuer that combines an Issuing CA with a TLS Profile (or template) with a DN Restriction set that only allow certain domain names. Then refer to this with a name - e.g. TLS Certificates  

When you request a certificate you then select the *Organisational TLS Certificates* issuer and certificates will be issued with the profile selected from the CA specified. The requested DN must also conform to the DN Restriction's rules

For more information on creating certificate issuers click one of the following links:

* [Create a Local Certificate Issuer](create_local_certificate_issuer.html)
* [Create a Microsoft AD CS Certificate Issuer](create_adcs_certificate_issuer.html)
* [Create an EJBCA Certificate Issuer](create_ejbca_issuer.html)



