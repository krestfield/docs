---
layout: default
title: nCipher HSM - Integration
parent: EzSign
nav_order: 24
---



# EzSign: Checking the HSM Configuration



Before configuring EzSign with an HSM it is worth performing a quick check that everything is working as expected and all libraries and passwords are correct 

The steps below outline some steps that can be taken to verify everything is ready to go  

 

### HSM Status

The nCipher HSMs provide several commands for verifying the setup is correct

These utilities are normally located here:  

On Linux/UNIX:  

```bash
/opt/nfast/bin
```

On windows:  

```bash
C:\Program Files (x86)\nCipher\nfast\bin
```

 

First run the enquiry command e.g. On Unix from a shell run:

```bash
./enquiry
```

On Windows, from a Command Prompt, run:

```bash
enquiry.exe
```



 

The output will be split into several sections:

```bash
  Server:

  ...

  Module #1:

  ...
```
And if there is more than one module configured you will also see headings for these, e.g.:
```bash

 Module #2:

 ...
```
 etc.




The key things to note are that each of the module entries are showing:

**mode   operational**

 

If there are no entries beneath the Server heading, first try starting the hardserver. On Unix:

```bash
/opt/nfast/sbin/init.d-ncipher start
```

 

On Windows, start the **nFast Server** service

 

### HSM Test Tool

If all looks OK, download the Krestfield HSM Test tool from [here](https://krestfield.s3.eu-west-2.amazonaws.com/trial/hsmtest.zip)

 

Run the tool as follows:

From a UNIX shell:

```bash
./hsmtest.sh
```



From a Windows Command Prompt:

```bash
hsmtest.bat
```

 

```
Krestfield HSM Test Tool

Enter PKCS#11 library path > /opt/nfast/toolkits/pkcs11/libcknfast-64.so  <-- Enter the full path to the PKCS#11 library
  PKCS#11 Token: Loading the PKCS#11 library: /opt/nfast/toolkits/pkcs11/libcknfast-64.so...
  PKCS#11 Token: Loaded PKCS#11 Driver /opt/nfast/toolkits/pkcs11/libcknfast-64.so OK

  HSM Driver loaded OK

  There are 2 slots:

  Slot: 0
   slotDescription:                                
   manufacturerID: nCipher Corp. Ltd       
   flags: CKF_TOKEN_PRESENT | CKF_HW_SLOT
   hardwareVersion: 0.00
   firmwareVersion: 0.00
  Slot: 1
   slotDescription: SFHSMTTOCS                           
   manufacturerID: nCipher Corp. Ltd       
   flags: CKF_TOKEN_PRESENT | CKF_REMOVABLE_DEVICE | CKF_HW_SLOT
   hardwareVersion: 0.00
   firmwareVersion: 0.00

Select Slot > 1 <-- Enter the slot number - normally 1 if an operatore card set is in use
 
  PKCS#11 Token: Opening session...
  PKCS#11 Token: Opened session for slot 1 OK
  HSM Session Opened OK. Session ID: 2251
  
Enter HSM OCS Passphrase > <-- Enter the operator cardset password and press enter

  PKCS#11 Token: Password provided, attempting logon...
  PKCS#11 Token: Logged on to Token

  Logged in OK. Configuration is good
```



This tool performs the same operations to connect to the HSM as EzSign. Therefore, if you see this success message, translating the values entered above into the following properties: 

```properties
channel.1.tokenType=*This must be set to PKCS11*
channel.1.token.password=*Set this as the operator password (as entered above) via the Management Utility*
channel.1.token.pkcs11.library=*Set this to be the same path as entered above*
channel.1.token.pkcs11.slot=*Set this to be the same number slot as entered above*
```

 e.g.

```properties
channel.1.tokenType=PKCS11
channel.1.token.password=Mt3WQvXz6fUy2yhpNC5ZBxCdPJWsy2Ol1QdLH3c1pogbHViP7oDeQA==
channel.1.token.pkcs11.library=/opt/nfast/toolkits/pkcs11/libcknfast-64.so
channel.1.token.pkcs11.slot=1
```



Should result in a successful HSM setup