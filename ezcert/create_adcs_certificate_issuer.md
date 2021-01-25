---
layout: default
title: Create an ADCS Certificate Issuer
parent: EzCert
nav_order: 6
---
# Create an ADCS Certificate Issuer



This guide describes how to create a Certificate Issuer for a Microsoft ADCS (Active Directory Certificate Services) instance  

A Certificate Issuer ties the following configuration items together, such that a user can then request certificates by just specifying the Issuer name 

1. A credential
   This is a an account on the system. It may be a service account or a user account
3. An ADCS certificate template
   This is the template on the ADCS system that you wish to obtain certificates from
4. An ADCS instance
   The actual Microsoft CA instance that will issue the certificate



Once these items have been configured as a Certificate Issuer, you must then set permissions for users to access this Issuer.  Those users will then able to request certificates from the UI or API



### Pre-Requisites

* You must have an instance of ADCS installed in a domain
* The [ADCS Driver](adcsdriver.html) must be installed onto a machine in the same domain as the ADCS instance
* You must have the correct credentials (username/password) for the Microsoft certificate template you wish to target. The template must be configured with the correct permissions to allow the credential to auto-enrol for a certificate
   For more information see [Setting Microsoft ADCS Template Permissions](setting_adcs_template_permissions.html)
* The ADCS Driver must be able to access to the EzCERT database

   If the EzCERT system is all installed on the same machine, this will be in place. If you have installed the ADCS Driver separately normally you need to ensure that port 27017 (the default database port) has outgoing access. Refer to the [ADCS Driver](adcsdriver.html)  document for further details



### 1. Create a Credential

   Skip this step if you already have a credential created.  If not, follow the guide on creating a credential [here](credentials.html)  

   The credential you create must be for an account that has permissions on the template. See [Setting ADCS Template Permissions](setting_adcs_template_permissions.html)

   

### 3. Create a Certificate Issuer

   Select **Certificate Issuers** from the menu

<img src=".\images\new_localca_issuer.png" alt="image-20210108170849399" style="zoom:67%;" />

   Click **Add New Issuer**

<img src=".\images\new_ms_ca_issuer.png" alt="image-20210116161811294" style="zoom:67%;" />

   From the drop down select **Microsoft Local CA** and click **Next**  

<img src=".\images\ms_issuer_1.png" alt="image-20210125143720260" style="zoom:67%;" />

Enter a **Name** for this issuer - this will be the name referenced when requesting certificates

Enter the CA **Configuration**. This is the value returned for Config when ``certutil`` is run on a machine in the same domain as the CA. E.g. Opening a command prompt and typing ``certutil`` will return something like the following:

```shell
Entry 0: (Local)
  Name:                         `Krestfield CA'
  Organizational Unit:          `PKI Services'
  Organization:                 `Krestfield Ltd'
  Locality:                     `'
  State:                        `'
  Country/region:               `GB'
  Config:                       `IssuingCA.int.krestfield.com\Krestfield CA'
  Exchange Certificate:         `'
  Signature Certificate:        `IssuingCA.int.krestfield.com_Krestfield CA.crt'
  Description:                  `'
  Server:                       `IssuingCA.int.krestfield.com'
  Authority:                    `Krestfield CA'
  Sanitized Name:               `Krestfield CA'
  Short Name:                   `Krestfield CA'
  Sanitized Short Name:         `Krestfield CA'
  Flags:                        `13'
  Web Enrollment Servers:
```

In this case the value that would be entered for **Configuration** is ``IssuingCA.int.krestfield.com\Krestfield CA``  

Select the **Credential** that has the permissions for the CA and template you are configuring. The Credential must have auto-enrol permissions on the selected template

The **Get Available Templates** button will now be present:  

<img src=".\images\ms_issuer_2.png" alt="image-20210125144250008" style="zoom:67%;" />

Click the **Get Available Templates** button. A request for templates will now be made to the CA referenced in the configuration using the credential specified. If the CA is contactable and the credential has permissions  

<img src=".\images\ms_issuer_3.png" alt="image-20210125144417207" style="zoom:67%;" />

If successful, the templates will be displayed. Select from the drop-down which template you wish to configure with this issuer.

For **Permitted Agents**, select all agents that you wish to be able to process the requests for this CA and template. The agent must have been installed and set to **Approved**  

Click **Add**

---

The Certificate Issuer is now ready to issue certificates. However, you must first give the accounts that need to use this issuer the correct permissions

See [Set User Permissions on a Certificate Issuer](set_user_permissions_on_cert_issuer.html) for details on how to do this



If you wish to request a certificate by just providing a DN i.e. with EzCert generating the CSR on your behalf, then a CSR Generator must be available. See [Create a CSR Generator](create_csr_generator.html) for more details

