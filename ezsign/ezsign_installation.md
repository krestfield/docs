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

<br>

### The lib folder and upgrades

The server scripts (including the Management Tool scripts) load **every** jar in the ``EzSignServer/lib`` folder. If two jars contain the same class at different versions, either copy may be loaded, which shows later as an error such as ``NoSuchMethodError`` or ``NoClassDefFoundError``. To avoid this:

* When upgrading, **replace** the whole ``EzSignServer/lib`` folder with the new one rather than copying the new jars into it, so no jar from the old version is left behind
* Do not copy other jars into ``EzSignServer/lib``. In particular the EzSign client jar (from ``EzSignClient/lib``) is for client applications and is not needed by the server

From version 4.6.0 the server and the Management Tool check for this when they start. Each class found in more than one jar with different contents is logged as an error by the server (and printed as a warning by the Management Tool), naming the jars, so the out of date jar can be removed. By default the server still starts; set ``server.failOnClasspathConflicts=true`` to stop it starting instead. The server also logs the EzSign version and the jar it was loaded from

For nCipher HSMs the account running the server must have access to the nCipher ``kmdata/local`` folder. This is usually achieved by adding the user to the ``nfast`` group
