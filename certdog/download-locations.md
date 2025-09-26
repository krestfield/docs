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

[Windows](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v1150_win.zip)

[RedHat](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/redhat/certdogfree_v1140.tar.gz)

[Debian](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/debian/certdogfreev1100.tar.gz)

<br>

### Full Version

Contact [support](mailto:support@krestfield.com) for your download location

<br>

### Windows File Hashes

V1.15.0 Full Version:  

* SHA1: ``eb4573f3796d6ab6443cb69b2aded2e68cb4d250``

* SHA256: ``477c2cf5322420ca09d604d3361532bdbf5de4ab30eb22124770b5232b677ab2``

V1.15.0 Free Version:  

* SHA1: ``a028048517155ba1510a7b18f473cfde7ac5f955``

* SHA256: ``68ed1c90fd6837a33b6786f6b8734a9ef1a1cfd6a3302ce88b373b30e72ee66c``

<br>

### RedHat File Hashes

V1.14.0 Free Version:  

* SHA1: ``7f06118d991cbca94df9afb3f3dfd39ede5f0885``

* SHA256: ``17d7a2690b02a58aded2b2f562804616807fcc6f1dec9b353b56bd92b4635b60``

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

