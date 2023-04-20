---
layout: default
title: Download Locations
parent: Certdog
nav_order: 500
---



# Download Locations

<br>

### Free Version  

Download the version for your OS:

[Windows](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v190.zip)

[RedHat](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/redhat/certdog.tar.gz)

[Debian](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/debian/certdog.tar.gz)

<br>

### Full Version

Contact [support](mailto:support@krestfield.com) for your download location

<br>

### Windows File Hashes

Full Version:  

* SHA1: ``03829a660ec0d5797e4397b4672c20833eabc633``

* SHA256: ``4f2078685d083aacb18c80f32c3b37441764c0d52e317f0a6ae1b044c58fc674``

Free Version:  

* SHA1: ``09a7e149f01c04a6aef0d78d4c7123b87f18813f``

* SHA256: ``9d19cb9b21d443d20c5e22453985e41603aa3f8a21c5f354399c70ce2974de6a``

<br>

For instructions on how to validate the file hashes over the download files, see [here](https://krestfield.github.io/docs/pki/check_file_hash.html)

<br>

### Unblock

Once the file has been downloaded, right click the file and choose **Properties**. Tick the **Unblock** option at the bottom of the dialog (if present) and click **OK**

<img src=".\images\unblock_zip.png" alt="unblock" style="zoom:80%;" />



### Download via PowerShell

Open a PowerShell window as Administrator and type the following:

```powershell
cd \

$webClient = New-Object System.Net.WebClient

$webClient.DownloadFile('https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v180.zip', 'c:\certdog.zip')
```

Once download is complete, run the following to unzip:

```powershell
Expand-Archive .\certdog.zip -DestinationPath .
```

This will expand to:

```powershell
c:\certdog
```

or for the free version:

```powershell
c:\certdogfree
```

