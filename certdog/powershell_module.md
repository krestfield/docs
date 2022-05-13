---
layout: default
title: PowerShell Module
parent: Certdog
nav_order: 33
---

# PowerShell Module

This module allows management of the certdog application from the command line, or can be integrated with your own scripts 

<br>

### Running from the Command Line

Open a PowerShell window as Administrator  

Navigate to ``[certdog install]\bin`` e.g. ``c:\certdog\bin``

Import the module:

```powershell
Import-Module .\certdog-module.psm1
```

<br>

To view the available commands run:

```powershell
Get-Command -Module certdog-module
```

<br>

Login with:

```powershell
login -username [username] -password [password]
```

Or just type ``login`` to be prompted

<br>

### Examples

Show available Certificate Issuers:

```powershell
Get-Cas
```

or

```powershell
Get-Cas | Format-Table
```

<br>

Show available CSR Generators:

```powershell
Get-CsrGenerators
```

<br>

Request a certificate from a CSR (provided as a file):

```powershell
Request-CertP10 -caName "Microsoft TLS" -csrFilename C:\Downloads\server22.certdog.local.csr
```

Where caName is the issuer name as configured within Certdog. This is the name that will be displayed when the ``cas`` command is run (above)

<br>

Request a certificate from a CSR (provided as data within a variable):

```powershell
# Read the CSR data
$csrData = Get-Content C:\Downloads\server22.certdog.local.csr
# Send to Certdog
Request-CertP10 -caName "Microsoft TLS" -csr $csrData
```

<br>

Request a certificate with Certdog creating the CSR:

```powershell
$cert = Request-Cert -dn "CN=PowerShell Test,C=GB" -caName "Microsoft TLS" -csrGeneratorName "RSA 2048 Generator" -p12Password "password"
```

Then save as a PFX

```powershell
Set-Content -Path C:\Downloads\powershell.pfx -Value $cert.p12Data
```



