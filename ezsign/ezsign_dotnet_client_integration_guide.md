---
layout: default
title: EzSign - Client Integration Guide
parent: EzSign
nav_order: 11
---
# EzSign .Net Client Integration Guide

<br>

## Introduction

The Krestfield EzSign Client is a lightweight .NET package which interfaces with the EzSign Server enabling applications to quickly generate and verify digital signatures or encrypt and decrypt data without the need for complex programming                                                                    

The client also provides utilities to hash data, supporting both SHA-1 and the SHA-2 range of hash algorithms 

This guide details the steps required to integrate the client into applications and make use of the API

For server side setup, please refer to the [Server Configuration](ezsign_server.html)

 

## Library

The client consists of the following library files:

* EzSignClient.dll

* EzSignClientUtils.dll

 These are located at ``[installation folder]\DotNetClient\lib``

 Where ``[installation folder]`` is the location the server was installed

 To make use of the signing, verification and encryption functions, add a reference to the ``EzSignClient.dll`` file from your project

 To make use of the hashing utilities, add a reference to the ``EzSignClientUtils.dll`` file from your project

<br>

## Client API

The API to the EzSign client has intentionally been kept simple. Decisions on which keys to use, what certificates to include in signatures and what hashing algorithms to use are configured at the server level

All the client API calls are included in the EzSignClient class, which is included in the com.krestfield.ezsign.client namespace

<br>

### Constructor

The constructor is defined as:

 ```java
 public EzSignClient(String host, int port)
 ```

Where:

* ``host`` is the EzSign Server hostname (or IP Address) 

* ``port`` is the EzSign Server listening port number

 The default connection timeout to the server is 5 seconds (5000 milliseconds). But this can be overridden by using the following constructor:

 ```java
 public EzSignClient(String host, int port, int timeoutInMs, int readTimeoutInMs)
 ```

Where:

* ``timeoutInMs`` is the connection timeout expressed in milliseconds 

* ``readTimeoutInMs`` is the read timeout expressed in milliseconds

 Example:

 ```java
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

If the communications between the client and server are to be secured, an Authentication Code may be used. The Authentication Code is provided by using one of the following constructors:

``` 
public EzSignClient(String host, int port, String authCode)
```



```java
public EzSignClient(String host, int port, int timeoutInMs, int readTimeoutInMs, String authCode)
```

This will result in the encryption of the traffic between the client and server

There are no restrictions on what Authentication Code can be used, but a longer more complex code will increase security 

The same Authentication Code must also be configured on the server. Refer to the Installation and Configuration Guide for details on how to configure this on the server

<br>

### Generate Signature Methods

The following method is called to generate a signature:

```java
public byte[] signData(String channelName, byte[] dataToSign, bool isDigest) 
```

The signature returned is dependent on the signature type specified at the server and will be either a PKCS#7 formatted signature or a raw PKCS#1 signature

Note: For large data sets, it is recommended to hash the data beforehand and provide this as the dataToSign together with ``isDigest=true``. This prevents large amounts of data being passed between the client/server interface. Note: The client utils can be used to generate the required hash

 This method throws the following exceptions:

* KSigningException

  There was an error during the signing process

* KEzSignException

​       There was an internal error, incorrect parameters or other error

* KEzSignConnectException

  There was an error connecting to the server 

 

Example:

 ```java
 byte[] dataToSign = Encoding.ASCII.GetBytes("Data to sign");
 byte[] signature = client.signData("SIGNCHANNEL", dataToSign, false);
 ```

<br>

### Verify PKCS#7 Signature Methods

The following methods are used to verify a PKCS#7 signature and will perform the required path building and revocation checking as configured at the server

<br> <u>Verifying Signature 1</u>

``` java
public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest)
```

If ``contentBytes`` is a hash of the data then ``dataIsDigest`` must be *true*, otherwise *false*

 This method throws the following exceptions:

* KVerificationException

​       There was an error during the verification process

* KPathException 

​       There was a path building error

* KRevocationException

​       A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 

Example:

``` java
try
{
   client.verifySignature("SIGNCHANNEL", signature, dataToVerify, false);
   Console.Out.WriteLine("Signature verified!");
}
catch (KEzSignException generalEx)
{
   Console.Out.WriteLine("There was an error calling the verify function: " + generalEx.Message);
}
catch (KVerificationException verifyEx)
{
   Console.Out.WriteLine("There was a signature verification error: " + verifyEx.Message);
}
catch (KPathException pathEx)
{
   Console.Out.WriteLine("There was a path building error: " + pathEx.Message);
}
catch (KRevocationException revEx)
{
   Console.Out.WriteLine("There was a revocation check error: " + revEx.Message);
}
```

<br>

 <u>Verifying Signature 2</u>

This method allows for the by-passing of revocation checking and the by-passing of path building i.e. only a simple verification check will be performed to confirm the data was signed by the certificate specified in the signature and has not been altered

``` java
public void verifySignature(String channelName, byte[] signature, 
byte[] contentBytes, bool dataIsDigest,
bool bypassRevocationCheck, bool bypassPathBuild)
```

If the values for ``bypassRevocationCheck`` and ``bypassPathBuild`` are both set to *false* the signature will be verified in the same way as the previous method

 This method throws the following exceptions:

* KVerificationException

​       There was an error during the verification process

* KPathException 

​       There was a path building error

* KRevocationException

​       A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 <br>

### Verify Raw Signature Methods

The following methods are used to verify Raw (PKCS#1) signatures and will perform the required path building and revocation checking as configured at the server

<br>

<u>Verifying Raw Signature 1</u>

 Note that as a PKCS#1 signature does not contain the signer certificate, this must be provided 

 If there are other certificates in the path that are not stored in the channel, use the Verify Raw Signature 2 method. Path building and revocation checking (if configured at the server) will be performed

 ```java
 public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest, 
                             X509Certificate signerCert)
 ```

This method throws the following exceptions:

* KVerificationException

​       There was an error during the verification process

* KPathException 

​       There was a path building error

* KRevocationException

​       A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 <br>

 <u>Verifying Raw Signature 2</u>

 This method accepts the signer certificate as well as other certificates in the path. Path building and revocation checking (if configured at the server) will be performed

 ```java
 public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, bool dataIsDigest, 
 		X509Certificate signerCert, X509Certificate[] otherCerts)
 ```

This method throws the following exceptions:

* KVerificationException

​       There was an error during the verification process

* KPathException 

​       There was a path building error

* KRevocationException

​       A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 <br>

<u>Verifying Raw Signature 3</u>

Use this method if you wish to bypass revocation checking (whether configured at the server or not) and/or path building 

```java
public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, boolean dataIsDigest, 							X509Certificate signerCert, X509Certificate[] otherCerts, 
                           bool bypassRevocationCheck, bool bypassPathBuild)
```

This method throws the following exceptions:

* KVerificationException

​       There was an error during the verification process

* KPathException 

​       There was a path building error

* KRevocationException

​       A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 Note:

``otherCerts`` can be null if you do not wish to specify any other certificates in the path

If you wish to perform just the signature verification operation. Set ``bypassRevocationCheck`` and ``bypassPathBuild`` both to *true* and ``otherCerts`` to *null*

 <br>

### Generate Random Number Methods

The following method is called to generate random data:

 ```java
 public byte[] generateRandomBytes(String channelName, int numBytes)
 ```

The number of random bytes selected will be returned

This method throws the following exceptions:

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 <br>

### Encrypt/Decrypt Methods

These methods provide encryption and decryption using AES keys previously generated on the server. The algorithm used is AES with CBC (Cipher Block Chaining) and PKCS#5 padding. A random IV (Initialisation Vector) is created every time data is encrypted and this IV is placed in the first 16 bytes of the returned data, with the remaining bytes being the encrypted data itself

 The following method is called to encrypt data:

 ```java
 public byte[] encryptData(String channelName, byte[] dataToEncrypt, String keyLabel)
 ```

This will encrypt the clear data contained in ``dataToEncrypt`` using the key referenced by keyLabel and return the encrypted data

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown

 This method throws the following exceptions:

* KEncipherException

​            There was an error whilst encrypting the data

* KEzSignConnectException

​            There was an error connecting to the server 

* KEzSignException

​            There was another error

 The following method is called to decrypt previously encrypted data:

 ```java
 public byte[] decryptData(String channelName, byte[] encryptedData, String keyLabel)
 ```

This will decrypt data previously encrypted with the ``encryptData`` method using the key referenced by ``keyLabel`` and return the clear data 

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown

 This method throws the following exceptions:

* KEncipherException

​       There was an error whilst decrypting the data  

* KEzSignConnectException

​       There was an error connecting to the server 

* KEzSignException

​       There was another error

 

Example:

 ```java
 try
 {
    byte[] originalClearData = Encoding.ASCII.GetBytes("Encrypt this");
    byte[] encryptedData = client.encryptData("ENCRYPTCHAN", originalClearData, "encryptkey1");
    byte[] clearData = client.decryptData("ENCRYPTCHAN", encryptedData, "encryptkey1");
 }
 catch (KEzSignException generalEx)
 {
    Console.Out.WriteLine("There was an error calling the EzSign server: " + generalEx.Message);
 }
 catch (KEncipherException encipherEx)
 {
    Console.Out.WriteLine("There was an error encrypting/decrypting data: " + encipherEx.Message);
 }
 ```

<br>

### Client Utils API

 The Client Utilis API calls are included in the ``KHash`` class

 This class is contained in the KEzSignClientUtils.dll file and held in the ``com.krestfield.ezsign.client.utils`` namespace

 

<u>KHash</u>

This class contains the following methods for the generation of hashes:

```java
public KHash(String hash)
```

The constructor can be passed the hash algorithm as a string. Accepted values are SHA-1, SHA-256, SHA-384 and SHA-512

 

```java
public byte[] digest(byte[] data)
```

This method calculates the hash value over all the data provided and returns the hash value

 

```java
public void update(byte[] data)
```

Sections or slices of data can be provided as received or processed and will be included in the overall hash generated

 

```java
public void doFinal(byte[] data)
```

If the update method has been called, when this method is called together with the last piece of data to be hashed, the hash over all the data will be calculated and returned

 

```java
public void reset()
```

This resets the internal buffer allowing the same object to be used to calculate a hash over fresh data

 

 

## Sample

The following is a transcript of a sample generating and verifying a signature

```java
import com.krestfield.ezsign.EzSignClient;
import com.krestfield.ezsign.KEzSignConnectException;
import com.krestfield.ezsign.KEzSignException;
import com.krestfield.ezsign.KPathException;
import com.krestfield.ezsign.KRevocationException;
import com.krestfield.ezsign.KSigningException;
import com.krestfield.ezsign.KVerificationException;
import com.krestfield.ezsign.client.utils.KHash;
import com.krestfield.ezsign.client.utils.KSignatureParser;
import com.krestfield.ezsign.client.utils.KConvert;

/**
 * TestClient
 *
 * This example demonstrates the use of the client and client utils
 *
 * Copyright Krestfield 2026
 */
public class TestClient
{
    public static void main(String args[])
    {
        /**
         * Specify the server IP Address. port number and channel name
         */
        String serverIPAddress = "127.0.0.1";
        int serverPortNumber = 5656;
        String channelName = "TEST";


        /**
         * Create the EzSign Client
         */
        EzSignClient client = new EzSignClient(serverIPAddress, serverPortNumber);
    
        /**
         * Specify the data to sign
         */
        byte[] dataToSign = "Hello".getBytes();
        byte[] signature = null;
    
        try
        {
            /**
             * Generate Signature Example
             */
            signature = client.signData(channelName, dataToSign, false);
            System.out.println("Generated signature successfully");
            System.out.println("Returned signature: " + KConvert.ToBase64String(signature));
    
            // Use the signature parser to obtain the signer DN and signature alg
            KSignatureParser signatureParser = new KSignatureParser(signature);
            System.out.println("Signer Certificate DN: " + signatureParser.getSignersSubjectDn());
            System.out.println("Signature Algorithm: " + signatureParser.getSignatureAlgorithmName());
    
            // Use the hash generation utils to hash the data
            KHash hash = new KHash(KHash.SHA256);
            hash.update(dataToSign);
            System.out.println("Hash over data: " + KConvert.BytesToHexStr(hash.digest()));
        }
        catch (KEzSignConnectException connEx)
        {
            System.out.println("There was an error connecting to the server: " + connEx.getMessage());
            return;	
        }
        catch (KEzSignException ex)
        {
            System.out.println("There was an error signing the data.  Error: " + ex.getMessage());
            return;
        }
        catch (KSigningException sigEx)
        {
            System.out.println("There was an error signing the data.  Error: " + sigEx.getMessage());
            return;
        }
        catch (Exception e)
        {
            System.out.println("There was an error: " + e.getMessage());
            return;
        }
    
        try
        {
            /**
             * Verify Signature Example
             */
            client.verifySignature(channelName, signature, dataToSign, false);
            System.out.println("Signature verified successfully");
        }
        catch (KVerificationException veriEx)
        {
            System.out.println("There was an error verifying the signature: " + veriEx.getMessage());
        }
        catch (KRevocationException revEx)
        {
            System.out.println("There was a revocation exception : " + revEx.getMessage());
        }
        catch (KPathException pathEx)
        {
            System.out.println("There was a path building exception : " + pathEx.getMessage());
        }
        catch (KEzSignConnectException connEx)
        {
            System.out.println("There was an error connecting to the server: " + connEx.getMessage());
        }
        catch (KEzSignException sigEx)
        {
            System.out.println("There was an error verifying the data.  Error: " + sigEx.getMessage());
        }
    }
}
```





