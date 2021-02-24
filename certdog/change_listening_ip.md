---
layout: default
title: Change Listening IP Address
parent: Certdog
nav_order: 14
---


# Change Listening IP Address

This document details how to configure the application so that the UI and API are accessible on either a specific IP address or all available IP addresses

1. Open the following file

   ``.\certdog\tomcat\conf\server.xml``

2. Navigate to the section starting ``<Connector port="443"``, this section may look like the following

   ```xml
       <Connector port="443"
       	   address="127.0.0.1"
   	   	   scheme="https" secure="true"
              SSLEnabled="true" clientAuth="false"
              sslProtocol="TLS"
              keystoreFile="C:/apps/certdog/config/sslcerts/tomcatssl.p12"
              keystorePass="*somepassword*" keystoreType="PKCS12"/>
   ```

3.  Locate  the ``address="127.0.0.1"`` section and change the IP to a specific IP address (e.g. ``192.168.10.155``) or set it to ``0.0.0.0`` if you want the application to listen on all IP addresses

4. Save the **server.xml** file

5. Restart the application by either restarting the Krestfield Certdog Service or running the following scripts:

   ``[Install Location]\bin\stop-tomcat.ps1``

   ``[Install Location]\bin\start-tomcat.ps1``





