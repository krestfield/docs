---
layout: default
title: Active Directory Integration
parent: Certdog
nav_order: 10
---

# Active Directory Integration

<br>

Certdog supports authentication of active directory users and the processing of group membership (including nested groups)  

Active directory users do not need to be specifically added to Certdog. Their permissions are managed by their Active Directory group membership. To achieve this, the AD Groups must be configured against Teams in Certdog

<br>

### Initial Configuration

Before AD integration will operate you need to to configure the following information in Certdog:

* The Domain Controller URL
  * This is the URL to the domain controller e.g. ``ldap://dc1.org.com``, ``ldap://10.144.17.277``, ``ldaps://dc2.orgname.com``
  * If using ldaps read the Using Ldaps section below

* The Search Base
  * The level in the directory at which the users and groups that you want to reference are stored
  * For example: ``OU=USERS,OU=PKI,DC=certdog,DC=local``
  * See the Locating the Search Base section below if you are unsure of what to put here


* A Credential
  * This should be an AD account that has read-only permissions and should not have any other rights
  * Ideally it should be a service account

<br>

Other Info

* Results Limit
  * This is the maximum number of results that will be returned from a query made to Active Directory e.g. when searching for groups 
  *  If queries are slow, consider reducing this value

* Time Limit
  * The maximum time (in milliseconds) to wait for a query or search to return
  * If your connection is very slow and you experience timeouts, consider increasing this value

<br>

To configure from the left hand menu, click **Settings** then **Active Directory Settings**

<img src=".\images\ad_settings.png" alt="Active Directory Settings" style="zoom:80%;" />

Enter the required values and click **Update**

<br>

### Granting Permissions

In Certdog, permissions to specific Certificate Issuers are granted via Teams. A Team is configured to allow access to issuers and users are made members of this Team  

To allow access for AD users, simply map the AD groups to the Certdog Teams  

The processing then completes as follows:

1. User authenticates with their AD account
2. Map the users AD Group Memberships to the Certdog Teams that have been configured with those Groups
3. The user obtains the permissions and restrictions as imposed by those Teams

Note that when an AD user authenticates their account will then appear in the Users list in Certdog. This will show what Certdog Teams the user is a member of (based on their AD group membership). None of the details for AD accounts can be managed via Certdog - they continue to be managed via Active Directory only  

<br>

### Configuring the Active Directory Credential

Follow the guide for creating a Username/Password [credential](credentials.html) specifying the account name as the Service Principal e.g. ``aduser@certdog.local``  

This account should only have read permissions and ideally be configured as a Service Account that is denied local logon and whose password does not expire

<br>

### Locating the Search Base

This can be the top level of your domain or reference a subsection (OU) of it

For example, if your organisation domain is someorg.com then the search base may be something like: ``DC=someorg,DC=com``  

If your directory is large there will most likely be multiple OUs and divisions which you may wish to restrict the search space to. This will result in faster queries  

You may get an idea of the search base that user accounts are in by running a PowerShell command such as: ``Get-ADUser <username>`` on your own (or another known) account e.g.

```
PS C:\Windows\system32> Get-ADUser certdoguser


DistinguishedName : CN=certdoguser,OU=USERS,OU=PKI,DC=certdog,DC=local
Enabled           : True
GivenName         :
Name              : certdoguser
ObjectClass       : user
ObjectGUID        : 466c8754-4583-44a6-b765-44224b416aa2
SamAccountName    : certdog
SID               : S-1-5-21-3549443890-123274070-2723549285-500
Surname           :
UserPrincipalName : certdoguser@certdog.local
```

In this example we can see that user accounts are stored here: ``OU=USERS,OU=PKI,DC=certdog,DC=local``

Searching for the location of a specific group can be obtained by running: ``Get-AdGroup <Group Name>`` e.g.

```
PS C:\Windows\system32> Get-AdGroup PKI_CERT_ISSUERS


DistinguishedName : CN=PKI_CERT_ISSUERS,OU=GROUPS,OU=PKI,DC=certdog,DC=local
GroupCategory     : Security
GroupScope        : Global
Name              : PKI_CERT_ISSUERS
ObjectClass       : group
ObjectGUID        : ea8a989d-f2a6-43d0-a030-ef8385b3dd65
SamAccountName    : PKI_CERT_ISSUERS
SID               : S-1-5-21-3549443890-123274070-2723549285-1106
```

Groups are contained within ``OU=GROUPS,OU=PKI,DC=certdog,DC=local``  

If the users and groups we are interested in for Certdog are all located here, we could set our search base to ``OU=PKI,DC=certdog,DC=local``    

If we wanted to encompass all OUs within the directory we could just set the search base to ``DC=certdog,DC=local``

<br>

### Using Ldaps

When using LDAPS (LDAP over SSL) the certificate issued to the Domain Controller must be trusted by Certdog. As Domain Controller certificates are usually issued by internal Microsoft CAs the root certificates will not be automatically trusted by Certdog  

If you simply configure the URL to use LDAPS rather than LDAP authentication with AD accounts will fail and you will be unable to search for AD groups when configuring teams  

Checking the logs you will see an error such as the following

```
There was an error communicating with the domain controller - unable to obtain groups from Active Directory. Search string was 'PKI'. Error was: simple bind failed: dc1.certdog.local:636; nested exception is javax.naming.CommunicationException: simple bind failed: dc1.certdog.local:636 [Root exception is javax.net.ssl.SSLHandshakeException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target]
```

They key part being ``unable to find valid certification path to requested target`` which essentially means Certdog could not find the root certificate from which the LDAPS certificate was issued from  

To enable this trust, obtain the root certificate of the CA that issued the LDAPS certificate. This will normally be your organisations Microsoft CA's root certificate. Save this certificate here:

```
[Certdog Install]\config\sslcerts\root.cer
```

  

Open a command prompt and navigate to ``[Certdog Install]\config\sslcerts`` then run the following

```
C:\certdog\config\sslcerts>..\..\java\jdk-17.0.2\bin\keytool -import -alias "Krestfield Root" -file root.cer -keystore dbssltrust.jks
```

Replace "Krestfield Root" with an alias for your root certificate (e.g. the certificate's common name)

At the following prompt

```
Enter keystore password:
```

Enter the password for the JKS file. If you have not changed this it will be held within the README.txt in the same folder e.g. ``C:\certdog\config\sslcert\README.txt``



The certificate details will be displayed. Ensure they are correct and when prompted ``Trust this certificate? [no]:`` type ``yes`` and press Enter

```
wner: CN=Certdog Root CA AZ, O=Krestfield, C=GB
Issuer: CN=Certdog Root CA AZ, O=Krestfield, C=GB
Serial number: 5b3065a7ff5ea8f22333cadab50f2a18
Valid from: Thu Mar 24 15:45:46 GMT 2022 until: Sun Mar 21 15:45:46 GMT 2032
Certificate fingerprints:
         SHA1: D2:8A:29:9F:C6:B7:A4:C8:BE:1A:1F:53:EA:9E:12:06:1B:36:65:43
         SHA256: F6:D4:AE:33:BD:F2:82:1B:85:56:13:4C:B3:60:42:C9:BC:74:3D:2A:92:44:99:25:55:C3:44:86:1B:E0:23:7D
Signature algorithm name: SHA256withRSA
Subject Public Key Algorithm: 4096-bit RSA key
Version: 3
...
...
Trust this certificate? [no]:  yes
Certificate was added to keystore
```



Restart the Certdog service and you should now be able to access the domain controller using LDAPS

