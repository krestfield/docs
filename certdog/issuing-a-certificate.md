---
layout: default
title: Issuing a Certificate
parent: Certdog
nav_order: 11
---

# Issuing a Certificate



### From the UI

From the menu, select **Request**  

If you have already generated a CSR, choose **CSR Request**  

If you want certdog to generate the request on your behalf and return a PKCS#12 (JKS or PEM) file, choose **DN Request**  



---

**CSR Request**  

<img src=".\images\csr_request.png" alt="image-20210319174811059" style="zoom:67%;" />

From the *Issuer to Process Request* drop down, select the issuer you want to issue this certificate  

Select the team that this certificate will be associated with  

Click **Paste CSR** if you have copied the data or choose **Upload CSR** if you want to upload a file CSR  

If you wish to add additional data to certificate, click **Click to add extra details**  

You may then enter text as Extra Information (e.g. "This certificate resides on server srv44772") or additional emails. Any emails entered will also be sent the certificate on issuance and renewal reminders (if configured). Multiple email addresses must be comma separated e.g. user1@org.com,user2@org.com 

Click **Request Certificate**





---

**DN Request**

<img src=".\images\dn_request.png" alt="image-20210319174905496" style="zoom:67%;" />

For the **Subject DN** enter the name required e.g. *CN=domain.com,O=organisation*  

For *Issuer to Process Request*, choose the required issuer  

Choose a *CSR Generator* from the drop down  

For *Team*, select the team you wish this certificate to be associated with  

If you wish to add additional data to certificate, click **Click to add extra details**  

You may then enter text as Extra Information (e.g. "This certificate resides on server srv44772") or additional emails. Any emails entered will also be sent the certificate on issuance and renewal reminders (if configured). Multiple email addresses must be comma separated e.g. user1@org.com,user2@org.com  

If you require any SANs (Subject Alternative Names) such as a DNS entry (as required for TLS certificates), click the drop down and add the required SANs:

<img src=".\images\sans.png" alt="image-20210121192822632" style="zoom:67%;" />

Enter a **password**. This password will protect the PKCS#12 (JKS or PEM) file. Then click **Request Certificate**

---

The certificate will be issued:

<img src=".\images\cert_issued.png" alt="image-20210121193025891" style="zoom:67%;" />

You may then download the certificate, chain or PKCS#12 file. Alternatively, click **More** to display further details:

<img src=".\images\download_options_ss.png" style="zoom:67%;" />

From here you can download other formats as well as the CSR if required  
Note: The PKCS#12, JKS and PEM options will only function whilst the key data is retained. This period is defined in the [settings](settings.html) as the *Private Key Retention Period*  

If this is set to 0 (zero), key data will not be retained, though you will still be able to download the PKCS#12 file immediately following issuance



### From PowerShell

Obtain the certdog powershell module from the krestfield website or github. If unable to locate this, contact [support](mailto:support@krestfield.com)  

If you are running on windows and have installed certdog locally, the module will be able to detect the API URL. If not, create a file called  

``apiurl.conf``

And populate with the location of the API URL e.g.  

``https://127.0.0.1/certdog/api``

Save the file  

  

Open a PowerShell window  

Import the module:

```powershell
Import-Module .\certdog-module.psm1
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
Attempting login at: https://127.0.0.1/certdog/api
Authenticated OK
```

**Request a certificate** 

```powershell
PS C:\temp> Request-Cert -dn "CN=mydomain.com,O=My Org" -caName "Certdog TLS Issuer" -csrGeneratorName "RSA 2048 CSR Generator" -subjectAltNames @('DNS:www.mydomain.com','DNS:www.mydomain2.com') -teamName "Test Team" -p12Password password | Format-List


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
token=$(curl --header "Content-Type: application/json" --request POST --data '{"username":"admin","password":"password"}' --insecure https://127.0.0.1/certdog/api/login | jq -r '.token')

# Request a PKCS12
p12Data=$(curl --data '{ "caName":"Certdog TLS Issuer", "dn":"CN=testcert.com", "csrGeneratorName":"RSA 2048 CSR Generator", "p12Password":"password", "teamName":"Test Team" }' --header "Content-Type: application/json" --header "Authorization: Bearer $token" --request POST --insecure https://127.0.0.1/certdog/api/certs/request | jq -r '.p12Data')

echo $p12Data
```











