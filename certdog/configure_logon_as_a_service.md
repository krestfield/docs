---
layout: default
title: Configuring Logon as a Service
parent: Certdog
nav_order: 133
---



# Configuring Logon as a Service

  

When configuring a Microsoft CA (ADCS), a credential is required. This credential is used by the ADCS Driver to request certificates from the CA. It must have the correct permissions on the CA and certificate templates in order to provision the certificates. See [here](https://krestfield.github.io/docs/pki/setting_adcs_template_permissions.html) for configuring permissions on a certificate template  

You will normally use a Service Account for this purpose. This account requires the **Logon as a Service** right and this is usually coupled with the **Deny Logon Locally** assignment. This is fairly self explanatory but means that this account can run as a service on a server but could not be used by a user to logon to that (or another) server

If your organisation has an account management process in place, simply requesting a service account will be sufficient, but to configure this yourself you may use the following instructions  

Note that everyone's domain will be configured differently and there may be processes or automation already in place to handle this, so this is for guidance only

<br>

### Summary

In summary the steps to create an account that can then be used as the Credential to access a Microsoft CA (via the ADCS Driver) are as follows:

1. Create an account in AD
2. Create a group for service accounts e.g. **SERVICE_ACCOUNTS**
4. Configure this group via Group Policy with:

   * Deny logon locally

   * Logon as a service
5. Add the account created in step 1 into this group
5. We can add this account to other groups that have permissions on the CA and required CA Templates to issue certificates (e.g. you may have a CERT_ISSUERS group configured for this purpose)
6. The account can then be configured in certdog as a Credential, this can be referenced when configuring a Microsoft CA Issuer
<br>

### Steps

Create a new user account in Active Directory. Uncheck the option **User must change password at next logon** and check **Password never expires**. At this point the user will be a member of *Domain Users* only - leave it as this for now  

If on the domain controller, click start and type: ``gpmc.msc`` and press **Enter** 

This starts the **Group Policy Management Console**. This is used to administer the policy for the domain (or a specific OU). On a non-AD connected machine you may use ``gpedit.msc`` to manage the local policy

Under *Forest and Domains*, right click **Default Domain Policy** and choose **Edit**

Under *Computer Configuration*, navigate to

```
Policies\Windows Settings\Security Settings\Local Policies\User Rights Assignment
```

(Note: If running locally, this will start from ``Windows Settings``)

Scroll down to **Deny logon locally** and double click

Check **Define these policy settings** and add the group e.g. **SERVICE_ACCOUNTS**

Scroll down to **Logon as a service** and double click 	

Check **Define these policy settings** and add the group e.g. **SERVICE_ACCOUNTS**

<br>

Run ``gpupdate /force`` on all machines for a quick update. <u>Remember to include the CA machine</u>

<br>

To verify that the setting has taken effect locally, run ``rsop.msc`` (Resultant Set of Policy). under Computer Configuration, navigate to:

```
\Windows Settings\Security Settings\Local Policies\User Rights Assignment
```

And verify the changes are present

<br>

Note, this will set these settings for the entire domain. If you want to restrict this for a certain OU perform this in the correct GPO. To create a new GPO, right click the selected OU and choose **Create a GPO in this domain and link it here**

