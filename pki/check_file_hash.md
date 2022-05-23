---
layout: default
title: Check File Hash
parent: General PKI
nav_order: 101
---

# Checking File Hashes

<br>

To check the hash of a file, you can use the ``certutil`` command as follows:

Open a command prompt or PowerShell window and navigate to the location of the file e.g.

``C:\Users\myname\Downloads``

To generate a SHA-1 hash over the file, at the prompt type:

``certutil -hashfile certdog.zip``

Certutil defaults to SHA-1, but you may also specify explicitly as follows:

``certutil -hashfile certdog.zip sha1``

<br>

To generate a SHA-256 hash over the file , type:

``certutil -hashfile certdog.zip sha256``

E.g.

```powershell
C:\temp\downloads>certutil -hashfile certdog.zip sha256
SHA256 hash of c:\Users\myname\Downloads\certdog.zip:
eeaab3196237b390e861cf5ab3c2abab51f70ba1d63069a40d97bc9852dc4e83
CertUtil: -hashfile command completed successfully.
```

The output is the hash, e.g. in the example above, the SHA-256 hash over the file is

``eeaab3196237b390e861cf5ab3c2abab51f70ba1d63069a40d97bc9852dc4e83``

