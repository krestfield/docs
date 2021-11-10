---
layout: default
title: Create a Local Certificate Issuer
parent: Certdog
nav_order: 6
---
# Create a Local Certificate Issuer



A Local Certificate Issuer enables you to issue certificates from a certdog controlled CA

A Certificate Issuer combines a Local CA (Certificate Authority) and a Certificate Profile  

<br>  

### 1. Create a Local CA Configuration  
   Select **Local CA** > **Configuration** from the menu and click **Add New CA**

<img src=".\images\new-local-ca.png" alt="image-20210717121009648" style="zoom:80%;" />

Complete the following details:  

<u>Main Certificate Authority Details</u>  

* **CA Name**: Enter a name for this CA

* **Key Store**: Choose from the drop down the Key Store that will be used to generate and store this CA's keys. See [here to create a key store](keystores.html)

* **Type**: You can create a Root CA (self-signed) or an Intermediate CA. A complete hierarchy of CAs can be configured with no limit to the chain length 

  If you choose Intermediate CA you also have the options:  **Local CA** or **External CA (Generate a CSR)**

  Choose **Local CA** if  you want to issue this intermediate CA from an existing Local CA

  Choose **External CA** if you want to generate a CSR for processing by an external CA - such as an existing Root CA (e.g. a Microsoft Root). See the section [Processing a CSR from an External CA](#processing-a-csr-from-an-external-ca) below for details on processing a request

* **Issuer**: If you select *Intermediate CA* and *Local CA* in the options above, a list of available parent CAs (issuers) will be displayed. Select the CA to be the parent/issuer CA

* **Subject DN**: Enter the CA Distinguished Name

* **Lifetime**: Specify the life of this CA. Note that if an Intermediate CA's lifetime is set to exceed that of the issuer, it will be automatically reduced to be equal to the issuers. I.e. you cannot issue an Intermediate CA with a longer life than its parent

  Note that this option is not available if *External CA* was selected above, since the issuing CA will determine this value when it issues the certificate

* **Algorithm**: Select RSA or ECDSA as the algorithm used to generate the CA keys

* **Key Size**: If RSA is selected, set the RSA key size

* **Curve**: If ECDSA is selected, set the name for the elliptic curve

* **Hash Algorithm**: Set the CA's hash algorithm

Note that once the CA is configured, the above options are fixed and cannot then be changed. You may delete and re-issue a CA but you cannot change its lifetime, algorithm etc.   

<br>

If you chose to *Issue From* an **External CA** above, the following options will not be available. This is because it will be the issuing CA that will decide on these values when it issues the certificate

<u>Extensions</u>  

* **CRL Distribution Points**: Enter a URL (or list of URLs separated by commas). These locations will be included in the CRL Distribution Points extension of all certificates issued by this CA and relate to where the CRL issued by this CA can be obtained

  E.g. http://server1.com/crl/ca1.crl,http://server2.com/crl/ca1.crl

* **AIA OCSP Locations**: Enter a URL (or list of OCSP URLs separated by commas). These locations will be included in the AIA (Authority Information Access) OCSP extension of all certificates issued by this CA and relate to where the certificate status can be obtained via OCSP

  E.g. http://server1.com/ocsp

* **AIA Issuer Cert Locations**: Enter a URL (or list of URLs separated by commas). These locations will be included in the AIA (Authority Information Access) extension of all certificates issued by this CA and relate to where the CA certificate can be obtained

  E.g. https://server3.com/ca1/cacert.cer

<u>CRL Generation</u>  

* **Generate CRLs**: If you want this CA to generate CRLs, enable this option

* **CRL Lifetime**: This is the lifetime of the CRL i.e. the period between the *Effective date* and *Next update* values in the CRL

* **CRL Generation Period**: This is how often you want the CRL to be generated. It must be less than the CRL Lifetime (set above). For example, if the lifetime were set to 2 days, you may set this to 1 day so there is always a 1 day overlap

* **CRL Filename**: This is the local location where the CRL file will be placed when generated. See the [Notes on the CRL Filename and CRL Distribution Points](#notes-on-the-crl-filename-and-crl-distribution-points) section below for more details

The above options (Extensions and CRL Generation) can be edited later if required)  

Click **Create**   

If you chose to *Issue From* an **External CA** above, the option will be **Create CSR**. See the section [Processing a CSR from an External CA](#processing-a-csr-from-an-external-ca) below for details on processing this CSR 

<br>

### 2. Create a Certificate Profile

Select **Local CA** > **Profiles** from the menu and click **Add New Profile**

See [Create a Local Certificate Profile](create_a_local_certificate_profile.html) for details on creating profiles

<br>

### 3. Create a Certificate Issuer

Select **Certificate Issuers** from the menu

<img src=".\images\new_ms_issuer.png" alt="image-20210108170849399" style="zoom:67%;" />

Click **Add New Issuer**

<img src=".\images\new_localca_issuer2.png" alt="image-20210108170947087" style="zoom:67%;" />

From the drop down select **Local CA** and click **Next**

<img src=".\images\new_localca_issuer3.png" alt="image-20210620124010018" style="zoom:67%;" />

Enter a **Name** and select the **Local Configuration** and **Certificate Profile** as just created from the drop downs  

Select the **Team**(s) that will be authorised to use this issuer. Members of these teams will be able to issue and revoke certificates  

Click **Add**  



If you wish to request a certificate by just providing a DN i.e. with certdog generating the CSR on your behalf, then a CSR Generator must be available.  See [Create a CSR Generator](create_csr_generator.html)

<br>

### Notes on the CRL Filename and CRL Distribution Points

A CRL must be available at the location(s) specified in the CRL Distribution points. You must therefore ensure that the CRL generated at the location specified by CRL Filename is either the location the CRL Distribution Point references, or is  copied to this location  

One option is to use the certdog web server to host this CRL. To do this perform the following steps:  

1. On the file-system navigate to where certdog is installed e.g. ``c:\certdog``

2. Create a CRL folder within the webapps of the tomcat instance (that hosts certdog). I.e. create the following folder:

   ``c:\certdog\tomcat\webapps\crl``

3. Set the CRL Distribution point to be: ``http://[your URL]/crl/ca.crl`` e.g. ``http://certdog.net/crl/ca.crl``

4. Set the CRL Filename to be: ``c:\certdog\tomcat\webapps\crl\ca.crl``

This will result in the CRL being created at ``c:\certdog\tomcat\webapps\crl\ca.crl`` which will then be available at this URL: ``http://certdog.net/crl/ca.crl``

<br>

### Processing a CSR from an External CA

If an external CA will be issuing the certificate, after clicking *Create CSR*, select the created CA entry from the list and choose **View/Edit**

<img src=".\images\int_ca_csr.png" alt="image-20211109215723096" style="zoom:80%;" />

The status will be shown as *This CA is awaiting a response from a CSR*

The CSR can be downloaded (or copied to the clipboard) for processing at the Issuing CA  

Once the certificate has been issued, obtain the issuing CA certificate (e.g. the Root CA certificate) as well as the certificate issued from the CSR  

Click the **Upload CA Certificate** button and navigate to the certificate issued from the CSR

Click the **Upload Issuer Certificate** button and navigate to the issuing CA certificate (e.g. the Root CA certificate)

Click **Accept**
