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

[Windows](https://krestfield.s3.dualstack.eu-west-2.amazonaws.com/certdog/certdog-free-win-v1.17.0.zip)

[RedHat](https://krestfield.s3.dualstack.eu-west-2.amazonaws.com/certdog/debian/certdog-free-linux-v1.17.tar.gz)

[Debian](https://krestfield.s3.dualstack.eu-west-2.amazonaws.com/certdog/debian/certdog-free-linux-v1.17.tar.gz)

<br>

### Full Version

Contact [support](mailto:support@krestfield.com) for your download location

<br>

### Windows File Hashes

V1.17.0 Full Version:  

* SHA1: ``6bcbb01bab4151823b4b0be6941fe06e32ad407b``
* SHA256: ``566a0766278b4f189b7bbf0fd53bfea8d7a18184bd8f834db1eda0ae597f78fb``

V1.17.0 Free Version:

* SHA1: ``97869acf094706da25e8c6b277d59874181dde77``
* SHA256: ``141a833640f2fff32f552b19b1f7ddb6b9c06c51637860c0d3f796f9397b356e``

<br>

### Linux (RedHat and Debian) File Hashes

V1.17.0 Full Version:  

* SHA1: ``1beae7825a9010fbec09b1b68d08b192a3aac1ee``
* SHA256: ``7ea9059af294dfb9a2cfdb95e64009a4a7ed55d3e84fa2f8dba5325959e7e8e4``

V1.17.0 Free Version:

* SHA1: ``7a41f27bac3a8cad97336f0866831948f76b9a47``
* SHA256: ``cd91d64ad1db6f7964477ac428f3af546f2ca97406ca2ee11ad87b0a46e105af``

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

