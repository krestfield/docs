---
layout: default
title: Issuing a Certificate
parent: EzCert
nav_order: 11
---

# Issuing a Certificate



### From the UI

From the menu, select **Request**  

If you have already generated a CSR, choose **CSR Request**  

If you want EzCERT to generate the request on your behalf and return a PKCS#12 file, choose **DN Request**  

---

**CSR Request**  

<img src=".\images\csr_request.png" alt="image-20210121192327033" style="zoom:67%;" />

From the *Issuer to Process Request* drop down, select the issuer you want to issue this certificate  

Click **Paste CSR** if you have copied the data or choose **Upload CSR** if you want to upload a file CSR  

Click **Request Certificate**

---

**DN Request**

<img src=".\images\dn_request.png" alt="image-20210121192611044" style="zoom:67%;" />

For the **Subject DN** enter the name required e.g. *CN=domain.com,O=organisation*  

For *Issuer to Process Request*, choose the required issuer  

Choose a *CSR Generator* from the drop down  

If you require any SANs (Subject Alternative Names) such as a DNS entry (as required for TLS certificates), click the drop down and enter the required SANs:

<img src=".\images\sans.png" alt="image-20210121192822632" style="zoom:67%;" />

Enter a **password**. This password will protect the PKCS#12 file. Then click **Request Certificate**

---

The certificate will be issued:

<img src=".\images\cert_issued.png" alt="image-20210121193025891" style="zoom:67%;" />

Click **Download PKCS12** to download. Note: If you do not download the PKCS12 file now you will not be able to come back and download it later. The PKCS12 file is not stored as all keys that were generated as part of the CSR generation process are deleted immediately the certificate is issued  

You can then download the certificate or certificate chain (you will be able to do this at any time in the future) or click **More** for further certificate details



### From PowerShell

Obtain the EzCERT powershell module from the krestfield website or github  

If you are running on windows and have installed EzCERT locally, the module will be able to detect the API URL. If not, create a file called  

``apiurl.conf``

And populate with the location of the API URL e.g.  

``https://127.0.0.1/ezcert/api``

Save the file  

  

Open a PowerShell window  

Import the module:

```powershell
Import-Module .\EzCert-Module.psm1
```

If your API is not secured with a trusted TLS certificate, type:

```powershell
PS C:\temp> IgnoreSSLErrors
SSL Errors will now be ignored
```

**Login**

You can just type login and be prompted for your username and password (that will be hidden) or pass in one command:

```powershell
PS C:\temp> login -username admin -password password
Attempting login at: https://127.0.0.1/ezcert/api
Authenticated OK
```

**Request a certificate** 

```powershell
PS C:\temp> Request-Cert -dn "CN=mydomain.com,O=My Org" -caName "EzCert TLS Issuer" -csrGeneratorName "RSA 2048 CSR Generator" -subjectAltNames @('DNS:www.mydomain.com','DNS:www.mydomain2.com') -p12Password password | Format-List


certId  : 6009da2a2c7b373bdc95bcbe
p12Data : MIIN7wIBAzCC....
```



### Using a shell script and cURL

Obtaining JSON data within shell scripts is messy. This example uses **jq** to carry out the parsing. On Mac machines, this can simply be installed by running the following:

```bash
brew install jq
```

Below is an example using cURL to login and request a certificate:

```bash
# First Login and Obtain the auth token
token=$(curl --header "Content-Type: application/json" --request POST --data '{"username":"admin","password":"password"}' --insecure https://127.0.0.1/ezcert/api/login | jq -r '.token')

# Request a P123
p12Data=$(curl --data '{ "caName":"EzCert TLS Issuer", "dn":"CN=testcert.com", "csrGeneratorName":"RSA 2048 CSR Generator", "p12Password":"password" }' --header "Content-Type: application/json" --header "Authorization: Bearer $token" --request POST --insecure https://127.0.0.1/ezcert/api/certs/request | jq -r '.p12Data')

echo $p12Data
```











