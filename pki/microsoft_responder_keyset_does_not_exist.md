---
layout: default
title: Microsoft Responder - Bad Signing Certificate
parent: General PKI
nav_order: 30
---

# Microsoft Online Responder - NTE_BAD_KEYSET



If you have configured your Responder to manually select a signing certificate (rather than having the responder enrol by itself) and you have imported a certificate into the Machine certificate store. Everything looks good but your responder is still complaining with:

**Bad signing certificate on Array controller**



And taking a look in the event logs you are seeing:

```
Level: Error
Event ID: 23
Source: OnlineResponder
The Online Responder Service could not locate a signing certificate for configuration CA16 New OCSP.(Keyset does not exist 0x80090016 (-2146893802 NTE_BAD_KEYSET))
```

This could be a permissions issue



The Online Responder Service runs under the local **NETWORK SERVICE** account. It is this account that requires permissions on the key



### Set the Permissions

1. Open a Windows Explorer
2. Navigate to:

``%ALLUSERSPROFILE%\Microsoft\Crypto\RSA\MachineKeys``

3. Select the key file from the list. Now, this may be easier said than done, as the filenames will be like this:

```
6687f9977771f049a15a9a5de0e17d82_8a8fdb36-f1a7-4fa3-bb7a-16297814b7a4
952203f4bd8a56ad04d5ba9ec9aab9c4_8a8fdb36-f1a7-4fa3-bb7a-16297814b7a4
...
```

You can sort by *Date modified* if you have an idea when you imported the key, or even re-import so you can spot the latest

4. Right click the file and select **Properties**

5. Select the **Security** tab (select *Continue* when asked, click *Advanced* if permissions are not shown)

6. Add the **NETWORK SERVICE** account (make sure you select the local machine as the *From this location* option - rather than your domain) and give it Read &execute permissions

7. Click **OK** to commit the change

8. Restart the **Online Responder** service

