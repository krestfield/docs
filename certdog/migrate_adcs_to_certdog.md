---
layout: default
title: Migrate ADCS to Certdog
parent: Certdog
nav_order: 56
---
# Migrate an ADCS instance to Certdog

> Applies to Certdog Version 1.5+

An existing ADCS instance (Microsoft CA) can be migrated to Certdog. This can include the existing CA keys and all issued certificates  

You may choose to do this for reasons such as:  

* To replace your Microsoft CA in order to make the issuance and management of your certificates simpler

* To host multiple CAs on the same instance of Certdog without having to maintain individual servers for each CA

* You wish to decommission an existing Microsoft CA but want to maintain a fall back as well as the ability to keep producing CRLs  

* As a backup for an existing Microsoft CA  

<br>

Migration can be achieved by following a few simple steps:

1. Migrate the CA key and certificate to Certdog
2. Import the issued certificates from the Microsoft CA database
3. Configure Certdog to operate in the same way as the Microsoft CA (CRL generation periods etc.)

<br>

### Step 1: Import the CA Certificate and CA Keys

If the CA to be imported is not a Root CA then the Root CA Certificate (and any other issuing CA Certificates) must be imported first, as follows:  

In Certdog, select **Certificates** from the menu 

Click the **Import Certificate** button and import the Root Certificate and any other Issuing CA certificates of the CA to be imported 

<br>

Next we need to import the CA keys and certificate

<u>Software Keys</u>

[Export the CA keys as a PFX and import into Certdog following the guide here](migrate_ca_software_keys_to_certdog.html)  

If your keys are not marked as exportable, [see the guide here](https://krestfield.github.io/docs/pki/exporting_a_nonexportable_certificate.html) or contact support for options 

<u>HSM Stored Keys</u>

If your keys are stored on an EnTrust nCipher HSM, we first need to re-target the keys (from the Microsoft format - CSP/CNG to the certdog format - PKCS11) [as described here](retarget_adcs_ncipher_keys.html)

Configure a PKCS#11 key store to reference the HSM. [Follow the steps here](keystores.html) to create the key store

<br>

Obtain the CA certificate (from the section above) as a PEM formatted file (e.g. ``ca.cer``) as we will need this for the next steps

Open a PowerShell window as Administrator, navigate to your ``[certdog install]\bin`` folder  

Import the certdog powershell module, as follows:

```powershell
PS C:\certdog\bin> Import-Module .\certdog-module.psm1
```

Login with an admin account:

```powershell
PS C:\certdog\bin> login
Username: certdogadmin
Password: *************
Attempting login at: https://cd1.krestfield.io/certdog/api
Authenticated OK
PS C:\certdog\bin>
```

List the available key stores

```powershell
PS C:\certdog\bin> Get-KeyStores | Format-Table -Property id, name, keyStoreType

id                       name                             keyStoreType
--                       ----                             ------------
613216278e7ff6189decc909 Software 1                       SOFTWARE
616f205944736e513d32fb34 PKCS11                           PKCS11
```

And note the id of the one you created above. i.e. the key store that references the same HSM as the Microsoft CA (e.g. ``616f205944736e513d32fb34``)

<br>

Now we will import the CAs keys into certdog. We need to provide a name for this new CA, the CA certificate (ca.cer) and the key store id we obtained from the step above. E.g.

```powershell
PS C:\certdog\bin> Import-LocalCAKeyFromKeyStore -name "Krestfield CA1" -caCertFilename ca.cer -keyStoreId 616f20d044736e513d32fb38
```

The created CA details will then be displayed

If you see an error such as:

```
There was an error importing the private key for certificate Krestfield CA1. No key found that matches certificate. Tried 2 private keys
```

This indicates that either 

* The Key Store configured is not the same Key Store/HSM on which the CA keys reside
* The CA Key has not been migrated. [Follow the guide here](retarget_adcs_ncipher_keys) to do this
* The Key does not reside on this HSM or Security World. If you are performing this on a new server to which you have copied the Security World, check all files in the ``Key Management Data\local`` folder are present (have been copied from the old server)

<br>

### Step 2: Import the CA database

We need to extract the certificates from the Microsoft database and then imported into Certdog. This ensures that all previously issued certificates and their status (whether revoked or active) will be available in Certdog  

[Follow the instructions here](import-adcs-database.html) on how to export and import the CA database

<br>

### Step 3: Complete the Configuration

The following information needs to be configured in your newly imported CA:

* AIA OCSP Locations

* AIA Issuer Cert Locations

* CRL Distribution Points

* The CRL lifetime and generation period

To obtain this information, from your Microsoft CA snapin, right click the CA name and select Properties  

Select the Extensions tab

For the **CRL Distribution Point (CDP)** extension, note the http and file locations of all entries where the

>  **Include in the CDP extension of issued certificates**

option is ticked  



For the **Authority Information Access (AIA)** extension note all entries where the following options are ticked

> **Include in the AIA extension of issued certificates**

> **Include in the online certificate status protocol (OCSP) extension**



From Certdog, locate your imported Local CA by navigating to **Local CAs > CA Configuration** from the menu, then clicking your CA and click **View/Edit**  

For each of the *Include in the online certificate status protocol (OCSP) extension* items add an entry for **AIA OCSP Locations**. Remember to comma separate each entry e.g. ``http://server1.com/ocsp,http://server2.com/ocsp``  

For each of the *Include in the AIA extension of issued certificates* items add an entry for **AIA Issuer Cert Locations**. Remember to comma separate each entry  

If you have any entries for *Include in the CDP extension of issued certificates* then check the **Generate CRLs** option.  For each of the *Include in the CDP extension of issued certificates* items add an entry for **CRL Distribution Points**, Again, remembering to separate each entry with a comma (if there are multiple)  

For the CRL Filename, ensure that the filename matches that from the CDP extension  

<br>

From your Microsoft CA, click the **Revoked Certificates** folder and note the **CRL Publication Interval**. Set this to be the **CRL Lifetime** in Certdog  

Set the **CRL Generation Period** to be a value less than this period. This could be 10% less or more to ensure there is adequate overlap of when a new CRL will be available before the old CRL expires

<br>

Once all configuration is complete. Click **Update** to apply the settings