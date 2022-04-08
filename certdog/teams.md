---
layout: default
title: Teams
parent: Certdog
nav_order: 8
---

# Teams



Teams manage permissions to *Certificate Issuers*.  Users that are members of these teams inherit these permissions (in the same way as Groups and members of groups work in Active Directory)  

Teams can also restrict members from specific IP Addresses (or ranges of IP Addresses) and suppress email sending to its members  

If the Team is marked as *Administrator* - all members of that team are Certdog Administrators  

Users can be members of multiple teams  

By default, one team exists called *Admin Team* which is set as *Administrator*. The initial admin user is a member of this team meaning they can manage all aspects of the system  

You may add, remove or edit teams as per your requirements and make users members of as many teams as required.  Generally, it is advisable to maintain a single administrator team (rather than multiple). A typical administrator team, as well as having the *Administrator* option set, may also restrict IP Addresses to localhost (127.0.0.1) or specific IP Addresses, meaning that administrators can only authenticate from the local machine or specific machines or networks, thus increasing security  

If you have configured Active Directory (so that users can authenticate to Certdog with their domain accounts), then you can also map Active Directory groups to a team (see more below)  

<br>

---

### Add a Team

Select **Teams** from the menu, click **Add New  Team**

<img src=".\images\teams1.png" alt="New Team" style="zoom:80%;" />



Enter a **name** and optionally, a **description**  

Select the **Certificate Issuers** that you want to be available to members of this team 

If you wish to make everyone in this team an administrator, select the **Administrator** option

<br>

**Active Directory Groups**

If Active Directory has been configured you will also see the following option

<img src=".\images\ad_groups1.png" alt="Active Directory Groups" style="zoom:80%;" />

This is where you can map Active Directory groups to this team. For example, if your PKI certificate security staff were all members of an Active Directory group called PKI_CERT_MANAGERS then you could specify that group here. If this Team had the Administrator option checked, then all the PKI certificate security staff would be administrators in Certdog  

To select a group, click **Click to add groups**:

<img src=".\images\ad_groups2.png" alt="Search AD Groups" style="zoom:80%;" />

The *Search for groups* pane will expand. Type part of the name of the group you wish to search for in the *Search Text* box and click **Search**. Select the required group in the list and click **Add**

<img src=".\images\ad_groups3.png" alt="AD Group Selected" style="zoom:80%;" />

The selected group is now mapped to this team  

To remove a group mapping, simply select the group and click **Remove**

<br>

**Email Suppression**

When certificates are issued, they are associated with a Team. If your [email settings](email_settings.html) are set to send emails upon certificate issuance, an email is sent to the requestor whenever a certificate is issued. If you wish to prevent these emails being sent out for this team, check the **Suppress Cert Issued Emails** option

If you wish to prevent reminder emails being sent for certificates associated with this team, check the **Suppress Expiry Reminder Emails** option

<br>

**Permitted IPs**

If you wish to restrict members of this team from accessing by IP address. Enter the allowed IP addresses here  

IP addresses can be:

* Specific, individual addresses e.g. ``192.168.15.10``  

* A range e.g. ``192.168.15.1-192.168.15.128``

* Wildcarded e.g. ``192.168.15.*``

These can be combined by separating with commas e.g.

```
192.168.15.10, 192.168.15.11, 10.15.116.1-10.15.116.128, 10.15.117.*
```

 Note, if the list is empty no restrictions are applied

See [IP Address Restricting](ip_restricting.html) for more details



Click **Add**  

---

### Add a User to a Team

Click **Users** from the menu  

Search for and click on the User then select **Edit**  

 <img src=".\images\teams2.png" alt="image-20210222160044126" style="zoom:67%;" />

Select the teams from the *Teams* list. Multiple teams may be selected (in windows you can select multiple by holding down CTRL, on Mac OS you hold down the Command Key). Click **Update**  

Note that if a user is already a member of any teams their resulting permissions will be displayed beside *Current Certificate Issuers*. This view is only updated once the user has been added to a team (it will not change as you select the teams from the list)  



If you wish  to change *your ow*n permissions

1. Click the ![image-20210109153916067](./images/user_icon.png) icon and select **Profile**   

2. Select the *Teams* you wish to be a member of 
3. Click **Update**



If a user is not a member of any Team, they will be able to logon to the system and view certificates but not request certificates nor make any changes to the system