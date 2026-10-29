---
layout: default
title: EzSign - Client Integration Guide
parent: EzSign
nav_order: 11
---

# Client Integration Guide

 

## Introduction

 

The Krestfield EzSign Client is a lightweight java package which interfaces with the EzSign Server enabling applications to quickly generate and verify digital signatures or encrypt and decrypt data without the need for complex programming.                                                                             

The client can communicate with the server using either the socket API (the default) or, from client version 4.6.0, the server's REST API. The calls made by an application are the same for both, so an application can switch between them by changing only how the client is created.

This guide details the steps required to integrate the client into applications and make use of the API.

For server side setup please refer to the *EzSign Installation and Configuration Guide*.

 

 <br/>

## JAR File

 

The client is packaged within the following JAR file:

* ``ezsign-client-x.y.z.jar``

(Where x.y.z is the version number e.g. 4.6.0)

Version 4.6.0 or later is required to use the REST API. The client requires Java 8 or later and has no other dependencies

 

This is located at ``[installation folder]/EzSignClient/lib``

Where ``[installation folder]`` is the location the server was installed

 

To make use of the signing, verification and encryption functions, add the ``ezsign-client-x.y.z.jar`` to your application’s class path.  

Alternatively, you can add the following maven dependency: 

```xml
<dependency>
 <groupId>com.krestfield.ezsign</groupId>
 <artifactId>ezsign-client</artifactId>
 <version>x.y.z</version>
</dependency>
```



  

 <br/>

## Client API



 The API to the EzSign client has intentionally been kept simple. Decisions on which keys to use, what certificates to include in signatures and what hashing algorithms to use are configured at the server level.  

 All the client API calls are included in the ``EzSignClient`` class, which is included in the ``com.krestfield.ezsign.client`` package.

A client can be created once and shared by the application's threads. With the socket API, requests are sent to the server one at a time per client. With the REST API, requests from different threads are sent at the same time  

  <br/>

### Constructor

The simplest constructor is defined as:

```java
public EzSignClient(String host, int port)
```



Where:

* ``host`` is the server hostname (or IP Address)

* ``port`` is the server listening port number

 

These constructors create a client that uses the socket API. To use the REST API, see [Using the REST API](#using-the-rest-api) below.

The default connection and read timeouts are 5 seconds (5000 milliseconds). But these can be overridden by using the following constructor: 

```java
public EzSignClient(String host, int port, int timeoutInMs, int readTimeoutInMs)
```

 

Where:

* ``timeoutInMs`` is the connection timeout expressed in milliseconds 

* ``readTimeoutInMs`` is the read timeout expressed in milliseconds

 

Example: 

```java
import com.krestfield.ezsign.client.EzSignClient;
 
public class ClientTest
{
   	public static void main(String[] args)
	{
		EzSignClient client = new EzSignClient(“10.100.12.15”, 5656);
	}
}
```



To encrypt communications between the client and server, you may utilise TLS and/or an Authentication code.  

<br/>

<u>Using TLS</u>

(Note: for information on configuring TLS at both the server and client, see the [Configuring TLS Guide](configuring_tls.html))

EzSign supports server side TLS as well as client-server TLS.  

If the server has been configured with a server side TLS certificate (and the ``server.useTls`` has been set to ``true``) or the server is sitting behind a load-balancer that terminates TLS sessions for example, the ``EzSignClient`` constructor must also have the ``useTls()`` option set, for example:

```java
EzSignClient client = new EzSignClient(“10.100.12.15”, 5656).useTls();
```

The client will now connect to the server over TLS.



If you wish to use client-server TLS, the client must make use of a client-side TLS certificate to authenticate to the server. The client must be created with the ``useClientTls()`` option. This also turns on TLS, so ``useTls()`` is optional when ``useClientTls()`` is used. 

``useClientTls`` requires three parameters:

* ``clientKeystoreFilename`` - The Keystore Filename
  * This is the full path to the keystore file
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

The client will now attempt to connect to the server using TLS and will now also provide the client authentication certificate supplied in the specified keystore file.

<br/>

<u>Trusting the Server's Certificate</u>

By default, the server's TLS certificate must be issued by a CA trusted by the Java instance running the application (i.e. in its ``cacerts`` file, or the trust store set with the ``javax.net.ssl.trustStore`` system property).

Alternatively, from version 4.6.0, the CA certificates to trust can be provided with the ``useTrustStore()`` option, which takes the same three parameters as ``useClientTls()`` (the trust store filename, password and type). For example:

```java
EzSignClient client = new EzSignClient(
    "ezsign.server1.local", 5656)
    .useTls()
    .useTrustStore("/opt/keystores/truststore.p12", "password", "PKCS12");
```

Note that ``useTrustStore()`` does not turn on TLS for the socket API. ``useTls()`` (or ``useClientTls()``) is still required

<br/>

<u>Host Name Checking</u>

From version 4.6.0, the client checks that the server's TLS certificate is valid for the host name (or IP Address) the client connects to. I.e. the certificate must include a Subject Alternative Name (SAN) for that DNS name or IP Address, as described in the [Configuring TLS Guide](configuring_tls.html). If it does not, the connection fails with a ``KEzSignConnectException``

If the client connects using an IP Address which is not included in the certificate, either add the IP Address to the certificate (recommended) or turn off the check with the ``verifyHostname(false)`` option:

```java
EzSignClient client = new EzSignClient(
    "10.100.12.15", 5656)
    .useTls()
    .verifyHostname(false);
```

TLS 1.2 and TLS 1.3 are supported

<br/>

<u>Using an Authentication Code</u>

If the communications between the client and server are to be secured, an Authentication Code may be used. The Authentication Code is provided by using one of the following constructors:

  

```java
public EzSignClient(String host, int port, String authCode)
```

 

```java
public EzSignClient(String host, int port, int timeoutInMs, int readTimeoutInMs, String authCode)
```

 

This will result in the encryption of the traffic between the client and server

There are no restrictions on what Authentication Code can be used, but a longer more complex code will increase security 

The same Authentication Code must also be configured on the server. Refer to the Installation and Configuration Guide for details on how to configure this on the server.

If the Authentication Code does not match the server's, the server closes the connection without responding and a ``KEzSignConnectException`` is thrown, stating the server closed the connection without responding

 <br/>

### Using the REST API

From version 4.6.0 the client can use the server's REST API instead of the socket API. The REST API must be enabled on the server, and a REST API user must be created for the application using the [Management Tool](ezsign_management_tool.html). The user must be granted the operations and channels the application uses.

The client is created in the same way, with the REST API port (``server.restapi.port``) and the ``useRestApi()`` option, together with the way the client authenticates: an API token or a TLS client certificate.

An Authentication Code is not used with the REST API, so the constructors that take an Authentication Code must not be used.

<br/>

<u>Authenticating with an API Token</u>

The ``useApiToken()`` option provides the API token issued when the REST API user was created:

```java
EzSignClient client = new EzSignClient(
    "ezsign.server1.local", 8443)
    .useRestApi()
    .useApiToken(apiToken);
```

The API token should be protected in the same way as a password e.g. read from a file which only the application can access, rather than being included in the code

<br/>

<u>Authenticating with a Client Certificate</u>

The ``useClientTls()`` option provides the keystore holding the client certificate, as described in *Using TLS* above. The certificate must be one the REST API user has been configured with:

```java
EzSignClient client = new EzSignClient(
    "ezsign.server1.local", 8443)
    .useRestApi()
    .useClientTls("/opt/keystores/client.p12", "password", "PKCS12");
```

<br/>

<u>Trusting the Server's Certificate</u>

The REST API always uses TLS (unless turned off at the server, see below). The server's certificate is trusted and checked in the same way as for the socket API, see *Trusting the Server's Certificate* and *Host Name Checking* above. For example, with a trust store:

```java
EzSignClient client = new EzSignClient(
    "ezsign.server1.local", 8443)
    .useRestApi()
    .useApiToken(apiToken)
    .useTrustStore("/opt/keystores/truststore.p12", "password", "PKCS12");
```

If the server's REST API has TLS turned off (``server.restapi.useTls=false``), use ``useRestApi(false)``. An API token is then required, and is sent unencrypted, so this is only suitable when the client and server are on the same machine

<br/>

<u>Errors</u>

All methods throw the same exceptions as with the socket API. For example, if a signature does not verify, ``KVerificationException`` is thrown, whichever API is used.

If the API token or client certificate is not recognised, the user is not permitted the operation or channel, or the server is busy, a ``KEzSignException`` is thrown. The message includes the HTTP status, the error code and the server's transaction ID, which can be used to locate the request in the server log. For example:

```
Not permitted. User app1 does not have the sign permission on channel CHANNEL1 (HTTP 403, FORBIDDEN, transaction ID 4963794784449164)
```

 <br/>

### Switching Between the Socket and REST APIs

An application that uses the socket API can move to the REST API by:

1. Using version 4.6.0 or later of the client JAR
2. Changing the port to the server's REST API port
3. Adding the ``useRestApi()`` option and either ``useApiToken()`` or ``useClientTls()``
4. Removing the Authentication Code, as this is not used with the REST API

No other changes are required: all the method calls remain the same. For example:

```java
// Socket API
EzSignClient client = new EzSignClient("ezsign.server1.local", 5656, authCode);

// REST API
EzSignClient client = new EzSignClient("ezsign.server1.local", 8443)
    .useRestApi()
    .useApiToken(apiToken);
```

To revert to the socket API, reverse these changes.

If settings for the two APIs are mixed, for example an Authentication Code with the REST API or an API token with the socket API, a ``KEzSignException`` is thrown explaining the problem.

To make the switch without changing code at all, the client can be created from a properties file, as described below

 <br/>

### Creating the Client from a Properties File

From version 4.6.0, the client can be created from a properties file:

```java
EzSignClient client = EzSignClient.fromProperties("/opt/myapp/ezsign-client.properties");
```

Or from a ``java.util.Properties`` object with ``EzSignClient.fromProperties(properties)``

For example, to use the socket API:

```
ezsign.api=socket
ezsign.host=ezsign.server1.local
ezsign.port=5656
ezsign.authCodeFile=/opt/myapp/authcode.txt
```

To use the REST API:

```
ezsign.api=rest
ezsign.host=ezsign.server1.local
ezsign.port=8443
ezsign.apiTokenFile=/opt/myapp/apitoken.txt
ezsign.trustStore=/opt/keystores/truststore.p12
ezsign.trustStorePasswordFile=/opt/myapp/truststore-password.txt
```

The following properties can be set:

| Property | Description |
|---|---|
| ``ezsign.api`` | ``socket`` (the default) or ``rest`` |
| ``ezsign.host`` | The server hostname (or IP Address). Required |
| ``ezsign.port`` | The socket or REST API port number. Required |
| ``ezsign.connectTimeoutMs`` | The connection timeout in milliseconds |
| ``ezsign.readTimeoutMs`` | The read timeout in milliseconds |
| ``ezsign.tls`` | For the socket API, ``true`` to use TLS (default ``false``). For the REST API, ``false`` if TLS has been turned off at the server (default ``true``) |
| ``ezsign.authCode`` | The Authentication Code (socket API only) |
| ``ezsign.apiToken`` | The API token (REST API only) |
| ``ezsign.clientKeyStore`` | The keystore holding the client certificate |
| ``ezsign.clientKeyStorePassword`` | The client keystore password |
| ``ezsign.clientKeyStoreType`` | ``PKCS12`` (the default) or ``JKS`` |
| ``ezsign.trustStore`` | The trust store holding the CA certificates to trust |
| ``ezsign.trustStorePassword`` | The trust store password |
| ``ezsign.trustStoreType`` | ``PKCS12`` (the default) or ``JKS`` |
| ``ezsign.verifyHostname`` | ``false`` to turn off host name checking (default ``true``) |

The secret values (``authCode``, ``apiToken``, ``clientKeyStorePassword`` and ``trustStorePassword``) can instead be read from a file by adding ``File`` to the property name, as in the examples above. The first line of the file is used. This keeps secrets out of the properties file

If a property is missing or invalid, a ``KEzSignException`` is thrown when the client is created

 <br/>

### Generate Signature Methods

The following method is called to generate a signature:

``` java
public byte[] signData(String channelName, byte[] dataToSign, boolean isDigest) 
```

 The signature returned is dependent on the signature type specified at the server and will be either a PKCS#7 formatted signature or a raw signature.

 

Note: For large data sets, it is recommended to hash the data beforehand and provide the hash as the ``dataToSign`` together with ``isDigest``=``true``. This prevents large amounts of data being passed between the client/server interface. 

 This method throws the following exceptions: 

* ``KSigningException``
  * There was an error during the signing process 


* ``KEzSignException``
  * There was an internal error, incorrect parameters or other error 


* ``KEzSignConnectException``
  * There was an error connecting to the server 




Example:

 ```java
 byte[] dataToSign = "Hello".getBytes();
 byte[] signature = client.signData(“CHANNEL1”, dataToSign, false);
 ```

 <br/>

### Verify PKCS#7 Signature Methods



The following methods are used to verify a PKCS#7 signature and will perform the required path building and revocation checking as configured at the server.

 

<u>Verifying Signature 1</u>

 ```java
 public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, 
                             boolean dataIsDigest)
 ```

 If ``contentBytes`` is a hash of the data then ``dataIsDigest`` must be ``true``, otherwise ``false``

 

 This method throws the following exceptions:

* ``KVerificationException``
  * There was an error during the verification process 


* ``KPathException``
  * There was a path building error 


* ``KRevocationException``
  * A certificate is revoked or there was an error during the revocation check process 


* ``KEzSignConnectException``
  * There was an error connecting to the server  


* ``KEzSignException``
  * There was another error




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
public void verifySignature(String channelName, byte[] signature, byte[] contentBytes, 
                            boolean dataIsDigest, boolean bypassRevocationCheck, boolean bypassPathBuild)
```

 If the values for ``bypassRevocationCheck`` and ``bypassPathBuild`` are both set to ``false`` the signature will be verified in the same way as the previous method.

 

This method throws the following exceptions:

* ``KVerificationException``
  * There was an error during the verification process


* ``KPathException``
  * There was a path building error


* ``KRevocationException``
  * A certificate is revoked or there was an error during the revocation check process


* ``KEzSignConnectException``
  * There was an error connecting to the server  


* ``KEzSignException``
  * There was another error


<br/>

### Verify Raw Signature Methods



The following methods are used to verify Raw (for RSA these are PKCS#1 formatted) signatures and will perform the required path building and revocation checking as configured at the server.

  

<u>Verifying Raw Signature 1</u>

Note that as a raw signature does not contain the signer certificate, this must be provided 

 

If there are other certificates in the path that are not stored in the channel, use the *Verify Raw Signature 2* method below.  Path building and revocation checking (if configured at the server) will be performed.

 ```java
 public void verifyRawSignature(String channelName, byte[] signature, byte[] contentBytes,
                             boolean dataIsDigest, X509Certificate signerCert)
 ```



This method throws the following exceptions:

* ``KVerificationException``
  * There was an error during the verification process


* ``KPathException``
  * There was a path building error


* ``KRevocationException``
  * A certificate is revoked or there was an error during the revocation check process


* ``KEzSignConnectException``
  * There was an error connecting to the server 


* ``KEzSignException``
  * There was another error




<u>Verifying Raw Signature 2</u>

This method accepts the signer certificate *as well as* other certificates in the path. Path building and revocation checking (if configured at the server) will be performed.

 ```java
 public void verifyRawSignature(String channelName, byte[] signature, byte[] contentBytes, 
                             boolean dataIsDigest, X509Certificate signerCert, 
                             X509Certificate[] otherCerts)
 ```

 

This method throws the following exceptions:

* ``KVerificationException``
  * There was an error during the verification process


* ``KPathException``
  * There was a path building error


* ``KRevocationException``
  * A certificate is revoked or there was an error during the revocation check process


* ``KEzSignConnectException``
  * There was an error connecting to the server 


* ``KEzSignException``
  * There was another error






<u>Verifying Raw Signature 3</u>

Use this method if you wish to bypass revocation checking (whether configured at the server or not) and/or path building. 

``` java
public void verifyRawSignature(String channelName, byte[] signature, byte[] contentBytes, 
                            boolean dataIsDigest, X509Certificate signerCert, 
                            X509Certificate[] otherCerts, boolean bypassRevocationCheck, 
                            boolean bypassPathBuild)
```

 

This method throws the following exceptions:

* ``KVerificationException``
  * There was an error during the verification process


* ``KPathException``
  * There was a path building error


* ``KRevocationException``
  * A certificate is revoked or there was an error during the revocation check process


* ``KEzSignConnectException``
  * There was an error connecting to the server  


* ``KEzSignException``
  * There was another error




Note:

``otherCerts`` can be null if you do not wish to specify any other certificates in the path

If you wish to perform just the signature verification operation. Set ``bypassRevocationCheck`` and ``bypassPathBuild`` both to ``true`` and ``otherCerts`` to ``null``

 <br/>

### Generate Random Number Methods

 

The following method is called to generate random data:

 ```java
 public byte[] generateRandomBytes(String channelName, int numBytes)
 ```

The number of random bytes specified will be returned. ``numBytes`` must be 1 or more

 

This method throws the following exceptions:

* ``KEzSignConnectException``
  * There was an error connecting to the server 

* ``KEzSignException``
  * There was another error

  <br/>

### Encrypt/Decrypt Methods



These methods provide encryption and decryption using AES keys previously generated on the server.   

The algorithm used is AES with CBC (Cipher Block Chaining) and PKCS#5 padding. A random IV (Initialisation Vector) is created every time data is encrypted and this IV is placed in the first 16 bytes of the returned data, with the remaining bytes being the encrypted data itself.

The following method is called to encrypt data:

 ```java
 public byte[] encryptData(String channelName, byte[] dataToEncrypt, String keyLabel)
 ```

This will encrypt the clear data contained in ``dataToEncrypt`` using the key referenced by ``keyLabel`` and return the encrypted data.

 

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown.

 

This method throws the following exceptions:

* ``KEncipherException``
  * There was an error whilst encrypting the data     


* ``KEzSignConnectException``
  * There was an error connecting to the server 


* ``KEzSignException``
  * There was another error




The following method is called to decrypt previously encrypted data:

 ```java
 public byte[] decryptData(String channelName, byte[] encryptedData, String keyLabel)
 ```

This will decrypt data previously encrypted with the ``encryptData`` method using the key referenced by ``keyLabel`` and return the clear data.

 

``keyLabel`` must refer to a key which has previously been generated on the server using the management utility. If the key does not exist ``KEncipherException`` will be thrown.

  

This method throws the following exceptions:

* ``KEncipherException``
  * There was an error whilst decrypting the data    


* ``KEzSignConnectException``
  * There was an error connecting to the server 


* ``KEzSignException``
  * There was another error




Example:

 ```java
 byte[] originalData = “Hello”.getBytes();
 byte[] encryptedData = client.encryptData(“CHANNEL1”, originalData, “key1”);
 byte[] clearData = client.decryptData(“CHANNEL1”, encryptedData, “key1”);
 // clearData will be equal to originalData i.e. “Hello”
 ```

 <br/>

## Upgrading to Version 4.6.0

Existing applications do not need to change to use version 4.6.0 with the socket API. However, note the following changes in behaviour:

* When TLS is used, the server's certificate must be valid for the host name or IP Address used to connect. See *Host Name Checking* above
* TLS 1.2 or TLS 1.3 is required
* ``useTrustStore()`` no longer turns on TLS by itself. Add ``useTls()`` if it was relied on
* Methods no longer return ``null``. If the server returns an unexpected response, a ``KEzSignException`` is thrown. A result with no data is returned as an empty array
* Channel names and key labels containing the ``~`` character or line breaks are rejected with a ``KEzSignException``, as these would corrupt the request sent to the server

 <br/>

## Support



All questions, queries around the API described within this document should be directed to *Krestfield Support* at the following email address:

 support@krestfield.com



