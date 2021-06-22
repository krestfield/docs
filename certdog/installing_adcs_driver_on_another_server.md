---
layout: default
title: Installing ADCS on Another Machine
parent: Certdog
nav_order: 60
---

# Installing the ADCS Agent on another machine

  

The free version of certdog assumes that all components will be installed on the same machine. But if you wish to connect to a Microsoft CA on another domain (or from a non-domain connected machine), you will need to install the ADCS driver separately

To do this, you need to make some changes to the free version's installation. We will re-install the database to make it accessible to external servers then install the ADCS driver on the new machine and configure it with the database URI

  

  

### Un-install the Database

From your certdog installation

1. Open a <u>new</u> PowerShell window as Administrator and navigate to the``.\certdogfree\install`` folder

2. Run the following commands:

   ``.\uninstall-db.ps1``

   When prompted, choose **y** to continue

   ``.\reset-db.ps1``

   When prompted, choose **y** to continue	

<br>
<hr>

### Edit Files with the new IP Address

Obtain the IP address of the server's externally visible interface. This is the IP address that the external ADCS Agent will connect to. On Windows you can run ``ifconfig`` to get this information. You will need this IP Address to plug-in to files in the next steps



Edit ``.\certdogfree\install\js\createreplicateset.js``

Replace the default ``127.0.0.1`` IP Address with your server IP Address. For example, if your server IP was ``192.55.13.17`` the file would be updated from:

```javascript
rs.initiate({_id: "replocal", members: [{_id: 0, host: "127.0.0.1:27017"}] })
rs.status
rs.status()
```

To this:

```javascript
rs.initiate({_id: "replocal", members: [{_id: 0, host: "192.55.13.17:27017"}] })
rs.status
rs.status()
```

Save the file  

<br>  

2. Edit: ``cerdogfree\install\templates\mongod.template.nossl.cfg``

Replace the default ``127.0.0.1`` bindIp address with ``0.0.0.0``. E.g.   

From:

```
net:
   bindIp: 127.0.0.1
   port: 27017
```

To this:

```shell
net:
   bindIp: 0.0.0.0
   port: 27017
```

Save the file  

  <br>

<hr>

### Re-Install the Database

From the PowerShell prompt, navigate to ``.\certdogfree\install`` and run: 

``.\install-db.ps1``

At the prompt: ``Download the database binaries (y/n)? (Choose n if you have previously downloaded)`` Choose **n**

Continue through the prompts, entering the required details as for the original installation (note: the passwords do not need to match the original installation, all will be reset)  

<hr>

### Obtain the connection string

Open the ``.\certdogfree\config\application.properties`` file, it will look something like the following:

```bash
spring.data.mongodb.uri=mongodb://certmanuser:bFhvqunuZRdvCZK@127.0.0.1/certman
management.endpoint.info.enabled=true
management.endpoints.web.exposure.include=*
server.error.include-message=always
logging.level.root=FATAL

# Check for cert expiry at 2:15AM every day
# It you want to change this ensure the cron setting is correct else, you could produce
# many unwanted emails - or none at all...
certexpirycheck.cron=0 15 2 * * ?
```

The part we are interested in is the top line. i.e.:

```powershell
spring.data.mongodb.uri=mongodb://certmanuser:bFhvqunuZRdvCZK@127.0.0.1/certman
```

We need the URI to configure the ADCS driver in the next step



Extract the string after the equals sign and replace the ``127.0.0.1`` IP address with your server's IP address. For example, if your server's IP address was ``192.55.13.17`` the string we want would be as follows:

```
mongodb://certmanuser:bFhvqunuZRdvCZK@192.55.13.17/certman
```

This string will be entered at the ADCS Driver next...

<hr>

### Install the ADCS Agent on the new machine

Download the ADCS stand-alone Installer from [here](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/adcsdriver_v120.zip)  

Unzip to a file on the new server  

Open a PowerShell window and navigate to ``[unzipped location]\adcsdriver\`` and run  

​	 ``.\install-certdog-adcs-service.ps1``  

The following output will be shown:

```powershell
PS C:\certdogfree\adcsdriver> .\install-certdog-adcs-service.ps1

AD Certificate Services Agent
-----------------------------

Do you wish to install the ADCS agent on this machine (y/n)?: y

Installing Adcs agent from C:\certdog\adcsdriver\AdcsDriverInstaller.msi
Services installed OK

Configure Adcs Service

Enter the full database URL. E.g. 'mongodb://certmanuser:mypassword@localhost/certman'

Full Database URL: 
```

When prompted to enter the full database URL, enter the string we obtained in the step above e.g.

```powershell
Full Database URL: mongodb://certmanuser:bFhvqunuZRdvCZK@192.55.13.17/certman
```

  The script will then continue:

```powershell
Starting the service...

Service started OK
If the database URL changes, re-run this script
```



  

The certdog database will now be able to accept connections from the ADCS agent. Note: Firewall restrictions must allow the port **27017**  

If the ADCS agent does not register, attempt to telnet from the server to the certdog server IP address on port 27017 e.g.

```powershell
telnet 192.55.13.17 27017
```

If this fails to connect, there is most likely a firewall restriction in place, at the network layer or on the server hosts. This must be relaxed for this port



