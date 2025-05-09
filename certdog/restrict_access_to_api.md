---
layout: default
title: Restrict Access to the API
parent: Certdog
nav_order: 550
---

# Restrict Access to the API



You can restrict access to the certdog API from specific IP addresses. Note: You can also restrict Teams to specific IPs or ranges of IP addresses as described [here](ip_restricting.html).  

You may wish to do this to limit access for configuration and the issuance of certificates from the local host for all users. Note that CRL and OCSP services will still be accessible from other IP addresses. 

<br>

To implement this, create a text file called ``context.xml``  

Populate this file as follows:

```xml
<Context antiJARLocking="true" path="/">
    <Valve className="org.apache.catalina.valves.RemoteAddrValve" allow="127.0.0.1" />
</Context>
```

Specifying the IP addresses required in the ``allow=""`` section. Multiple IPs can be specified by separating with the ``|`` character. E.g. ``allow="192.168.54.10|192.168.54.11"``

<br>

Save the file to:

```
..\certdog\tomcat\webapps\certdog#api\META-INF
```

E.g.

```
C:\certdog\tomcat\webapps\certdog#api\META-INF\context.xml
```



