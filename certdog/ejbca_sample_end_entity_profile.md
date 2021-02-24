---
layout: default
title: EJBCA - End Entity Profile Setup
parent: Certdog
nav_order: 11
---

# EJBCA - End Entity Profile Setup  



This example demonstrates how to create an End Entity profile for use with certdog



---



Navigate to the EJBCA Administration console (e.g. https://myhostname:8443/ejbca/adminweb)  

Under ***RA Functions***, select **End Entity Profiles**  

Under ***Add Profile***, enter a name for the profile e.g. **CERTDOG_PROFILE**, click **Add**, then select this profile from the list and click **Edit End Entity Profile**

Ensure that at least the **Common Name** subject attribute is present, but set as *modifiable* and *not required*:

<img src=".\images\ejbca_ee_profile3.png" alt="image-20210208114139733" style="zoom: 67%;" />



Under *Main certificate data*, select the certificate profile(s) (e.g. CERTDOG_TLS) and the CA(s) you wish to issue your certificates

For available tokens, leave at the defaults  

For information, when certdog calls EJBCA, certdog creates the CSR - this requires that *User Generated* is available 

<img src=".\images\ejbca_ee_profile2.png" alt="image-20210206091121351" style="zoom: 67%;" />

Scroll to the bottom and click **Save**

