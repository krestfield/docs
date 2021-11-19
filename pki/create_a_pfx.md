---
layout: default
title: Create a PFX
parent: General PKI
nav_order: 22
---

# Create a PFX

Whilst Certdog allows for certificates to be provisioned as PFX files (as well as JKS and PEM). There are occasions when you need to generate a PFX file using standard Microsoft tooling  

In this example, we will generate a CSR (marking it as exportable)

<br>

### Create the INF File

Create a .inf file as follows:

```ini
[Version]
Signature="$Windows NT$"
 
[NewRequest]
Subject="CN=server1.comp.org, O=Comp Ltd, C=GB"
Exportable=true
MachineKeySet=true
SMIME=false
RequestType=PKCS10
ProviderName="Microsoft RSA SChannel Cryptographic Provider"
ProviderType=12
HashAlgorithm=sha256
KeyLength=2048
KeyUsage="CERT_KEY_ENCIPHERMENT_KEY_USAGE | CERT_DATA_ENCIPHERMENT_KEY_USAGE"

[RequestAttributes]
CertificateTemplate=WebServer

[Extensions]
2.5.29.17 = "{text}"
_continue_ = "DNS=server1.comp.org&"
_continue_ = "DNS=server2.comp.org&"
_continue_ = "DNS=server3.comp.org&"
```

The key items to edit here are:

* Subject

  * Enter your required DN

* Exportable=true

  * This marks the key that will be generated as part of the request, as exportable. Meaning we can export it as a PFX later

* MachineKeySet=true

  * The keys will be stored in the Local Machine store. Certificates that are used by web servers or services will require the keys to be stored here

* HashAlgorithm

  * The hash algorithm e.g. sha256, sha512 etc.

* KeyLength

  * The key length in bits

* KeyUsage (Optional)

  * The key usages ORd together. Available values are:
    * CERT_DIGITAL_SIGNATURE_KEY_USAGE 
    * CERT_NON_REPUDIATION_KEY_USAGE 
    * CERT_DATA_ENCIPHERMENT_KEY_USAGE 
    * CERT_KEY_AGREEMENT_KEY_USAGE 
    * CERT_KEY_CERT_SIGN_KEY_USAGE 
    * CERT_OFFLINE_CRL_SIGN_KEY_USAGE 
    * CERT_CRL_SIGN_KEY_USAGE 
    * CERT_ENCIPHER_ONLY_KEY_USAGE 
    * CERT_DECIPHER_ONLY_KEY_USAGE 

* Extensions (Optional)

  * Here you can specify extensions. In the example above we specify the ``2.5.29.17`` extension which refers to Subject Alternative Names
  * Specify the required SANS. Available options for SANs are:
    * DNS
    * EMail
    * UPN
    * DirectoryName
    * URL
    * IPAddress
    * RegisteredId

* CertificateTemplate (Optional)

  * If submitting to a Microsoft CA you may also specify the template name here

  * Note the name is the template *name* (doesn't include spaces) rather than the template *display name* (which allows spaces)

  * You can specify the template when submitting to the CA later as well

    

Update as required and save the .inf file

<br>

### Generate the CSR

Open a command prompt as Admin, navigate to where you saved the .inf file (e.g. request.inf) and type

```powershell
certreq -new request.inf cert.csr
```

The request will be generated and saved to ``cert.csr``

<br>

### Submit the CSR for Processing

Follow normal processes to obtain a certificate from your CSR. If you have privileges to issue from a Microsoft CA, you may simply be able to run the following command:

```powershell
certreq cert.csr
```

If you didn't specify a template in the .inf file you can do so as follows:

```powershell
certreq -attrib "CertificateTemplate:SubCA" cert.csr
```

You will be prompted to choose the CA to send the request to

The certificate will be issued. Download this to the same location as the .inf file. E.g. ``.\cert.cer``

<br>

### Import the Certificate

We now import the issued certificate into the Windows store. If all is correct this will match up with the keys we generated when the CSR was created  

Run the following

```powershell
certreq -accept cert.cer
```

You may see output such as:

```powershell
Installed Certificate:
  Serial Number: 450eaefcca0e939a7dff86039c8f5e4e
  Subject: CN=server1.comp.org, O=Comp Ltd, C=GB
  NotBefore: 16/11/2021 16:09
  NotAfter: 16/11/2022 16:09
  Thumbprint: d11475aed31aa89f17d5720d311e0a3afaa68853
```

But in some cases no output is observed. As long as no errors are received, things should be OK

<br>

### Export as a PFX

You can now either open up mmc.exe, locate the issued certificate in the machine store and export

Or you can use PowerShell:  

First get the certificate we imported. You can use the s

```powershell
$certificate = Get-ChildItem -Path Cert:\LocalMachine\My\ | Where-Object {$_.Subject -match "server1.comp.org"}
```

Which should work OK if that's the only certificate you have with that name  

Otherwise, we can also specify the Thumbprint - this was displayed when we accepted the certificate above:  

```powershell
$certificate = Get-ChildItem -Path Cert:\LocalMachine\My\ | Where-Object {$_.Thumbprint -match "d11475aed31aa89f17d5720d311e0a3afaa68853"}
```

Then, we set the password we will export under:

```powershell
$password="strongpassword" | ConvertTo-SecureString -AsPlainText -Force
```

And export it to a file:

```powershell
Export-PfxCertificate -Cert $certificate -FilePath cert.pfx -Password $password
```

<br>

More info on certreq can be found [here](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/certreq_1) for more info

<br>

### Using Certdog

Of course. This can all be performed with Certdog in a few clicks or a couple of REST API or PowerShell calls

E.g. The equivalent PowerShell to obtain the same from Certdog is:

```powershell
login -username user -password $pass
$resp = Request-Cert -dn "CN=server1.comp.org, O=Comp Ltd, C=GB" -caName "Certdog TLS Issuer" -csrGeneratorName "RSA2048" -subjectAltNames @('DNS:server1.comp.org','DNS:server2.comp.org','DNS:server3.comp.org') -teamName "My Team" -p12Password 'strongpassword'
Set-Content -Path cert.pfx -Value $resp.p12Data
```

...and that is all you need to do...

See [here](https://krestfield.github.io/docs/certdog/issuing-a-certificate.html) for issuing certs via the UI

<br>
