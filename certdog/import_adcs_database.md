---
layout: default
title: Import ADCS Database
parent: Certdog
nav_order: 58
---

# Import the ADCS Database into Certdog

The certificates stored within an ADCS instances (Microsoft CA) database can be imported into Certdog  

You may wish to do this for reasons such as:

* To benefit from a simplified search and query of the certificates

* To use Certdogs certificate expiry monitoring and alerting capability

* As a backup of certificates stored 

* As part of a migration of ADCS to Certdog (where you are also importing the ADCS keys into Certdog)

<br>

### Quick Overview

Export the certificates from the Microsoft CA to a file by running the following script from a command prompt:

```powershell
certutil -view -restrict "GeneralFlags>0" -out "CertificateTemplate,Disposition,Request.RevokedEffectiveWhen,Request.RevokedReason,Request.RawRequest,RawCertificate" > certs.txt
```

Import this file into Certdog by running the following PowerShell script on the Certdog instance:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -template "Certdog TLS" -fromRowNum 0 -username certdog -password password
```

To obtain the IDs for ``ownerId``, ``teamId`` and ``certIssuerId``, run:

```powershell
PS C:\> Import-Module .\certdog-module.psm1
PS C:\> login
```


Then run commands such as ``users`` (to obtain the ``ownerId``), ``teams``(to obtain the ``teamId``) and ``cas`` (to obtain the ``certIssuerId``)

<br>

<br>

For a more in-depth explanation keep reading...

<br>

### Step 1 - Prepare for the import

<u>ADCS Account</u>

In order to export certificates from the Microsoft CA (ADCS) you will need to have an account that has the permissions on the Microsoft CA to perform this operation. Often this can be carried out using a local Administrator account but your system may have restrictions in place to prevent this  

<u>Certdog Users/Teams</u>

We then need to decide how to organise the certificates that will be imported. Certificates in Certdog can be organised by Teams and assigned to specific users. You can manage this so that certificates issued from a specific ADCS template are associated with a specific team and associated with a user  

It may be beneficial to allocate all imported certificates to a new Team or even allocate them to a specific user. Whether creating new or using existing the target user and team must be created before the import can take place

You can read how to manage teams [here](teams.md)

You can read how to manage users [here](users.md)

The import into Certdog itself will require an Certdog administrator account



**NOTE:** If the import is part of an ADCS migration, in that you are also importing the CA keys and you wish to be able to revoke these certificates and ensure that those already revoked will appear in any generated CRLs. Then, you must have first performed the following:

* Imported the CA keys into Certdog following the guide here

* Created an Issuer from this CA

This will then create the link from the certificates to the issuer

<br>

### Step 2 - Export from the Microsoft CA

Logon to the machine hosting the ADCS instance (Microsoft CA). This operation is the same whether this is a root or intermediate, Enterprise or Standalone CA  

Open a command prompt as an Administrator  

We are going to export the certificates to a text file (in the example below this is called ``certs.txt``). Navigate to a location where you want to save this file and run the following command:

```powershell
certutil -view -restrict "GeneralFlags>0" -out "CertificateTemplate,Disposition,Request.RevokedEffectiveWhen,Request.RevokedReason,Request.RawRequest,RawCertificate" > certs.txt
```

Extract the ``certs.txt`` file (or whatever you decided to call it) as this must then be transferred to the Certdog instance

Note, for instances that contain a large number of certificates, this may take a while to complete. It could impact the performance of the CA so if this will be an issue, run the impact will be minimal

<br>

### Step 3 - Import into Certdog

On the machine where Certdog is installed, open a PowerShell window as Administrator  

Navigate to the ``[certdog installation]\bin\utils`` directory e.g. ``c:\certdog\bin\utils``

Copy the exported certificates file (``certs.txt`` in the example above) to this directory  

<br>

We will be using the ``import-adcs-certs.ps1`` script to import the certificates contained in the ``certs.txt`` file into Certdog. This script has the following parameters:

* -certsFilename [Filename] 
  * This is ``certs.txt`` in the example above
* -template [Template Name]
  * This is the Microsoft CA template name. If you specify this parameter e.g. ``-template "Web Server"`` then only certificates that were issued from this template on the Microsoft CA will be imported
  * If this parameter is not provided - all certificates will be imported
* -ownerId [User ID]
  * This is the ID of the user who will own the certificates that will be imported. By using the template parameter above, you can arrange different certificate types to be owned by different users. For example, you can assigning all certificates issued from template A to user A, and those issued from template B to user B etc.
  * To view available owners (users), import the ``certdog-module.psm1`` and run the ``users`` command
  * This parameter is required
* -teamId [Team ID]
  * This is the ID of the team the imported certificates will be associated with. As for ownerID you may wish to arrange things such that certain templates belong to certain teams. E.g. you may create a dedicated team called ``Imported`` for these imported certificates 
  * To view available teams, import the ``certdog-module.psm1`` and run the ``teams`` command
  * This parameter is required
* -certIssuerId [Cert Issuer ID]
  * If you are performing a full migration from a Microsoft CA to Certdog and have imported the Microsoft CA's keys and created a Certificate Issuer, you can associate the imported certificates with that issuer. This will mean that you may revoke these certificates and any existing revoked certificates will be included in generated CRLs 
  * To view available issuers, import the ``certdog-module.psm1`` and run the ``cas`` command
* -fromRowNum [Rown Number]
  * To only process from a specific row number in the certs file, provide a value with this parameter e.g. ``-fromLastRow 200``
* -fromLastRow
  * Once the script has been run once, it stores the last row number processed in a file called ``lastrow.txt``. If this switch is provided on subsequent runs, processing will start from the last row number as stored in this file
* -saveCreds
  * Run the script with only this switch to store the certdog credentials (username and password). This stores them securely for the user running the command
  * You can then use ``-useSavedCreds`` to use these saved credentials
  * This can be used when automating the script e.g. when running the script from a scheduled task. Meaning that the username and password do not need to be provided as parameters
* -useSavedCreds
  * If credentials have been saved using the ``-saveCreds`` switch, providing this switch instructs the script to use those saved credentials
* -username [Username]
  * The username of a Certdog account that has admin privileges in Certdog
* -password [Password]
  * The password of the Certdog account
* -WhatIf
  * Specifying this switch parses the cert import file but does not import into Certdog. This can be used to verify the file is correct and how many entries it contains

<br>

**Examples**

Import all certificates contained in the certs.txt file. Associating them with the owner, team and cert issuer whose IDs are specified:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password
```

  

As above but start processing from row 200

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -fromLastNum 200
```

  

If the script had been run previously then a new ``certs.txt`` file was generated containing additional certificates. We can just import the new entries by providing the ``-fromLastRow`` switch:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -fromLastRow
```



Only import certs that have been issued by the Web Server template:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -template "Web Server"
```

  

Save credentials

```powershell
.\import-adcs-certs.ps1 -saveCreds
```

  

Run the script with these saved credentials:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -issuerId 1631fe2ef6b6c54c34c56530 -useSavedCreds
```

<br>

<br>

**Running the Script**

Run the script with the required parameters. You will see output such as the following

```powershell
Read 2112 entries from the file OK
Starting from row number 0

Logging in...
Attempting login at: https://127.0.0.1/api
Authenticated OK
Pushing certificates to certdog starting from row 0...

Imported 2104 certificates OK
8 certificates in the file were skipped as they were marked as 'denied' by the CA
```

In the example above, 8 certificates were skipped. This is because the ``certs.txt`` file contains all entries - whether successfully issued or not. In some cases, even though a request has been sent to the Microsoft CA, the CA may deny the request. These *denied* requests are what is being referred to here  

If any errors are seen, such as the following:

```powershell
Imported 1220 certificates OK
4 certificates in the file were skipped as they were marked as 'denied' by the CA
204 certificates failed to import. See errorlog.txt for details
```

Check the ``errorlog.txt`` file, where all error details are held. E.g. in this case there were several entries such as:

```powershell
@{timestamp=2021-10-31T11:20:20.325+00:00; status=409; error=Conflict; message=Failed to import certificate. 409 CONFLICT "The certificate is already present in the system. Details: id: 617e76765a68a535d91d7142, owner: admin, team id: 617aae4d91b6ab12b829237f"; path=/api/certs/import}
-----BEGIN CERTIFICATE-----
MIIGGzCCBAOgAwIB
...
PBEc8JdAbTIsmw==
-----END CERTIFICATE-----
```

The failure is since the certificate has already been imported. You can avoid re-importing certificates by using the ``-fromRowNum`` parameter or the ``fromLastRow`` switch



If incorrect user, team or certIssuerIds are provided, you will see errors such as the following:

```powershell
@{timestamp=2021-10-31T14:56:00.245+00:00; status=422; error=Unprocessable Entity; message=Failed to import certificate. 422 UNPROCESSABLE_ENTITY "The provided certIssuerId (617a6c684eaeb271fa97d596) does not exist. Either pass in a valid issuer ID or you may re-create the issuer referencing the correct local CA that issued this certificate"; path=/api/certs/import}

```



### Step 4 - Verifying

Log into Certdog and verify the certificates have been imported OK. If you created a dedicated team for these certificates you will be able to search for all certificates issued from that team  

If a error has been made or you need to roll back for any reason, all imported certificates can be removed from the database using a simple script, such as:

```powershell
Import-Module .\certdog-module.psm1

try 
{   
	# This will prompt for the certdog username and password
    login
    
    $certs = Get-Certs
    $numCerts = 0
    foreach ($cert in $certs)
    {
		# Only looking at certificates that have been imported
		if ($null -ne $cert.imported -And $cert.imported -eq $true)
        {
			# Delete if the import time contains the date
			# 31st October 2021 and the time was 3pm
			if ($cert.importTime -Match "2021-10-31T15")
            {            
                Remove-Cert -id $cert.id *> $null
                $numCerts = $numCerts + 1
            }
        }
    }

    logout

    Write-Host "Removed $numCerts certs"
}
catch {
   
    Write-Host $_
}
```



