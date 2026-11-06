---
layout: default
title: EzSign - .NET Client Integration Guide
parent: EzSign
nav_order: 15
---
# EzSign .NET Client Integration Guide

<br>

## Introduction

The Krestfield EzSign Client is a lightweight .NET library which interfaces with the EzSign Server, enabling applications to quickly generate and verify digital signatures, encrypt and decrypt data and generate random data without the need for complex programming

The client can communicate with the server using either the socket API or, from client version 4.6.0, the server's REST API. The operations are called in the same way for both, so an application can move from one to the other by changing only how the client is created

The client also provides utilities to hash data (SHA-1 and the SHA-2 family), parse signatures and convert data

This guide details the steps required to integrate the client into applications and make use of the API

For server side setup, please refer to the [Server Configuration](ezsign_server.html) and, for the REST API, the [REST API](ezsign_rest_api.html) guide

<br>

## Library

The client consists of the following library files:

* ``EzSignClient.dll`` - the client: signing, verification, encryption, decryption and random data, over the socket API or the REST API

* ``EzSignClientUtils.dll`` - optional utilities: hashing, signature parsing and data conversion

These are located at ``[installation folder]\DotNetClient\lib``, where ``[installation folder]`` is the location the server was installed

Add a reference to ``EzSignClient.dll`` from your project to use the client, and to ``EzSignClientUtils.dll`` to use the utilities

<br>

### Choosing the Build

The libraries are provided in two builds, with the same features. Use the one that matches the .NET version the application is built with:

| Folder | For applications built with | Runs on |
| --- | --- | --- |
| ``net48`` | .NET Framework 4.8 or 4.8.1 | Windows |
| ``net10.0`` | .NET 10 or later | Windows, Linux, macOS |

The build depends on the application, not the version of Windows it runs on. The application's project file shows which it is: ``<TargetFrameworkVersion>v4.8</TargetFrameworkVersion>`` is .NET Framework (use ``net48``) and ``<TargetFramework>net10.0</TargetFramework>`` is .NET 10 (use ``net10.0``). Applications built with .NET 8 or .NET 9 cannot use either build and should move to .NET 10

``EzSignClient.dll`` needs no other files. On .NET 10, ``EzSignClientUtils.dll`` also needs the **System.Security.Cryptography.Pkcs** package (version 10.0.14 or later), which is part of .NET Framework but not of .NET 10. Add it to the project:

```
dotnet add package System.Security.Cryptography.Pkcs --version 10.0.14
```

or, in Visual Studio, install it with **Manage NuGet Packages**

The libraries are code signed by Krestfield Ltd

<br>

## Client API

The API to the EzSign client has intentionally been kept simple. Decisions on which keys to use, what certificates to include in signatures and what hashing algorithms to use are configured at the server level

There are two client classes, both in the ``com.krestfield.ezsign.client`` namespace:

* ``EzSignClient`` - uses the socket API

* ``EzSignRestClient`` - uses the REST API (EzSign server 4.6.0 or later)

Both provide the same operations (``signData``, ``verifySignature``, ``verifyRawSignature``, ``encryptData``, ``decryptData`` and ``generateRandomBytes``), which are described under [Operations](#operations) below

<br>

### The Socket API

<u>Constructor</u>

The constructor is defined as:

```csharp
public EzSignClient(String host, int port)
```

Where:

* ``host`` is the EzSign Server hostname (or IP Address)

* ``port`` is the EzSign Server listening port number

The default connection and read timeouts are 5 seconds (5000 milliseconds). These can be overridden by using the following constructor:

```csharp
public EzSignClient(String host, int port, int timeoutInMs, int readTimeoutInMs)
```

Where:

* ``timeoutInMs`` is the connection timeout expressed in milliseconds

* ``readTimeoutInMs`` is the read timeout expressed in milliseconds

Example:

```csharp
using com.krestfield.ezsign.client;

namespace App1
{
    class Program
    {
        static void Main(string[] args)
        {
            EzSignClient client = new EzSignClient("10.100.56.11", 5656);
        }
    }
}
```

To protect the communications between the client and server, an Authentication Code and/or TLS may be used

<br>

<u>Authentication Code</u>

The Authentication Code is provided by using one of the following constructors:

```csharp
public EzSignClient(String host, int port, String authCode)
```

```csharp
public EzSignClient(String host, int port, int timeoutInMs, int readTimeoutInMs, String authCode)
```

This will result in the encryption of the traffic between the client and server

There are no restrictions on what Authentication Code can be used, but a longer more complex code will increase security

The same Authentication Code must also be configured on the server. See [Set Authentication Code](ezsign_management_tool.html#set-authentication-code) in the Management Tool guide

<br>

<u>Using TLS</u>

If the server's socket API is configured with a TLS certificate, the client connects with TLS by calling ``useTls()``:

```csharp
EzSignClient client = new EzSignClient("ezsign.example.com", 5656).useTls();
```

The server's certificate must be trusted by Windows (or, on Linux and macOS, by the operating system) and must be valid for the host name or IP Address used to connect. If the server's certificate is issued by a private CA that is not trusted, the CA certificate can be trusted by this client only, without adding it to the certificate store:

```csharp
using com.krestfield.ezsign.utils;

EzSignClient client = new EzSignClient("ezsign.example.com", 5656)
    .useTls(KCertificateFiles.LoadCertificate(@"C:\certs\serverca.cer"));
```

If the server requires a client certificate, provide it in a PFX (PKCS#12) file with its private key. This also turns on TLS:

```csharp
EzSignClient client = new EzSignClient("ezsign.example.com", 5656)
    .useClientTls(@"C:\certs\client.pfx", pfxPassword);
```

TLS 1.2 or TLS 1.3 is used, as the operating system supports. TLS and an Authentication Code can be used together

<br>

### The REST API

From version 4.6.0 the client can use the server's REST API with the ``EzSignRestClient`` class. The REST API must be enabled on the server, and a REST API user must be created for the application using the [Management Tool](ezsign_management_tool.html). The user must be granted the operations and channels the application uses, see [Authentication and Permissions](ezsign_rest_api.html#authentication-and-permissions)

<u>Constructor</u>

```csharp
public EzSignRestClient(String baseUrl)
```

Where ``baseUrl`` is the scheme, host and REST API port (``server.restapi.port``) e.g. ``https://ezsign.example.com:8443``

The client then authenticates with an API token, a client certificate, or both (the server uses the token if both are sent). These options, and the others below, are set when the client is created, before its first request

<br>

<u>API Token</u>

``withApiToken()`` provides the API token issued for the REST API user (``ezsign-manage users add-token``). It is sent in the ``Authorization: Bearer`` header:

```csharp
using com.krestfield.ezsign.client;

EzSignRestClient client = new EzSignRestClient("https://ezsign.example.com:8443").withApiToken(apiToken);
```

The token should be held securely by the application, for example in a protected configuration file or a secrets store, and not written in the source code

<br>

<u>Client Certificate</u>

``withClientCertificate()`` provides a TLS client certificate and its private key, in a PFX (PKCS#12) file. The certificate must be one the REST API user has been configured with:

```csharp
EzSignRestClient client = new EzSignRestClient("https://ezsign.example.com:8443")
    .withClientCertificate(@"C:\certs\client.pfx", pfxPassword);
```

An ``X509Certificate2`` with its private key, for example from the Windows certificate store, can be passed instead of the file name and password

<br>

<u>Trusting the Server's Certificate</u>

The server's TLS certificate must be trusted by Windows (or the operating system) and must be valid for the host name in the URL. If it is issued by a private CA that is not trusted, the CA certificate can be trusted by this client only:

```csharp
using com.krestfield.ezsign.utils;

EzSignRestClient client = new EzSignRestClient("https://ezsign.example.com:8443")
    .withApiToken(apiToken)
    .withTrustedServerCa(KCertificateFiles.LoadCertificate(@"C:\certs\serverca.cer"));
```

If the server's REST API has TLS turned off (``server.restapi.useTls=false``), use an ``http://`` URL. The API token is then sent unencrypted, so this is only suitable when the client and server are on the same machine

<br>

<u>Timeout</u>

The default timeout for each request is 30 seconds. It can be changed with ``withTimeout()``, in milliseconds:

```csharp
EzSignRestClient client = new EzSignRestClient(url).withApiToken(apiToken).withTimeout(10000);
```

<br>

<u>Using the Client</u>

Create one client and reuse it for the life of the application: it can be used by many threads at the same time and keeps its connections to the server open. Creating a client for each request is slower. ``EzSignRestClient`` is ``IDisposable``: dispose of it when the application no longer needs it

```csharp
using (EzSignRestClient client = new EzSignRestClient("https://ezsign.example.com:8443").withApiToken(apiToken))
{
    byte[] signature = client.signData("SIGNCHANNEL", data, false);
    client.verifySignature("SIGNCHANNEL", signature, data, false);
}
```

Each operation also has an asynchronous version, with the same name ending in ``Async``, that returns a ``Task`` and takes an optional ``CancellationToken``:

```csharp
byte[] signature = await client.signDataAsync("SIGNCHANNEL", data, false);
```

The REST client also provides:

* ``isHealthy()`` - returns *true* if the REST API is running. This needs no authentication

* ``whoAmI()`` - returns the user the server authenticated the client as, the authentication method and the user's permissions (a ``KWhoAmI``, in the ``com.krestfield.ezsign.client.rest`` namespace). This is useful to check the client is set up correctly

* ``getStatusJson()`` - returns the server status as JSON. The user needs the ``status`` permission

<br>

<u>REST API Errors</u>

A failed operation throws the same exceptions as the socket API, described for each operation below. Other errors throw a ``KEzSignRestException``, which is a ``KEzSignException`` with these properties:

* ``HttpStatus`` - the HTTP status, e.g. *401* (not authenticated), *403* (the user does not have the permission) or *503* (the server is busy)

* ``ErrorCode`` - the server's error code, e.g. *FORBIDDEN*. The error codes are listed in the [REST API Reference](rest-api/index.html)

* ``TransactionId`` - the ID of the request in the server log

* ``IsBusy`` - *true* if the server was busy (503), and the request can be tried again later

Errors connecting to the server, including a server certificate that is not trusted, throw a ``KEzSignConnectException``

<br>

### Switching Between the Socket and REST APIs

An application that uses the socket API can move to the REST API by:

1. Creating an ``EzSignRestClient`` instead of an ``EzSignClient``, with the server's REST API URL and port
2. Providing an API token or client certificate, instead of an Authentication Code (an Authentication Code is not used with the REST API)
3. Granting the REST API user the permissions for the operations and channels the application uses

The operations are called in the same way and throw the same exceptions, so the rest of the application does not change:

```csharp
// Socket API
EzSignClient client = new EzSignClient("ezsign.example.com", 5656, authCode);

// REST API
EzSignRestClient client = new EzSignRestClient("https://ezsign.example.com:8443").withApiToken(apiToken);
```

<br>

## Operations

The following operations are provided by both ``EzSignClient`` and ``EzSignRestClient``. With the REST API, the user needs the permission named for each operation on the channel used

The exception classes are separate classes (none derives from another, apart from ``KEzSignRestException``), so they can be caught in any order

<br>

### Generate Signature Methods

The following method is called to generate a signature (REST API permission: ``sign``):

```csharp
public byte[] signData(String channelName, byte[] dataToSign, bool isDigest)
```

The signature returned is dependent on the signature type specified at the server and will be either a PKCS#7 formatted signature or a raw (e.g. PKCS#1) signature

Note: For large data sets, it is recommended to hash the data beforehand and provide this as the ``dataToSign`` together with ``isDigest=true``. This prevents large amounts of data being passed between the client and server. The client utils can be used to generate the required hash

This method throws the following exceptions:

* KSigningException

  There was an error during the signing process

* KEzSignConnectException

  There was an error connecting to the server

* KEzSignException

  There was an internal error, incorrect parameters or other error

Example:

```csharp
byte[] dataToSign = Encoding.UTF8.GetBytes("Data to sign");
byte[] signature = client.signData("SIGNCHANNEL", dataToSign, false);
```

<br>

### Verify PKCS#7 Signature Methods

The following methods are used to verify a PKCS#7 signature and will perform the required path building and revocation checking as configured at the server (REST API permission: ``verify``)

<br> <u>Verifying Signature 1</u>

```csharp
public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest)
```

If ``contentBytes`` is a hash of the data then ``dataIsDigest`` must be *true*, otherwise *false*

The method returns if the signature is valid, and throws an exception if it is not

This method throws the following exceptions:

* KVerificationException

  The signature did not verify, e.g. the data has been altered

* KPathException

  There was a path building error

* KRevocationException

  A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

  There was an error connecting to the server

* KEzSignException

  There was another error

Example:

```csharp
try
{
    client.verifySignature("SIGNCHANNEL", signature, dataToVerify, false);
    Console.WriteLine("Signature verified!");
}
catch (KVerificationException verifyEx)
{
    Console.WriteLine("There was a signature verification error: " + verifyEx.Message);
}
catch (KPathException pathEx)
{
    Console.WriteLine("There was a path building error: " + pathEx.Message);
}
catch (KRevocationException revEx)
{
    Console.WriteLine("There was a revocation check error: " + revEx.Message);
}
catch (KEzSignConnectException connectEx)
{
    Console.WriteLine("There was an error connecting to the server: " + connectEx.Message);
}
catch (KEzSignException generalEx)
{
    Console.WriteLine("There was an error calling the verify function: " + generalEx.Message);
}
```

<br>

<u>Verifying Signature 2</u>

This method allows for the by-passing of revocation checking and the by-passing of path building i.e. only a simple verification check will be performed to confirm the data was signed by the certificate specified in the signature and has not been altered

```csharp
public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest,
                            bool bypassRevocationCheck, bool bypassPathBuild)
```

If the values for ``bypassRevocationCheck`` and ``bypassPathBuild`` are both set to *false* the signature will be verified in the same way as the previous method

With the REST API, bypassing either check also needs the ``verify.bypass`` permission

This method throws the same exceptions as Verifying Signature 1

<br>

### Verify Raw Signature Methods

The following methods are used to verify raw (e.g. PKCS#1) signatures and will perform the required path building and revocation checking as configured at the server (REST API permission: ``verify``)

As a raw signature does not contain the signer certificate, this must be provided

<br>

<u>Verifying Raw Signature 1</u>

If there are other certificates in the path that are not stored in the channel, use the Verifying Raw Signature 2 method. Path building and revocation checking (if configured at the server) will be performed

```csharp
public void verifyRawSignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest,
                               X509Certificate signerCert)
```

This method throws the same exceptions as Verifying Signature 1

<br>

<u>Verifying Raw Signature 2</u>

This method accepts the signer certificate as well as other certificates in the path. Path building and revocation checking (if configured at the server) will be performed

```csharp
public void verifyRawSignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest,
                               X509Certificate signerCert, X509Certificate[] otherCerts)
```

This method throws the same exceptions as Verifying Signature 1

<br>

<u>Verifying Raw Signature 3</u>

Use this method if you wish to bypass revocation checking (whether configured at the server or not) and/or path building

```csharp
public void verifyRawSignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest,
                               X509Certificate signerCert, X509Certificate[] otherCerts,
                               bool bypassRevocationCheck, bool bypassPathBuild)
```

This method throws the same exceptions as Verifying Signature 1

Note:

``otherCerts`` can be null if you do not wish to specify any other certificates in the path

If you wish to perform just the signature verification operation, set ``bypassRevocationCheck`` and ``bypassPathBuild`` both to *true* and ``otherCerts`` to *null*. With the REST API this needs the ``verify.bypass`` permission

The certificates can be loaded from files with ``KCertificateFiles.LoadCertificate()`` in the ``com.krestfield.ezsign.utils`` namespace:

```csharp
X509Certificate2 signerCert = KCertificateFiles.LoadCertificate(@"C:\certs\signer.cer");
client.verifyRawSignature("RAWCHANNEL", signature, dataToVerify, false, signerCert);
```

<br>

### Generate Random Number Methods

The following method is called to generate random data (REST API permission: ``random``):

```csharp
public byte[] generateRandomBytes(String channelName, int numBytes)
```

The number of random bytes requested will be returned. With the REST API, up to 65536 bytes can be requested at a time

This method throws the following exceptions:

* KEzSignConnectException

  There was an error connecting to the server

* KEzSignException

  There was another error

<br>

### Encrypt/Decrypt Methods

These methods provide encryption and decryption using AES keys previously generated on the server. The algorithm used is AES with CBC (Cipher Block Chaining) and PKCS#5 padding. A random IV (Initialisation Vector) is created every time data is encrypted and this IV is placed in the first 16 bytes of the returned data, with the remaining bytes being the encrypted data itself

The following method is called to encrypt data (REST API permission: ``encrypt``):

```csharp
public byte[] encryptData(String channelName, byte[] dataToEncrypt, String keyLabel)
```

This will encrypt the clear data contained in ``dataToEncrypt`` using the key referenced by ``keyLabel`` and return the encrypted data

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown. With the REST API, ``keyLabel`` may be *null* to use the channel's default key

This method throws the following exceptions:

* KEncipherException

  There was an error whilst encrypting the data

* KEzSignConnectException

  There was an error connecting to the server

* KEzSignException

  There was another error

The following method is called to decrypt previously encrypted data (REST API permission: ``decrypt``):

```csharp
public byte[] decryptData(String channelName, byte[] encryptedData, String keyLabel)
```

This will decrypt data previously encrypted with the ``encryptData`` method using the key referenced by ``keyLabel`` and return the clear data

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown

This method throws the following exceptions:

* KEncipherException

  There was an error whilst decrypting the data

* KEzSignConnectException

  There was an error connecting to the server

* KEzSignException

  There was another error

Example:

```csharp
try
{
    byte[] originalClearData = Encoding.UTF8.GetBytes("Encrypt this");
    byte[] encryptedData = client.encryptData("ENCRYPTCHAN", originalClearData, "encryptkey1");
    byte[] clearData = client.decryptData("ENCRYPTCHAN", encryptedData, "encryptkey1");
}
catch (KEncipherException encipherEx)
{
    Console.WriteLine("There was an error encrypting/decrypting data: " + encipherEx.Message);
}
catch (KEzSignException generalEx)
{
    Console.WriteLine("There was an error calling the EzSign server: " + generalEx.Message);
}
```

<br>

## Client Utils API

The utilities are contained in the ``EzSignClientUtils.dll`` file and held in the ``com.krestfield.ezsign.client.utils`` namespace

<br>

<u>KHash</u>

This class contains the following methods for the generation of hashes:

```csharp
public KHash(String hash)
```

The constructor is passed the hash algorithm as a string. Accepted values are SHA-1, SHA-256, SHA-384 and SHA-512, also available as the constants ``KHash.SHA1``, ``KHash.SHA256``, ``KHash.SHA384`` and ``KHash.SHA512``

```csharp
public byte[] digest(byte[] data)
```

This method calculates the hash over the data provided and returns the hash value

```csharp
public void update(byte[] data)
```

Sections or slices of data can be provided as received or processed and will be included in the overall hash generated

```csharp
public byte[] doFinal(byte[] data)
```

After the update method has been called, this method is called with the last piece of data to be hashed (which may be empty). The hash over all the data is calculated and returned

```csharp
public void reset()
```

This resets the internal buffer allowing the same object to be used to calculate a hash over fresh data

<br>

<u>KSignatureParser</u>

This class reads the details of a PKCS#7 signature. It is created with the signature, as bytes or base64:

```csharp
public KSignatureParser(byte[] signature)
public KSignatureParser(String b64Signature)
```

And provides methods including ``getSignerCertificate()``, ``getSignersSubjectDn()``, ``getSignersIssuerDn()``, ``getCertificates()``, ``getSignatureAlgorithmName()`` and ``includesSignedAttributes()``

<br>

<u>KConvert</u>

This class converts data: ``ToBase64String()``, ``B64StringToBytes()``, ``BytesToHexStr()`` and ``HexStrToBytes()``

<br>

## Sample

The following sample generates and verifies a signature, and uses the client utils:

```csharp
using System;
using System.Text;
using com.krestfield.ezsign.client;
using com.krestfield.ezsign.client.utils;

/**
 * This example demonstrates the use of the client and client utils
 */
public class TestClient
{
    public static void Main(string[] args)
    {
        // The server's address, socket API port number and the channel name
        String serverIPAddress = "127.0.0.1";
        int serverPortNumber = 5656;
        String channelName = "TEST";

        // Create the client. For the REST API use, for example:
        //   EzSignRestClient client = new EzSignRestClient("https://127.0.0.1:8443").withApiToken(apiToken);
        EzSignClient client = new EzSignClient(serverIPAddress, serverPortNumber);

        // The data to sign
        byte[] dataToSign = Encoding.UTF8.GetBytes("Hello");
        byte[] signature = null;

        try
        {
            // Generate a signature
            signature = client.signData(channelName, dataToSign, false);
            Console.WriteLine("Generated signature successfully");
            Console.WriteLine("Returned signature: " + KConvert.ToBase64String(signature));

            // Use the signature parser to obtain the signer DN and signature algorithm
            KSignatureParser signatureParser = new KSignatureParser(signature);
            Console.WriteLine("Signer Certificate DN: " + signatureParser.getSignersSubjectDn());
            Console.WriteLine("Signature Algorithm: " + signatureParser.getSignatureAlgorithmName());

            // Use the hash utility to hash the data
            KHash hash = new KHash(KHash.SHA256);
            Console.WriteLine("Hash over data: " + KConvert.BytesToHexStr(hash.digest(dataToSign)));
        }
        catch (KSigningException sigEx)
        {
            Console.WriteLine("There was an error signing the data. Error: " + sigEx.Message);
            return;
        }
        catch (KEzSignConnectException connEx)
        {
            Console.WriteLine("There was an error connecting to the server: " + connEx.Message);
            return;
        }
        catch (KEzSignException ex)
        {
            Console.WriteLine("There was an error signing the data. Error: " + ex.Message);
            return;
        }

        try
        {
            // Verify the signature
            client.verifySignature(channelName, signature, dataToSign, false);
            Console.WriteLine("Signature verified successfully");
        }
        catch (KVerificationException veriEx)
        {
            Console.WriteLine("There was an error verifying the signature: " + veriEx.Message);
        }
        catch (KRevocationException revEx)
        {
            Console.WriteLine("There was a revocation exception: " + revEx.Message);
        }
        catch (KPathException pathEx)
        {
            Console.WriteLine("There was a path building exception: " + pathEx.Message);
        }
        catch (KEzSignConnectException connEx)
        {
            Console.WriteLine("There was an error connecting to the server: " + connEx.Message);
        }
        catch (KEzSignException ex)
        {
            Console.WriteLine("There was an error verifying the data. Error: " + ex.Message);
        }
    }
}
```

<br>

## Upgrading to Version 4.6.0

Existing applications do not need to change to use version 4.6.0 with the socket API. However, note the following changes in behaviour:

* The libraries are built for .NET Framework 4.8 and .NET 10, see [Choosing the Build](#choosing-the-build)
* When TLS is used, TLS 1.2 or TLS 1.3 is used, as the operating system supports, rather than only TLS 1.2
* Methods no longer return ``null`` when the server returns an unexpected response. A ``KEzSignException`` is thrown instead
* Large responses, such as signatures over large data or with many certificates, are now always read in full
* The client connects over IPv4 or IPv6, as the server's host name resolves

<br>

## Support

All questions, queries around the API described within this document should be directed to *Krestfield Support* at the following email address:

support@krestfield.com
