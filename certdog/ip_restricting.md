---
layout: default
title: IP Restricting
parent: Certdog
nav_order: 55
---

# IP Address Restricting



It is possible to restrict access to certdog via IP address filtering. Both IPv4 and IPv6 addresses are supported  

IP addresses are permitted or whitelisted (rather than denied) and these settings are managed at the *Team* level  

<br>

### Setting Permitted IPs

Select **Teams** from the menu and either click **Add New  Team** - to create a new team or choose a team and select **View/Edit**  

More information on setting teams can be found [here](teams.html) but the section of interest is:

<img src=".\images\permitted_ips1.png" alt="Permitted IPs" style="zoom:80%;" />

Here you enter a comma separated list of IP addresses, where addresses can be in the following forms:

* Specific, individual addresses e.g. ``192.168.15.10``  

* A range e.g. ``192.168.15.1-192.168.15.128``

* Wildcarded e.g. ``192.168.15.*``

You may specify as many of each as you like to build your permitted IP string. E.g.

```
192.168.15.10, 192.168.15.11, 10.15.116.1-10.15.116.128, 10.15.117.*
```



**Note**

* If the list is empty - users will be able to access from any IP address. There will be no restrictions  

* If any rules are in place, access from localhost is always permitted i.e. you cannot restrict access to certdog from the machine it is running on
  

### Processing

Users may be a member of one of more teams. For each team the permitted IP list is concatenated. For example, if a user is a member of Team A which has the following Permitted IPs set:

```
192.168.1.1-192.168.1.128
```

And they are also a member of Team B which has the Permitted IPs set as:

```
192.168.16.4, 192.168.16.5
```

Then the user may access certdog via any of the following IP addresses:

```
192.168.1.1-192.168.1.128, 192.168.16.4, 192.168.16.5
```

I.e. any IP address allowed from both teams. For example, if their IP address was: ``192.168.1.12`` they would be permitted access

<br>

### Recommendations and Tips

Having multiple teams with lists of permitted IPs can get confusing. Consider creating teams that are used only for IP permissions. For example, you could create a team such as:

<img src=".\images\permitted_ips2.png" alt="Permitted IPs Team" style="zoom:80%;" />

Then make all users that require this restriction members of this team -  alongside other teams that provide them with access to the required Certificate Issuers

<br>

It is advised to create a single Administrator team and then add in all users requiring administration privileges to that team. You can therefore restrict administrators to specific IPs. For example, you may only want to allow administrators to be able to access the system from localhost. In this case simply set the Permitted IPs for the Administrator team - this can be an IP address such as ``127.0.0.1`` as when any rules are set access from localhost is always permitted anyway

<br>

Set Permitted IPs carefully, it is quite easy to inadvertently lock users out. Remember that access from localhost is always permitted. Therefore, if all users are accidentally locked out, access certdog from the local machine to correct
