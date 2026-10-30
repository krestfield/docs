---
layout: default
title: EzSign - Server
parent: EzSign
nav_order: 4
---
# EzSign Server

<br>

The EzSign Server is a multi-channel, digital signature and encryption processing application capable of interfacing with Hardware Security Modules for secure signature generation and validation or encryption/decryption operations

The Server supports several different key stores including a software key store (useful for non-production or systems that do not require a high level of security) and hardware key stores

Hardware key stores support any HSM (Hardware Security Module) which exposes the industry standard PKCS#11 interface (including the nCipher range of HSMs).  It also supports several cloud based HSMs and the Thales PayShield HSMs

The Server makes use of a properties file for its configuration.  Certain operations such as the setting of passwords, generation of CSRs (Certificate Signing Requests) and importing of issued certificates are carried out via the Management utility

<br>

### Channels

A single Server can be configured with multiple channels.  A channel contains only the keys and certificates which were generated or imported for that particular channel.  Therefore a channel provides key separation such that different applications can access only the keys and certificates of interest to them
A channel also supports its own token

Each channel can utilise a different key store and different configuration options.  For example, one channel can make use of a PayShield and be configured to perform OCSP revocation checking whilst another channel can be configured for an nCipher HSM and not perform any revocation checking

There are two types of channel

* **PKI**: Performs digital signature generation and verification
* **Symmetric**: Provides encryption an decryption operations

<br>

### Key Store Files

Whichever key store is used the server stores information locally about each key and certificate held by, or protected by the key store

The server will store these files in a folder which has the same name as the channel.  This folder will be located beneath the key store directory (specified by the keyStoreDir property)

For example, if keyStoreDir is set to ``/opt/ezsign/keystore`` and a channel is configured called ``ChannelOne``, then the keys and certificates associated with ChannelOne will be stored here:

```
/opt/ezsign/keystore/ChannelOne
```

These files are encrypted by the server and may contain encrypted key information (in the case of a software key store).  If an HSM is used, either references to keys will be stored (identifiers or labels) or key data that is encrypted by the HSM’s itself (as in the case of the PayShield HSMs)

Access to these files should be controlled such that only the server is able to access them as although they are encrypted, accidental deletion or corruption may prevent the server from operating correctly

The account used to run the server must have read/write permissions to the keystore location

<br>

### Logging

Logging is performed via Apache Log4J2.  See http://logging.apache.org/log4j/2.x/

By default, logs are written to: 

```
EzSignServer/logs/ezsign.log 
```

Logs are rolled over once they reach 100mb.  At which point they are zipped and stored in a folder (a separate folder is created per month) e.g. 

```
EzSignServer/logs/2026-01/ezsign-2026-01-21-1.log.gz
```

Thus saving log files automatically whilst preserving space

Log4J is highly configurable and these options can easily be altered by editing the configuration file located here:

```
EzSignServer/logconf/log4j2.xml
```

If an alternative location for the configuration file is required, update the LOGCONFIG property in the ezsign-daemon-start script to point to the new location e.g.

```
LOGCONFIG=/opt/ezsign/server1/log4j2.xml
```

Refer to the Apache documentation for more information on the configuration options

<br>

### The Thread Pool

When the server starts it creates a pool of channels.  Each channel loads its keys and certificates and creates a connection to the HSM (if required)

The size of the pool is configured via the threadPoolSize property and defaults to 1 if omitted.  Larger sizes will allow for greater parallelism but may result in slower start up times.  Some degree of experimentation with a particular setup may be required to find the optimum value.  Usually, a good starting point is to set this value to the number of clients (or client threads) expected to connect to the server at any one time

As each request arrives the next available free channel instance processes the request.  If no free instance is available the server will wait a short time and then check again whether any instances have become free.  It will do this until the waitTimeoutIfAllBusy value has been reached at which point an error will be returned to the client.  This prevents hanging if, for example external OCSP servers were running particularly slowly.  The client may choose to try again if this does occur


Properties Configuration
The server’s configuration is contained within a properties file.   The properties file must be passed to the server (as a parameter) at start up.  The server will then load the properties and then wait for client requests

Essentially the properties file contains information about the IP Addresses and Ports to listen on, the key store location, logging settings and channel configurations

For detailed information about the available properties, refer to the following:

[EzSign Properties](ezsign_properties.html)

A sample properties file can be found here:

[EzSign Sample Properties](ezsign_sample_properties.html)

<br>

### Certificate Path Checking

During signature verification, EzSign will perform the following operations:

1.	Verify the signature data against the signer certificates’ public key
2.	Build a certificate path
3.	Perform path checks
4.	Check certificate revocation

**Step 1** performs the mathematical calculations over the signature data I.e. digesting the data, decryption and digest comparisons

**Step 2** builds a path, using the certificates from the signature and certificates that may have been uploaded into the channel.  A trusted root must have been imported into the channel for this step to succeed as the path must terminate on a trusted root

Each certificate is checked for time validity (the Valid From date is before the current time and the Valid To date after) and its signature is verified against the issuing certificates public key

**Step 3** then performs the following checks:

1. If the setting ``channel.N.verify.denyWeakCertificateHash`` is *true*, any certificate in the path with a weak hash (anything weaker than SHA-2) is rejected

2. If the setting ``channel.N.verify.relaxAllCertExtensionChecks`` is *true*, none of the checks below are performed. If it is false (or not set), the following checks are performed:

   * **Key size** - each certificate's key size must be within ``channel.N.verify.minKeySize`` and ``channel.N.verify.maxKeySize``
   * **Signer key usage** - the signer certificate must have the *keyUsage* extension, marked critical, with *Digital Signature* set. If ``channel.N.verify.nonRepudiationRequired`` is *true* (the default), *Non Repudiation* must also be set
   * **CA key usage** - CA and root certificates must have the *keyUsage* extension with *Key Cert Sign* set
   * **CA basic constraints** - if ``channel.N.verify.caBasicConstraintsRequired`` is *true* (the default), CA and root certificates must have the *Basic Constraints* extension, marked critical, with CA set, and the path length it allows is checked

   From version 4.6.0 these checks are also performed:

   * **Critical extensions** - a certificate (other than the root) must not have a critical extension that EzSign does not process, such as policy constraints or a private extension, as RFC 5280 requires
   * **Name constraints** - the subject name, email addresses and subject alternative names of each certificate must meet the name constraints of the CA certificates above it
   * **Extended key usage** - if the signer certificate has the extended key usage extension, it must contain a purpose that permits signing (by default any extended key usage, email protection, code signing or document signing). A signer certificate without the extension is not restricted
   * **CA signer** - the signer certificate must not be a CA certificate, unless it is self-signed

   If the setting ``channel.N.verify.relaxRootCertExtensionChecks`` is *true*, none of these checks are carried out on the root certificate. This may be required if legacy root certificates are being used

From version 4.6.0, when CRLs are checked (Step 4), the certificate that issued the CRL must also have the *CRL Sign* key usage

Each of the checks added in version 4.6.0 can be relaxed on its own, without turning off all the checks with ``relaxAllCertExtensionChecks``. When a relaxed check would have failed, the certificate is accepted and a warning is logged, so the logs show what has been accepted. When a check fails, the error names the setting that would allow it

| Check | Setting to relax it | Narrower alternative |
| --- | --- | --- |
| Critical extensions | ``channel.N.verify.relaxCriticalExtensionChecks=true`` | List the extension OIDs to accept in ``channel.N.verify.allowedCriticalExtensions`` |
| Name constraints | ``channel.N.verify.relaxNameConstraints=true`` | |
| Extended key usage | ``channel.N.verify.relaxExtendedKeyUsageChecks=true`` | Set the purposes (OIDs) that permit signing in ``channel.N.verify.allowedExtendedKeyUsages``. This replaces the default list |
| CA signer | ``channel.N.verify.relaxCaSignerCheck=true`` | |
| CRL issuer's CRL Sign key usage | ``channel.N.revocationChecker.crl.relaxCrlSignCheck=true`` | Also relaxed by ``relaxAllCertExtensionChecks`` |

#### Allowed critical extensions

``channel.N.verify.allowedCriticalExtensions`` does not make EzSign process an extension. EzSign still ignores its contents; it only stops rejecting the certificate because the extension is marked critical. Listing an OID states that the certificate is known to carry this extension and it is safe to ignore

A critical extension is treated as follows:

| Extension | What EzSign does |
| --- | --- |
| One that EzSign processes: key usage, basic constraints, extended key usage, name constraints, subject or issuer alternative name | Always checked. Listing it in ``allowedCriticalExtensions`` has no effect |
| Not processed, but listed in ``allowedCriticalExtensions`` | The certificate is accepted (no warning is logged). The extension's contents are ignored |
| Not processed and not listed | The certificate is rejected, or if ``relaxCriticalExtensionChecks=true``, accepted with a warning |

The list cannot switch off a check EzSign performs. For example, to relax name constraints use ``relaxNameConstraints``; listing the name constraints OID does nothing

For example, if a CA issues signing certificates with a private policy extension ``1.3.6.1.4.1.12345.1`` marked critical, these are rejected by default. Setting:

```
channel.1.verify.allowedCriticalExtensions=1.3.6.1.4.1.12345.1
```

accepts them, while any other unknown critical extension is still rejected. This is narrower than ``relaxCriticalExtensionChecks=true``, which accepts every unknown critical extension, including ones that have not been seen before

#### Allowed extended key usages

``channel.N.verify.allowedExtendedKeyUsages`` is not about criticality. The extended key usage extension is always processed on the signer certificate, whether or not it is marked critical:

* If the signer certificate does not have the extended key usage extension, it is accepted and the list is not used
* If it has the extension, at least one of its purposes must be in the list, otherwise the certificate is rejected (or if ``relaxExtendedKeyUsageChecks=true``, accepted with a warning)

The default list is: any extended key usage (2.5.29.37.0), email protection (1.3.6.1.5.5.7.3.4), code signing (1.3.6.1.5.5.7.3.3), document signing (1.3.6.1.5.5.7.3.36), Microsoft document signing (1.3.6.1.4.1.311.10.3.12) and Adobe authentic documents trust (1.2.840.113583.1.1.5)

Setting ``allowedExtendedKeyUsages`` **replaces** the default list, it does not add to it. For example, a signer certificate with the purposes client authentication and server authentication is rejected by default. To also accept client authentication certificates, list the defaults plus client authentication (1.3.6.1.5.5.7.3.2):

```
channel.1.verify.allowedExtendedKeyUsages=2.5.29.37.0,1.3.6.1.5.5.7.3.4,1.3.6.1.5.5.7.3.3,1.3.6.1.5.5.7.3.36,1.3.6.1.4.1.311.10.3.12,1.2.840.113583.1.1.5,1.3.6.1.5.5.7.3.2
```

The certificate is then accepted because client authentication is in the list. With ``relaxExtendedKeyUsageChecks=true`` it would also be accepted, but with a warning, as would a certificate with any other purpose

All the checks performed in Step 3 may be overridden by developing a custom path check class (see below)

#### The risks of relaxing these checks

These checks follow RFC 5280. Relaxing them may be needed where certificates were not issued to the standard, but the decision and its risks are then the customer's:

* **Critical extensions** - the CA marked the extension critical because the certificate must not be used by software that does not understand it. Accepting it ignores whatever restriction it carries
* **Name constraints** - a CA restricted to certain names (e.g. one organisation's domain) could issue certificates for any name and they would be accepted
* **Extended key usage** - certificates issued for another purpose, such as TLS server or client certificates, would be accepted as signers. The private keys of such certificates are often held with weaker protection
* **CA signer** - a CA key that signs documents is used for more than issuing certificates, and a signature cannot be told apart from a CA operation
* **CRL sign** - a CRL signed by a key not authorised for it would be trusted, so revocation information could be wrong

Where possible, prefer the narrowest setting, e.g. list the one extension in ``allowedCriticalExtensions`` or the one extra purpose in ``allowedExtendedKeyUsages`` rather than relaxing the whole check

<br>

### Custom Certificate Path Checking

Specific checks may be performed on certificate paths by developing a custom java class.  You may develop the custom class yourself following the details below, or Krestfield can develop one to your specific requirements.  Custom path checking may be required, if for example you wish to check a certificate has been registered, check custom extensions or any other specific certificate checks your system may require
To create a custom path checker perform the following operations:

1. Create a Java project and add a reference to the ``ezsign-x.y.z.jar`` (located in the``EzSignServer/lib`` directory of the installation)

2. Create a new class (e.g. ``MyCustomPathChecker``) which implements the ``KPathCheckBase`` interface e.g.

```java
package com.myorg.ezsign.pathcheck;

import com.krestfield.ezsign.KEzSignException;
import com.krestfield.ezsign.KPathException;
import com.krestfield.ezsign.log.KSigLog;
import com.krestfield.ezsign.path.KPathCheckBase;

public class MyCustomPathChecker implements KPathCheckBase
{
	public void loadProperties(int channelNum, Properties props) throws KEzSignException
    {
        KSigLog.LogEvent("Loading properties from CustomPathCheck.loadProperties");

        // Load any specific properties required
    }
    
    public void check(ArrayList<X509Certificate> certPath) throws KPathException
    {
        // Perform custom checks on the path
        throw new KPathException("MyCustomPathChecker – Not yet implemented");
    }
}
```

3. Implement the loadProperties and check methods (see below), add the compiled class to the server classpath and reference this class in the server properties as follows:

```
channel.N.verify.pathCheckClass=com.myorg.ezsign.pathcheck.MyCustomPathChecker
```

Note: If a custom path checker is implemented, the default checks will not be performed.  If you require any of the custom checks to be implemented, Krestfield can supply source code snippets to assist with this

<br>

<u>Implement the loadProperties Method</u>

This method is passed the channel number and the properties object – which is the loaded server properties

Therefore, you may add any specific properties into an existing server properties file.  These can then be read in this method

E.g. You could add in the following specific properties for channel 1:

```
channel.1.mypathchecker.allowedExtensions=2.5.29.19,2.5.29.31,1.2.840.114021.1.4.2
channel.1.mypathchecker.validityTimeDays=30
```

Or you could have server wide settings such as:

```
mypathchecker.allowedExtensions=2.5.29.19,2.5.29.31,1.2.840.114021.1.4.2
mypathchecker.validityTimeDays=30
```

If there is a failure to load any properties, throw an KEzSignException

<br>

<u>Implement the check Method</u>

All certificates in the path are included in the ArrayList, index 0 is always the end-entity (signer) certificate, other certificates are CA certificates and the last certificate in the list will be the root
Perform the required checks on these certificates and throw a ``KPathException`` if there are any failures or rejections

<br>

### Start Scripts
The server is started by calling the ``ezsign-daemon-start`` script located in the ``EzSignServer/bin`` directory.  This starts the server managing process (the daemon) and also starts the server listening on the interface and port configured

The script must be passed the properties file and the master password.  The master password may be passed as an additional parameter e.g.

```
ezsign-daemon-start.sh server.properties masterpassword
```

Or if the master password is held within a file, the filename may be passed after the -f switch e.g.

```
ezsign-daemon-start.sh server.properties -f masterpassfile.txt
```

Finally, the master password may be set within the environment variable ``EZMASTERPASS``, in which case no password parameter is required e.g.

```
ezsign-daemon-start.sh server.properties
```

Once the daemon has started the status can be monitored via the EzSign Control utility (see below).  The listening server can be stopped and started by running the following scripts

```
ezsign-server-stop
ezsign-server-start
```

These scripts do not halt the daemon process but stop and start the server listening process which will either prevent or permit further requests from the client being processed

To stop the main daemon process run the following script

```
ezsign-daemon-stop
```

<br>

### Overriding Properties

The following properties can be overridden by system properties

- keyStoreDir

- server.port

- server.bindIpAddress

- server.threadPoolSize

- server.allowedSourceIpAddresses

- server.waitTimeoutIfAllBusy

- log.level

- server.ctrl.port

- server.ctrl.bindIpAddress

- server.ctrl.allowedSourceIpAddresses

  

If included as –D parameters at server start up, they will override any settings configured within the properties file

For example. The ``ezsign-daemon-start.sh`` script could be updated as follows:

```
java -Dserver.port=1234 -Dserver.bindIpAddress=127.0.0.1 -cp $CLASSPATH com.krestfield.ezsign.server.EzSignServer $1 $2
```

(where ``server.port`` and ``server.bindIpAddress`` have been added)

This would result in the server.port being set to 1234 and the bindIpAddress to 127.0.0.1 whatever values the properties file held

These fields could be configured as parameters which would allow for the dynamic setting of these values.  For example: 

```
java -Dserver.port=$PORT -cp $CLASSPATH com.krestfield.ezsign.server.EzSignServer $1 $2
```

Or if you intended to pass these as parameters to the start script, such as:

```
ezsign-daemon-start.sh [port] [properties file] [password]
```

e.g.

```
ezsign-daemon-start.sh 5006 server.properties mypassword
```

You could update the start script as follows:

```
java -Dserver.port=$1 -cp $CLASSPATH com.krestfield.ezsign.server.EzSignServer $2 $3
```

This functionality allows for the dynamic control of the server which may be of use to automate multi-instance deployments

<br>

### Passwords

The EzSign server requires two passwords:  A Token Password and a Master Password.  The Token Password is used to either encrypt software keys or to authenticate to HSMs and is stored in the properties file, encrypted.  The Master Password is not stored but is used to derive a key under which the Token Passwords are encrypted

Token Passwords are per channel and each channel can be configured with a different Token Password

The Master password is per server.  The same Master Password must be provided each time a Token Password is configured or the server started

When the server is started the Master Password must be provided.  This password is then used to decrypt the Token Passwords stored in the properties file.  If the Master Password provided is incorrect, the server cannot start

If using the Start Script (e.g. ezsign-daemon-start.sh) the master password can be provided in one of three ways:

As clear text e.g. the server could be started as follows:

```
ezsign-daemon-start.sh server.properties masterpassword
```

Where masterpassword is the master password

Or the master password can be stored within a file, and the filename them passed to the start script.  If this option is chosen then the -f switch must be specified before the filename e.g.

```
ezsign-daemon-start.sh server.properties -f masterpassfile.txt
```

Where``masterpassfile.txt`` is the file containing the master password

Finally, the master password may be set within the environment variable ``EZMASTERPASS``, in which case no password parameter is required when calling the start script e.g.

```
ezsign-daemon-start.sh server.properties
```

On UNIX/Linux the master password could be set as follows:

```
export EZMASTERPASS=masterpassword
```

Note: If no password is passed in this way and the ``EZMASTERPASS`` variable is not available you will be prompted to enter a password before the server will start

If automating start-up you may wish to add further protection around the master password. For example, on a Microsoft OS, the server could be started by a PowerShell script or Scheduled Task that run under a specific windows account. This account could then store the master password in the Windows Credential Manager and either set as an environment variable or pass to the script when starting

On Linux/UNIX systems the master password could be stored in a file. The account starting the server could then be configured to be the only account with read access to this file
