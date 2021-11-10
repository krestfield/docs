---
layout: default
title: Create a Local Certificate Profile
parent: Certdog
nav_order: 6
---
# Create a Local Certificate Profile

A certificate profile determines the details that will be included in an issued certificate including the lifetime and extensions, such as key usages and enhanced key usages  

A certificate profile is coupled with a Local CA configuration to form a Certificate Issuer  

As well as the options set in the profile, the issued certificate will also contain information that is set in the Local CA Configuration - including what algorithm will be used to generate the certificate as well as the following extensions:

* AIA (Authority Information Information)
  * This extension contains the locations of the issuer CA certificate and OCSP responders

* CDP (CRL Distribution Points)
  * This extension contains the locations of CRLs

<br>

### Creating a Certificate Profile

Select **Local CA** > **Profiles** from the menu and click **Add New Profile**

<img src=".\images\new_localca_profiles2.png" alt="image-20211110065538884" style="zoom:80%;" />



* Enter a **Profile Name**

* Select the **lifetime**.  This will be the lifetime of the issued certificate

* If you wish SANs (Subject Alternative Names) that are provided in the CSR (Certificate Signing Request) to be included in any issued certificates, ensure the **Include SANs from CSR** option is checked  

* The Common Profiles drop-down contains some common profile types and selecting one of the options will populate the values for **Key Usages**, **Enhanced Key Usages**, **Include OCSP No Check** and **Include Basic Constraints**. You may start with one of these options then alter the settings or leave as Empty and manually set all entries

* Select the **Key Usages** - these will be applied to the issued certificate

* Select the **Enhanced Key Usages** - these will be applied to the issued certificate  

* If this is to be an OCSP certificate and you do not wish the status of this certificate to be checked. Set the **Include OCSP No Check** option

* Select the Include Basic Constraints option if this extension is to be included in the issued certificate

  If this profile will be issuing Sub CA certificates, select the **Is CA** option. This indicates the issued certificate will be a Certificate Authority. For end-entity certificates leave the **Is CA** option as unchecked

  If the *Is CA* option is checked you may also select the **Path Length Constraint**. Select **None** if you do not want to impose any restrictions on the path length (number of CAs in the chain). Otherwise, specify the path length. Note that a Path Length of 0 will mean the issued certificate cannot issue Sub CA certificates below it

* To include policy information in the certificate click **Policies**:

<img src=".\images\policies1.png" alt="image-20211110075432818" style="zoom:80%;" />

You may select a policy type of **OID Only**, **User Notice** or **CPS**. Select the required option, populate the required information (OID and either CPS location or notice text) and click **Add**. You may add further policy entries as required

<br>

When the settings are complete, click **Add**  

<br>

See [RFC5280](https://tools.ietf.org/html/rfc5280) for more details on certificate attributes and extensions

