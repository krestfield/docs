---
layout: default
title: Issuing Sub CA from Microsoft CA
parent: Certdog
nav_order: 111
---

# Issuing a Sub CA Certificate from a Microsoft CA

<br>

Certdog allows the generation of a CSR for a Sub CA which can then be signed by an existing CA  

The following outlines the instructions for issuing a Sub CA from either an [Enterprise](#enterprise-ca) or [Stand-Alone](#stand-alone-offline-root) Microsoft CA

<br>

## Stand Alone Offline Root

The following instructions will result in a CA certificate being issued using a default Microsoft template. The certificate will contain the *Basic Constraints* extension (as is required for a CA) but the *Key Usage* extension will not be marked as critical. If this is required, follow the steps in the [next section](#set-the-key-usage-as-critical)

<br>

Copy the CSR that was generated from Certdog to the offline root machine and save it to a file e.g. ``c:\temp\certdog.csr``  

Open a command prompt as Administrator and run the following:  

```powershell
cd c:\temp
C:\temp>certreq -attrib "CertificateTemplate:SubCA" certdog.csr
```

This command submits the CSR to the CA and tells the CA to use the default *SubCA* template which will add the required Basic Constraints and Key Usage extensions for a CA  

Note: If your policy module settings require you to manually issue the certificate, the request will be sitting in the *Pending Requests* folder of the CA. In this case, right click this pending request and select **All Tasks > Issue**  

From the *Issued Certificates* folder, locate the issued certificate and download e.g. to ``c:\temp\certdog.cer``  

Also download the Root CA's certificate as this is also required for import into Certdog  

<br>

### Set the Key Usage as Critical

To issue the CA certificate with Key Usage marked as critical, perform the following:

<br>

We need the CA to set the request as pending 

From the Microsoft CA snapin, right click the CA, then select **Properties**  

From the *Properties* windows, select the **Policy Module** tab

<img src=".\images\msca_policy.png" alt="image-20211001080648311" style="zoom:80%;" />

Select the **Set the certificate request status to pending. The administrator must explicitly issue the certificate** option and click **OK** and **OK** again on the *Properties* window

<br>

Next we need to tell the CA to use the key usage that is provided in the request, rather than add its default extension (which results in the Key Usage being non-critical)

<br>

On the CA machine, open a command prompt as Administrator and run the following commands:  

   ```powershell
   certutil -setreg policy\editflags -EDITF_ADDOLDKEYUSAGE
   net stop certsvc
   net start certsvc
   ```

<br>

Then submit the request to the CA, specifying the default *SubCA* template:

   ```powershell
   cd c:\temp
   C:\temp>certreq -attrib "CertificateTemplate:SubCA" certdog.csr
   RequestId: 12
   RequestId: "12"
   Certificate request is pending: Taken Under Submission (0)
   ```

Note the **RequestId** (which in the example above is 12) as we now need to update this request. We are going to add the Key Usage extension and mark it as critical

<br> Create a new text file called ``c:\temp\keyusage.txt`` and populate with the following:  

``03 02 01 86``

This value is the ASN.1 encoded key usage - encoded as hexadecimal. The important part here is the last byte 86 (which is 134 decimal). Key usage is encoded as a bit string, and if you set the bits for digitalSignature, KeyCertSign and cRLSign you get ``10000110`` which is 86 hexadecimal

<br>

Save the file and run the following from the prompt:  

   ```powershell
   c:\temp>certutil -setextension 12 2.5.29.15 1 @keyusage.txt
   ```

Where 

   ``12`` Is the RequestId obtained from above  
   ``2.5.29.15`` is the OID of the key usage extension  
   `1` indicates that this extension is to be marked as critical - this is the important part  
   ``@keyusage.txt`` contains the content of the extension  

<br>

From the CA, in the *Pending Requests* folder right click this request and select **All Tasks > Issue**  

From the *Issued Certificates* folder, locate the issued certificate and download e.g. to ``c:\temp\certdog.cer``  

Also download the Root CA's certificate as this is also required for import into Certdog  

<br>

## Enterprise CA 

From an Enterprise CA you can manipulate templates as required. Normally, the *Subordinate Certification Authority* template is used (often duplicated to your own requirements)

To discover what templates are available on the CA, run the following:

```powershell
certutil -catemplates -config "Machine\CAName"
```

(Where the value for ``-config`` is obtained from the ``Config`` as displayed when you run ``certutil``)



e.g.

```powershell
C:\Windows\system32>certutil -catemplates -config "CA1.certdog.local\Certdog"
CertdogSubCertAuthority: Certdog Sub Cert Authority -- Auto-Enroll: Access is denied.
CertdogComputer: Certdog Computer -- Auto-Enroll: Access is denied.
CertDog90DayTLS: CertDog 90 Day TLS -- Auto-Enroll: Access is denied.
CertUtil: -CATemplates command completed successfully.
```

Identify the Sub CA template which in this case is **CertdogSubCertAuthority** and the run the same commands as for the offline CA above e.g.

```powershell
c:\temp\certreq -attrib "CertificateTemplate:CertdogSubCertAuthority" .\certdog.csr
```

The certificate may be taken under submission (if your policy module is configured that way), so must be issued via the CA console. Otherwise, you will be prompted to save the issued certificate  

Obtain both this issued certificate as well as the issuing CA certificate as both are required for import into Certdog

