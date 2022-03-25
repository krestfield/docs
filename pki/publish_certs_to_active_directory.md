---
layout: default
title: Publishing Certs to Active Directory
parent: General PKI
nav_order: 61
---


# Publishing CA Certs to Active Directory



When you create CAs in certdog you may want them to be trusted in your Windows domain. One way to achieve this is outlined below

<br>

### Root CA Certificates

To be trusted by domain users and machines, a root CA certificate must reside in the Local Computer's **Trusted Root Certificate Authorities** store  

We can publish a root CA certificate so that it is trusted by everything in that domain, or we can limit its trust to specific OUs or sites  

To enable domain wide trust, the following command can be run from an elevated command prompt:

 ```
 certutil –dspublish -f rootca.cer RootCA 
 ```

Where ``rootca.cer`` is the Root CA certificate downloaded from certdog

Note: This must be run with an account that is a member of either *Domain Admins* or *Enterprise Admins*

E.g.

```
C:\>certutil -dspublish -f "Certdog Root CA AZ.cer" RootCA
ldap:///CN=Certdog Root CA AZ,CN=Certification Authorities,CN=Public Key Services,CN=Services,CN=Configuration,DC=certdog,DC=local?cACertificate

Certificate added to DS store.

ldap:///CN=Certdog Root CA AZ,CN=AIA,CN=Public Key Services,CN=Services,CN=Configuration,DC=certdog,DC=local?cACertificate

Certificate added to DS store.

CertUtil: -dsPublish command completed successfully.
```

Once complete the certificate (rootca.cer) will be published to the *Trusted Root Certification Authorities* folder of the *Local Computer* store for all machines that are a member of the domain e.g.

![image-20220324160409079](.\images\publishedcert.png)

 <br>

### Intermediate CA Certificates

Although intermediate CA certificates can be made available via http links which are configured in end entity certificates as part of the AIA extension, they can also be published to Active Directory if required  

We want these certificates to be placed in the local machines in the *Intermediate Certification Authorities* folder   

To achieve this, run the following command:

```
certutil –dspublish -f ca.cer SubCA 
```

Where ``ca.cer`` is the CA certificate downloaded from certdog  

Again, *Domain Admins* or *Enterprise Admins* permissions are usually required



