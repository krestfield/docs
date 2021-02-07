---
layout: default
title: Credentials
parent: EzCert
nav_order: 7
---

# Credentials



A credential is a secure store of an account or password.  It may be an account on a system that has the required permissions to request certificates from a Microsoft CA in which case it will be Microsoft Windows domain account  

When you configure a Microsoft Certificate Issuer you must either specify a credential or select *No Credential*  

When you configure other issuers, you may only need to configure a password credential

When a certificate is requested from the Certificate Issuer (or the Microsoft CA's templates are queried) this account is used by the ADCS Agent. If *No Credential* is selected the account that the ADCS Agent service is running under will be used instead  

---

To create a new Credential:

1. Select **Credentials** from the menu
2. Click **Add New Credential**

<img src=".\images\new_credential.png" alt="image-20210207171112963" style="zoom:67%;" />

1. For **Credential Type**, select whether this is a *username password* credential - or simply to store a *password*
2. For the **Credential Name**, choose a name you will reference this credential by
3. For *username password* credentials, enter the **username**. If this is a domain account it must include the domain name in the form ``user@domain.com`` or ``domain\user``
4. Enter the **password** for the account and re-type
5. Click **Add**

---

Credentials are encrypted and then stored in the database





