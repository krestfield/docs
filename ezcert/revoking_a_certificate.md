---
layout: default
title: Revoking a Certificate
parent: EzCert
nav_order: 17
---

# Revoking a Certificate

From the menu choose Certificates  

Locate the certificate you wish to revoke. Refer to [Searching Certificates](searching_certificates.html) for details on how to find a specific certificate  

Click on the certificate:

<img src=".\images\cert_info.png" alt="image-20210122125547911" style="zoom:67%;" />

Click **More**  

Within the certificate details view, Click **More Details** then click **Click to show revocation options**:  

<img src=".\images\revoke_cert_details.png" alt="image-20210122125811949" style="zoom:67%;" /> 

For *Revocation Reason*, select the reason you are revoke this certificate and click the **Revoke This Certificate** button

<img src=".\images\confirm_revocation.png" alt="image-20210122125954211" style="zoom:67%;" />

Click **Revoke Now**  

If you now expand the **History** section you will see the new entry and the status of the certificate will change from **Active** to **Revoked**

<img src=".\images\cert_history.png" alt="image-20210122130101123" style="zoom:80%;" />

If this is a certificate from an external CA (e.g. a Microsoft CA), the certificate will be revoked on that CA. CRLs from that CA should now include this certificate's serial number