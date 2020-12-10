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

   

   





