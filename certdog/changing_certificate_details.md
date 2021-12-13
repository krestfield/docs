---
layout: default
title: Changing Certificate Details
parent: Certdog
nav_order: 13
---

# Changing Certificate Details



Although a certificate cannot be altered. The information that Certdog associates with a certificate can be altered, including:

* The owner
  * This is the user who owns the certificate

* The team
  * The certificate will be associated with this team. This may mean that other team members may be able to view and manage this certificate (if configured in the Settings)
* Extra information
  * Any extra information that a user wishes to assign to the certificate

* Additional emails
  * Email addresses, in addition to the owners, whom will also be sent reminder emails

* Expiry Monitoring
  * Whether to prevent emails being sent when this certificate nears expiry (if configured)
* Deletion
  * If the certificate is no longer required or created in error it may be deleted
  * Note that this will not revoke the certificate! It will only remove it from the local store. If CRL or OCSP is in use, revoke the certificate BEFORE deleting

<br>

These options are available from the *Certificate Details* view (From **Certificates** in the left hand menu, click a **Certificate** then choose **More**)

<img src=".\images\change_cert_details1.png" alt="Certificate Details" style="zoom:80%;" />

Click **Actions** to view the available options

<br>

If **Change Owner** or **Change Team** are selected you may select the new value from a drop down:

<img src=".\images\change_cert_details3.png" alt="Change Owner" style="zoom:80%;" />

Note that, if not an admin, you are restricted to selecting your team membership and only assigning to users in those teams 

<br>

To update *Extra Information* or *Additional Emails*, as you begin typing in these fields a *Click to Update* button will appear. Click when the updates are complete. The changes will be saved

<img src=".\images\extra_info_and_emails.png" alt="Extra Info" style="zoom:80%;" />

Remember to separate additional emails with commas. E.g. user1@krestfield.com,user2@krestfield.com

