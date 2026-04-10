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



Alternatively, provide an API key:

```
Set-ApiToken -token [API Token]
```

See [here](https://krestfield.github.io/docs/certdog/users.html#api-tokens) for details on obtaining an API token

<br>

### Examples

<u>Show available Certificate Issuers</u>

```powershell
Get-Cas
```

or

```powershell
Get-Cas | Format-Table
```

<br>

<u>Show available CSR Generators</u>

```powershell
Get-CsrGenerators
```

<br>

<u>Request a certificate from a CSR (provided as a file)</u>

```powershell
Request-CertP10 -caName "Microsoft TLS" -csrFilename C:\Downloads\server22.certdog.local.csr
```

Where caName is the issuer name as configured within Certdog. This is the name that will be displayed when the ``cas`` command is run (above)

<br>

<u>Request a certificate from a CSR (provided as data within a variable)</u>

```powershell
# Read the CSR data
$csrData = Get-Content C:\Downloads\server22.certdog.local.csr
# Send to Certdog
Request-CertP10 -caName "Microsoft TLS" -csr $csrData
```

<br>

<u>Request a certificate with Certdog creating the CSR</u>

```powershell
$cert = Request-Cert -dn "CN=PowerShell Test,C=GB" -caName "Microsoft TLS" -csrGeneratorName "RSA 2048 Generator" -p12Password "password"
```

Then save as a PFX

```powershell
Set-Content -Path C:\Downloads\powershell.pfx -Value $cert.p12Data
```

<br>

<u>Search for certificates</u>

Search based on expiry dates:

```powershell
$certs = search -validToFrom "2026-05-02T11:00" -validToTo "2026-05-02T13:00"
```
Search based on issued dates:

```powershell
$certs = search -validFromFrom "2026-05-02T11:00" -validFromTo "2026-05-10T13:00"
```

Search for all certificates that have "test" including in their DN:

```powershell
$certs = search -subjectDn "test"
```

Search for all certificates issued by CN=Certdog Test Issuing CA, O=Krestfield

```
$certs = search -issuerDn "CN=Certdog Test Issuing CA, O=Krestfield"
```

Find all active certificates:

```powershell
$certs = search -status "active"
```

Find all active certificates, issued in the last 30 days:

```powershell
$now = Get-Date
$nowStr = $now.ToString("yyyy-MM-ddTHH:mm")
$30daysAgoStr = $now.AddDays(-30).ToString("yyyy-MM-ddTHH:mm")
$certs = search -validFromFrom $30daysAgoStr -validFromTo $nowStr -status "active"
```



