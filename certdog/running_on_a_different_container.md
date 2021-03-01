---
layout: default
title: Running on a different container
parent: Certdog
nav_order: 15
---

# Running on a different container



By default the system runs on a provided Tomcat servlet container, but it can also be deployed on an existing container. If you choose this option, there are a few things that must be considered:



### Environment Variables

When the system starts it requires the following environment variables to be set:

* spring_config_location
  * This references the *spring* properties file
  * In the default installation this file is located here:
  ``.\certdog\config\application.properties``
* cmmasterpassword
  * This is the master password which was entered during installation



The system cannot start without these settings  

Normally, the start scripts (e.g. ``.\start-certdog.ps1``) configure these variables. On Windows the Service secures the master password and sets it as the environment variable when it starts the application



If using another (e.g. shared) instance of Tomcat, these variables can be provided in the ``setenv.bat`` or ``setenv.sh`` file which should be placed in the ``[Tomcat Home]\bin`` directory. E.g.

```shell
set spring_config_location=C:/certdog/application.properties
set cmmasterpassword=somepassword
```

On Linux/Unix

```shell
export spring_config_location="/opt/certdog/application.properties"
export cmmasterpassword="somepassword"
```



Note that if the ``cmmasterpassword`` value starts with ``file:`` it will read the master password from the file referenced which can be more secure e.g.

```shell
set cmmasterpassword=file:C:/certdog/secure/masterpassword.txt
```



If the database is secured with an untrusted SSL certificate (e.g. if you are still using the default certificate) then you must also provide the JKS (Java Key Store) that contains the root certificate as java options e.g.

```shell
set JAVA_OPTS=%JAVA_OPTS% -Djavax.net.ssl.trustStore="/opt/certdog/config/sslcerts/dbssltrust.jks" -Djavax.net.ssl.trustStorePassword=password
```

It is recommended that a certificate from a trusted CA be used to secure the database



A complete ``setenv.bat`` file could look like:

```shell
set spring_config_location=/opt/certdog/application.properties
set cmmasterpassword=file:/opt/certdog/secure/masterpassword.txt
set JAVA_OPTS=%JAVA_OPTS% -Djavax.net.ssl.trustStore="/opt/certdog/config/sslcerts/dbssltrust.jks" -Djavax.net.ssl.trustStorePassword=password
```

``setenv.sh``:

```shell
export spring_config_location="/opt/certdog/application.properties"
export cmmasterpassword="file:/opt/certdog/secure/masterpassword.txt"
export JAVA_OPTS="$JAVA_OPTS -Djavax.net.ssl.trustStore="/opt/certdog/config/sslcerts/dbssltrust.jks -Djavax.net.ssl.trustStorePassword=password"
```



If you do not wish to use the ``setenv`` mechanism, the account starting the services should have these environment variables set



### Application Properties

This file was mentioned above and is referenced by the **spring_config_location** property. It contains a few pieces of information including the database URL and the certificate expiry checking schedule  

By default this file resides in ``.\ecert\config\application.properties``  

Ensure you copy this file to a location that is accessible by the container




### Deploying Applications

From the ``.\certdog\tomcat\webapps`` directory, copy the ``certdog#ui`` folder and the ``certdog#api.war`` file to the new container's application deployment area  

The ``ROOT`` folder just contains a redirection such that if a user navigates to the home location of the site e.g.  

https://mysite.com  

They will be re-directed to the UI application e.g.  

https://mysite.com/certdog/ui  

It does not need to be copied across unless you want to maintain this behaviour



 