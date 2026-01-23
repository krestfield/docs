---
layout: default
title: EzSign - Installation
parent: EzSign
nav_order: 2
---
# EzSign Installation

<br>

The software is delivered as either a zip or gzip (tar.gz) file. Unzip and unpack the installation file to a location of your choice

The installation files are organised as follows:

```
[Installation Folder]/EzSignVX.Y.Z/EzSignClient
[Installation Folder]/EzSignVX.Y.Z/EzSignServer
```

(Where X.Y.Z is the version number e.g. EzSignV4.4.0)



The EzSignClient folder (or just the kezsign-client-X.Y.Z.jar file) should be copied to all clients that will be accessing the server

 Within the EzSignClient folder there are the following directories

* /doc – contains EzSignClient documentation
* /lib – contains the EzSignClient jar files
* /samples – contains client samples



 Within the EzSignServer folder there are the following directories

* /bin – scripts to start, stop and manage the server

* /doc – contains this document

* /lib – the EzSignServer libraries

* /logconf – contains the logging (log4j2.xml) configuration file

* /logs – the default location for log files

* /samples – contains sample configurations

 

The product is bundled with a Java runtime but if you prefer to use your own, edit the envs.sh file in the EzSignServer/bin directory and edit the JAVA_HOME parameter so that it points to your JDK/JRE installation folder e.g. 

```
JAVA_HOME=/fs01/app/jdk1.8.0_251
```

 

The account used to run the server must have permissions to access the ``EzSignServer`` folder and be able to execute the scripts (located in the /bin directory) and jar files (located in the ``/lib`` directory). The account must also have read/write access to the keystore location (see the Key Store Files section later)

Client applications must be able to access the jar files located in the ``EzSignClient/lib`` folder

For nCipher HSMs the account running the server must have access to the nCipher ``kmdata/local`` folder. This is usually achieved by adding the user to the ``nfast`` group
