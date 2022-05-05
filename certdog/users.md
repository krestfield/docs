---
layout: default
title: Users
parent: Certdog
nav_order: 6
---

# Users

A user can authenticate via the UI or to the API (See [REST API](rest_api_overview.html))  

A user account can be a member of a team and, via the team permissions, then has access to specific Certificate Issuers  

The management of Active Directory users remains with Active Directory - you cannot edit those accounts here, although when an AD user logs in, their account will show up in the list of users  

Users may also be sent emails on certificate issuance and reminders when certificates are nearing expiry   

---
### Creating a User Account
As an administrator, select **Users** from the menu  

Click **Add New User**  

<img src=".\images\users3.png" alt="New User" style="zoom:80%;" />



Enter a **Username**  and an **Email Address**  

For the password, you can choose a password for the user or you can click **Generate random password and email**.  This will generate a strong password and email to the email address configured. By default, the user will also have to change this password on first use  

See [Email Settings](email_settings.html) to edit the message that is sent to the user  

You can also just set a password manually and also have the option at any time of selecting the **Force change at next login**

Choose the team(s) to add the user to. Note that if no team is chosen, the user will be able to login but will be unable to request any certificates as *Certificate Issuer* permissions are managed at the team level  

Click **Add**  

Note you cannot add Active Directory accounts - they are still managed via Active Directory and what they can access in the system is defined by the group mappings made to [Teams](teams.html)

---

### Editing and Deleting Users

Select Users from the menu and click on the user account you wish to update  

<img src="./images/users2.png" alt="image-20210222211340396" style="zoom:80%;" />

Click **Edit** or **Delete** as required  

Note that when editing a user, if you do not enter a new password the existing password will remain set. Thus, you may edit the email address, team membership and whether the account is enabled or not without having to reset the password  

<img src=".\images\users4.png" alt="Edit User" style="zoom:80%;" />

Editing a user also displays the last login time and IP address  

If the account is an Active Directory you will be unable to make any changes as all details are managed by Active Directory





