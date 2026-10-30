---
layout: default
title: EzSign Properties
parent: EzSign
nav_order: 10
---

# EzSign Properties



The server’s configuration is contained within a properties file. The properties file must be passed to the server (as a parameter) at start up. The server loads the properties and waits for client requests  

Essentially the properties file contains information about the IP Addresses and Ports to listen on, the key store location, logging settings and channel configurations. These are contained in a single properties file. The description below breaks out the sections for easier reading

Click [here](ezsign_sample_properties.html) to view a sample properties file

<br>

## Server Properties

The following settings dictate what ports and interfaces the server listens on and other settings that are relevant to the running server, rather than individual channels

| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| server.bindIpAddress|The interface/IP Address the server will bind to. *If omitted the server will listen on all available interfaces*|10.100.15.32|
| server.port|The port the server will listen on|5656|
| server.allowedSourceIpAddresses|A comma separated list of IP Addresses (IPv4 or IPv6) which can connect to the server. *If omitted or empty any client can connect*|10.100.15.40,10.100.15.41|
| server.threadPoolSize|The pool size that will be created at start up and used to process requests.  *If omitted, defaults to 1*|5|
| server.waitTimeoutIfAllBusy|The maximum time to wait for a thread to become free.  If all instances in the thread pool are busy the server will wait this number of milliseconds before returning an error. *If omitted, defaults to 1000 (i.e. 1 second)*|1000|
| server.waitForMessageTimeout|The maximum time to wait for a message to be sent following connection. This should be increased if there are connection issues under load. *If omitted, defaults to 1000 (i.e. 1 second)*|1000|
| server.logMessages| If true, the received and sent messages are logged. These can contain the data being signed, encrypted or decrypted, so only set this to true when needed. *If omitted defaults to false (true before version 4.6.0)* |false|
| server.maxMessageSize|The longest message accepted from a client, in characters. Longer messages are refused with an error. Set to 0 for no limit. *If omitted defaults to 67108864 (about 48MB of data)* (from version 4.6.0)|67108864|
| server.socketapi.enabled|If false, the socket interface (used by the EzSign client) is not started, e.g. when only the REST API is used. At least one of the socket interface and the REST API must be enabled. *If omitted defaults to true* (from version 4.6.0)|true|
| server.useTls|If true, clients must connect to the socket interface over TLS. The server's TLS certificate and key are set with tls.clientKeyStore.filename, type and password. See [Configuring TLS](configuring_tls.html). *If omitted defaults to false*|false|
| server.useClientTls|If true (and server.useTls is true), clients must also present a TLS client certificate. Client certificates are checked against tls.trustStore.filename, which should hold only the CA(s) that issue client certificates. If no trust store is set, Java's default trust store (cacerts) is used and a warning is logged. *If omitted defaults to false*|false|
| server.tls.protocols|If server.useTls is true, the TLS protocols enabled. *If omitted the Java defaults are used* (from version 4.6.0)|TLSv1.3,TLSv1.2|
| server.ctrl.bindIpAddress|The interface/IP Address the *control* server will bind to. *If omitted the server will listen on all available interfaces*|127.0.0.1|
| server.ctrl.port|The port the control server will listen on|5657|
| server.ctrl.allowedSourceIpAddresses|A comma separated list of IP Addresses which can connect to the control server. *If omitted no client can connect*|10.100.15.40,10.100.15.41|
| server.ctrl.authCode|The passphrase used to encrypt messages sent to the control server, encrypted with the master password. Set this with the Management Tool. If set, the control client must use the same passphrase. *If omitted, control messages are sent in the clear*|yjjWoLfE...Zlew==|
| server.ctrl.logStatusMessages|By default the server will log every status request message sent to the control interface.  If regular monitoring is in place this can fill logs.  Set this value to false to switch off this logging. *Defaults to true*|true|
| server.failOnClasspathConflicts|When the server starts it checks that no class is in more than one jar in the lib folder with different contents (e.g. an out of date jar left behind after an upgrade), and logs an error for each one found. If true, the server also refuses to start. See [The lib folder and upgrades](ezsign_installation.html#the-lib-folder-and-upgrades). *If omitted defaults to false* (from version 4.6.0)|false|
| server.authCode|The passphrase used to encrypt messages between the client and server.  If set the client must pass the same string to the constructor.  If not set, messages will be sent in the clear (which may be OK if client and server are on the same machine or using a private network)|x55tHH#ih65W|
| keyStoreDir |The folder beneath which all channel key stores will be held|/opt/ezsign/STORE|
| log.level |The logging level.  The range is from 0 to 4 as follows: **0**: Logging is off, **1**: Only error messages will be logged, **2**: Errors and Warning messages will be logged, **3** : Errors, Warnings and Events will be logged, **4** : This is the debug level - all messages (as well as low level events) will be logged|4|
| tls.trustStore.filename |If using TLS to communicate with an HSM (such as the payShield) AND you are supplying a custom trust store (containing the trusted CA certificates), this specifies the full path to the trust store file. See [payShield TLS Configuration](payshield_tls_configuration.html) for more details|/opt/stores/payshield.jks|
| tls.trustStore.type |This specifies the trust store type referenced above. Options are **jks** or **pkcs12**|jks|
| tls.trustStore.password |The encrypted password that protects the trust store referenced above. Use the Management Utility to set this password|yjjWoLfE...Zlew==|
| tls.clientKeyStore.filename |If the server is using server-side TLS this is the full path to the keystore file containing the TLS certificate. See [Configuring TLS](configuring_tls.html) for more details. If using a client TLS certificate to authenticate to a payShield HSM, this is the full path to the keystore file containing the client-authentication certificate. See [payShield TLS Configuration](payshield_tls_configuration.html) for more details.|/opt/stores/client.jks|
| tls.clientKeyStore.type |This specifies the trust store type referenced above. Options are **jks** or **pkcs12**|pkcs12|
| tls.clientKeyStore.password |The encrypted password that protects the key store referenced above. Use the Management Utility to set this password|FGchg3Kv...Ycsg==|

<br>

## REST API Properties

From version 4.6.0 the server can also offer a REST API. These settings configure it. See [REST API](ezsign_rest_api.html) for details

| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| server.restapi.enabled|Enables the REST API. *If omitted defaults to false*|true|
| server.restapi.port|The port the REST API listens on. Required if the REST API is enabled|8443|
| server.restapi.bindIpAddress|The interface/IP Address the REST API will bind to. *If omitted the REST API will listen on all available interfaces*|10.100.15.32|
| server.restapi.allowedSourceIpAddresses|A comma separated list of IP Addresses (IPv4 or IPv6) which can connect to the REST API. *If omitted any client can connect*|10.100.15.40,10.100.15.41|
| server.restapi.threadPoolSize|The number of requests processed at once. *If omitted, server.threadPoolSize is used*|5|
| server.restapi.waitTimeoutIfAllBusy|The time in milliseconds to wait for a free instance before returning 503 (busy). *If omitted, server.waitTimeoutIfAllBusy is used*|1000|
| server.restapi.maxRequestSize|The largest request body accepted, in bytes. *If omitted defaults to 10485760 (10MB)*|10485760|
| server.restapi.usersFile|The users file, which holds the users that may call the REST API, their API tokens or certificates and their roles. Managed with the [Management Tool](ezsign_management_tool.html). Required if the REST API is enabled|/opt/ezsign/users.json|
| server.restapi.usersFile.signerCerts|A comma separated list of admin certificate files. If set, the users file must be signed by one of these certificates, so it cannot be changed without an admin's key. *If omitted the users file is not signed*|/opt/ezsign/admin1.pem,/opt/ezsign/admin2.pem|
| server.restapi.stateFile|Written by the server to record the trusted admin certificates, so a change to them between restarts is reported. *If omitted defaults to ezsign-rest-state.properties*|/opt/ezsign/ezsign-rest-state.properties|
| server.restapi.logRequests|If true, one line is logged per request (the user, operation, channel, result and time taken). Request bodies are never logged. *If omitted defaults to true*|true|
| server.restapi.useTls|If true, the REST API uses HTTPS. Only set this to false for testing. *If omitted defaults to true*|true|
| server.restapi.tls.keyStore.filename|The key store holding the REST API's TLS certificate and private key. Required if useTls is true|/opt/ezsign/rest-tls.p12|
| server.restapi.tls.keyStore.type|The key store type: **PKCS12** or **JKS**. *If omitted defaults to PKCS12*|PKCS12|
| server.restapi.tls.keyStore.password|The password for the key store, encrypted with the master password. Set this with the Management Tool|FGchg3Kv...Ycsg==|
| server.restapi.tls.trustStore.filename|A trust store holding only the CA(s) that issue client certificates. Client certificates are only checked against this trust store, never Java's cacerts file. *If omitted client certificates cannot be used*|/opt/ezsign/client-ca.p12|
| server.restapi.tls.trustStore.type|The trust store type: **PKCS12** or **JKS**. *If omitted defaults to PKCS12*|PKCS12|
| server.restapi.tls.trustStore.password|The password for the trust store, encrypted with the master password. Set this with the Management Tool|yjjWoLfE...Zlew==|
| server.restapi.tls.clientAuth|Whether clients present a TLS certificate: **none**, **optional** (a certificate or an API token can be used) or **required**. *If omitted defaults to optional if a trust store is set, otherwise none*|optional|
| server.restapi.tls.protocols|The TLS protocols enabled. *If omitted defaults to TLSv1.3,TLSv1.2*|TLSv1.3,TLSv1.2|

<br>

## Generic Channel Properties

The properties file may have multiple channels specified. Each channel must have a number assigned e.g.

```
channel.1.name=CHANNEL1
channel.1.type=PKI
...
channel.2.name=CHANNEL2
channel.2.type=SYM
...
channel.3.name=AnotherChannel
...
```

This number is represented by ``N`` in the following sections. There is no limit on the number of channels



| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| channel.N.name|The name of the channel.  This will also be used as the folder name where the keys and certificates for this channel will be stored|CHAN1|
| channel.N.type|The channel type: **PKI** or **SYM**. PKI channels can perform signature generation and verification SYM (symmetric) channels can perform encryption or decryption|PKI|
| channel.N.enabled|If false, the channel is disabled and will not be loaded.  If missing, defaults to **true**|true|
| channel.N.tokenType|The token type: **SOFTWARE**, **PKCS11**, **PAYSHIELD** (or **HSM9000**), **GOOGLEKMS**, **AZUREKEYVAULT**|SOFTWARE|
| channel.N.token.password|The token password required for all token types and will be used to encrypt key store objects. This must be set by running the ezsign-manange script. If tokenType=PKCS11 this is the PIN or Passphrase.  For nCipher devices this will be the operator smartcard passphrase|zijFhJ....vA==|
| channel.N.defaultKeyLabel|Relates to symmetric channels only (type=SYM). Specifies the default AES key label to use if none is passed to the client|key1|
| channel.N.saveObjectsToDisk |If this is true, files will not be written to the keystore folder. Use this option if you are passing properties to EzSign and managing key storage externally e.g. in a database|true|

<br>

## PKCS11 Token Properties

If  ``channel.N.tokenType=PKCS11`` is set then the following properties must also be configured. These are specific to the HSM being used and its configuration

| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| channel.N.token.useModuleProtection|If an HSM normally requires a password to logon (such as some PKCS#11 tokens).  This can be overridden by setting this value to **true**.  This means the HSM will not be logged on to and only the module’s keys will be used (rather than an operator card set etc)|false|
| channel.N.token.pkcs11.library|The full path to the PKCS11 library|/opt/nfast/toolkits/p11/ibcknfast.so|
| channel.N.token.pkcs11.slot|The PKCS11 slot number | 0 |
| channel.N.token.pkcs11.model | The particular HSM model. Options are:  **Generic**, **NCipher**, **Luna**, **AWSCloudHSM**, **Utimaco**, **YubiHSM**, **Custom** | Utimaco |
| channel.N.token.pkcs11.customTemplateClass | If the model above is **Custom**, then the class containing the customised templates must be specified here. See [here](https://krestfield.github.io/docs/ezsign/custom_pkcs11_templates.html) for more details.  Version 4.2.1 onwards | NewHsmTemplates |

<br>

## GoogleKMS Token Properties

If ``channel.N.tokenType=GOOGLEKMS`` is set then the following properties must also be configured. You will obtain these from your Google KMS configuration


| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| channel.N.token.googleKms.project|The ID of the project as created in the Google Cloud Console. For full details on the setup for Google KMS refer to the specific tech note|ezsign|
| channel.N.token.googleKms.location|The location of the key ring e.g. europe-west2|global|
| channel.N.token.googleKms.keyRing|The name of the key ring|ezsignkeys|
| channel.N.token.googleKms.credentialFile|The JSON file containing the private key associated with the service account with permissions to the KMS|/opt/google/googlekms.json|
| channel.N.token.googleKms.jsonCredentialString |The raw JSON text provided as a string (rather than a file as above). Note: supply one of jsonCredentialString or credentialFile. If both are provided credentialFile takes priority|{ "type": "service_account", "project_id": "pkcloud"....}|
| channel.N.token.googleKms.keyImportVersion|If using imported keys that are not at version 1 set this to the version of the keys you use to be imported|1|
| channel.N.token.googleKms.keyProtectionLevel |Can be HSM or SOFTWARE. Defines the protection level for keys at creation (e.g. when generating a CSR).|HSM|

<br>

## Azure KeyVault Token Properties

If ``channel.N.tokenType=AZUREKEYVAULT`` is set  then the following properties must also be configured. Refer to your Azure KeyVault configuration for details


| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| channel.N.token.azureKeyVault.clientId|The client ID as configured on the Azure platform|eb1739f5-6dd2-43b1-9bf7-266717a24cf4|
| channel.N.token.azureKeyVault.tenantId|The Tenant ID as configured on the Azure platform|d12c3e45-350c-4413-2bb3-34514a35407c|
| channel.N.token.azureKeyVault.keyVault|The full DNS name of the Key Vault e.g. https://yourvault.vault.azure.net/|https://yourvault.vault.azure.net/|

<br>

## PayShield Token Properties

If ``channel.N.tokenType=PAYSHIELD or HSM9000`` then the following properties must also be configured.

Note properties named hsm9000 (e.g. ``channel.N.token.hsm9000.port``) are still supported but all new properties will use the ``payShield`` name.

| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| channel.N.token.payShield.ipAddress |The IP Address of the PayShield|10.100.15.101|
| channel.N.token.payShield.ipAddress |The port the HSM9000 listens on. Required if tokenType=HSM9000|1500|
| channel.N.token.payShield.timeoutMs |The time to wait for a response from the HSM before failing. Required if tokenType=HSM9000|3000|
| channel.N.token.payShield.connectTimeoutMs |The time to wait for a connection to the HSM before failing.|5000|
| channel.N.token.payShield.headerLen |The HSM command header length. Required if tokenType=HSM9000|4|
| channel.N.token.payShield.useVariantLmk |If the HSM has a variant LMK installed, set this to true. If not specified, defaults to false (meaning a KeyBlock LMK will be used). Ensure this matches against the lmkId and port numbers (that usually map to specific LMKs)|false|
| channel.N.token.payShield.lmkId |If the HSM has multiple LMKs loaded, set this to the LMK ID  that you wish EzSign to use.  Range 0-99. If not specified, the default LMK (as configured on the HSM) will be used|0|
| channel.N.token.payShield.useTls |Whether communications between the client and HSM are protected using TLS. Options are **true** or **false**. If true then the **tls** server properties must also be set to configure the client key store (and optionally the trust store). See *Server Properties* above.|false|

**Note**: All settings except for **useTls** are still named **hsm9000** for versions **4.2.3** to **4.3.0.** E.g. ``channel.N.token.hsm9000.ipAddress``

<br>

## Signature Generation and Verification Properties

There are various options when generating and verifying signatures. The following settings also dictate what algorithms, key-sizes etc. that will be used when CSRs are generated

| Property                             | Description                                                  | Example      |
| ------------------------------------ | ------------------------------------------------------------ | ------------ |
| channel.N.signature.algorithm|The signature key algorithm.  Possible values are: **RSA**, **ECDSA**, **ML-DSA-44**, **ML-DSA-65** and **ML-DSA-87**. <br />If RSA is chosen the keysize must also be specified. <br />If elliptic curve (ECDSA) is chosen the curve must also be specified. See [here](ezsign-algorithms.html) for more details|RSA|
| channel.N.signature.keySize|The RSA key (modulus) size in bits (**1024**, **2048**, **4096**, **8192**, **16384**, **32768**)|2048|
| channel.N.signature.ecc.curve|The named curve e.g. **secp192r1**, **secp224r1**, **secp256r1**, **secp384r1**, **secp521r1** or any name supported by the version of java or HSM being used|secp256r1|
| channel.N.signature.hash|The hash that will be generated over the data to be signed before signing. Possible values: **SHA1**, **SHA256**, **SHA512**, **SHA3-224**, **SHA3-256**, **SHA3-384**, **SHA3-512**<br />Note: For ML-DSA algorithms no hash is required (data is not hashed)|SHA256|
| channel.N.signature.type|The signature type to generate.  Options are: **PKCS7**, **RAW**. If RAW is chosen the signature will be PKCS#1 formatted if RSA is chosen|PKCS7|
| channel.N.signature.includeCerts|What certificates to include in the signature.  Possible values: **ALL** – all certificates including the root will be included, **ALLEXCEPTROOT** – all certificates except the root will be included, **SIGNERONLY** – only the signer certificate will be included|ALLEXCEPTROOT|
| channel.N.signature.includeContent|Whether to include the content with the signature or not|false|
| channel.N.signature.includeSignedAttribs |If true signed attributes will be included in the signature including signing time, message digest and content type|true|
| channel.N.signature.keyId|The key which will be used to generate the signature. This can be set by running the ezsign-manange script|15723e16cd89401|
| channel.N.verify.pathCheckClass|To override the default path checker with a custom version, specify the path checker class here.  This must be in the classpath. If omitted the default path check class is used|org.pathcheck.PathChecker|
| channel.N.verify.signedAttribsRequired|If true and signed attributes are not included in a signature being verified the signature will be rejected|true|
| channel.N.verify.denyWeakSignatureHash|If true, signatures will be rejected if they have not been generated with a SHA-2 or SHA-3 hash|false|
| channel.N.verify.denyWeakCertificateHash|If true, certificates will be rejected if they have not been generated with a SHA-2 or SHA-3 hash|false|
| channel.N.verify.relaxRootCertExtensionChecks|If true, none of the usual certificate extension checks will be performed on the root certificate (including, key usage, basic constraints or key size). *Defaults to false*|false|
| channel.N.verify.relaxAllCertExtensionChecks|If true, none of the usual certificate extension checks will be performed including key usage criticality, basic constraints, key size, critical extensions, name constraints, extended key usage, the CA signer check and the CRL issuer's CRL sign key usage. *Defaults to false*|false|
| channel.N.verify.relaxCriticalExtensionChecks|If true, a certificate with a critical extension that EzSign does not process (e.g. policy constraints or a private extension) is accepted and a warning logged. If false the certificate is rejected, as RFC 5280 requires. The root certificate is not checked. *Defaults to false* (from version 4.6.0)|false|
| channel.N.verify.allowedCriticalExtensions|A comma separated list of OIDs of critical extensions to accept although EzSign does not process them, as a narrower alternative to relaxCriticalExtensionChecks. Listed extensions are not processed: their contents are still ignored, the certificate is just no longer rejected for carrying them. Listing an extension EzSign does process (e.g. key usage or name constraints) has no effect. See [Certificate Path Checking](ezsign_server.html#allowed-critical-extensions) (from version 4.6.0)|1.3.6.1.4.1.99999.1|
| channel.N.verify.relaxNameConstraints|If true, a certificate whose subject name, email address or subject alternative names break the name constraints of a CA above it is accepted and a warning logged. *Defaults to false* (from version 4.6.0)|false|
| channel.N.verify.relaxExtendedKeyUsageChecks|If true, a signer certificate whose extended key usage contains none of the allowedExtendedKeyUsages (e.g. a TLS server certificate) is accepted and a warning logged. A signer certificate without the extended key usage extension is always accepted. *Defaults to false* (from version 4.6.0)|false|
| channel.N.verify.allowedExtendedKeyUsages|A comma separated list of extended key usage OIDs that permit signing. If the signer certificate has the extended key usage extension it must contain one of these. This **replaces** the default list rather than adding to it, so to add a purpose list the defaults as well. The defaults are: any extended key usage (2.5.29.37.0), email protection (1.3.6.1.5.5.7.3.4), code signing (1.3.6.1.5.5.7.3.3), document signing (1.3.6.1.5.5.7.3.36), Microsoft document signing (1.3.6.1.4.1.311.10.3.12) and Adobe authentic documents trust (1.2.840.113583.1.1.5). See [Certificate Path Checking](ezsign_server.html#allowed-extended-key-usages) (from version 4.6.0)|1.3.6.1.5.5.7.3.4,1.3.6.1.5.5.7.3.2|
| channel.N.verify.relaxCaSignerCheck|If true, a CA certificate (basic constraints CA is true) is accepted as the signer certificate and a warning logged. A self-signed signer certificate is always accepted. *Defaults to false* (from version 4.6.0)|false|
| channel.N.verify.nonRepudiationRequired|If true, a signer certificate must have the non-repudiation key usage set. *Defaults to true*|true|
| channel.N.verify.caBasicConstraintsRequired|If true, a CA certificate must have basic constraints CA extension. *Defaults to true*|true|
| channel.N.verify.minKeySize|Sets the minimum permitted key size for all certificates in the chain. *Defaults to 1024*|2048|
| channel.N.verify.maxKeySize|Sets the maximum permitted key size for all certificates in the chain. *Defaults to 8192*|8192|
| channel.N.allowExpiredCerts|Whether to permit expired certificates.  This MUST only be set to true in extreme circumstances (such as to maintain a live service) where other checks can be performed that ensure the certificate would otherwise still be valid|false|
| channel.N.allowExpiredCertsForDays|If allow ExpiredCerts=true then the number of days permitted to all an expired certificate for e.g. if set to 5 a certificate will be permitted for 5 days after it has expired|5|

<br>

## Revocation Checker Properties

The revocation check options are configured with the following settings. If nothing is specified, no revocation checking will be performed

| Property                     | Description                                                  | Example      |
| ---------------------------- | ------------------------------------------------------------ | ------------ |
| channel.N.revocationChecker.type|The revocation checker type. Possible values: **NONE** - No revocation checking will be performed. **CRL** - CRLs will be used to check revocation. **OCSP** - OCSP will be used to check revocation. **ANY** - OCSP will be tried first.  If this fails (e.g. if there is no OCSP URL or if the server or status is unavailable) then CRL will be attempted|OCSP|

If **NONE** is chosen as the revocation checker, no further settings are required  

If **CRL** is chosen, refer to the CRL Specific Properties below  

If **OCSP** is chosen, refer to the OCSP Specific Properties below  

If **ANY** is chosen, both the CRL and OCSP specific properties will be applied

<br>

### OCSP Specific Properties

if ``revocationChecker.type=OCSP`` then the following settings can be applied

| Property                     | Description                                                  | Example      |
| ---------------------------- | ------------------------------------------------------------ | ------------ |
| channel.N.revocationChecker.ocsp.connectTimeoutSecs|If revocationChecker.type=OCSP then this determines the OCSP Server connection timeout.  *Defaults to 5 seconds*|5|
| channel.N.revocationChecker.ocsp.readTimeoutSecs|If revocationChecker.type=OCSP then this determines the OCSP Server read timeout.  *Defaults to 5 seconds*|5|
| channel.N.revocationChecker.ocsp.useDefaultUrl|If revocationChecker.type=OCSP then this determines whether the default URL (which must be specified) will always be used or, if false, the certificate's AIA extensions will be used to extract the OCSP URL|true|
| channel.N.revocationChecker.ocsp.defaultUrl|If useDefaultUrl is true the default URL must be specified in this property|https://ocsp.server.com|
| channel.N.revocationChecker.ocsp.signRequest|If true, the OCSP request will also be signed|true|
| channel.N.revocationChecker.ocsp.signingKeyId|if signRequest=true. The signing key used to sign the OCSP requests. This is set to the same key as the signature signing key|15723e16cd89401|
| channel.N.revocationChecker.ocsp.signatureHash|The hash used in the OCSP request signature generation.  Used when signRequest=true.  Possible values: **SHA1**, **SHA224**, **SHA256**, **SHA384**, **SHA512**|SHA256|
| channel.N.revocationChecker.ocsp.checkOcspSigningCertUsage|Whether to check the key usage on the certificate used to sign the OCSP response.  If true, the certificate's extended key usage will be checked for the ocsp-signing attribute|false|
| channel.N.revocationChecker.ocsp.maxProducedAtAgeMins|Revocation checking will fail if the time the OCSP was generated (indicated in the producedAt field) is more than this number of  minutes in the past i.e. this is the maximum lifetime allowed  for an OCSP response. *If omitted this will not be checked*|4|
| channel.N.revocationChecker.ocsp.maxAgeWithoutNextUpdateMins|An OCSP response without a nextUpdate time is only accepted for this number of minutes after its thisUpdate time, so an old response cannot be replayed. Set to 0 to accept these responses whatever their age. *Defaults to 60* (from version 4.6.0)|60|
| channel.N.revocationChecker.ocsp.includeNonce|If true, a random nonce is sent with each OCSP request and the response must contain the same nonce, so an old response cannot be replayed. Only set this if the OCSP responder supports nonces. *Defaults to false* (from version 4.6.0)|false|
| channel.N.revocationChecker.ocsp.onlyCheckEndEntity|If this is true, only the end-entity certificate will be checked for revocation i.e. none of the other certificates in the path (nor any OCSP signing certificates) will be checked|false|
| channel.N.revocationChecker.ocsp.relaxSigningPath|RFC 6960 requires that the issuer of the certificate being checked sign the OCSP request or this is performed by a certificate that it has issued.  If the response is signed by another trusted certificate (e.g. a root CA issued certificate – as is often the case for IdenTrust responders), set this option to true|false|
| channel.N.revocationChecker.ocsp.ignoreSSLErrors|If true, when sending an OCSP request, if SSL/TLS  is used and the SSL certificate is not specifically trusted, setting this to true will still permit the connection. From version 4.6.0 this only applies to this channel's OCSP requests|false|
| channel.N.revocationChecker.ocsp.enableCache|Enable or disable OCSP response caching. *Default is false*|true|
| channel.N.revocationChecker.ocsp.cacheSeconds|If enableCache is true, this is the maximum time to cache an OCSP response  in seconds. *Default is 120*|60|
| channel.N.revocationChecker.ocsp.cacheCaCertsOnly|If true, only OCSP responses for CA certs will be cached i.e. end entities will always be checked. *Default is true*|true|
| channel.N.revocationChecker.ocsp.useProxy|Whether to send OCSP requests via a proxy. If true the other proxy settings are required|true|
| channel.N.revocationChecker.ocsp.proxyServer|If useProxy=true, this specifies the proxy server address|proxyserver|
| channel.N.revocationChecker.ocsp.proxyPort|If useProxy=true, this specifies the proxy server port|8080|
| channel.N.revocationChecker.ocsp.proxyAuthRequired|If useProxy=true and the server requires authentication set this to true and specify the username and password below|false|
| channel.N.revocationChecker.ocsp.proxyUsername|If proxyAuthRequired=true set the *username* here|user1|
| channel.N.revocationChecker.ocsp.proxyPassword|If proxyAuthRequired=true set the *password* here|password|

<br>

### CRL Specific Properties

if ``revocationChecker.type=CRL`` then the following settings can be applied

| Property                     | Description                                                  | Example      |
| ---------------------------- | ------------------------------------------------------------ | ------------ |
| channel.N.revocationChecker.crl.downloadFolder|The location to which CRL files will be downloaded and stored|/opt/ezsign/crl|
| channel.N.revocationChecker.crl.forceDownload|Whether to force the download of the CRL for each request.|false|
| channel.N.revocationChecker.crl.allowExpiredCrl|Whether to allow expired CRLs or not Note: This MUST only be used in extreme circumstances e.g. a live service outage  as a revoked certificate may be accepted|false|
| channel.N.revocationChecker.crl.allowExpiredCrlForDays|If allowExpiredCrl=true then the number of days expiry that will be permitted|1|
| channel.N.revocationChecker.crl.relaxCrlSignCheck|If true, a CRL is accepted when its issuer certificate does not have the CRL sign key usage, and a warning logged. Also relaxed when channel.N.verify.relaxAllCertExtensionChecks is true. *Defaults to false* (from version 4.6.0)|false|
| channel.N.revocationChecker.crl.onlyCheckEndEntity|If this is true, only the end-entity certificate will be checked for revocation i.e. none of the other certificates in the path will be checked|false|
| channel.N.revocationChecker.crl.ignoreSSLErrors|If true, when downloading a CRL, if SSL/TLS  is used and the SSL certificate is not specifically trusted, setting this to true will still permit the connection. From version 4.6.0 this only applies to this channel's CRL downloads|true|
| channel.N.revocationChecker.crl.connectTimeoutSecs|The timeout for connecting to the server a CRL is downloaded from. *Defaults to 5 seconds* (from version 4.6.0)|5|
| channel.N.revocationChecker.crl.readTimeoutSecs|The timeout for reading a CRL being downloaded. *Defaults to 30 seconds* (from version 4.6.0)|30|
| channel.N.revocationChecker.crl.useProxy|Whether to download CRLs via a proxy. If true the other proxy settings are required|false|
| channel.N.revocationChecker.crl.proxyServer|If useProxy=true, this specifies the proxy server address|proxyserver|
| channel.N.revocationChecker.crl.proxyPort|If useProxy=true, this specifies the proxy server port|8080|
| channel.N.revocationChecker.crl.proxyAuthRequired|If useProxy=true and the server requires authentication set this to true and specify the username and password below|true|
| channel.N.revocationChecker.crl.proxyUsername|If proxyAuthRequired=true set the *username* here|user2|
| channel.N.revocationChecker.crl.proxyPassword|If proxyAuthRequired=true set the *password* here|password1|