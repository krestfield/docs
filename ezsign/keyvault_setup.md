---
layout: default
title: EzSign - KeyVault Setup
parent: EzSign
nav_order: 40
---



# Azure Key Vault Configuration

> From version 4.1.3

Note: For previous versions contact [support](mailto:support@krestfield.com)

<br>

This document gives a brief overview of the installation and setup steps required to support Azure Key Vaults from EzSign

<br>

## Pre-Requisites

You must have an Azure account and the correct permissions to either create a Key Vault or manage access to one  

You must have created a Key Vault on the Premium pricing tier (in order to support HSM backed keys)  

You must have registered an application and have the following information available:  

* Client ID
* Tenant ID
* Client Secret
* Key Vault URL

See the [Registering a Client Application](#registering-a-client-application) section below for an example of how to obtain these values

<br>

## Configuring the Software
Navigate to 

```
./EzSignV[Version]/EzSignServer/config
```

and edit 

```
azurekv.properties
```

Update the following properties:  



<u>keyStoreDir</u>  

This is where EzSign stores its key components. When using an HSM of any kind, these components only ever contain references to keys stored on the HSMs  

By default it is set to a relative path ``../keystores`` which means if you run the commands from the ``./bin`` directory this will get picked up ok. But if you call any jars directly then you must set this to the full path. This can point to ``[Install Dir]/EzSignServer/config/keystores`` or you can choose an alternative location. The account running the software must have write permissions on this folder and it must already exist  

e.g.

```
keyStoreDir=/opt/ezsign/EzSignV4.1.0/EzSignServer/keystores
```

<br>

<u>channel.1.token.azureKeyVault</u>  

Set the following properties to the values that were obtained when the client was registered in Azure  

```
channel.1.token.azureKeyVault.clientId=[Client ID]
channel.1.token.azureKeyVault.tenantId=[Tenant ID]
channel.1.token.azureKeyVault.keyVault=[Key Vault URI]
```

Where:  

``channel.1.token.azureKeyVault.clientId`` is client ID/App ID of the client that has been registered in Azure. See the section  [Registering a Client Application](#registering-a-client-application) below for an example on how to register a client  

``channel.1.token.azureKeyVault.tenantId`` is the tenant ID of your Azure subscription

``channel.1.token.azureKeyVault.keyVault`` is the full URI of the Key Vault. This is displayed as the DNS name when viewing the vault from Azure  

Your configuration should then look something like the following:

```
log.level=3
keyStoreDir=/opt/ezsign/EzSignV4.1.0/EzSignServer/keystores

# Azure Key Vault Channel Properties
channel.1.name=Azure
channel.1.tokenType=AZUREKEYVAULT
channel.1.token.azureKeyVault.clientId=3a13c4fa0-4469-ed2c-32c2-c58ad10915b0
channel.1.token.azureKeyVault.tenantId=45bfc4469-fd1c-32f2-b68a-d10915b0654d
channel.1.token.azureKeyVault.keyVault=https://myvault1.vault.azure.net/
channel.1.token.password=
channel.1.signature.keyId=

```

Note that none of the values are surrounded by quotes. Quotes are not required

<br>

Next, open a terminal, shell or command prompt and navigate to  

```
/EzSignV4.1.0/EzSignServer/bin  
```

and run:  

```
ezsign-manage.sh ../config/azurekv.properties
```

Select option ``1. Set Passwords  ``

For the Master Password, enter any strong password. This password will be required to be entered when the server is started  

For the Token Password enter the **Azure Client Secret** or **password**, without any enclosing quotes. This is the password/secret that would have been obtained when registering the client application in Azure  

Re-enter then say **yes** when asked if you wish to update the properties file  

<br>

## Importing Existing Keys  

Keys that are already configured in the Key Vault can be imported into EzSign. Note, that this does not extract any key material from the Key Vault, but rather obtains details about the keys so they can be used by EzSign for signing  

Navigate to 

```
./EzSignV[Version]/EzSignServer/bin
```

 and edit 

```
envs.sh 
```

 set the ``JAVA_HOME`` parameter to the location of java you are using  

Save ``envs.sh`` then run  

```
./ezsign-manage.sh ../config/azurekv.properties  
```

The management utility will start....

```
Krestfield EzSign Management
----------------------------

The master password is required to manage the server
Enter password:
```

Type the master password chosen above (when setting passwords) and press **Enter**

From the options displayed, select

```
4. Import Existing HSM Keys
```

At the *Channels* section, enter the number of the Azure channel and press **Enter**  

For the Token Password enter Azure Application password (Client Secret) and press **Enter**  

```
Importing objects from the HSM...
Objects imported from the HSM OK
```

If you see this message it indicates that the keys (or rather, references to them) have been imported from Azure into EzSign  

To verify, check the keyStores folder configured above. There should now be a sub-directory called Azure which will contain new files with extensions of .priv and .pub e.g.  

```
-rw-rw-r-- 1 ec2-user ezs-user 204 Jul 1 08:12 17305b484ff8593.priv
-rw-rw-r-- 1 ec2-user ezs-user 204 Jul 1 08:12 17305b484ff8593.pub
-rw-rw-r-- 1 ec2-user ezs-user 184 Jul 1 08:12 bass1.priv
-rw-rw-r-- 1 ec2-user ezs-user 184 Jul 1 08:12 bass1.pub
```

If no keys are shown, check your settings and that there are actually existing, enabled keys in the key vault. Checking the logs at ``./EzSignServer/logs/ezsign.log`` will help identify which of these issues have occurred  



## Making Calls from your Java Application

Normally, EzSign is run as a server application called via the Krestfield Client API or a REST API. This is the simplest option and enables local configuration that does not need to be connected to or managed by your application  

However, if you choose to call the java directly, from your java application, add a reference to the following jar:

```powershell
[EzSign Installation Dir]/EzSignV[Version]/EzSignServer/lib/ezsign-[Version].jar  
```



In your application, set the following imports:  

```java
import com.krestfield.ezsign.KEzSign; 
import com.krestfield.ezsign.KEzSignException; 
import com.krestfield.ezsign.KSigningException;
```

and the following is an example showing the use of the KEzSign class for signing:

```java
try { 
	// You can also load the properties in to a java.util.Properties object and 
	// pass this in place of the filename 
	String propertiesFile = "/EzSignV4.1.0/EzSignServer/config/azurekv.properties"; 
	
	// The password here is the master password. If you change this in the 
	// configuration you must also change it here 
	KEzSign ezSign = new KEzSign(propertiesFile, "password", 1); 
	String channelName = "Azure"; 
	
	// hashedData is a SHA-256 hash of the original data 
	// You can provide the raw data (and let EzSign hash it for you) but in production 
	// it is more efficient to hash the data first 
	byte[] hashedData = {0x55, 0xb5 ... 0x9d}; // 32 bytes required 
	
	// The data returned in sig will be a PKCS7 formatted signature 
	byte[] sig = ezSign.signData("1", channelName, hashedData, true); 
} 
catch (KEzSignException e) 
{ 
	e.printStackTrace(); 
} 
catch (KSigningException e) 
{ 
	e.printStackTrace(); 
}
```


<br>

## Registering a Client Application 

A key vault is required to perform the following steps. The key vault must be in the *Premium* pricing tier as this is the only tier that supports HSM backed keys. This option is set at creation, so if your existing target Key Vault is on the *Standard* pricing tier you will need to create a new Key Vault

We will register an application in Azure Active Directory, then create a service principal (SPN) for this application. This will provide us with authentication credentials. Finally we set a policy which allows this application to manage keys and certificates in our key vault

<br>

From the Azure Console navigate to **Azure Active Directory** and select **App Registrations** from the left hand menu  

From the top menu click **New registration**  

Provide a name for the application (e.g. **ezsignhsm**) and click **Register**

Open Azure Cloud Shell either by following a link from the console or by navigating to https://shell.azure.com/  

At the prompt, type:

```powershell
az ad sp create-for-rbac -n [App Name Registered] --skip-assignment
```

 Where [App Name Registered] is the name you registered in the step above e.g. ezsignhsm

```json
{ 
  "appId": "fd94f971-ebd9-4a32-a56e-97427655429e", 
  "displayName": "ezsignhsm", 
  "password": "nScc7-6T.gOI7.ugHawFRRoUbwUA_agrC-", 
  "tenant": "d10c2e35-390b-4343-9fb3-36524a35717c" 
} 
```

Extract and retain the following: 

* appId
  * This is also referred to as the client ID and must be configured in EzSign as the ``channel.1.azureKeyVault.clientId property``
* password
  * Also referred to as the client secret. This must be configured as the token password in EzSign
* tenant
  * This must be configured in EzSign as the ``channel.1.azureKeyVault.tenantId`` property

<br>

We need to configure these values as environment variables in the Azure Shell so we can set further permissions  

From the shell run the following commands:

If using the Bash Shell:

``export AZURE_CLIENT_ID=[value for appId returned above]``

e.g.

```
export AZURE_CLIENT_ID="fd94f971-ebd9-4a32-a56e-97427655429e"
```

Or, if using PowerShell:

```
$AZURE_CLIENT_ID="fd94f971-ebd9-4a32-a56e-97427655429e"
```



Then run the following command (all on one line) to set the permissions for this application on the Key Vault: 

```
az keyvault set-policy --name [key vault name] --spn $AZURE_CLIENT_ID --key-permissions delete get list create sign verify encrypt decrypt wrapKey unwrapKey --certificate-permissions get list
```

You will get a stream of JSON output from this command. Verify it all looks correct for your requirements and adjust any other values as required  

This operation can also be performed from the Azure console, if preferred   

Note: If you are using EzSign for signature generation and verification (including generation of CSRs) only the following key permissions are required:

* create

* get

* list

* delete

* sign

* verify

If you need to import your Key Vault keys into EzSign, you also need the following certificate permissions

* get
* list

If you are using the encrypt/decrypt functionality, you also need the following key permissions

* wrap

* unwrap

To verify all is OK, in the **Azure Console**, navigate to the **Key Vault** and select **Access policies** and verify that the application is registered and the correct permissions have been set. You can alter them here if required by adding and editing access policies  

Note: To obtain the Key Vault URL – this is shown as the DNS name when viewing the Overview details for the Key Vault
         

## Troubleshooting

When signing if you see this an error such as: 

```
The user, group or application 'appid=7f464c48-906f-462f-b0fd-79d904297ee8;oid=7ffdac3f-deb8-4ae2-a019-1015e18db6a3;iss=https://sts.windows.net/d00c2e35-390b-4643-9eb3-36524c35707c/' does not have keys sign permission on key vault 'ezsign;location=westeurope'. For help resolving this issue, please see https://go.microsoft.com/fwlink/?linkid=2125287","innererror":{"code":"ForbiddenByPolicy"}}}"
```

 This means that the registered application does not have the sign permission set on the Key Vault  

Go to the **Key Vault**, under **Settings** select **Access policies** and under the drop down for **Key Permissions**, check the **Sign** permission 

<br>If you see an error such as:

```
2022-11-24 10:31:40.391 [main] ERROR EzSignLog - Max retries 3 times exceeded. Error Details: AADSTS7000222: The provided client secret keys for app '7412f649-8e14-471f-bfc1-733b36a42705' are expired
```

This indicates that the credentials have expired. Renew by following the steps [here](refresh_azure_key_vault_credentials.html)
