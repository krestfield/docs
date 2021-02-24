---
layout: default
title: Create an EJBCA Issuer
parent: Certdog
nav_order: 7
---

# Create an EJBCA Issuer



To configure certdog to be able to request certificates from EJBCA, the following is  required:

* The Web Service option is enabled
  * You can check this from Admin Web. Choose System Configuration then click the Protocol Configuration tab. the Web Service option should be *Enabled*
* A User KeyStore
  * This is an end-entity certificate issued from EJBCA's current ManagementCA that is configured to have access to the RA administrative functions
  * This is the certificate that certdog will use  to authenticate to the EJBCA RA.  You must obtain this as a JKS (Java Key Store) file from EJBCA
* A certificate profile must be configured to allow *Subject DN Override by CSR* and *Allow Extension Override*. See [EJBCA - Sample TLS Certificate Profile](ejbca_sample_tls_profile.html) fore more details
* An end-entity profile must be configured with no subject DN attributes and set to allow *User Generated* tokens. See [EJBCA - Sample End Entity Profile](ejbca_sample_end_entity_profile.html) for more details



### 1. Obtaining the User KeyStore

If you are already familiar with EJBCA and issuing certificates for administrator access, skip this section and just ensure that you obtain a password protected JKS with a certificate that has RA Administration privileges



There are several ways in which this can be obtained e.g. via the Admin Web console, the RA (Registration Authority) console or the CLI (Command Line Interface). The following details the RA process  

Log on to the **RA console**

Click **Enroll** and select Make New Request

<img src=".\images\ejbca_ra_enroll1.png" alt="image-20210205153413676" style="zoom:80%;" />

The above shows some initial default settings, but there may be specific certificate and end-user profiles configured for this purpose (that limit available options)

Select **On server** 

Choose an **algorithm**. Note: With the default profiles, you have access to all algorithms, if unsure which to choose, consult with your security personnel, though **RSA 2048 bits** is a common choice

For the *Subject DN Attributes*, enter a common name e.g. **certdog** and scroll down

In the *Provide User Credentials* section, enter a **username** and for **Enrollment code** - just enter a password

<img src=".\images\ejbca_ra_usercreds.png" alt="image-20210205154913701" style="zoom:67%;" />

You can leave *Email* empty

Scroll down to the *Confirm request* section and click **Download JKS**

Save this **file** and retain the **username** and **password** (Enrollment code) entered above - these are required for the certdog configuration  





### 2. Set Administrator Permissions

From the RA, select **Role Management** and click **Roles**. If you have already configured a role which only allows RA administrator access you may use this, otherwise, click **Create New Role**

For the Role name, enter a name for this role e.g. Certdog RA Administrators

For the *Certificate Authorities*, add those that you wish to issue certificates from certdog

<img src=".\images\ejbca_ra_roles_cas.png" alt="image-20210205155549640" style="zoom:67%;" />

Select *all End Entity* permissions

For *End Entity Profiles*, add those profiles that you want to be applied for certificates issued from certdog. See the [EJBCA - Sample End Entity Profile](ejbca_sample_end_entity_profile.html) for an example   

Click **Add**

<img src=".\images\ejbca_ra_roles.png" alt="image-20210205160154396" style="zoom:67%;" />

From the list, click **Members**

<img src=".\images\ejbca_ra_role_member.png" alt="image-20210205160559465" style="zoom:67%;" />

Just click **Add Role Member**

<img src=".\images\ejbca_ra_add_member.png" alt="image-20210205160701792" style="zoom:67%;" />

For CA, select **ManagementCA**, select **Match with Serial Number (recommended)** then paste in the **certificate serial number** in the *Match Value* and click **Add**. This is the serial number of the certificate created in [step 1](#Obtain the User KeyStore) above

Note: You can obtain this serial number by choosing **Search** in the RA, then click **Certificates**  and type the certificate name (e.g. certdog). Copy the serial number and paste into the **Match Value** above



From the administrative console (/adminweb), under **System Functions**, select Administrator Roles

Locate the role (e.g. Certdog RA Administrators) and select **Access Rules**

For the *Role Template*, ensure it says **RA Administrators**, select it if not. Check CAs selected are as required and click **Save**



### 3. Certificate Profile

Whichever profiles you wish to use with certdog - you must **check** the **Allow Subject DN Override by CSR** and **Allow Extension Override** options. For details on how to configure a sample profile for TLS, see [EJBCA - Sample TLS Certificate Profile](ejbca_sample_tls_profile.html)




### 4. End Entity Profile

It is recommended that a new End Entity profile be created for certdog. Ensure that under the *Main certificate data* section, the **User Generated** option is selected in *Available Tokens*. This is because certdog will be generating the CSRs (or they will be provided)

For an example on setting up an end-entity profile, see [EJBCA - Sample End Entity Profile](ejbca_sample_end_entity_profile.html)




## certdog Configuration

Before starting this, ensure you have the following:

* The Web Services URL
  * Usually something like: https://hostname:8443/ejbca/ejbcaws/ejbcaws

* The user JKS file and its password
  * As created in step 1 above

* The name of the CA you wish to issue certificates from
* The name of the Certificate profile you wish to configure

* The name of the End Entity profile you wish to configure

* If an un-trusted TLS certificate is used to protect the RA Web Services site, you will also need to download the JKS for the CA that issued this certificate
  * This can be obtained by navigating to CA Certificates and CRLs in the RA and clicking on the JKS option in the Certificate chain column



### Set Credentials

First we need to set some credentials. Credentials are password stores that are then referenced by a name. We will need one for the User KeyStore (JKS file) and optionally, one for the Trust KeyStore

From the certdog menu, select **Credentials** and select **Add New Credential**

<img src=".\images\ejbca_cred.png" alt="image-20210205164409660" style="zoom:67%;" />

For *Credential Type*, select **Password**

Choose a name then enter the password. Note for the User KeyStore, this password will be the one you set in step 1 above when enrolling for the certificate

Click **Add**

If required, create another credential for the Trust KeyStore (i.e. the keystore downloaded from the CA). This default password for this keystore will be displayed by EJBCA when you download



### Configure EJBCA Issuer

From the certdog menu, select **Certificate Issuers** and select **Add New Issuer**

For the *CA Type*, select **PrimeKey EJBCA** and click **Next**

<img src=".\images\ejbca_config1.png" alt="image-20210205163525205" style="zoom:80%;" />

Enter the details as follows:

* Name: This is the name you will refer to this issuer, it has nothing to do with what has been configured in EJBCA and can be a name of your choice

* Web Services URL: The EJBCA Web Services end point. E.g. https://hostname:8443/ejbca/ejbcaws/ejbcaws

  If this end point is protected with a TLS certificate which is not trusted by the certdog system (and this will be the case if an initial EJBCA installation has just been performed), browse to the Trust KeyStore JKS file - this is the CA Certificate Chain file downloaded as JKS. If the ManagementCA issued the TLS certificate, then that is the CA you need to download the JKS file from

* Select the credential created in the steps above for *Trust KeyStore Credential*

* For EJBCA username, enter the username from step 1 above. I.e. the username of the end-entity

* Browse to the User KeyStore and then select the credential containing the keystore password for *User KeyStore Credential*

* For EJBCA Issuing CA Name - this is the CA configured in EJBCA that you wish to issue certificates from

* Then enter the **End Entity** and **Certificate Profile** names that you would have identified or created in steps 3 and 4 above

* Click **Add**



If all is correct you will get a success confirmation. If any of the details or are incorrect you may get errors such as:

<img src=".\images\ejbca_error1.png" alt="image-20210205165350575" style="zoom: 80%;" />

This is most likely due to the User Key Store password being incorrect.  Reset the password in the credential and try again

<img src=".\images\ejbca_error2png" alt="image-20210205165642593" style="zoom:80%;" />

The most likely cause is that the certificate included in the User KeyStore does not have RA Administrative permissions. Go back to EJBCA and check the Administrator Roles

<img src=".\images\ejbca_error3.png" alt="image-20210205170327789" style="zoom:80%;" />

The Web Service URL is most likely protected with a TLS certificate that is not trusted.  Identify the CA that issued the TLS certificate and download its certificate chain as a JKS - then upload as outlined above

