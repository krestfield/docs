---
layout: default
title: Certdog YubiHSM 2 Configuration
parent: Certdog
nav_order: 212
---
# Certdog YubiHSM 2 Configuration

<br>

From version 1.10 certdog supports the Yubi HSM 2. Here we outline the steps to configure certdog to use this device as a key store

<br>

## YubiHSM Setup

Follow the YubiHSM guide to install the *Yubi HSM Connector* software for your operating system  

Once setup, you should be able to open a browser and navigate to:

[http://127.0.0.1:12345/connector/status](http://127.0.0.1:12345/connector/status)

(on Linux you may be able to run: ``curl http://127.0.0.1:12345/connector/status``)

And if all is operating correctly, you should see something like the following:

```
status=OK
serial=*
version=3.0.4
pid=13164
address=127.0.0.1
port=12345
```

If the status shows ``no device`` this indicates the USB HSM has not been detected. Refer to the YubiHSM documentation to resolve

<br>

### PKCS11 Configuration

Certdog uses the PKCS#11 interface to communicate with the YubiHSM 2. Follow the Yubi documentation to configure this, but essentially it involves creating a file named ``yubihsm_pkcs11.conf`` with the following content:

```
# URL of the connector to use. This can be a comma-separated list
connector = http://127.0.0.1:12345
```

Note that this file may already be present when you installed the YubiHSM software (e.g. on windows, it may be located here: ``C:\ProgramData\YubiHSM\yubihsm_pkcs11.conf``), but if not, create it 

<br>

Next create an environment variable ``YUBIHSM_PKCS11_CONF`` that references this file e.g.

```
YUBIHSM_PKCS11_CONF=C:\ProgramData\YubiHSM\yubihsm_pkcs11.conf
```

or, for Linux

```
export YUBIHSM_PKCS11_CONF=/opt/yubihsm/yubihsm_pkcs11.conf
```

<br>

You may also wish to add the YubiHSM Shell *bin* directory to your path to enable you to start the yubihsm shell from any location e.g. On windows you could add ``C:\Program Files\Yubico\YubiHSM Shell\bin`` to your path

<br>

### Authentication Keys

It is recommended to create an authentication key specifically for certdog. This essentially creates a login for certdog with limited capabilities  

Note: It is also recommended to replace the default, fully privileged authentication key (or at least change the password), but for the purposes of these instructions we will use the default settings (authentication key ID: 1, default password: password)

<br>

Start the YubiHSM Shell:

```
yubihsm-shell.exe
```

If you did not update your path variable, this must be run from the ``YubiHSM SHell/bin`` directory

At the prompt, type the following commands:

```
yubihsm> keepalive on
yubihsm> connect
yubihsm> yubihsm> session open 1 password
Created session 0
```

Note the session ID created (in this case 0)

Next, create a new authentication key for certdog, using the following command:

```
yubihsm> put authkey [session ID] [key ID] [label] [domains] [capabilities] [delegated capabilities] [password]
```

Where 

* ``[session ID]`` is the current session, in this example: 0

* ``[key ID]`` can be a number e.g. 2

* ``[label]`` is any string to refer to this key

* ``[domains]`` a domain is a logical partition and users are permitted access to a partition. This provides segregation for applications

* ``[capabilities]`` and ``[delegated capabilities]`` are the permissions this *user* will have. For certdog the required capabilities are: 

  * generate-asymmetric-key

  * sign-pkcs

  * sign-pss

  * get-opaque

  * put-opaque

For example, to create a new authentication key using the current session ``0``, with ID ``2``, label ``CERTDOG`` for domain/partition ``1`` and with a password of ``password1234`` we would run the following:

```
yubihsm> put authkey 0 2 "CERTDOG" 1 delete-asymmetric-key:generate-asymmetric-key:sign-pkcs:sign-pss sign-pkcs:sign-pss password1234
```

You should see:

```
Stored Authentication key 0x0002
```

<br>

## Certdog KeyStore Setup

From Certdog, under *Local CAs*, select **Key Stores**. Click **Add New Key Store**

Enter a **name** and select **PKCS#11** as the *Type*

The password is constructed from the authentication key ID and password. We take the authentication key ID and pad it to 4 characters with leading zeros (so an ID of 1 would be 0001, 2 would be 0002 and so on) then concatenate this to the password i.e.

```
[Padded Key ID][Password]
```

So in the example above, where we created a new authentication key with ID **2** and password **password1234**, the PKCS#11 password (that must be entered for the Key Store) would be: 

```
0002password1234
```

Enter this in the *Password* and *Re-Type Password* fields

For the PKCS#11 Library, enter the full path to the library. In windows this will be something like:

```
C:\Program Files\Yubico\YubiHSM Shell\bin\pkcs11\yubihsm_pkcs11.dll
```

and on Linux, something like:

```
/usr/lib/x86_64-linux-gnu/pkcs11/yubihsm_pkcs11.so
```

For HSM Model, select **YubiHSM 2**

For slot, select **0**

Leave Use Module Protection un-checked

Click **Create**

<br>

You can now select this Key Store when creating a new CA











