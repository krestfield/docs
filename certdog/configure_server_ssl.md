---
layout: default
title: Configuring the Server's SSL Certificates
parent: Certdog
nav_order: 4
---
# Configuring the Server's TLS Certificates

 

The system uses TLS server certificates to protect the UI and API end-points  

Once installed, the system will be configured with a default SSL certificate issued under a test CA with the subject ``CN=127.0.0.1``  

With this certificate in place, you will see warning when accessing via a browser and REST API calls may fail  



You may temporarily, install the associated root certificate, located here:

``[Install Dir]\config\sslcerts\dbssl_root.cer``

into the Local Machines' **Trusted Root Certification Authorities** store. This will remove the obvious browser errors.  But this is a temporary measure and you should replace this certificate by following the steps below 



### Create a New SSL Certificate

1. Ensure you have a **Certificate Issuer** configured which includes either an ADCS Template or Local CA Profile that supports SSL/TLS. If one has not yet been configured, refer to the [Create a Local Certificate Issuer](create_local_certificate_issuer.html) or [Create an ADCS Certificate Issuer](create_adcs_certificate_issuer.html) guides
2. **Choose Request > DN Request** from the menu

<img src=".\images\ssl_cert_req.png" alt="image-20210116155244109" style="zoom:67%;" />

For **Subject DN** enter the server DNS name as the CN value. E.g. if your server is called ``myserver.com`` the DN would contain ``CN=myserver.com``  

Choose the **Issuer** and **CSR Generator** to process the request  

Click on **Subject Alternative Names** and add a DNS entry that matches the server name e.g. myserver.com  

Enter a password and click Request Certificate  

When the certificate has been issued, click Download PKCS12 and save the file to ``.\certdog\config\sslcerts``  

You can choose any filename and password you like for this certificate. The initial filename is **tomcatssl.p12** with a temporary password of **temp1234!**  

If you reuse these values no other updates are required and the new SSL certificate will take effect once you restart the application  

If you have chosen a strong password and/or changed the filename, perform the following steps:  

1. Open ``.\certdog\tomcat\conf\server.xml``
2. Locate the following section:
```xml
    <Connector port="443"
    	   address="0.0.0.0"
	       scheme="https" secure="true"
           SSLEnabled="true" clientAuth="false"
           sslProtocol="TLS"
           keystoreFile="C:/certdog/config/sslcerts/tomcatssl.p12"
           keystorePass="temp1234!" keystoreType="PKCS12"/>
```
3. Set **keystoreFile** to point to your new p12 file and set **keystorePass** to be the new password
4. Save ``server.xml``
5. Restart the application



