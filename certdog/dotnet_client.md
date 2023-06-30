---
layout: default
title: DotNet Client
parent: Certdog
nav_order: 12
---

# Certdog DotNet Client

This client enables rapid integration with your .NET applications enabling the ability to obtain certificates from the certdog application  

You can obtain the client from GitHub [here](https://github.com/krestfield/certdog-dotnet-client)  

Or the dll from [here](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdognet.dll)



## Usage

Add **certdognet** as a reference to your project  

```c#
using certdognet;

String p12Base64Data = Certdog.GetCert(certDogUrl, certIssuer, requestedDn, 
                                       csrGenerator, p12Password, sans, certDogUsername, certDogPassword);
```

Where:

  **certDogUrl**:  Is the URL to the api e.g. https://yourhost/certdog/api

  **certIssuer**: Is the name of the issuer as configured in certdog

  **requestedDn**: Is the DN of the certificate required e.g. ``CN=MyCert,O=My Org``

  **csrGenerator**: Is the name of the CSR generator to generate the CSR, as configured in certdog

  **p12Password**: Is the password the returned PKCS#12 file will be returned protected under

  **sans**: Is a ``List<String>`` of subject alternative names, e.g. {"DNS:domain.com", "IP:10.1.1.2"}. Pass an empty list of null if not required

  **certDogUsername**: Is the username of the user as configured in certdog that has access to the required certificate issuer

  **certDogPassword**: Is the password of the user  



For example, to obtain a certificate from the demo environment and save the response to a local PFX file you could do the following:

```c#
List<String> sans = new List<String>();
sans.Add("DNS:mydomain.com");

String p12Base64Data = Certdog.GetCert("https://certdog.net/certdog/api", "Certdog TLS", "CN=mydoma.com", 
    "RSA2048 Generator", "password", sans, "certdogtest", "password");

byte[] p12BinaryData = Convert.FromBase64String(p12Base64Data);
using (BinaryWriter binWriter = new BinaryWriter(File.Open("C:\\temp\\test.pfx", FileMode.Create)))
	binWriter.Write(p12BinaryData);
```



You also have the option of storing the certdog credentials in the Windows Credential Manager (see Setting Credentials below for details on storing these). You can then simplify the call further:

```c#
String p12Base64Data = Certdog.GetCert(certDogUrl, certIssuer, requestedDn, csrGenerator, p12Password, sans);
```







## Setting Credentials

It is possible to store the certdog username and password in the Windows Credential Manager. This secures these credentials and ensures they can only be accessed by that user, on that machine  

If you will perform these steps with the same account that the application (that calls the dot net client) will be running under, then you only need to run the commands without the username and password  

If the application will be running under another account (e.g. the LOCAL SYSTEM account), then you need to run these commands under that account. See [Running as Local System](#Running as Local System) for an example

1. Open a Command Prompt
2. Type the following
```
cmdkey /generic:CERTDOGCREDS /user:certdogusername /pass:certdogpassword
```
3. Setting the required username and password for **certdogusername** and **certdogpassword**



To list the updates, type the following:

```shell
cmdkey /list:CERTDOGCREDS
```



### Running as Local System

If not already installed, obtain **PSTools** from here:  

[https://docs.microsoft.com/en-us/sysinternals/downloads/pstools](https://docs.microsoft.com/en-us/sysinternals/downloads/pstools)  

Unzip to a local folder and optionally, update your path to reference the folder (this will allow you to run the tools from any location on the machine)  

1. Open a new command prompt as Administrator  

2. Type  

```shell
psexec -i -s cmd.exe
```

3. And press Enter  

A new command prompt will open - running under the LOCAL SYSTEM account  

Now run the cmdkey steps above. This will result in these credentials being accessible by an application running under the LOCAL SYSTEM account



