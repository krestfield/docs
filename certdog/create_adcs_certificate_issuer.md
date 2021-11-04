---
layout: default
title: Create an ADCS Certificate Issuer
parent: Certdog
nav_order: 6
---
# Create an ADCS Certificate Issuer

  

This guide describes how to create a Certificate Issuer for a Microsoft ADCS (Active Directory Certificate Services) instance  

A Certificate Issuer ties the following configuration items together, such that a user can then request certificates by just specifying the Issuer name:  

1. A Credential  
   This is an account on the system. It may be a service account or a user account
3. An ADCS Certificate Template  
   This is the template on the ADCS system that you wish to obtain certificates from
4. An ADCS Instance  
   The actual Microsoft CA instance that will issue the certificate

  

Once these items have been configured as a Certificate Issuer, users with permissions may then request certificates from the UI or API  



### Pre-Requisites

* You must have an instance of ADCS installed in a domain

* The [ADCS Driver](adcsdriver.html) must be installed onto a machine in the same domain as the ADCS instance

* You must have the correct credentials (username/password) for the Microsoft certificate template you wish to target  
  
   The template must be configured with the correct permissions to allow the credential to enrol for a certificate  
   For more information see [Setting Microsoft ADCS Template Permissions](https://krestfield.github.io/docs/pki/setting_adcs_template_permissions.html)
   
* The ADCS Driver must be able to access the certdog database  

   If the certdog system is all installed on the same machine, this will be in place. If you have installed the ADCS Driver separately, you need to ensure that port 27017 (the default database port) is open. Refer to the [ADCS Driver](adcsdriver.html)  document for further details

  



### 1. Create a Credential

   Skip this step if you already have a credential created.  If not, follow the guide on creating a credential [here](credentials.html)  

   The credential you create must be for an account that has permissions on the template. See [Setting Microsoft ADCS Template Permissions](setting_adcs_template_permissions.html)  

​     

### 2. Create a Certificate Issuer

   Select **Certificate Issuers** from the menu  

<img src=".\images\new_ms_issuer.png" alt="image-20210620094636154" style="zoom: 67%;" />

   Click **Add New Issuer**  

<img src=".\images\new_ms_ca_issuer.png" alt="image-20210116161811294" style="zoom:67%;" />

   From the drop down select **Microsoft CA** and click **Next**  

<img src=".\images\ms_issuer_1.png" alt="image-20210125143720260" style="zoom:67%;" />

Enter a **Name** for this issuer - this will be the name referenced when requesting certificates  

Enter the CA **Configuration**. This is the value returned for Config when ``certutil`` is run on a machine in the same domain as the CA. E.g. Opening a command prompt and typing ``certutil`` will return something like the following:  

![image-20210620094957527](.\images\ms-ca-certutil.png)


In this case the value that would be entered for **Configuration** is ``IssuingCA.int.krestfield.com\Krestfield CA``  

Select the **Credential** that has the permissions for the CA and template you are configuring. The Credential must have enrol permissions on the selected template  

The **Get Available Templates** button will now be present:  

<img src=".\images\ms_issuer_2.png" alt="image-20210125144250008" style="zoom:67%;" />

Click the **Get Available Templates** button. A request for templates will now be made to the CA referenced in the configuration using the credential specified. If the CA is contactable and the credential has permissions  

<img src=".\images\ms_issuer_3.png" alt="image-20210125144417207" style="zoom:67%;" />

If successful, the templates will be displayed. Select from the drop-down which template you wish to configure with this issuer  

<img src=".\images\msca-setup.png" alt="image-20210620095612254" style="zoom:67%;" />

For **Permitted Agents**, if running a single agent (i.e. the default) only one will be present and it will be selected. If you have multiple agents configured, select the agent(s) you wish to process the requests for this CA  

Note that the agent must be *approved* for it to appear. If no agent is shown, select Agents from the menu and approve the required agent  

Finally, select the **team** that will have access to this Certificate Issuer. All members of this team will be able to request and revoke certificates from this issuer

Click **Add**  

---

The Certificate Issuer is now ready to issue certificates. Selecting one of the Request options will now display the issuer as a selection  

If you do not see the Issuer as an option, check that you are a member of the Team that has access. See [here](teams.html) for more information on managing teams

If you wish to request a certificate by just providing a DN i.e. with certdog generating the CSR on your behalf, then a *CSR Generator* must also be available. See [Create a CSR Generator](create_csr_generator.html) for more details

