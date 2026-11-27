---
layout: default
title: OCSP
parent: Certdog
nav_order: 212
---
# OCSP

> From version: 1.8.0

<br>

Certdog can provide OCSP services for local CAs and external CAs (e.g. Microsoft AD CS)  

When using OCSP services for local CAs, certdog can setup all of the components required to enable automatic issuance of an OCSP signing certificate, and retrieval of the certificate status. Users just need to select the **Create OCSP Server** option when creating (or editing) a Local CA  

When using OCSP services for external CAs, users must create the OCSP configuration manually 

The OCSP signing certificate can be obtained automatically from a CA that certdog connects to, or, from version 1.18.0, issued by an external CA that certdog is not connected to (see [Signing Certificate from an External CA](#signing-certificate-from-an-external-ca)). This allows certdog to provide OCSP services for CAs it does not control

<br>

### Configuration for an Internal CA  

From the Local CA (**Local CAs, CA Configuration** menu), simply check the **Create OCSP Server** option:

<img src=".\images\enable_ocsp.png" alt="image-20230217154109764"  />

Once **Add** (or **Update**) is clicked for the Local CA, the following will then be automatically generated:

* An OCSP Server. You can view configured servers from the *OCSP Servers* menu item
* A Certificate Profile. This profile will be configured to issue OCSP signing certificates
* A Certificate Issuer. This will combine the profile above with the local CA - so that the CA is able to issue OCSP signing certificates
* A User and a Team. The user will be a member of the team and the team will only have permissions to request certificates from the Certificate Issuer mentioned above. The user account will be used by the OCSP server to authenticate to certdog and request a signing certificate. The team is given the built-in *OCSP Service* role, which only permits requesting and renewing certificates. See [Service Roles](roles.html#service-roles)

With the above items in place an OCSP server will automatically obtain a signing certificate from the CA. This certificate will also be auto-renewed  

Certificate status will be obtained from the internal database meaning this information will be up to date  

You may edit the OCSP settings my clicking on the **OCSP Servers** menu then selecting the OCSP server (see [OCSP Server Settings](#ocsp-server-settings) for the specific settings)

<br>

### Configuration for an External CA 

For external CAs (e.g. a Microsoft AD CS instance) an OCSP server must be manually created. to do this from the OCSP Servers menu, click **Add New OCSP Server** then complete following the [OCSP Server Settings](#ocsp-server-settings) section below  

The OCSP signing certificate can be obtained in one of two ways:

* **Managed CA (certdog issuer)** - if the CA is configured in certdog as a Certificate Issuer, the OCSP server obtains its signing certificate through certdog and renews it automatically
* **External CA (Generate a CSR)** - if certdog is not connected to the CA, certdog generates a CSR, you have the certificate issued by the CA, and then import it. See [Signing Certificate from an External CA](#signing-certificate-from-an-external-ca)

<br>

### OCSP Server Settings

The following settings are available for each OCSP Server

<br>

<img src=".\images\ocsp1.png" alt="image-20230223092728625" style="zoom:80%;" />

* Server Name
  * This is simply the OCSP Server name. It can be changed without affecting any functionality
* Enabled
  * If not enabled the OCSP server will not process any OCSP requests. Unauthorized will be returned

<br>

<u>Status Source Location</u>

This is where the information about the certificate status (good or revoked) will be obtained. Options are to retrieve from the internal database (for local CAs) or from CRL files

This can be set to one of the following

<br>

**Local CA (database)**

<img src=".\images\ocsp2.png" alt="image-20230223092822285" style="zoom:80%;" />

The status will be obtained from the internal database of a local CA. This will provide the most up to date certificate status information

If you select this option then the Local CA option will be available

Note: This option is not available when the signing certificate is obtained from an External CA (see [Signing Certificate from an External CA](#signing-certificate-from-an-external-ca)). A Local CA issues the signing certificate automatically

* Local CA

  Select the local CA from the drop down list

<br>

**Local CRL File**

<img src=".\images\ocsp3.png" alt="image-20230223093526520" style="zoom:80%;" />

Obtain status from a local CRL file

If you choose this option you must then set the following options

* CRL Filename

  The full path to the CRL file. The file that must be located on the server hosting certdog (not your local machine)

* Refresh Every

  The period at which to re-read the file to get up to date information. Note, the OCSP server will also automatically re-read the CRL when it expires
* CA Certificate

  The certificate of the CA that this OCSP server is providing information for

  Click Browse.. to navigate to this certificate. This file can be uploaded from your local machine and does not need to reside on the certdog server

<br>

**CRL URL**

Obtain status from a CRL hosted at an http address

If you choose this option you must then set the following options

* CRL URL

  The http location of the CRL e.g. http://server.certdog.local/crl/issuingca.crl of the CRL

* Refresh Every

  The period at which to re-read the file to get up to date information. Note, the OCSP server will also automatically re-read the CRL when it expires

* CA Certificate

  The certificate of the CA that this OCSP server is providing information for

  Click Browse.. to navigate to this certificate. This file can be uploaded from your local machine and does not need to reside on the certdog server

<br>

<u>Signing Certificate Details</u>

This section contains details about the OCSP signing certificate, including where to obtain it from, what to name it and when to renew

<img src=".\images\ocsp_signing_cert_from.png" alt="Signing Certificate From" style="zoom:80%;" />

* Signing Certificate From
  * **Managed CA (certdog issuer)** - the certificate is obtained from a certdog Certificate Issuer and renewed automatically. The settings below are used
  * **External CA (Generate a CSR)** - the certificate is issued by a CA that certdog is not connected to. The URL, Certdog Username, Certdog Password, Certificate Issuer and Renew at settings are not used. See [Signing Certificate from an External CA](#signing-certificate-from-an-external-ca)

The following settings apply when the signing certificate is from a **Managed CA**

<img src=".\images\ocsp4.png" alt="image-20230223094343934" style="zoom:80%;" />

* URL
  * This is the Certdog API URL that the OCSP server will use to request certificates. It will be of the form ``https://[certdog server]/certdog/api`` 
  * See [Operational Notes](#operational-notes) below for details as to why this is required
  * Note: If running on a Linux machine or other where you are mapping external ports to internal ones, ensure you correct the URL. For example, if your local services are listening on port 1433 (routed from external port 443), the internal address should be https://127.0.0.1:1433/certdog/api rather than https://127.0.0.1/certdog/api
* Certdog Username

  * This is the username of the account that has permissions to request the OCSP signing certificate. If the OCSP was created automatically, this user account would have been generated for you. If you wish to configure this yourself, use an account that has permissions on the Certificate Issuer which will provide the correct OCSP Signing certificates
* Certdog Password

  * This is the password associated with the account name mentioned above
* Certificate Issuer

  * This is the Certificate Issuer. If the OCSP was created automatically, this issuer would have been generated for you. If you wish to create this yourself, the issuer must be associated with the same CA that this responder is serving and be configured with an OCSP compliant Certificate Profile (See [OCSP Certificate Profile](#ocsp-certificate-profile) below)
* Bypass Issuer Check
  * If setting manually for an external CA (not a Local CA hosted by certdog), select this option
  * By default the Certificate Issuer must be associated with the same CA as the Local CA i.e. you obtain an OCSP signing certificate from the CA whose status is being provided by the OCSP server. In some cases you may want to issue an OCSP signing certificate from another CA or the root CA. If this option is checked it will then allow these configurations
* Signing Cert DN

  * If you wish for the OCSP Signing certificate to have a specific DN, you may set it here. If this is left empty a default DN will be created of the form: ``CN=OCSPServer-[CA Name]-[ID]``
* Renew at
  * This is the percentage of life remaining on the OCSP Signing certificate at which it will be renewed. For example, if you set this to 50. When the current signing cert has 50% of its lifetime remaining, it will be renewed. 
* Current Signing Certificate

  * This provides a link to the current OCSP signing certificate in use. If no certificate has been issued (e.g. when initially setting up) this will show *<u>No certificate available yet</u>*
* Renew Certificate
  * This option is only visible once a certificate has been issued
  * If this option is checked, the current OCSP signing certificate will be renewed at the next expiry check (which by default is every minute) whether it is currently expiring or not. Check this option if you have made changes to the certificate details such as Certificate Issuer or Signing Cert DN and wish to force a renewal 

<br>

<u>Key Store and Signing Algorithm Details</u>

<img src=".\images\ocsp6.png" alt="image-20230223094839265" style="zoom:80%;" />

* Key Store
  * This is the Key Store where the responder will store its own signing keys. By default the same Key Store as used by the CA is selected, but another can be configured
* Algorithm
  * The algorithm that will be used to sign OCSP responses (this also dictates what algorithm the signing certificate will use)
* Key Size
  * The key size of the signing certificate if RSA is selected as the Algorithm
* Curve
  * The ECC curve. If ECDSA is selected as the Algorithm

* Hash Algorithm
  * This is the hash algorithm that will be used when signing OCSP responses and not the algorithm that will be included in the signing certificate (as this is dictated by the issuing CA). Some systems require a specific hashing algorithm to be configured

<br>

<u>Other Settings</u>



<img src=".\images\ocsp7.png" alt="Other Settings" style="zoom:80%;" />

* Respect Number Once
  * If this is checked, if a Number Once value is provided in the OCSP request, that same value will be returned in the response. This option is often employed by clients to ensure that the OCSP response is freshly generated

* Requests must be signed
  * If this option is checked then OCSP requests must be signed and will be rejected (with an Unauthorized response) otherwise

* Return for Not Issued
  * If an OCSP request is received for this CA but the serial number of the certificate has not been issued from this CA, here you can specify what to return in this instance. 
  * If the OCSP responder is being used to provide responses for an external CA (such as Microsoft), it is unable to verify all issued serial numbers, so this option should be set to *Good*
  * For internal CAs, this should be set to either *Revoked* or *Unknown*, depending on how your clients will cope with those responses e.g. if your clients will continue even if the response is *Unknown*, you may need to set the response to *Revoke* to force the client to reject the response
  * Note that CAB Forum, compliance 2013-08-01 section 3.2.2.6 states *OCSP Responders SHALL NOT respond "Good" for Unissued Certificates*. Therefore, if you need to adhere to this requirement, ensure that *Good* is not set

* Next Update Period
  * This is the time that will be added to the *Produced At* period of the OCSP response, and is essentially the validity of the response

* Time Skew
  * If there are any clock deviations between clients and the OCSP Server, you may set this value to allow a time skew (in seconds). E.g. if you set this value to 5 then the produced at date of the OCSP response will be NOW minus 5 seconds and the response's expiry date (Next Update) will be EXPIRY TIME plus 5 seconds

<br>

### Signing Certificate from an External CA

> From version: 1.18.0

<br>

If certdog is not connected to the CA that the OCSP server provides status for, the OCSP signing certificate can be issued by that CA from a CSR that certdog generates. The certificate is then imported into certdog and the OCSP server signs responses with it

Note the following:

* The status must come from the CA's CRL (**Local CRL File** or **CRL URL**). **Local CA (database)** is not available, as a Local CA issues its OCSP signing certificate automatically. If **External CA** is selected while the status source is Local CA (database), the status source is changed to CRL URL
* The certificate is not renewed automatically. Before it expires, generate a new CSR and import the new certificate (see [Renewing the Certificate](#renewing-the-certificate) below). The certdog log records a warning when the certificate is nearing expiry
* The key is generated in the Key Store selected in the [Key Store and Signing Algorithm Details](#ocsp-server-settings) section, using the Algorithm, Key Size or Curve set there. Set these before generating the CSR

<br>

<u>Generating the CSR</u>

1. Add a new OCSP server (or edit an existing one) and set the **Status Source Location** to **Local CRL File** or **CRL URL**, and upload the **CA Certificate**

   <img src=".\images\ocsp_external_status.png" alt="Status source for an External CA" style="zoom:80%;" />

2. Set **Signing Certificate From** to **External CA (Generate a CSR)**

3. Enter the **CSR Subject DN**. This is the subject that will be requested for the signing certificate e.g. ``CN=Partner OCSP Signer,O=Example Partner,C=GB``. If it is left empty, ``CN=[Server Name]`` is used

   <img src=".\images\ocsp_external_details.png" alt="External CA signing certificate details" style="zoom:80%;" />

4. Click **Generate CSR**. The OCSP server settings are saved (for a new server, the server is added), a key is generated in the Key Store and the CSR is displayed

   <img src=".\images\ocsp_external_csr.png" alt="Generated CSR" style="zoom:80%;" />

5. Click **Copy** to copy the CSR to the clipboard, or **Download** to save it as a ``.csr`` file, and submit it to the external CA

The certificate issued by the CA should:

* Include the **OCSP Signing** Enhanced Key Usage, and the **digital signature** Key Usage. Clients may reject responses signed by a certificate without these
* Ideally be issued by the CA that the OCSP server provides status for (the CA Certificate above). This is known as a *delegated responder* certificate and clients can verify it with the CA certificate they already hold
* Optionally include the **OCSP No Check** extension (see [OCSP Certificate Profile](#ocsp-certificate-profile))

The CSR remains on the OCSP server's page until a certificate is accepted, so you can return to it later. If you change the Key Store or algorithm settings while waiting for the certificate, the CSR is discarded and a new one must be generated

<br>

<u>Accepting the Certificate</u>

1. Edit the OCSP server and click **Upload Certificate**. Select the certificate issued by the CA. This may be:
   * The certificate on its own, or
   * A PKCS#7 (``.p7b``) containing the certificate and its chain

   PEM (base64) and DER (binary) encodings are both accepted

2. The certificate is checked and its details shown. It must be for the key generated with the CSR, and must not have expired

3. If the certificate was not issued by the CA Certificate of the OCSP server (for example, it was issued by the root CA) and its issuer was not included in the uploaded file, the issuer certificate is required. An **Upload Issuer** option is displayed - upload the issuer's certificate, or a PKCS#7 containing the chain

   <img src=".\images\ocsp_external_issuer_required.png" alt="Issuer certificate required" style="zoom:80%;" />

   The issuer certificate is not requested if the certificate was issued by the CA Certificate

4. Once the certificate (and issuer, if required) have been checked, click **Accept Certificate**

   <img src=".\images\ocsp_external_accept.png" alt="Certificate ready to accept" style="zoom:80%;" />

   Any warnings are displayed above the button, for example if the certificate does not have the OCSP Signing Enhanced Key Usage, or was not issued by the CA that the OCSP server provides status for. These do not prevent the certificate being accepted, but clients may reject the responses

The certificate is imported into certdog (and is available from the **Current Signing Certificate** link) and the OCSP server begins signing responses with it once it reloads its configuration. If an issuer certificate was required, it is included in OCSP responses so that clients can verify the signing certificate

<br>

<u>Renewing the Certificate</u>

Certificates from an external CA are not renewed automatically. To replace the certificate, edit the OCSP server and click **Generate New CSR**, then follow the steps above. The current certificate continues to be used until the new certificate is accepted

<br>

<u>Changing the Signing Certificate Source</u>

* Changing from **Managed CA** to **External CA**: the current signing certificate continues to be used until a certificate from the external CA is accepted
* Changing from **External CA** to **Managed CA**: the certdog URL, username, password and Certificate Issuer must be provided. A new certificate is obtained from the Certificate Issuer at the next check. The imported certificate is used until then

<br>

### Operational Notes

Although they run on the same server by default, OCSP Servers run independently of certdog. This is to allow for the OCSP Server to run on a separate machine to the certdog instances. E.g. you may wish to run your OCSP servers in a more accessible environment and load-balance

It is for this reason that the certdog URL, Username and Password need to be set above - as the certdog instance providing the certificates may not always be on the same machine. These are not required when the signing certificate is from an External CA, as the OCSP server does not request it

<br>

### OCSP End Point (AIA)

By default the OCSP server will be located at the following URL

```
http://[server name]/certdog/ocsp
```

For example, if your certdog server is at https://certdog.krestfield.com then your OCSP end point would be

```
http://certdog.krestfield.com/certdog/ocsp
```

Note: The URL is not SSL protected (http rather than https). This is intentional as SSL protected OCSP end points are not often utilised (and not supported by many systems)  

If you do require an SSL protected end point, contact [krestfield support](mailto:support@krestfield.com)

You may have additional DNS settings that reference the certdog server e.g.

```
CNAME: status.pki.com -> certdog.krestfield.com
```

Which would mean your OCSP services could be contacted at:

```
http://status.pki.com/certdog/ocsp
```

Whatever location/URL you choose, this value must be added as the AIA OCSP Location for certificates issued from the CA. This value will be populated for you when you select the *Create OCSP Server* option for a Local CA, but if using an external CA this value must be set there

<br>

### OCSP Certificate Profile

If you wish to create your own Certificate Profile for an OCSP server you must configure the following:

* Key Usage
  * This must include the **digital signature** key usage
* Enhanced Key Usage
  * This must include the **OCSP Signing** option

Optionally, you may set Include **OCSP No Check**. This indicates to the client that the OCSP signing certificate itself should not be OCSP checked. If this is not set, then the client may then carry out an additional OCSP check on the OCSP signing certificate itself
