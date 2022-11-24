---
layout: default
title: Refresh Azure Key Vault Credentials
parent: EzSign
nav_order: 50
---

# Refresh Azure Key Vault Credentials

<br>

If when using an Azure Key Vault Token type, you receive an error such as:

```powershell
2022-11-24 10:31:40.391 [main] ERROR EzSignLog - Max retries 3 times exceeded. Error Details: AADSTS7000222: The provided client secret keys for app '7412f649-8e14-471f-bfc1-733b36a42705' are expired
```

This indicates that your credentials have expired. These can be refreshed as follows:

<br>

## Refresh the Token in Azure

Login to the Azure Portal and from the console, navigate to **Azure Active Directory** and select **App Registrations** from the left hand menu  

Click **All applications** and locate the application configured in EzSign

<img src=".\images\azure-apps.png" alt="Azure Apps" style="zoom:80%;" />



This will have the same **Application (client) ID** as specified in the EzSign ``channel.1.token.azureKeyVault.clientId`` property  

Click on this application  

From the top row, click the **Cloud shell** icon which should start the shell. If you are asked to create a storage account, click OK  

From the shell type the following command:  

```powershell
az ad sp create-for-rbac -n [App Name Registered] --skip-assignment
```

Where ``[App Name Registered]`` is the **Display name** of the app you clicked on above (e.g. ``ezsign2``)  

This will output new credentials e.g.

```json
{ 
	"appId": "fd94f971-ebd9-4a32-a56e-97427655429e", 
	"displayName": "ezsign2", 
	"name": "http://ezsign2", 
	"password": "nScc7-6T.gOI7.ugHawFRRoUbwUA_agrC-", 
	"tenant": "d10c2e35-390b-4343-9fb3-36524a35717c" 
}
```

All the settings should be the same as previously configured, except the password entry would have changed  

<br>

## Set the new password in EzSign

Now, start the ``ezsign-manage.sh`` utility, choose the **Set Passwords** option and set this password as the new Token password for the channel. Note that you must enter the password minus the quotes i.e. enter ``nScc7-6T.gOI7.ugHawFRRoUbwUA_agrC-`` and not ``"nScc7-6T.gOI7.ugHawFRRoUbwUA_agrC-"``  

Restart the EzSign server and authentication to Azure should now complete OK









