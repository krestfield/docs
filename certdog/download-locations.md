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

V1.17.0 Full Version:  

* SHA1: ``6bcbb01bab4151823b4b0be6941fe06e32ad407b``
* SHA256: ``566a0766278b4f189b7bbf0fd53bfea8d7a18184bd8f834db1eda0ae597f78fb``

<br>

### Linux (RedHat and Debian) File Hashes

V1.17.0 Full Version:  

* SHA1: ``1beae7825a9010fbec09b1b68d08b192a3aac1ee``
* SHA256: ``7ea9059af294dfb9a2cfdb95e64009a4a7ed55d3e84fa2f8dba5325959e7e8e4``

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

