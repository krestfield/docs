---
layout: default
title: EJBCA TLS Certificate Profile Setup
parent: EzCert
nav_order: 10
---

# EJBCA - TLS Certificate Profile Setup  



This example demonstrates how to create a TLS profile in EJBCA for use within EzCERT

For this example, we will be limiting the certificates to RSA 2048 bit



---



Navigate to the Administration console (e.g. https://myhostname:8443/ejbca/adminweb)  

Under ***CA Functions***, select **Certificate Profiles**  

Enter a name for this profile e.g. **EZCERT_TLS** and click **Add**, then click **Edit**  



Choose **End Entity**, select **RSA** and **2048** for the ***Available Bit Lengths***:  

<img src=".\images\ejbca_cert_profile1.png" alt="image-20210205095237155" style="zoom:80%;" />

For Permissions, tick **Allow Subject DN Override by CSR** and **Allow Extension Override**:  

<img src=".\images\ejbca_cert_profile2.png" alt="image-20210205172403638" style="zoom: 67%;" />

For the extensions, set **Digital Signature** and **Key Encipherment** for ***Key Usage*** and **Server Authentication** for *Extended Key Usage* (if you plan to use these certificates for client TLS authentication then also select Client Authentication)  

<img src=".\images\ejbca_cert_profile3.png" alt="image-20210205095745952" style="zoom:80%;" />

Scroll down to *Other Data* and uncheck the box for **LDAP DN Order**, select the **CA** you wish to be able to issue these certificates  

<img src=".\images\ejbca_cert_profile4.png" alt="image-20210205095912354" style="zoom:80%;" />

Click **Save**   

Note the profile name you selected as this name is required when configuring EzCERT  