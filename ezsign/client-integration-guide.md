---
layout: default
title: EzSign - Client Integration Guide
parent: EzSign
nav_order: 11
---

# Client Integration Guide

 

## Introduction

 

The Krestfield EzSign Client is a lightweight java package which interfaces with the EzSign Server enabling applications to quickly generate and verify digital signatures or encrypt and decrypt data without the need for complex programming.                                                                             

This guide details the steps required to integrate the client into applications and make use of the API.

For server side setup please refer to the *EzSign Installation and Configuration Guide*.

 

 

## JAR Files

 

The client is packaged within the following JAR file:

* kezsign-client-x.y.z.jar

(Where x.y.z is the version number e.g. 4.0.0)

 

This is located at ``[installation folder]/EzSignClient/lib``

Where ``[installation folder]`` is the location the server was installed

 

To make use of the signing, verification and encryption functions, add the ``ezsign-client-x.y.z.jar`` to your application’s class path. Alternatively, you can add the following maven dependency: 

```xml
<dependency>
 <groupId>com.krestfield.ezsign</groupId>
 <artifactId>ezsign-client</artifactId>
 <version>x.y.z</version>
</dependency>
```



  

 

## Client API



 The API to the EzSign client has intentionally been kept simple. Decisions on which keys to use, what certificates to include in signatures and what hashing algorithms to use are configured at the server level.  

 All the client API calls are included in the ``EzSignClient`` class, which is included in the ``com.krestfield.ezsign`` package.  

  

### Constructor

The simplest constructor is defined as:

```java
public EzSignClient(String host, 
                    int port)
```



Where:

* ``host`` is the server hostname (or IP Address)

* ``port`` is the server listening port number

 

The default connection timeout to the server is 5 seconds (5000 milliseconds). But this can be overridden by using the following constructor: 

```java
public EzSignClient(String host, 
                    int port, 
                    int timeoutInMs, 
                    int readTimeoutInMs)
```

 

Where:

* ``timeoutInMs`` is the connection timeout expressed in milliseconds 

* ``readTimeoutInMs`` is the read timeout expressed in milliseconds

 

Example: 

```java
import com.krestfield.ezsign;
 

public class ClientTest
{
   	public static void main(String[] args)
	{
		EzSignClient client = new EzSignClient(“10.100.12.15”, 5656);
	}
}
```



To encrypt communications between the client and server, you may utilise TLS and/or an Authentication code.  



<u>Using TLS</u>

(Note: for information on configuring TLS at both the server and client, see the [Configuring TLS Guide](configuring_tls.html))

EzSign supports server side TLS as well as client-server TLS.  

If the server has been configured with a server side TLS certificate, in that the ``server.useTls`` has been set to ``true`` or the server is sitting behind a load-balancer that terminates TLS sessions for example, the ``EzSignClient`` constructor must also have the ``useTls()`` option set, for example:

```java
EzSignClient client = new EzSignClient(“10.100.12.15”, 5656).useTls();
```

The client will connect to the server over TLS.



If you wish to use client-server TLS, the client must make use of a client-side TLS certificate to authenticate to the server. The client must be created with the ``useClientTls()`` option. This is in addition to the ``useTls()`` option. 

``useClientTls`` requires three parameters:

* ``clientKeystoreFilename`` - The Keystore Filename
  * This is the full path to the PKCS12 file
* ``clientKeystorePassword`` - The Keystore Password
  * This is the password that protects the keystore file
* ``keyStoreType`` - The Keystore Type
  * This can be "JKS" or "PKCS12"

I.e.

```java
EzSignClient client = new EzSignClient(
    serverAddress, serverPort)
    .useTls()
    .useClientTls(keystoreFilename, keystorePassword, keystoreType);
```

For example:

```java
EzSignClient client = new EzSignClient(
    "ezsign.server1.local", 5656)
    .useTls()
    .useClientTls("/opt/keystores/client.p12", "password", "PKCS12");
```

The client will now attempt to connect to the server using TLS and will now also provide the certificate supplied in the specified keystore file.





<u>Using an Authentication Code</u>

If the communications between the client and server are to be secured, an Authentication Code may be used. The Authentication Code is provided by using one of the following constructors:

  

```java
public EzSignClient(String host, 
                    int port, 
                    String authCode)
```

 

```java
public EzSignClient(String host, 
                    int port, 
					int timeoutInMs, 
                    int readTimeoutInMs, 
					String authCode)
```

 

This will result in the encryption of the traffic between the client and server

There are no restrictions on what Authentication Code can be used, but a longer more complex code will increase security 

The same Authentication Code must also be configured on the server. Refer to the Installation and Configuration Guide for details on how to configure this on the server.

 

### Generate Signature Methods

The following method is called to generate a signature:

``` java
public byte[] signData(String channelName, 
                       byte[] dataToSign, 
                       boolean isDigest) 
```

 The signature returned is dependent on the signature type specified at the server and will be either a PKCS#7 formatted signature or a raw signature.

 

Note: For large data sets, it is recommended to hash the data beforehand and provide the hash as the ``dataToSign`` together with ``isDigest``=``true``. This prevents large amounts of data being passed between the client/server interface. 

 This method throws the following exceptions: 

* KSigningException

​            There was an error during the signing process 

* KEzSignException

​            There was an internal error, incorrect parameters or other error 

* KEzSignConnectException

​            There was an error connecting to the server 

 

Example:

 ```java
 byte[] dataToSign = "Hello".getBytes();
 byte[] signature = client.signData(“CHANNEL1”, dataToSign, false);
 ```

 

 

### Verify PKCS#7 Signature Methods



The following methods are used to verify a PKCS#7 signature and will perform the required path building and revocation checking as configured at the server.

 

<u>Verifying Signature 1</u>

 ```java
 public void verifySignature(String channelName, 
                             byte[] signature, 
                             byte[] contentBytes, 
                             boolean dataIsDigest)
 ```

 If ``contentBytes`` is a hash of the data then ``dataIsDigest`` must be ``true``, otherwise ``false``

 

 This method throws the following exceptions:

* KVerificationException

​            There was an error during the verification process 

* KPathException 

​            There was a path building error 

* KRevocationException

​            A certificate is revoked or there was an error during the revocation check process 

* KEzSignConnectException

​            There was an error connecting to the server  

* KEzSignException

​            There was another error

 

Example:

``` java
try 
{
	client.verifySignature(“CHANNEL1”, signature, content, false);
} 
catch (KVerificationException verifyEx) {
   System.out.println(“There was a verification error: ” + verifyEx.getMessage());
} 
catch (KPathException pathEx) {
   System.out.println(“There was a path build error: ” + pathEx.getMessage());
} 
catch (KRevocationException revEx){
   System.out.println(“There was a revocation check error: ” + revEx.getMessage());
}
...
```



 

 <u>Verifying Signature 2</u>

 This method allows for the by-passing of revocation checking and/or the by-passing of path building i.e. only a simple verification check will be performed to confirm the data was signed by the certificate specified in the signature and has not been altered.

``` java
public void verifySignature(String channelName, 
                            byte[] signature, 
							byte[] contentBytes, 
                            boolean dataIsDigest, 
                            boolean bypassRevocationCheck, 
							boolean bypassPathBuild)
```

 If the values for ``bypassRevocationCheck`` and ``bypassPathBuild`` are both set to ``false`` the signature will be verified in the same way as the previous method.

 

This method throws the following exceptions:

* KVerificationException

​            There was an error during the verification process

* KPathException 

​            There was a path building error

* KRevocationException

​            A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​            There was an error connecting to the server  

* KEzSignException

​            There was another error

 

  

### Verify Raw Signature Methods



The following methods are used to verify Raw (for RSA these are PKCS#1 formatted) signatures and will perform the required path building and revocation checking as configured at the server.

  

<u>Verifying Raw Signature 1</u>

Note that as a raw signature does not contain the signer certificate, this must be provided 

 

If there are other certificates in the path that are not stored in the channel, use the *Verify Raw Signature 2* method below.  Path building and revocation checking (if configured at the server) will be performed.

 ```java
 public void verifySignature(String channelName, 
                             byte[] signature, 
 							byte[] contentBytes, 
                             boolean dataIsDigest, 
                             X509Certificate signerCert)
 ```



This method throws the following exceptions:

* KVerificationException

​            There was an error during the verification process

* KPathException 

​            There was a path building error

* KRevocationException

​            A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​            There was an error connecting to the server 

* KEzSignException

​            There was another error

  

<u>Verifying Raw Signature 2</u>

This method accepts the signer certificate *as well as* other certificates in the path. Path building and revocation checking (if configured at the server) will be performed.

 ```java
 public void verifySignature(String channelName, 
                             byte[] signature, 
                             byte[] contentBytes, 
 							boolean dataIsDigest, 
                             X509Certificate signerCert, 
 							X509Certificate[] otherCerts)
 ```

 

This method throws the following exceptions:

* KVerificationException

​            There was an error during the verification process

* KPathException 

​            There was a path building error

* KRevocationException

​            A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​            There was an error connecting to the server 

* KEzSignException

​            There was another error

 

 

<u>Verifying Raw Signature 3</u>

Use this method if you wish to bypass revocation checking (whether configured at the server or not) and/or path building. 

``` java
public void verifySignature(String channelName, 
                            byte[] signature, 
							byte[] contentBytes, 
                            boolean dataIsDigest, 
							X509Certificate signerCert, 
							X509Certificate[] otherCerts,
							boolean bypassRevocationCheck, 
                            boolean bypassPathBuild)
```

 

This method throws the following exceptions:

* KVerificationException

​            There was an error during the verification process

* KPathException 

​            There was a path building error

* KRevocationException

​            A certificate is revoked or there was an error during the revocation check process

* KEzSignConnectException

​            There was an error connecting to the server  

* KEzSignException

​            There was another error

  

Note:

``otherCerts`` can be null if you do not wish to specify any other certificates in the path

If you wish to perform just the signature verification operation. Set ``bypassRevocationCheck`` and ``bypassPathBuild`` both to ``true`` and ``otherCerts`` to ``null``

  

 

### Generate Random Number Methods

 

The following method is called to generate random data:

 ```java
 public byte[] generateRandomBytes(String channelName, 
                                   int numBytes)
 ```

The number of random bytes specified will be returned

 

This method throws the following exceptions:

* KEzSignConnectException

​            There was an error connecting to the server 

* KEzSignException

​            There was another error

  

 

### Encrypt/Decrypt Methods



These methods provide encryption and decryption using AES keys previously generated on the server.   

The algorithm used is AES with CBC (Cipher Block Chaining) and PKCS#5 padding. A random IV (Initialisation Vector) is created every time data is encrypted and this IV is placed in the first 16 bytes of the returned data, with the remaining bytes being the encrypted data itself.

The following method is called to encrypt data:

 ```java
 public byte[] encryptData(String channelName, 
                           byte[] dataToEncrypt, 
                           String keyLabel)
 ```

This will encrypt the clear data contained in ``dataToEncrypt`` using the key referenced by ``keyLabel`` and return the encrypted data.

 

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown.

 

This method throws the following exceptions:

* KEncipherException

​            There was an error whilst encrypting the data     

* KEzSignConnectException

​            There was an error connecting to the server 

* KEzSignException

​            There was another error

 

The following method is called to decrypt previously encrypted data:

 ```java
 public byte[] decryptData(String channelName, 
                           byte[] encryptedData, 
                           String keyLabel)
 ```

This will decrypt data previously encrypted with the ``encryptData`` method using the key referenced by ``keyLabel`` and return the clear data.

 

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown.

  

This method throws the following exceptions:

* KEncipherException

​            There was an error whilst decrypting the data    

* KEzSignConnectException

​            There was an error connecting to the server 

* KEzSignException

​            There was another error

 

Example:

 ```java
 byte[] originalData = “Hello”.getBytes();
 byte[] encryptedData = encryptData(“CHANNEL1”, originalData, “key1”);
 byte[] clearData = decryptData(“CHANNEL1”, encryptedData, “key1”);
 // clearData will be equal to originalData i.e. “Hello”
 ```

 

 

## Support



All questions, queries around the API described within this document should be directed to *Krestfield Support* at the following email address:

 support@krestfield.com



