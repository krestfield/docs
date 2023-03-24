---
layout: default
title: Debian Installation
parent: Certdog
nav_order: 200
---

# Certdog RedHat Installation

<br>

## Pre-Requisites

* A RedHat 8 installation. Note that other versions may work but this version is confirmed

* Java 8 or above

* An account with sudo/root permissions

* The ability to install mongodb community edition

  

It is recommended that a separate, dedicated user be created which will run the certdog application, although it can be run under an existing account

<br>

## Install Mongo DB

Follow the instructions to download and install Mongo DB Community Edition e.g.

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-red-hat/

At the time of writing, the following was performed:

Create a new yum repo file for mongodb e.g.:

```
sudo vi /etc/yum.repos.d/mongodb-org-6.0.repo
```

Populate this file with the following and then save:

```
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
```

Then run:

```
sudo yum install -y mongodb-org
```

And start the database with the following command:

```
sudo systemctl start mongod
```

<br>

Confirm mongo DB is running by typing:

```
mongosh
```

and ensure you connect and get the mongo db prompt. Type ``exit``, to exit the prompt

<br>

Note, by default the mongo configuration is here:

```
/etc/mongo.conf
```

and mongo database files here:

```
/var/lib/mongo
```



<br>

## Get Certdog

See [here](download-locations.html) for the download locations



## Installation

From the location where you wish to locate certdog, extract the installation e.g.

```
sudo tar xvfz ./certdog.tar.gz
```

This will extract all files into ``./certdog``

Navigate to:

```
./certdog/install
```

and run:

```
./configure.sh
```

The configuration will start and will take a few seconds to complete:

```shell
-------------------------------------------------------------------------------
Configuring Certdog...please wait...
-------------------------------------------------------------------------------

Configuration is complete
```

If you see any errors or things do not seem to be working, first examine the install log:

```
./certdog/install/install_log.txt
```

Other logs, including the application (certdog.log) and startup/shutdown logs are stored here:

```
./certdog/logs
```

<br>

Certdog will be available on ``127.0.0.1`` on port **1443** e.g.:

```
https://127.0.0.1:1433/certdog
```

CRLs and OCSP services will be available on port **1480**

Follow the steps below to configure the firewall to forward the standard ports of 443 and 80 to these internal ports  

Note that until you configure a trusted SSL certificate you will be presented with browser warnings when navigating to this address. See the [Final Configuration](#final-configuration) section below to configure a trusted SSL certificate  

<br>

### Port Forwarding

If using the firewall, running the following commands will forward port 443 to the internal port 1443 and port 80 to the internal port 1480

```
firewall-cmd --add-forward-port=port=443:proto=tcp:toport=1443
firewall-cmd --add-forward-port=port=80:proto=tcp:toport=1480
firewall-cmd --runtime-to-permanent
```

Note that this port forwarding may not work from the local machine but should be available when calling this machine using its IP address/FQDN

<br>

### Final Configuration

Now follow [the guide here](configure_server_ssl.html) to configure an SSL certificate

<br>

## Post Install

Open a browser on the server and navigate to:

https://127.0.0.1:1433/certdog

Login with the initial username and password as displayed at the end of the installer. These are temporary credentials - as soon as you first login with these details you will be forced to set a new password

Follow [the guide here](configure_server_ssl.html) to configure an SSL certificate

<br>

## Starting/Stopping

In this folder:

```
./certdog/bin
```

There are two scripts:

* start-certdog.sh
* shutdown-certdog.sh

You may examine these scripts, or configure such that the application starts on boot following standard processes for your OS

<br>

To start and stop the mongo database you may use the following commands:

```
sudo systemctl start mongod
sudo systemctl stop mongod
```

<br>

## Troubleshooting and Known Issues

#### CRL Locations

When creating a new CA and setting **Generate CRLs** you may get the error: ``The CRL filename must be a complete path. The path in the filename specified: [path to CRL file] does not exist``

This is because the path is not reported consistently. The correct path should be:

```
[installation directory]/tomcat/crlwebapps/certdog#crl/[CRL Name].crl
```

E.g.

```
/home/pkiuser/certdog/tomcat/crlwebapps/certdog#crl/rootca.crl
```

But may be displayed as something like the following:

```
/home/pkiuser/certdog/crlwebapps/certdog#crl/rootca.crl
```

Just update the to the correct path manually



#### OCSP API End Point URL

When creating a new CA , if the **Create OCSP Server** option was selected but no certificate has been issued to the OCSP server, check the logs  

If a ``Connection refused`` error such as the following is seen:

```
Unable to renew OCSP signing certificate for OCSP Server: OCSPServer-test-64143f37f95e3d1466af2316-6735. Error: I/O error on POST request for "https://127.0.0.1/certdog/api/login": Connect to 127.0.0.1:443 [/127.0.0.1] failed: Connection refused (Connection refused); nested exception is org.apache.http.conn.HttpHostConnectException: Connect to 127.0.0.1:443 [/127.0.0.1] failed: Connection refused (Connection refused)
```

This is because the server assumes the API will be listening on port 443. On RedHat the default *internal* port will be 1443

To correct, from *OCSP Servers*, edit the OCSP configuration of the OCSP server in question and alter the URL so that the 1443 port is specified e.g. change from:

```
https://127.0.0.1/certdog/api
```

to:

```
https://127.0.0.1:1443/certdog/api
```

Monitor the logs and OCSP server configuration and confirm that a certificate is then generated



#### Other Troubleshooting

Examine the log files as mentioned above  to see if anything obvious appears  

Attempt to stop and start certdog using the ``./shutdown-certdog.sh`` and ``start-certdog.sh`` scripts  

Try restarting the database then restarting certdog  

<br>

Full Certdog Documentation can be found here: [https://krestfield.github.io/docs/certdog/certdog.html](https://krestfield.github.io/docs/certdog/certdog.html)



