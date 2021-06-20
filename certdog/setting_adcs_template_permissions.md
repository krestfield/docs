---
layout: default
title: Setting Microsoft ADCS Template Permissions
parent: Certdog
nav_order: 7
---

# Setting Microsoft ADCS Template Permissions



In order to be able to issue certificates from your Microsoft CA via Certdog, the correct user-permissions must be set on the certificate template  

Common practise is for a group to have the *enroll* permission on a template and a service account to be a member of this group. The service account can be created specifically for Certdog's use. But stand-alone accounts may also be created for this purpose   

However, you manage your groups and user accounts, the requirement is that an account have the *enroll* permissions on the template, and this can be configured as follows:  

Open the **Certificate Authority snapin**:

<img src=".\images\ca-snapin.png" alt="image-20210620101115322" style="zoom: 80%;" />

Select the **Certificate Templates** node, **right click** and choose **Manage**

<img src=".\images\manage-templates.png" alt="image-20210620103520718" style="zoom: 80%;" />

Right click the **template** you wish to issue certificates from and select **Properties**

<img src=".\images\ca-template1.png" alt="image-20210620103822626" style="zoom: 80%;" />

Select the **Security** tab and ensure that either the **user/service account** or the **group** (that the account is a member of) has the **Enroll** permission set. In the configuration shown above the *PKI_CERT_ISSUERS* group has the required permission. A service account (svc-certdog-ca) is a member of this group    

Click **OK**  

If this template is not already configured on the CA for issuance, back on the **Certificate Authority snapin**, right click the **Certificate Templates** node and select **New > Certificate Template to Issue**  

<img src=".\images\template-to-issue.png" alt="image-20210620104317315" style="zoom:80%;" />

Select the **template** and click **OK**  

The account that has permissions on this template can now be configured as a Credential within Certdog and selected when configuring a Microsoft CA Certificate Issuer 
