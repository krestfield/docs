---
layout: default
title: EzSign - payShield 10k Support
parent: EzSign
nav_order: 50
---



# EzSign payShield 10k Support

> Supported from version 4.2.3



EzSign supports the Thales payShield 10k HSM for RSA PKI operations (sign, verify) and random number generation.  



## Changes from version 4.2.2

All properties are now named **payShield** e.g. ``channel.1.token.payShield.port`` although all properties available in previous versions still named **hsm9000** are still accepted.   

There is a new property: **useTls** e.g. ``channel.1.token.payShield.useTls=true``. Set this to **true** if you want to protect traffic between the client and server using TLS.  

If **useTls** is **true** then the following server properties may also need to be set:

* tls.trustStore.type
* tls.trustStore.filename
* tls.trustStore.password
* tls.clientKeyStore.type
* tls.clientKeyStore.filename
* tls.clientKeyStore.password

These are discussed in the EzSign Configuration section below.





## payShield Configuration

The HSM must be configured correctly, including host settings and at least one LMK loaded. EzSign supports both Variant and KeyBlock LMKs.  

Communications between EzSign and the HSM must be in place.  



### Enabling Commands

EzSign uses the following payShield commands:

* **EI** - Generate a Public/Private Key Pair

* **EW** - Generate an RSA Signature

* **N0** - Generate a Random Value

These commands must be enabled on the HSM.  

To enable these commands you may refer to the steps below, although it is always preferable to refer to the vendor documentation.

* Logon to the **payShield manager** with the required **smartcards**.

* From the menu on the bottom right of the screen, set the state to be **Secure**.

* Select **Configuration** from the top menu, then select **Configure Commands**.

* Select the **Host** tab.

* Check the enable box for the following commands: **EI**, **EW** and **N0** (note: this is 'N' 'zero' - there is another command named NO).

* Click **Apply**.

* Set the state back to **Online**.



### Authorising Commands

The **EI** command (Generate Public/Private Key Pair) needs to be authorised on the payShield.  

To authorise this command you may refer to the steps below, although it is always preferable to refer to the vendor documentation.

* From the **payShield Manager**, login with the required **smartcards**.

* Select **Operational** from the top menu.

* Under **LMK Operations**, for the LMK in use, click the **settings icon** and choose **Set authorised activities**.

* On the **Host** tab, scroll down to **generate** and authorise **03** (for a limited time or until reboot).  You may authorise all any other (or all) commands at the same time.

* You will be asked to insert the required **smartcards** to authorise.

Note: If performing via the *Console* then **generate.rsa.host** needs to be authorised.  



### TLS Configuration

If you wish to secure the communications between EzSign and the payShield using TLS. Refer to the [payShield TLS Configuration](payshield_tls_configuration..html) guide.

  



## EzSign Configuration

The following properties are used to configure a payShield within EzSign:

* tokenType
  * This must be set to **PAYSHIELD** (although will still support **HSM9000**)
* token.payShield.ipAddress
  * The **IPv4 Address** of the payShield
* token.payShield.port
  * The port the payShield host interface has been configured to listen on 
    * For non-TLS connections this usually defaults to **1500**
    * For TLS connections this usually defaults to **2500**
* token.payShield.timeoutMs
  * The **timeout in milliseconds** to wait for a response from the HSM. Defaults to **10000** if not set.
* token.payShield.headerLen
  * The message header length. Defaults to **4**
* token.payShield.useVariantLmk
  * Set this to **true** to use a *Variant LMK*, **false** otherwise. Defaults to **false** (i.e. a *KeyBlock LMK*) if not specified
* token.payShield.lmkId
  * If multiple LMKs are loaded you may specify the LMK ID (starts from **0** and increments)
* useTls
  * If using TLS to communicate with the HSM, set this to true. Defaults to **false** if not set
  * Refer to [payShield TLS Configuration](payshield_tls_configuration..html) for more detailed information on configuring TLS



If ``useTls=true`` then the following may also need to be set:

* tls.trustStore.filename
  * If the certificate being used by the HSM is not trusted by the Java runtime, then you may need to provide a keystore containing the required CA certificate(s). Refer to [payShield TLS Configuration](payshield_tls_configuration..html) for information on how to construct this
  * This property must contain the full path to the trust store file (e.g.`` /opt/stores/trust.jks``)
* tls.trustStore.type
  * The Trust Store can be supplied as a JKS or PKCS12 file. Specify either **jks** or **pkcs12**


* tls.trustStore.password

    * The Trust Store is password protected. Use the Management Utility to configure this password - choosing the *Set TLS Trust Keystore Password* option


  

* tls.clientKeyStore.filename

    * The payShield requires a client certificate. This must be held within a password protected file. The full path to this file must be set here. E.g. ``/opt/stores/payshield_client.p12``



* tls.clientKeyStore.type

    * The client key store can be provided as a JKS or PKCS12 file. Specify either **jks** or **pkcs12**



* tls.clientKeyStore.password

    * The Client Key Store is password protected. Use the Management Utility to configure this password - choosing the *Set TLS Client Keystore Password* option.





An example configuration using TLS is shown below:

```properties
# payShield Specific Settings
channel.1.tokenType=PAYSHIELD
channel.1.token.payShield.ipAddress=192.168.0.211
channel.1.token.hsm9000.port=1500
channel.1.token.payShield.timeoutMs=10000
channel.1.token.payShield.headerLen=4
channel.1.token.payShield.useVariantLmk=false
channel.1.token.payShield.lmkId=0
channel.1.token.payShield.useTls=true

# As useTls is true, then the following are also required:
tls.trustStore.type=jks
tls.trustStore.filename=/opt/stores/payshield.jks
tls.trustStore.password=yjjWoLfEv23FC7MoRapATZSi0RBvosGaTXVBATxo+D1lkUT6wqZlew==

tls.clientKeyStore.type=pkcs12
tls.clientKeyStore.filename=/opt/stores/payshieldclient.p12
tls.clientKeyStore.password=FGchg3Kv516z3o3hvkq+bUECtJ/rHTTTYLhuI9Ifijpc+lFlW7Ycsg==
```



If TLS is not required, the configuration would simplify to the following:

```properties
channel.1.tokenType=PAYSHIELD
channel.1.token.payShield.ipAddress=192.168.0.211
channel.1.token.hsm9000.port=1500
channel.1.token.payShield.timeoutMs=10000
channel.1.token.payShield.headerLen=4
channel.1.token.payShield.useVariantLmk=false
channel.1.token.payShield.lmkId=0
channel.1.token.payShield.useTls=false
```



## Common Errors

The following are some common errors that may be seen in the EzSign logs when configuring EzSign with a payShield:



```
Token Exception: Failed to connect to HSM at IP Address/server: 192.168.0.211 port: 1500. Error: Connection refused (Connection refused)
```

The HSM cannot be accessed over the network. Check you have configured the correct port and IP Address. Check that you can connect to the HSM at that port (e.g. run ``telnet 192.168.0.211 1500``). Also check that the HSM state is *Online* (if set to Offline or Secure it will not be accepting traffic).



```
Token Exception: Failed to connect to HSM at IP Address/server: 192.168.0.211 port: 2500. Error: java.security.NoSuchAlgorithmException: Error constructing implementation (algorithm: Default, provider: SunJSSE, class: sun.security.ssl.SSLContextImpl$DefaultSSLContext)
```


This error is seen when configuring TLS. It is seen when the incorrect password is provided for either the trust or client key stores. Verify the passwords are correct and reset using the Management Utility.



```
Token Exception: There was an error sending the message. Connection reset
```


This error is seen when non-TLS traffic is sent to the TLS port or the TLS settings are not correct. Check the TLS port configuration on the HSM and ensure you match this with the EzSign settings. If targeting the TLS port, ensure that **useTls** is *true* e.g. ``channel.1.token.payShield.useTls=true``.



```
Token Exception: Failed to connect to HSM at IP Address/server: 192.168.0.211 port: 2500. Error: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

This error indicates that the HSM's TLS server certificate is not trusted by EzSign. Add the CA certificates to the trust store and specify this in the *tls* settings i.e. ``tls.trustStore.type``, ``tls.trustStore.filename`` and ``tls.trustStore.password``.



```
...Token Exception: Failed to connect to HSM at IP Address/server: 192.168.0.211 port: 2500. Error: an established connection was aborted by the software in your host machine
```

This is seen when the client TLS certificate is not configured, not trusted or not being accepted by the HSM due to a configuration issue. Refer to the [payShield TLS Configuration](payshield_tls_configuration..html) guide to set the client certificate correctly.

