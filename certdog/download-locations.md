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

[Windows](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v1100.zip)

[RedHat](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/redhat/certdogfree1100.tar.gz)

[Debian](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/debian/certdog.tar.gz)

<br>

### Full Version

Contact [support](mailto:support@krestfield.com) for your download location

<br>

### Windows File Hashes

Full Version:  

* SHA1: ``9da252cf4022751c4f46296d9ded63a49f8a3992``

* SHA256: ``80ee13d233788a3e064bfce36ee442f471ccd99a34b62ac20822f223b3752e5c``

Free Version:  

* SHA1: ``9c3c7c1ad6e7e49c67444675f2d42d98d65f15af``

* SHA256: ``96810972063ce7aee8bf769fde5c2b0f453b434fc63dc1ea97140e9f001ff704``

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

