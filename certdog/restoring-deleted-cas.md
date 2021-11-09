---
layout: default
title: Restoring Deleted CAs
parent: Certdog
nav_order: 110
---

# Restoring Deleted CAs

If a Certificate Issuer is inadvertently deleted, you can re-create by simply specifying the same options as before e.g. for a Microsoft CA you would just need to create a new issuer with the same CA config and template configuration  

However, if a Local CA is deleted - this will also delete the CA keys meaning that even if you re-created a Local CA with the same details as before, it would still result in a new (different) certificate generated using new keys  

To protect against this Certdog retains deleted Local CAs, Key Stores and Certificate Issuers for a specified amount of time  

This retention period is defined in the ``application.properties`` file which resides in the installation folder here: ``[Certdog installation]\config``  

In this file there is the following setting:

```shell
# Deleted items will be permanently removed after this many days
deleteditems.purge.afterdays=30
```

If you need to adjust this value, change the number of days and then restart the Certdog services

<br>

### Restoring Deleted Items

If a Local CA, Key Store or Certificate Issuer have been accidentally deleted, they can be restored using the REST API or PowerShell scripts

<br> 

**<u>REST API</u>**

For an example of calling the REST API [check here](rest_api_example.html)

To obtain a list of the deleted Local CAs, login to obtain a JWT token then call:

```http
GET [Base URL]/api/admin/localca/deleted
```

E.g.

```http
GET https://certdog1.com/api/admin/localca/deleted
```

This returns a list of all deleted items (that have not yet been purged).  Locate the item to be restored and note its ID

To restore that item, call:

```http
POST [BASE URL]/api/admin/localca/restore/{id}
```

Where ID is the ID of the item to be restored e.g.

```http
POST https://certdog1.com/api/admin/localca/restore/60f07d2f40eb186c96aed6b3
```

<br>

Perform similar operations to obtain and restore deleted Key Stores:

```http
GET [Base URL]/api/admin/keystores/deleted
POST [BASE URL]/api/admin/keystores/restore/{id}
```

And certificate issuers:

```http
GET [Base URL]/api/admin/ca/deleted
POST [BASE URL]/api/admin/ca/restore/{id}
```

<br>

**<u>PowerShell</u>**

Open a PowerShell window as Administrator, navigate to

``[Certdog Install\bin]``

Import the PowerShell Module:

```powershell
Import-Module .\certdog-module.ps1
```

Login

```powershell
login
```

You will be prompted for username and password. These must be the credentials of a certdog administrator

To obtain deleted Local CAs run:

```powershell
Get-DeletedLocalCAs
```

Locate the ID of the item to be restored and call:

```powershell
Restore-DeletedLocalCA -id [Item ID]
```

e.g.

```powershell
Restore-DeletedLocalCA -id 60f07d2f40eb186c96aed6b3
```

Similarly for Key Stores:

```powershell
Get-DeletedKeyStores
Restore-DeletedKeyStore -id 6182e2240e70e9747d622d86
```

 and Certificate Issuers:

```powershell
Get-DeletedCertIssuers
Restore-DeletedCertIssuer -id 6182e1020e70e9747d622d52
```

<br>

### To Force Delete

If you do not want to retain any material associated with a deleted Key Store or Local CA either set the property in ``application.properties`` to zero:

```shell
deleteditems.purge.afterdays=0
```

Note: If you then accidentally delete a Local CA - you will not be able to recover it

Or use the REST API to force delete the item. In this case use the regular delete calls but append ``/force`` to the end of the URL. For example, to force delete a Local CA call:

```http
DELETE [Base URL]/api/admin/localca/{local ca id}/force
```

e.g.

```http
DELETE https://certdog1.com/api/admin/localca/6182e0020e70e9747d622d1b/force
```

Similarly for Key Stores

```http
DELETE [Base URL]/api/admin/keystores/{key store id}/force
```

And Certificate Issuers

```http
DELETE [Base URL]/api/admin/ca/{cert issuer id}/force
```



