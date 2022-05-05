---
layout: default
title: Certdog Errors and Solutions
parent: Certdog
nav_order: 2000
---

# Certdog Errors and Solutions

<br>

The following contains some common errors that may be experienced when using Certdog together with their solutions  
<br>
<br>

### There are no CA issuers that can process a request. This may be because you do not have permissions on any of the configured CA issuers

<u>Error Details</u>

When you navigate to Request by CSR or DN this message appears and you are unable to see any CA Issuers  

<u>Solution</u>

This is because the Team(s) you are a member of have not been assigned any permissions on CA Issuers. To rectify, first click on the top right *user* icon and select **Profile** under *My Account*  

The Team(s) you are a member of will be highlighted. Note these teams  

Next click on **Teams** from the menu, select one of the Teams you noted above and click **View/Edit**  

Next to *Permitted Certificate Issuers*, select the issuers that you wish this team to have permissions to obtain certificates from. As you are a member of this team you will also be provided with these permissions  

Re-attempt the certificate issuance



<hr>

### A CSR generator must be configured before you can request a certificate from a DN

<u>Error</u>

When navigating to Request - DN, this error is presented  

Solution  

If you want to request a certificate by only supplying the DN, Certdog must also create the CSR (Certificate Signing Request) on your behalf. In order to do this a CSR Generator is required  

To create a new CSR generator follow the steps outlined [here](create_csr_generator.html)



<hr>

### Credential fails when attempting to obtain templates or certificates from a Microsoft CA (ADCS)

<u>Error</u>

A credential is configured but when attempting to obtain templates or a certificate the following is seen:

```
The request to obtain the templates from the CA agent failed. Reason: There was an error obtaining the templates from the CA. Check the CA details are correct - they should be in the format 'hostname\ca name' as returned in the Config entry when certutils is run. Details (Logon failure: the user has not been granted the requested logon type at this computer)
```

Or

```
The request to obtain the certificate failed. Reason: Failed to process request. Logon failure: the user has not been granted the requested logon type at this computer
```

The important part being:

```
Logon failure: the user has not been granted the requested logon type at this computer
```

<u>Solution</u>

A service account should be used as a credential when accessing the Microsoft CA. The credential will normally be configured with the *Deny logon locally* and the *Logon as a service* user right assignments. If *Deny logon locally* is set but *Logon as a service* is not, this error will occur

You may run ``rsop.msc`` to obtain the local policy settings and check the assignments for the group that the user is a member of

Arrange for the correct permissions and assignments to be added to the user. See [here](https://krestfield.github.io/docs/certdog/configure_logon_as_a_service.html) for information on how to configure the account correctly   



<hr>

### Login screen runs slow

On some virtual machines that have limited graphics processing power or that may have 3d acceleration switched off, the login screen can appear to run slow

<u>Error</u>

Login screen slow to respond

<u>Solution</u>

This is due to the login screen background. This can be removed as follows:

* Stop the Krestfield Certdog Service

* Delete (or move to a backup location if still required) the following file:

```
[certdog install]\tomcat\webapps\certdog#ui\background.mp4
```

* Start the Krestfield Certdog Service

If your browser is still showing the background this will be because of the browser cache. Try closing the browser or performing a full refresh (e.g. CTRL-F5 on Chrome)



<hr>

### Cannot stop Krestfield CertDog Service

<u>Error</u>

Windows could not stop the Krestfield CertDog Service service on Local Computer.

Error 1061: The service cannot accept control messages at this time

<u>Solution</u>

Open a PowerShell window as Administrator and navigate to: ``[certdog install]\bin``  

Run ``.\stop-tomcat.ps1``

Next, open task manager, click on the Services tab and locate **Krestfield Certdog Service**

Right click and select **Go to details**

Click **certman-service.exe** and click **End task**



<hr>

### The request to obtain the certificate failed. Reason: Failed to process request. Index was outside the bounds of the array

<u>Error Details</u>

Applicable to versions up until version 1.6 only

If running the Krestfield ADCS Service under a specific Service Account and you have set the Microsoft CA Issuer in Certdog to use No Credential. You may see this error when requesting a certificate

<u>Solution</u>

Set the Krestfield ADCS Service to run under the Local System account and set the service account (that has permissions on the CA) as a Credential in Certdog. For your Microsoft Certificate Issuer - select this credential









