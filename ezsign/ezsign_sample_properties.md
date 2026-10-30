---
layout: default
title: EzSign Sample Properties
parent: EzSign
nav_order: 11
---

# EzSign Sample Server Properties

The simplest configuration you could get started with is as follows:

```properties
server.ctrl.port=6656
server.port=5656
keyStoreDir=/home/user/ezsign/keystores
channel.1.name=CHANNEL1
channel.1.tokenType=SOFTWARE
```

(Setting the values to those required)

Before the server could run with these properties you would first need to configure the passwords. To do this you run the ``ezsign-manage`` script and choose option **1. Set Passwords**

This will result in the properties file being updated as follows:

```properties
server.ctrl.port=6656
server.port=5656
keyStoreDir=/home/user/ezsign/keystores
channel.1.name=CHANNEL1
channel.1.tokenType=SOFTWARE
channel.1.token.password=sfN93wyVBNDNjIk/vKfjnMZotMjVDL4t+mQDMTV1eWyXBx6gopW0/Q==
```

I.e. the encrypted password has been added

At this point the server can be started. Although, to be of any real use you would need import your certificates and generate CSR's for any signing certificates etc.



Further details of the available properties can be found in the sample below. For more details on each of the options, refer to the guide [here](ezsign_properties.html)


```properties
###############################################################################
# Server Control 
# These settings define how the server will listen to control messages
# such as pause server, restart server, get server status etc.
###############################################################################

# The IP Address that the control listener will bind to
server.ctrl.bindIpAddress=127.0.0.1

# A comma seperated list of IP addresses that the control server
# will permit to send control messages
# Set this to local host (127.0.0.1) to ensure that only the same server can
# send control messages
server.ctrl.allowedSourceIpAddresses=127.0.0.1,192.168.1.78

# The port the control server will listen on
server.ctrl.port=5657

###############################################################################
# Server
# These settings define how the server listens to API messages sent from
# the client
# The client must send messages to the port and IP address defined here
###############################################################################

# The port the server will listen on
# Ensure this is not the same as the control server above
server.port=5656

# The IP Address that the server listener will bind to
# If this is commented out/missing the server will bind to all interfaces
#server.bindIpAddress=127.0.0.1

# A comma seperated list of IP addresses that the server
# will permit to send messages
# Set this to local host (127.0.0.1) to ensure that only the same server can
# send messages
# If omitted any client can send messages
#server.allowedSourceIpAddresses=127.0.0.1,192.168.1.78

# The pool size that will be created at start up and used to process requests
# If omitted, defaults to 1
server.threadPoolSize=5

# The maximum time (milliseconds) to wait for a thread to become free
# If all instances in the thread pool are busy the server will wait this 
# number of milliseconds before returning an error
server.waitTimeoutIfAllBusy=1000

# The maximum time (milliseconds) to wait for a message to be received following
# connection
# Increase if there are issues connecting under load
server.waitForMessageTimeout=1000

# Whether to log all received and returned messages
# If encrypting sensitive data, set this to false to prevent cleartext being
# sent to the log file
# Defaults to false (true before version 4.6.0)
server.logMessages=false

# The longest message accepted from a client, in characters. Longer
# messages are refused with an error. 0 means no limit
# Defaults to 67108864 (about 48MB of data)
server.maxMessageSize=67108864

# The passphrase used to encrypt messages between the client and server,
# encrypted with the master password. Set this with the Management Tool
# If omitted messages are sent in the clear
#server.authCode=

# The passphrase used to encrypt messages sent to the control server,
# encrypted with the master password. Set this with the Management Tool
#server.ctrl.authCode=

# Whether the socket interface (used by the EzSign client) is started
# Set to false if only the REST API is used. Defaults to true
server.socketapi.enabled=true

# Whether clients must connect over TLS. If true, the server's TLS
# certificate is set with tls.clientKeyStore.filename, type and password
# Defaults to false
server.useTls=false

# If server.useTls is true, whether clients must also present a TLS client
# certificate. These are checked against tls.trustStore.filename
# Defaults to false
server.useClientTls=false

# If server.useTls is true, the TLS protocols enabled
# If omitted the Java defaults are used
#server.tls.protocols=TLSv1.3,TLSv1.2

###############################################################################
# REST API
# From version 4.6.0 the server can also offer a REST API
###############################################################################

# Enables the REST API. Defaults to false
server.restapi.enabled=false

# The port the REST API listens on
server.restapi.port=8443

# The IP Address the REST API binds to. If omitted, all interfaces
#server.restapi.bindIpAddress=127.0.0.1

# A comma separated list of IP addresses permitted to connect
# If omitted any client can connect
#server.restapi.allowedSourceIpAddresses=127.0.0.1

# The number of requests processed at once and the time (milliseconds) to
# wait for a free instance before returning 503 (busy)
# If omitted server.threadPoolSize and server.waitTimeoutIfAllBusy are used
#server.restapi.threadPoolSize=5
#server.restapi.waitTimeoutIfAllBusy=1000

# The largest request body in bytes. Defaults to 10485760
server.restapi.maxRequestSize=10485760

# The users file holding the users, their API tokens or certificates and
# their roles. Managed with the Management Tool
server.restapi.usersFile=/var/ezsign/users.json

# If set, the users file must be signed by one of these admin certificates
#server.restapi.usersFile.signerCerts=/var/ezsign/admin1.pem,/var/ezsign/admin2.pem

# Written by the server to record the trusted admin certificates
# Defaults to ezsign-rest-state.properties
#server.restapi.stateFile=/var/ezsign/ezsign-rest-state.properties

# Log one line per request. Request bodies are never logged. Defaults to true
server.restapi.logRequests=true

# Use HTTPS. Only set to false for testing. Defaults to true
server.restapi.useTls=true

# The REST API's TLS certificate and key. The password is encrypted with
# the master password using the Management Tool
server.restapi.tls.keyStore.filename=/var/ezsign/rest-tls.p12
server.restapi.tls.keyStore.type=PKCS12
server.restapi.tls.keyStore.password=FGchg3Kv...Ycsg==

# Only the CA(s) that issue client certificates
#server.restapi.tls.trustStore.filename=/var/ezsign/client-ca.p12
#server.restapi.tls.trustStore.type=PKCS12
#server.restapi.tls.trustStore.password=

# none, optional or required. Defaults to optional with a trust store,
# otherwise none
#server.restapi.tls.clientAuth=optional

# The TLS protocols enabled. Defaults to TLSv1.3,TLSv1.2
#server.restapi.tls.protocols=TLSv1.3,TLSv1.2


###############################################################################
# Key Store Location
# This is where all of the keys and certificates (either encrypted files
# or references to objects residing on HSMs) will be stored
# A folder per channel is created beneath this location e.g.
# if keyStoreDir=/var/keystore and you configure channel1 and channel2
# folders /var/keystore/channel1 and /var/keystore/channel2 will 
# be created
###############################################################################
keyStoreDir=/var/KEYSTORE

###############################################################################
# Logging settings
# Note: Changes to log filenames, rollover frequency and size etc. can be
# made by editing the log4J2.xml file located in the EzSignServer/logconf
# directory
###############################################################################
# Set the logging level.  The range is from 0 to 4 as follows:
# 0 : Logging is off
# 1 : Only error messages will be logged
# 2 : Errors and Warning messages will be logged
# 3 : Errors, Warnings and Events will be logged
# 4 : This is the debug level - all messages as well as low level events will be logged
log.level=3

###############################################################################
# Channel settings
# Channels are configured here
# The format shall be:
#   channel.1.property1
#   channel.1.property2
#   ...
#   channel.2.property1
#   channel.2.property2
#   etc.
###############################################################################

# The channel name.  Do not include spaces in the name
# A folder will be created beneath keyStoreDir with this name
channel.1.name=CHANNEL1

# Whether the channel is enabled or disabled
# If disabled it will not be loaded and cannot be used
channel.1.enabled=true

# The channel type - can be PKI or SYM
# PKI channels can sign and verify, SYM channels can encrypt and decrypt
channel.1.type=PKI

# If the channel is type=SYM the default key label can be specified here
# If no channel name is passed
channel.1.defaultKeyLabel=test1

# The token type - can be SOFTWARE, PKCS11, HSM9000 or GOOGLEKMS
# If PKCS11 the pkcs11.library and pkcs11.slot settings must also be specified
# If HSM9000 the hsm9000.port, hsm9000.ipAddress, hsm9000.timeoutMs 
# and hsm9000.headerLen settings must also be specified
channel.1.tokenType=SOFTWARE

# If tokenType=PKCS11 the following properties must be set 
# The path to the PKCS#11 library:
channel.1.token.pkcs11.library=/opt/nfast/toolkits/cknfast-64.dll
# The slot number:
channel.1.token.pkcs11.slot=1

# If tokenType=GOOGLEKMS the following properties must be set 
# The ID of the project as created in Google Cloud
channel.1.token.googleKms.project=ezsign
# The location of the key ring
channel.1.token.googleKms.location=europe-west2
# The name of the key ring
channel.1.token.googleKms.keyRing=ezsign
# if importing keys under a version other than 1, set the version to import
channel.1.token.googleKms.keyImportVersion=2

# If tokenType=HSM9000 the following properties must be set 
# The HSM IP Address:
channel.1.token.hsm9000.ipAddress=10.0.1.101
# The HSM listening port:
channel.1.token.hsm9000.port=1500
# The timeout to use when connecting to the HSM:
channel.1.token.hsm9000.timeoutMs=10000
# The command header length:
channel.1.token.hsm9000.headerLen=4
# Whether to use a Variant or KeyBlock LMK:
channel.1.token.hsm9000.useVariantLmk=true
# The ID of the LMK to use:
channel.1.token.hsm9000.lmkId=1

# The token password required for all token types
# This must be set by running the ezsign-manange script
# If tokenType=SOFTWARE this is used to encrypt the keys and certificates only
# If tokenType=PKCS11 this is the PIN or Passphrase, for nCipher devices this will be
# the operator smartcard passphrase
# If tokenType=HSM9000 this is used to re-encrypt the keys and certificates
channel.1.token.password=zijFhJ+BMAO8B3bYw9XD0AZlOYt4eYACY4zW9UXtZk2EC7hl+dgevA==

# The signature key algorithm
# RSA – RSA algorithm
# ECDSA – Elliptic Curve Digital Signature Algorithm
channel.1.signature.algorithm=RSA

# The signature key size (if algorithm ia RSA)
channel.1.signature.keySize=2048

# The signature key named curve (if algorithm ia ECDSA)
channel.1.signature.curve=secp256r1

# The hash that will be used to sign the data
# SHA1, SHA256, SHA512, SHA3-256 etc
channel.1.signature.hash=SHA256

# What certificates to include in the produced signature
# ALL - All certificates including the root
# SIGNERONLY - Only the signer certificate
# ALLEXCEPTROOT - All certificates in the path except the root
channel.1.signature.includeCerts=ALL

# If true, signed attributes containing signing time, content type
# and message digest will be included in the signature
channel.1.signature.includeSignedAttributes=true

# Whether to include the content within the signature or not
channel.1.signature.includeContent=false

# The key which will be used to generate the signature
# This can be set by running the ezsign-manange script
channel.1.signature.keyId=15723e16cd89401

# To override the default path checker with a custom version, specify the
# path checker class here.  This must be in the classpath
channel.1.verify.pathCheckClass=com.myorg.ezsign.pathcheck.MyCustomPathChecker

# If true, the signature being verified must include signed attributes
# otherwise it will be rejected
channel.1.verify.signedAttribsRequired=true

# If true, the signature being verified must have been generated with 
# a strong hash or be rejected 
# i.e. SHA-2 range and above i.e. MD5 and SHA-1 will be rejected
channel.1.verify.denyWeakSignatureHash=false

# If true, the certificates being verified must have been generated with 
# a strong hash or be rejected 
# i.e. SHA-2 range and above i.e. MD5 and SHA-1 will be rejected
channel.1.verify.denyWeakCertificateHash=false

# If true, none of the usual certificate extension checks will be 
# performed on the root certificate (including, key usage, basic 
# constraints or key size)
# Defaults to false
channel.1.verify.relaxRootCertExtensionChecks=false

# If true, none of the usual certificate extension checks will be 
# performed including, key usage, basic constraints, key size,
# critical extensions, name constraints, extended key usage, the
# CA signer check and the CRL issuer's CRL sign key usage
# Defaults to false
channel.1.verify.relaxAllCertExtensionChecks=false

# The following relax one check each. When a relaxed check would
# have failed, a warning is logged. All default to false

# Accept critical extensions that are not processed (e.g. policy
# constraints). Or list the OIDs to accept in allowedCriticalExtensions.
# Listed extensions are still not processed, the certificate is just
# no longer rejected for carrying them
channel.1.verify.relaxCriticalExtensionChecks=false
#channel.1.verify.allowedCriticalExtensions=

# Accept names that break a CA's name constraints
channel.1.verify.relaxNameConstraints=false

# Accept a signer whose extended key usage does not permit signing.
# allowedExtendedKeyUsages replaces the default list of OIDs (shown
# below), so to add a purpose, keep the defaults and append it
channel.1.verify.relaxExtendedKeyUsageChecks=false
#channel.1.verify.allowedExtendedKeyUsages=2.5.29.37.0,1.3.6.1.5.5.7.3.4,1.3.6.1.5.5.7.3.3,1.3.6.1.5.5.7.3.36,1.3.6.1.4.1.311.10.3.12,1.2.840.113583.1.1.5

# Accept a CA certificate as the signer
channel.1.verify.relaxCaSignerCheck=false

# If true, a signer certificate must have the non-repudiation
# key usage set
# Defaults to true
channel.1.verify.nonRepudiationRequired=true

# If true, a CA certificate must have basic constraints CA extension
# Defaults to true
channel.1.verify.caBasicConstraintsRequired=true

# Sets the minimum permitted key size for all certificates in the chain
# Defaults to 1024
channel.1.verify.minKeySize=2048

# Sets the maximum permitted key size for all certificates in the chain
# Defaults to 8192
channel.1.verify.maxKeySize=8192

# Whether to permit expired certificates
# This MUST only be set to true in extreme circumstances (such as to 
# maintain a live service) where other checks can be performed that
# ensure the certificate would otherwise still be valid
channel.1.allowExpiredCerts=true

# If allow ExpiredCerts=true then the number of days permitted
# to all an expired certificate for e.g. if set to 5 a certificate 
# will be permitted for 5 days after it has expired
channel.1.allowExpiredCertsForDays=5

# The revocation checker type
# This can be:
# NONE - No revocation checking will be performed
# CRL - CRLs will be used to check revocation
# OCSP - OCSP will be used to check revocation
channel.1.revocationChecker.type=OCSP

# If revocationChecker.type=OCSP then this determines whether the 
# default URL (which must be specified) will always be used or, 
# if false, the certificate's AIA extensions will be used to extract
# the OCSP URL
channel.1.revocationChecker.ocsp.useDefaultUrl=true

# If useDefaultUrl is true the default URL must be specified here
channel.1.revocationChecker.ocsp.defaultUrl=https://ocsp.server.co.uk

# If true, the OCSP request will also be signed with the signing
# key specified
channel.1.revocationChecker.ocsp.signRequest=true

# The signing key used to sign the OCSP requests if signReques=true
# This can be set by running the ezsign-manange script
channel.1.revocationChecker.ocsp.signingKeyId=1557ca2b4ba3283

# The hash used in the OCSP request signature generation
# Used when signRequest=true.  Can be SHA1, SHA256, SHA512 etc
channel.1.revocationChecker.ocsp.signatureHash=SHA1

# Whether to check the key usage on the certificate used to sign the
# OCSP response.
# If true, the certificate's extended key usage will be checked for the 
# ocsp-signing attribute
channel.1.revocationChecker.ocsp.checkOcspSigningCertUsage=true

# Revocation checking will fail if the time the OCSP was generated 
# (indicated in the producedAt field) is more than this number of 
# minutes in the past i.e. this is the maximum lifetime allowed
# for an OCSP response
# If ommitted this will not be checked
channel.1.revocationChecker.ocsp.maxProducedAtAgeMins=4

# An OCSP response without a nextUpdate time is only accepted for this
# number of minutes after its thisUpdate time. 0 accepts any age
# Defaults to 60
channel.1.revocationChecker.ocsp.maxAgeWithoutNextUpdateMins=60

# If true, a random nonce is sent with each OCSP request and the response
# must contain it. Only set if the OCSP responder supports nonces
# Defaults to false
channel.1.revocationChecker.ocsp.includeNonce=false

# The OCSP server connection and read timeouts in seconds
# Default to 5
channel.1.revocationChecker.ocsp.connectTimeoutSecs=5
channel.1.revocationChecker.ocsp.readTimeoutSecs=5

# If true, only the end-entity certificate is checked for revocation
channel.1.revocationChecker.ocsp.onlyCheckEndEntity=false

# If true, a response signed by another trusted certificate (rather than
# the issuer or a certificate it issued, as RFC 6960 requires) is accepted
channel.1.revocationChecker.ocsp.relaxSigningPath=false

# If true, when sending an OCSP request, if SSL/TLS
# is used and the SSL certificate is not specifically trusted, setting
# this to true will still permit the connection
channel.1.revocationChecker.ocsp.ignoreSSLErrors=true

# Enable or disable OCSP response caching
# Default is false
channel.1.revocationChecker.ocsp.enableCache=true

# If enableCache is true, this is the maximum time to cache an OCSP response
# in seconds
# Default is 120
channel.1.revocationChecker.ocsp.cacheSeconds=120

# If true, only OCSP responses for CA certs will be cached 
# i.e. end entities will always be checked
# Default is true
channel.1.revocationChecker.ocsp.cacheCaCertsOnly=true

# Whether to send OCSP requests via a proxy
# If true the other proxy settings are required
channel.1.revocationChecker.ocsp.useProxy=true

# If useProxy=true, this specifies the proxy server address
channel.1.revocationChecker.ocsp.proxyServer=10.0.0.12

# If useProxy=true, this specifies the proxy server port
channel.1.revocationChecker.ocsp.proxyPort=8080

# If useProxy=true and the server requires authentication set this to true
# and specify the username and password below
channel.1.revocationChecker.ocsp.proxyAuthRequired=true

# If proxyAuthRequired=true set the username here
channel.1.revocationChecker.ocsp.proxyUsername=user1

# If proxyAuthRequired=true set the password here
channel.1.revocationChecker.ocsp.proxyPassword=password

# If revocationChecker.type=CRL then the following properties are required
# The location to which CRL files will be downloaded and stored:
channel.1.revocationChecker.crl.downloadFolder=/opt/crl

# Whether to force the download of the CRL for each request:
channel.1.revocationChecker.crl.forceDownload=false

# Whether to allow expired CRLs or not
# Note: This MUST only be used in extreme circumstances e.g. a live service outage
# as a revoked certificate may be accepted
channel.1.revocationChecker.crl.allowExpiredCrl=false

# If allowExpiredCrl=true then the number of days expiry that will be permitted
channel.1.revocationChecker.crl.allowExpiredCrlForDays=5

# If true, a CRL is accepted when its issuer certificate does not have the
# CRL sign key usage (a warning is logged). Defaults to false
channel.1.revocationChecker.crl.relaxCrlSignCheck=false

# If true, only the end-entity certificate is checked for revocation
channel.1.revocationChecker.crl.onlyCheckEndEntity=false

# The timeouts for connecting to the server and reading a CRL, in seconds
# Default to 5 and 30
channel.1.revocationChecker.crl.connectTimeoutSecs=5
channel.1.revocationChecker.crl.readTimeoutSecs=30

# If true, when downloading a CRL, if SSL/TLS
# is used and the SSL certificate is not specifically trusted, setting
# this to true will still permit the connection
channel.1.revocationChecker.crl.ignoreSSLErrors=true

# Whether to send CRL download requests via a proxy
# If true the other proxy settings are required
channel.1.revocationChecker.crl.useProxy=true

# If useProxy=true, this specifies the proxy server address
channel.1.revocationChecker.crl.proxyServer=10.0.0.12

# If useProxy=true, this specifies the proxy server port
channel.1.revocationChecker.crl.proxyPort=8080

# If useProxy=true and the server requires authentication set this to true
# and specify the username and password below
channel.1.revocationChecker.crl.proxyAuthRequired=true

# If proxyAuthRequired=true set the username here
channel.1.revocationChecker.crl.proxyUsername=user1

# If proxyAuthRequired=true set the password here
channel.1.revocationChecker.crl.proxyPassword=password
```

