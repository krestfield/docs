---
layout: default
title: EzSign Service - Silent Installation
parent: EzSign
nav_order: 25
---

# EzSign Service - Silent Install

> Version 1.4
>
> January 2021



The EzSign service is installed using the **.msi** installer package  

But, if automating a build, it can also be installed silently using the ``msiexec`` command, as outlined below  



### Pre-Requisites

Before installing EzSign, ensure that the following are in place:

* Any HSM client software is installed and the HSM has been configured with the correct passphrases and security world
* If you choose to use your own instance of Java, ensure it has been installed (Java 14 is bundled with the service but you may use any version from 8u241)
* If you are storing your logs and/or keystore files in a location other than the defaults - ensure these folders have been created and the permissions on the folders are correct (to permit write from the service)
* If re-using any previous EzSign property files, ensure they are available
  
  

### Installation

* Step 1  
  

  Open or start a PowerShell instance as Administrator

* Step 2  

  Run the following command

  ```powershell
  msiexec /i EzSignServiceInstallerV1.4.msi /qn /norestart
  ```

  This will perform the install without any interaction  
  Note: To create a log file of the installation, add the ``/l*v [Log File]`` switch. E.g.  

  ```powershell
  msiexec /i EzSignServiceInstallerV1.4.msi /l*v C:\ezsign_install_log.txt /qn /norestart
  ```
To install in a specific directory (other than ``C:\Program Files`` etc.), add the TARGETDIR switch, as follows:
  ```powershell
  msiexec /i EzSignServiceInstallerV1.4.msi TARGETDIR="E:\EzSignService" /qn /norestart
  ```

* Step 3  

  To Start the service after install, run:  
  ```powershell
  Start-Service "Krestfield EzSign Service"
  ```
  You can view the status of the service by running the following:  
  ```powershell
  PS C:\> Get-Service "Krestfield EzSign Service"
  ```

  ```powershell
  Status   Name               DisplayName
  ------   ----               -----------
  Running  Krestfield EzSi... Krestfield EzSign Service
  ```

  


### Configuration

Configuration may then continue as normal. But to automate this part, you may copy the relevant properties and keystore files before starting the service. I.e. after step 2 above  

The files that may need to be copied are:

* The *Service* Properties

  This is, by default stored here: 

  ```powershell
  C:\ProgramData\Krestfield\EzSignService\ezsignservice.properties
  ```

  It contains information relating to the location of java, keystores, the service configuration and the location of the EzSign instance properties

* The *Server* *Instances* Properties Files

  By default, these are held here:

  ```powershell
  C:\Program Files\Krestfield\EzSign Service\EzSign\config
  ```

  But can be anywhere on the file system. You can view their location from the the configuration utility:  

![image-20210129154805057](.\images\image-20210129154805057.png)

* Keystore files

  This is referenced in the properties file mentioned above e.g. in the above example, the following file is referenced:

  ``C:\Program Files\Krestfield\EzSign Service\EzSign\config\test.properties``

  Within this file there will be an entry as follows:

  ``keyStoreDir=C:/keystores`` *Forward slash is required in the properties file*

  It is this location (C:\keystores) including sub-directories and their contents that need to be copied over  

  Note: If you are creating new keys and certificates it is not required to copy the contents or sub-directories across. But the folder (C:\keystores) should be present



Once all relevant files are in place you can continue to start the Service as outlined in step 3 above  



### Uninstall

To uninstall silently, the following command may be run

```
msiexec /x EzSignServiceInstallerV1.4.msi /qn
```

