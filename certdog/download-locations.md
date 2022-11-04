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

* SHA1: ``1b4846aaa36f05cc267cc7593dec11ba3e913260``

* SHA256: ``31f9d0a7e4a6a7008bc0ef154b92b30cd7792e55e945901a14f8be782a83f431``

Free Version:  

* SHA1: ``70f513df4f526c9582f8623bb5e178af81218452``

* SHA256: ``a1d9475c84baca8679fc3883fd1dbc5280951dace3a92d844555b04e01d9449e``

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

