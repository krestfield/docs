---
layout: default
title: Setting Microsoft ADCS CA and Template Permissions
parent: General PKI
nav_order: 7
---

# Setting Microsoft ADCS CA and Template Permissions

<br>

### Permissions on the CA

In order to be able to issue certificates from your Microsoft CA via Certdog, the correct user-permissions must be set on the CA and certificate templates  

On the CA itself the user (or group) must have the **Read** and **Request Certificates** permissions set:  

<img src=".\images\ca-permissions1.png" alt="CA Permissions" style="zoom:80%;" />

This will allow the user to request certificate from the CA - and, if the template allows, be issued with a certificate  

To enable a user to perform the following additional operations:

* Revoke certificates

* Approve pending requests

Then the user must also have the **Issue and Manage Certificates** permission set to **Allow**

<br>

In Certdog, a service account is usually provisioned that is a member of a group set with *Allow* permissions for:

* Read

* Issue and Manage Certificates

* Request Certificates

e.g.

<img src=".\images\ca-permissions2.png" alt="CA Permissions" style="zoom:80%;" />

This enables that account to be used (set as the Credential to use in the Microsoft Certificate Issuer) to issue and revoke certificates  

This user/group is then configured in the templates that you wish Certdog to be able to issue certificates from, as per the instructions below

<br>

<br>

### Permissions on Templates

In order to be able to issue a certificate from a specific template, the user or group being used must have the following permissions set to Allow:

* Read

* Enroll

If the template has the **CA certificate manager approval** option set (as configured on the *Issuance Requirements* tab). This means that by default the request will not be automatically issued, but moved to the *Pending Requests* folder instead, awaiting approval from a Certificate Manager  

The Certdog ADCS agent will attempt to automatically approve this request. However, in order for this to succeed the account the agent is running under (as configured as the Credential in the Microsoft Certificate Issuer) must also have the **Issue and Manage Certificates** permissions set to **Allow** on the CA (as mentioned above)

<br>

<br>

### Configuring Permissions on the CA

Right click the **CA node** (e.g. Certdog in the example below) and choose **Properties**

<img src=".\images\ca-snapin.png" alt="CA Snapin" style="zoom: 80%;" />

From the *Properties* dialog, select the **Security** tab  

Click **Add...** and start typing the name of the **user or group** you wish to add permissions for. Click **Check Names** to perform a search based on the entered text. Select the **user or group** from the list. Click **OK**  

Select the **user or group** and check the required permissions. Click **OK**  

<br>

### Configuring Template Permissions

From the **Certificate Authority snapin**:

<img src=".\images\ca-snapin.png" alt="CA Snapin" style="zoom: 80%;" />

Select the **Certificate Templates** node, **right click** and choose **Manage**

<img src=".\images\manage-templates.png" alt="Templates Console" style="zoom: 80%;" />

Right click the **template** you wish to issue certificates from and select **Properties**

Select the **Security** tab

Click **Add...** and start typing the name of the **user or group** you wish to add permissions for. Click **Check Names** to perform a search based on the entered text. Select the **user or group** from the list. Click **OK**  

E.g. in the example below, the PKI_CERT_ISSUERS group has the *Enroll* permission set  

<img src=".\images\ca-template1.png" alt="Template Security Tab" style="zoom: 80%;" />

Click **OK**  

If this template is not already configured on the CA for issuance, perform the following:  

Back on the **Certificate Authority snapin**, right click the **Certificate Templates** node and select **New > Certificate Template to Issue**  

<img src=".\images\template-to-issue.png" alt="Enable Templates" style="zoom:80%;" />

Select the **template** and click **OK**  

