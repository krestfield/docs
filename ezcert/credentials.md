---
layout: default
title: Credentials
parent: EzCert
nav_order: 7
---

# Credentials



A credential is simply an account on the system that has the required permissions to request certificates from the Microsoft CA. It is usually a Microsoft Windows domain account  

When you configure a Microsoft Certificate Issuer you must either specify a credential or select *No Credential*  

When a certificate is requested from the Certificate Issuer (or the CA's templates are queried) this account is used by the ADCS Agent. If *No Credential* is selected the account that the ADCS Agent service is running under will be used instead  

---

To create a new Credential:

1. Select **Credentials** from the menu
2. Click **Add New Credential**

<img src=".\images\new_credential.png" alt="image-20210116161358897" style="zoom: 67%;" />

1. For the **Credential Name**, choose a name you will reference this credential by
2. Enter the **username**. If this is a domain account it must include the domain name in the form ``user@domain.com`` or ``domain\user``
3. Enter the **password** for the account
4. Click **Add**

---

Credentials are encrypted and then stored in the database





