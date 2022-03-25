---
layout: default
title: Setting Microsoft ADCS Template Permissions
parent: General PKI
nav_order: 7
---

# Setting Microsoft ADCS Template Permissions



In order to be able to issue certificates from your Microsoft CA via Certdog, the correct user-permissions must be set on the CA and certificate template  

* In order to request certificates an account must have the *Enroll* permission on the template  

* In order to be able to revoke certificates an account must have the *Issue and Manage Certificates* permission on the CA

Good practise is to create a group that has the correct permissions on the CA. Then create a service account for Certdog's use and add this to that group (although you can just assign the correct permissions directly to a specific account)  

In this example we have created a group called ``PKI_CERT_ISSUERS`` and a service account called ``svc-certdog``  

The ``svc-certdog`` account must have the *Logon as a Service* and ideally the *Deny Local Logon* rights assigned (as usual for service accounts). See [here](https://krestfield.github.io/docs/certdog/configure_logon_as_a_service.html) for details on creating a service account   

The ``svc-certdog`` account is a member of ``PKI_CERT_ISSUERS`` so we configure the correct permissions for this group as follows:

<br>

To configure the *Enroll* permission on a specific template:

Open the **Certificate Authority snapin**:

<img src=".\images\ca-snapin.png" alt="CA Snapin" style="zoom: 80%;" />

Select the **Certificate Templates** node, **right click** and choose **Manage**

<img src=".\images\manage-templates.png" alt="Templates Console" style="zoom: 80%;" />

Right click the **template** you wish to issue certificates from and select **Properties**

Select the **Security** tab and click **Add**...  Select the ``PKI_CERT_ISSUERS`` group and check *Allow* for **Enroll**

<img src=".\images\ca-template1.png" alt="Template Security Tab" style="zoom: 80%;" />

Click **OK**  

If this template is not already configured on the CA for issuance, perform the following:  

Back on the **Certificate Authority snapin**, right click the **Certificate Templates** node and select **New > Certificate Template to Issue**  

<img src=".\images\template-to-issue.png" alt="Enable Templates" style="zoom:80%;" />

Select the **template** and click **OK**  

Members of the ``PKI_CERT_ISSUERS`` group (which includes ``svc-certdog``) can now request certificates from the CA for this template  

<br>

To also allow *Revoke*, perform the following:

From the **Certificate Authority snapin** right click the **CA node** and click **Properties**

Select the **Security** tab and click **Add...**

Select the ``PKI_CERT_ISSUERS`` group and check *Allow* for **Issue and Manage Certificates**

<img src=".\images\ca-security-tab.png" alt="CA Security Tab" style="zoom:80%;" />

Click **OK**

Now any member of the ``PKI_CERT_ISSUERS`` group can revoke and request certificates for this template  

<br>

The ``svc-certdog`` account can now be configured as a Credential within certdog and used to connect to this Microsoft CA when configuring an Issuer



