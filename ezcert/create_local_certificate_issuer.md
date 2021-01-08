---
layout: default
title: Create a Local Certificate Issuer
parent: EzCert
nav_order: 3
---
# Create a Local Certificate Issuer



A Local Certificate Issuer enables you to issue certificates from an EzCert controlled CA

A Certificate Issuer combines a CA (Certificate Authority) and Certificate Profile

1. Create a Local CA Configuration
   Select **Local CA** | **Configuration** from the menu

<img src=".\images\new_localca_issuer_config.png" alt="image-20210108165700507" style="zoom:67%;" />

Click **Add New CA**

<img src=".\images\new_localca_issuer_config2.png" alt="image-20210108165822066" style="zoom:70%;" />

Enter details for *CA Name* and *Subject DN*.  Alter the algorithms and key sizes if required.  Click **Create**

Create a Certificate Profile

Select **Local CA** | **Profiles** from the menu

<img src=".\images\new_localca_profiles.png" alt="image-20210108170056632" style="zoom: 67%;" />

Click **Add New Profile**

<img src=".\images\new_localca_profiles2.png" alt="image-20210108170237149" style="zoom:67%;" />

And enter details for *Profile Name*  

Select the lifetime.  This will be the lifetime of the issued certificate

If you wish SANs (Subject Alternative Names) that are provided in the CSR (Certificate Signing Request) to be included in any issued certificates, ensure this option is checked  

Select the Key Usages - these will be applied to the issued certificate

Select the Enhanced Key Usages - these will be applied to the issued certificate  

See [RFC5280]([RFC 5280 - Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile (ietf.org)](https://tools.ietf.org/html/rfc5280)) for more details on key usages

Click **Add**

Create a Certificate Issuer

Select **Certificate Issuers** from the menu

<img src=".\images\new_localca_issuer.png" alt="image-20210108170849399" style="zoom:67%;" />

Click **Add New Issuer**

<img src="C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\new_localca_issuer2.png" alt="image-20210108170947087" style="zoom:67%;" />

From the drop down select **Local CA** and click **Next**

<img src=".\images\new_localca_issuer3.png" alt="image-20210108171200950" style="zoom:67%;" />

Enter a **Name** and select the **Local Configuration** and **Certificate Profile** as just created from the drop downs  

Click **Add**



The Certificate Issuer is now ready to issue certificates. However, you must first give the accounts that need to use this issuer the correct permissions



See [Set User Permissions on a Certificate Issuer](set_user_permissions_on_cert_issuer.html)



If you wish to request a certificate by just providing a DN i.e. with EzCert generating the CSR on your behalf, then a CSR Generator must be available



See [Create a CSR Generator](create_csr_generator.html)

