---
layout: default
title: Master Password Reset
parent: Certdog
nav_order: 101
---
# Master Password Reset

<br>

The master password is the top level secret used to secure other encryption keys in the system

At install it is written to: ``./install/MasterSecret.txt`` and (on windows) secured under the current user's account, preventing access from other users

However, it should be securely backed up and removed from the server to prevent access

If the master password is not being picked up by the system, the server may fail to start and you will see errors such as:

```
Krestfield certdog failed to start. There was an error decrypting the data. Check the password is correct.

There was an error decrypting the keystore password. Check master password has been set correctly for this server
```

This may happen if you have migrated certdog to a new server, are running services under different accounts, or the local credential store has been wiped

<br>

If you have the master password recorded, go to Option 1 below

<br>

If the master password has been lost the ALL sensitive credentials will be unavailable and will need to be re-entered. This includes key store passphrases and credentials

If this is the case go to Option 2 below

<br>

## Option 1 - You have the Master Password

If you have the master password recorded. Then open a PowerShell window, navigate to: ``./certdog/bin`` and run:

```
./start-certdog-service.ps1
```

Enter the master password when prompted

 The service should start and, if the master password is correct, continue to operate as before

<br>

## Option 2 - The Master Password has been Lost

This option can be a dramatic failure, requiring several steps to rectify. This is by design, as without this top level secret, no-one should be able to access any sensitive information

Note that, certificates and any configuration data will not be lost

To recover from this, we need to perform the following steps:

1. Set a new Master Password
2. Remove Previous Encryption Keys - to force the creation of new ones
4. Reset all credentials and passphrases

<br>

### Step 1 - Set a new Master Password

Choose a new master password and ensure it is recorded safely and securely

Follow Option 1 above, entering the new master password

Note, at this stage the server will most likely still not start

<br>

### Step 2 - Remove Previous Encryption Keys

Open a Command Prompt (or shell) and navigate to:

```
./certdog/mongodb/bin
```

Run:

```
mongo.exe
```

(``./mongosh`` on linux and later certdog versions)

<br>

Enter the following commands:

```
use certmanuser
db.auth("certmanuser")
```

Type in the **certmanuser** password. This would have been entered (and should have been recorded) at install. However, it is also available in the ``application.properties`` file e.g.

```
spring.data.mongodb.uri=mongodb://certmanuser:T6Dy1fCK3D5K32HbOHZi@127.0.0.1/certman
```

In this case the password is:

```
T6Dy1fCK3D5K32HbOHZi
```

<br>

Enter the following command

```
db.settings.updateOne({version:"1.0"}, {$set:{encryptionKeyUnderMaster:""}})
db.settings.updateOne({version:"1.0"}, {$set:{jwtSecretUnderMaster:""}})
```

For each of these you should see an output such as:

```
{ "acknowledged" : true, "matchedCount" : 1, "modifiedCount" : 1 }
```

<br>

Now attempt to start the server. It should go through a process of creating new encryption keys and start. However, you will not be able to logon at this stage

<br>

### Step 3 - Reset all credentials and passphrases

Reset any Key Stores. If these are associated with a CA, then they CA must first be taken offline.  Then the password can be set. See [here](keystores.html) for details on keystores

Then [reset the passwords of any credentials](credentials.html)

You may also need to re-create any OCSP, ACME and SCEP services

If using the AD CS driver. Go to **Agents** in the UI and delete any agents. From a PowerShell window, navigate to``.\install`` and run ``.\configure-adcs-services.ps1`` then wait for the agent to re-register in the UI. When it appears, select and click **Approve**.
