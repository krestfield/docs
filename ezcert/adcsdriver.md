---
layout: default
title: ADCS Driver
parent: EzCert
nav_order: 2
---
# ADCS Driver

This component is the interface to ADCS (Active Directory Certificate Services) 

As any driver can process requests to a CA you can install on several servers in the same, or different domains



## Requirements

- Windows Server 2016
- Windows Server 2019
- .NET Framework 4.8

The server hosting the driver must be in the same domain as the CA

Ensure that port 4474 is open to wherever the database is hosted


## Installation

1. Download the installer from [here](https://www.krestfield.com) 

2. Unzip onto a location on a supported server (see [Requirements](## Requirements)) 

3. Run the .msi installer

   

## Configuration

At this point, the agent is installed but needs to be configured to connect to the EzCert instance
We do this by running a powershell script
Note: This only has to be done on first install.  For upgrades (or if you are just re-installing) skip to step 10. 
If you change the user the service is running under, or 

   

   



## File Logging

To enable more logging, set the following environment variable to true:

``ADCS_DRIVER_FILE_LOGGING``

e.g.  
![image-20201222143624266](C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\loggingenvvar.png)

Log file will be written to:

``Environment.SpecialFolder.CommonApplicationData \Krestfield\AdcsAgent``

Which is here in Windows Server 2019

``C:\ProgramData\Krestfield\AdcsAgent\log.txt``



Note: This log provides debug level, verbose output and may be useful for tracing issues but the log file will continue to grow.  You should therefore, switch this level of logging off when not required

 

## Threading

By default, the driver creates a number of threads (typically 5) to process certificate requests. But this value can be tuned, if required

To change this value, set the following environment variable to the number of threads required:  

``ADCS_DRIVER_THREADS``

e.g.  
![image-20201222143722766](C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\threadsenvvar.png) 



