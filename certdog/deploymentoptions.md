---
layout: default
title: Deployment Options
parent: Certdog
nav_order: 21
---
# Deployment Options



certdog can be deployed on

* Windows Server 2016

* Windows Server 2019
* Windows 10

* Mac OS

* Linux (including RedHat, Debian and Ubuntu)

However, the ADCS agent (the interface to the Microsoft CA) can only be deployed on the Windows Server platforms



### Single Server Installation

There are several options available when deploying certdog, the simplest is to install all components on the same Windows server:

<img src=".\images\deployment1.png" alt="image-20210226152239356" style="zoom:67%;" />



This is the default installation and if the host is in the same domain as your Microsoft CA, then the ADCS Agent will be able to access it. Other CAs (e.g. PrimeKey EJBCA) will also be accessible as long as network rules allow  



### Single Server - Multiple ADCS Instances

The host does not need to be in the same domain (or any domain), nor on the same operating system as the Microsoft CA.  It can access CAs in other and multiple Microsoft domains, as shown below:

<img src=".\images\deployment2.png" alt="image-20210226154741211" style="zoom:67%;" />

In this example, the host could be a Linux machine.  Domains 1 and 2 would be two separate active directory domains, that may or may not have a trust relationship

For each domain, an ADCS agent would be deployed onto a server that is in the same domain as the CA i.e. Server 1 and Server 2 in this example 

Outgoing ports (by default these are 27017,27018 and 27019) from the servers (Server 1 and Server 2) would need to be opened to the Linux host



### Multi Server Load Balanced

The main components can all easily be split across several servers for load-balancing and redundancy

![image-20210226160951017](.\images\deployment3.png)

The API can be placed in several different locations - as long as it can access the database (or an instance in the cluster)

In the example above, there is a dedicated server hosting the API (Server 2). You may wish to do this if you were to dedicate that instance to integration API calls e.g. from your own applications or scripts

The database can be clustered and hosted across multiple servers...or in the cloud



### Cloud and On Premises

The examples given above can be applied to cloud as well as on-premises and other hosted services, for example:

<img src=".\images\deployment4.png" alt="image-20210226171252202" style="zoom: 50%;" />

In this example you have the database located in AWS. Mongo offer the Atlas service, which allows for clustering, monitoring and access controls

You could run other services in AWS  including the API or UI or, as shown above, in Azure  

This could connect back to your on-premises CAs, via the ADCS agent and you could use other hosted services such as those offered by PrimeKey for EJBCA



## Summary

Deployment of certdog is flexible in order to fit in with any environment, options are not limited to those mentioned above  

If you wish to discuss your requirements with us, drop us a line at 

[support@krestfield.com](mailto:support@krestfield.com)

