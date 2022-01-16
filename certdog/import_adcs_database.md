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

Note, for instances that contain a large number of certificates, this may take a while to complete. It could impact the performance of the CA so if this will be an issue, run when the impact will be minimal

<br>

You may export the database in chunks if preferred. This can be achieved by altering this section of the command:

```powershell
-restrict "GeneralFlags>0"
```

For example, if you wanted to export in chunks of 1000 certificates, you could update this property as follows:

```powershell
-restrict "GeneralFlags>0,RequestId<1000"
```

This would export certificates whose RequestId is less than a 1000 - which should result in the first 1000 certificates being exported (though it may be less as not every assigned RequestId may be successful)  

For the next run, you would set the property as:

```powershell
-restrict "GeneralFlags>0,RequestId>=1000,RequestId<2000"
```

Which would export the next 1000. Then

```powershell
-restrict "GeneralFlags>0,RequestId>=2000,RequestId<3000"
```

Would export the next 1000. And so on. This operation could be scripted

<br>

You may also export based on validFrom dates. For example, if you only wanted to export certificates issued from a certain date (e.g. yesterday) you would set this property as:

```powershell
-restrict "GeneralFlags>0,notBefore>=10/01/2022 00:00"
```

A command such as this could be run every day, incrementing the date. Each export could then be imported into Certdog

Just note, that the date format must match what your CA is configured for. E.g. this may be UK (day/month/year) or US (month/day/year) etc.

<br>

### Step 3 - Import into Certdog

<u>Deciphering the time format</u>

First we need to determine the time format of the output file (e.g. ``certs.txt``). As the CA may have been using a US 12 hour time format, UK 24 hour format or some other format  

The time format only applies to revoked certificates. If there are no revoked certificates you may set the date and time formats to any setting  

To decipher the format used, open the ``certs.txt`` file and search for ``Revoked``. This should take you to the ``Revoked`` string within a row entry such as the following:

```
Row 56:
  Certificate Template: "1.3.6.1.4.1.311.21.8.5713573.4140818.2442627.4655406.2487952.157.15198871.15916228" Test Web Server
  Request Disposition: 0x15 (21) -- Revoked
  Effective Revocation Date: 7/30/2019 11:29 AM
  Revocation Reason: 0x0 -- Reason: Unspecified
```

If the *Revoked* text is not found then there are no revoked certificates. You may set the ``dateFormat`` and ``timeFormat`` as follows:

```
-dateFormat US -timeFormat 24
```

In the case where revoked certificates exist, examine the row containing the timestamp:

```
  Effective Revocation Date: 7/30/2019 11:29 AM
```

You now need to determine whether this is US (month/day/year), UK (day/month/year) or an ISO (year/month/day) based format. Also, whether the time is 12 or 24 hour  

In the example above the date/time value is:

```
7/30/2019 11:29 AM
```

Which is US format

As the time ends with AM it is a 12  hour format. If there is no AM or PM the time is in 24 hour format

If it is not clear what the format is e.g. you have a data such as ``1/2/2022`` check other entries in the file for a hint. Otherwise, it is quite likely the CA will follow your local format (e.g. if you are US based, it will likely be using a US format)

<br>

<u>Run the Script</u>

On the machine where Certdog is installed, open a PowerShell window as Administrator  

Navigate to the ``[certdog installation]\bin\utils`` directory e.g. ``c:\certdog\bin\utils``

Copy the exported certificates file (``certs.txt`` in the example above) to this directory  

<br>

We will be using the ``import-adcs-certs.ps1`` script to import the certificates contained in the ``certs.txt`` file into Certdog. This script has the following parameters:

* -certsFilename [Filename] 
  * This is ``certs.txt`` in the example above

* -template [Template Name]

  * This is the Microsoft CA template name (not the OID). If you specify this parameter e.g. ``-template "Web Server"`` then only certificates that were issued from this template on the Microsoft CA will be imported

  * These entries will appear in your exported certs file as something like:

    ``Certificate Template: "1.3.6.1.4.1.311.21.8.5713573.4140818.2442627.4655406.2487952.157.15198871.15916228" Test Web Server``

  * You only ned to specify the name ``Test Web Server`` and not the OID value

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

* -fromRowNum [Row Number]

  * To only process from a specific row number in the certs file, provide a value with this parameter e.g. ``-fromLastRow 200``

* -toRowNum [Row Number]

  * Only process up until this row number. For large files, you may want to process certificates in batches. Stops processing at this point but can be restarted to carry on from this position by using the ``-fromLastRow`` switch (below)

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

* -dateFormat [US  or UK or ISO]

  * You deciphered this from the section above. If US format enter ``US``, for UK format enter ``UK`` and for ISO format enter ``ISO`` e.g. ``-dateFormat US``
  * If you do not specify this you will be prompted to by the script

* -timeFormat [12 or 24]

  * You also deciphered this from the section above. Enter ``12`` or ``24`` e.g. ``-timeFormat 24`` 
  * If you do not specify this you will be prompted to by the script

* -WhatIf

  * Specifying this switch parses the cert import file but does not import into Certdog. This can be used to verify the file is correct and how many entries it contains

<br>

**Examples**

Import all certificates contained in the ``certs.txt`` file. Associating them with the owner, team and cert issuer whose IDs are specified:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -dateFormat UK -timeFormat 24
```

  

As above but start processing from row 200

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -fromLastNum 200 -dateFormat UK -timeFormat 24
```

  

If the script had been run previously then a new ``certs.txt`` file was generated containing additional certificates. We can just import the new entries by providing the ``-fromLastRow`` switch:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -fromLastRow -dateFormat UK -timeFormat 24
```



Only import certs that have been issued by the Web Server template:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -username certdogadmin -password password -template "Web Server" -dateFormat UK -timeFormat 24
```

  

Save credentials

```powershell
.\import-adcs-certs.ps1 -saveCreds
```

  

Run the script with these saved credentials:

```powershell
.\import-adcs-certs.ps1 -certsFilename certs.txt -ownerId 6131fe2fb6b0c54c13c59935 -teamId 617aae4d91b6ab12b829237f -certIssuerId 617a6c684eaeb271fa97d556 -issuerId 1631fe2ef6b6c54c34c56530 -useSavedCreds -dateFormat UK -timeFormat 24
```

<br>

<br>

**Script Execution**

Note: The script can take a long time to run if a large number of certificates are being imported 

When the script is run you will see output such as the following

```powershell
Import ADCS Certificates
------------------------

Using timestamp format M/d/yyyy h:m tt for revocation time

Parsing certificates from file...

Read 46458 entries from the file OK

Importing certificates into certdog...

Starting from row number 0

Logging in...
Attempting login at: https://127.0.0.1/certdog/api
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

<br>

## Example Uses

### Managing Large Files

If you have a large file, you may wish to import in sections. This can be achieved by importing by template (importing one template at a time), or by using the ``-fromRowNum``, ``-toRowNum`` and ``-fromLastRow`` options

<br>

<u>Importing Per Template</u>

To import certificates from one particular template, use the ``-template`` option. In this case the name to specify must be the name as it appears in the certs file  

For example, in the file you may see entries such as the following:

```
Certificate Template: "1.3.6.1.4.1.311.21.8.5713573.4140818.2442627.4655406.2487952.157.15198871.15916228" Web Server
```

The template name to specify in this case is ``Web Server``

I.e. you would run a command with the following option:

```
-template "Web Server"
```

Also consider, associating templates with Teams for easier searching and separation. E.g. you could associate the *Web Server* template certificates with the *Networks* team  

<br>

<u>Importing in Stages</u>

Importing tens of thousands of certificates may take some time 

To split up the processing you may wish to import in chunks (e.g. a thousand certificates at a time)  

You can achieve this by using the ``-fromLastRow`` and ``-toRowNum`` options  

For example, to import in chunks of 1000 you would first run the command with the following options:

```
... -fromLastRow -toRowNum 1000
```

Which would import up until row 1000  

Then run with the following option:

```
... -fromLastRow -toRowNum 2000
```

As the last row would be 1000, this would import the next 1000 certificates. And so on

<br>

### Automating Import

You may automate the import process. For example, if you are continuing to use your Microsoft CA and wish to have a regular import of certificates in to Certdog  

In this case, the easiest option would be to create a scheduled task which runs the export command (see above), followed by the running of the ``import-adcs-certs.ps1`` script  

Use the options to export from the CA based on ``validFrom`` to export certificates issued in the last day

There is no need to worry about overlapping/duplicating certificates as Certdog will not import any certificate that is already in the system
