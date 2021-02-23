---
layout: default
title: Teams
parent: EzCert
nav_order: 8
---

# Teams



Teams group users and permissions together  

A team manages the permissions for Certificate Issuers and dictates whether members are administrators or standard users  

By default, one team exists called *Admin Team*  

You may add, remove or edit teams as per your requirements. However, generally, it is advisable to maintain a single administrator team (rather than multiple) and have separate teams for specific Certificate Issuer access  

This will enable you to quickly search and view users with administrative privileges on the system. If a user requires administrative access, they can then be added to this one team   

---

### Add a Team

Select **Teams** from the menu, click **Add New  Team**

<img src=".\images\teams1.png" alt="image-20210222155155216" style="zoom:67%;" />

Enter a **name** and optionally, a **description**  

Select the **Certificate Issuers** that you want to be available to members of this team 

If you wish to make everyone in this team an administrator, select the **Administrator** option  

Click **Add**  

---

### Add a User to a Team

Click **Users** from the menu  

Search for and click on the User then select **Edit**  

 <img src=".\images\teams2.png" alt="image-20210222160044126" style="zoom:67%;" />

Select the teams from the *Teams* list. Multiple teams may be selected (in windows you can select multiple by holding down CTRL, on Mac OS you hold down the Command Key). Click **Update**  

Note that if a user is already a member of any teams their resulting permissions will be displayed beside *Current Certificate Issuers*. This view is only updated once the user has been added to a team (it will not change as you select the teams from the list)  



If you wish  to change *your ow*n permissions

1. Click the ![image-20210109153916067](C:/Users/darre/Documents/_mystuff/development/_Krestfield Products/docs/ezcert/images/user_icon.png) icon and select **Profile**   

2. Select the *Teams* you wish to be a member of 
3. Click **Update**



If a user is not a member of any Team, they will be able to logon to the system and view certificates but not request certificates nor make any changes to the system