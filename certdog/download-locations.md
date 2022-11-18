---
layout: default
title: Download Locations
parent: Certdog
nav_order: 500
---



# Download Locations

<br>

### Free Version

The free version is available to download from [here](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v180.zip)

<br>

### Full Version

Contact [support](mailto:support@krestfield.com) for your download location

<br>

### File Hashes

Full Version:  

* SHA1: ``fe634549728b0c3199ec438ee0e25b49ac8d1dd7``

* SHA256: ``4fed32c50aecbe64da969f90cf6c333e58c2bfdf7ce1a0bb1f086b62e23fef28``

Free Version:  

* SHA1: ``269eebcdd7a72b892e493d1cc3d4da79345a798b``

* SHA256: ``bb1e801e7211853c211cfc67f3b5867ba4c83e402b15a63201900eec3f683902``

<br>

For instructions on how to validate the file hashes over the download files, see [here](https://krestfield.github.io/docs/pki/check_file_hash.html)

<br>

### Unblock

Once the file has been downloaded, right click the file and choose **Properties**. Tick the **Unblock** option at the bottom of the dialog (if present) and click **OK**

<img src="C:\Users\darre\Documents\_mystuff\development\_krestfield products\docs\certdog\images\unblock_zip.png" alt="unblock" style="zoom:80%;" />



### Download via PowerShell

Open a PowerShell window as Administrator and type the following:

```powershell
cd \

$webClient = New-Object System.Net.WebClient

$webClient.DownloadFile('https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v180.zip', 'c:\certdog.zip')
```

Once download is complete, run the following to unzip:

```powershell
Expand-Archive .\certdog.zip
```

This will expand to:

```powershell
c:\certdog
```

or for the free version:

```powershell
c:\certdogfree
```

