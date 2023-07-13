---
layout: default
title: Debian Installation
parent: Certdog
nav_order: 200
---

# Certdog Debian Installation <br>

<br>

## Pre-Requisites

* A Debian 11 (bullseye) installation. Note other versions may work but this version is confirmed

* An account with sudo/root permissions

* The ability to install mongodb community edition

  

It is recommended that a separate, dedicated user be created which will run the certdog application, although it can be run under an existing account

<br>

## Install Mongo DB

Follow the instructions linked below to download and install Mongo DB Community Edition. The Debian installation has been tested and confirmed to work with MongoDB Community Edition 5.0.9 and 6.0.7.

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-debian/

Confirm mongo DB is running by typing:

```
mongosh
```

and ensure you connect and get the mongo db prompt. Type ``exit``, to exit the prompt

<br>

## Get Certdog

1. Download Certdog from [here](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/debian/certdogfreev190.tar.gz)

   File Hashes:

   * SHA1: ``edebedb0c5571603ce00b629c476f0832d3fbfad``

   * SHA256: ``28d0344832709a5f9b4691d041779f350ebec3202ebb7fe99f85afabf9b7eda3``

e.g.

```
curl https://krestfield.s3.eu-west-2.amazonaws.com/certdog/debian/certdogfreev190.tar.gz --output certdog.tar.gz
```

<br>

## Installation

Extract the installation e.g.

```
tar xvf ./certdog.tar.gz
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

The installation will start and will take a few minutes to complete:

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

Other logs, including the mongodb, application (certdog.log) and startup/shutdown logs are stored here:

```
./certdog/logs
```

<br>

<br>

By default the main certdog application listens on port 1443 on all interfaces and the CRL server on port 1480. To access over the standard ports (443 and 80) you must configure routes. For example:

```
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 1443
sudo iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 1480
sudo iptables-save
```

This will redirect incoming traffic on port 443 to 1443 and port 80 to 1480

<br>

You may need to open firewall rules to allow ports 80 and 443, e.g.

```
sudo iptables -I INPUT -p tcp -m tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT -p tcp -m tcp --dport 80 -j ACCEPT
sudo iptables-save
```

<br>

To confirm that the application is listening on ports 1443 and 1480, you may use 

```
netstat -tuplen
```

Which should show something like the following:

```
Proto Recv-Q Send-Q Local Address           Foreign Address         State       User       Inode      PID/Program name
tcp        0      0 127.0.0.1:27017         0.0.0.0:*               LISTEN      108        146542     -
tcp6       0      0 :::1443                 :::*                    LISTEN      1004       139335     -
...
```

Which indicates port 1443 is listening in all interfaces

<br>

Note that on Debian, iptables may not be persisted at reboots. After running the above commands you can persist the changes across reboots by installing the iptables-persistent package, as follows:

```
apt-get install iptables-persistent
```

If you need to make changes, first uninstall the package:

```
sudo apt-get remove iptables-persistent
sudo apt-get purge iptables-persistent
```

Then make the iptables updates and re-install

<br>

Enable any other firewall rules that may be in place to allow ports 80 and 443 to the server e.g. in Azure Networking or AWS Security Groups

<br>

## Post Install

Open a browser and navigate to:

>  https://[Server Name or IP]/certdog

You will observe a browser SSL error which is due to the initial default SSL certificate. See [here](https://krestfield.github.io/docs/certdog/configure_server_ssl.html) to reconfigure the SSL certificate for your server. For now you may bypass the warning  

Login with the initial username and password as displayed at the end of the installer. These are temporary credentials - as soon as you first login with these details you will be forced to set a new password

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



### Start on Boot

To start the mongo database on boot, run the following command:

```
sudo systemctl enable mongod
```

To start certdog on boot, run the following command to start the crontab editor:

```
crontab -e
```

Then enter the following line (after the comments and any other cron entries):

```
@reboot /home/certdoguser/certdog/bin/start-certdog.sh
```

(replace the ``/home/certdoguser`` location with wherever your installation resides)

<br>

## Troubleshooting

Examine the log files as mentioned above  to see if anything obvious appears  

Attempt to stop and start certdog using the ``./shutdown-certdog.sh`` and ``start-certdog.sh`` scripts  

Try restarting the database then restarting certdog  



To attempt a re-install, perform the following:

Remove the created database and user from mongodb:

Start the mongo shell:

```
mongosh
```

Then enter the following commands:

```
use certman
show users
db.dropUser("certmanuser")
db.dropDatabase()
```



Remove the files created within the install:

```
cd
cd ./certdog/config
rm -f MASTERPASSWORD.txt
rm -f application.properties
rm -f ./pwd/*
```



Ensure no rogue processes are running, such as java:

```
ps -ef | grep "certdog/java"
```

And for each entry, kill the process, forcibly:

```
kill -9 [Process ID]
```



Then re-run the ``./configure.sh`` script

<br>

Full Certdog Documentation can be found here: [https://krestfield.github.io/docs/certdog/certdog.html](https://krestfield.github.io/docs/certdog/certdog.html)
