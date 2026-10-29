---
layout: default
title: EzSign - Management Tool
parent: EzSign
nav_order: 5
---
# EzSign Management Tool

<br>

The Management utility enables the following operations:

- Setting of Token Passwords
- Generation of CSRs (Certificate Signing Requests) 
- Specifying Signing Keys
- Importing Certificates, including certificate chains (PKCS#7)
- Importing existing HSM keys
- Deleting Certificates
- Displaying Certificates
- Generating AES Keys
- Displaying AES Keys
- Deleting AES Keys
- Translating Keystore Objects from an old password to new
- Setting the Authentication Code
- Setting TLS Passphrases
- Managing the REST API users, their API tokens and certificates
- Setting the REST API TLS Passphrases
- Changing the Master Password

<br>

The tool can be run in two ways:

- As an interactive menu, where each operation is chosen from a list and the details are prompted for
- As a command line tool (CLI), where each operation is a single command. This is useful for scripts, automation and remote sessions

Both carry out the same operations on the same files.  Each section below describes the menu option and then the same operation via the CLI

<br>

The server will not start until the token passwords have been set and you will be unable to sign or verify signatures until the required keys and certificates have been generated and imported.  Encrypting and decrypting requires an AES key to be generated.  Therefore, the Management tool must usually be run before the server can be started (if you are duplicating configurations there is no need to re-run the tool)

<br>

## Starting

To start the management utility menu, run the following script which requires that the server properties file is passed as a parameter e.g.

```
ezsign-manage.sh ../config/serverconfig.properties
```

(On Windows run ``ezsign-manage.bat``)

Once the script starts you will be asked to enter the Master Password before being able to proceed

<br>

```
  Krestfield EzSign Management
  ----------------------------

  The master password is required to manage the server

  Enter password:
```

The master password can also be provided in the same ways as for the server, so that it does not need to be typed:

```
ezsign-manage.sh ../config/serverconfig.properties -f master.txt
ezsign-manage.sh ../config/serverconfig.properties MyMasterPassword
```

With ``-f`` the password is read from the first line of the file.  If neither is given, the ``EZMASTERPASS`` environment variable is used if set, otherwise the password is prompted for.  Note that a password given as a parameter can be seen by other users in the process list, so the file or the prompt is preferred

<br>

### Checking the Master Password

The tool checks that the master password entered is the one the configuration uses.  This is done using the ``masterPassword.check`` value in the properties file, which is a salted hash of the master password (the master password cannot be recovered from it).  The tool writes this value; it should not be edited

If the properties file does not have this value yet, the master password is checked by decrypting the values encrypted with it (such as the token passwords).  If they all decrypt you will be offered to record the check value:

```
  The master password decrypts the 3 encrypted value(s) in the properties file
  Record a check of this master password in the properties file so it can be verified in future? (y/n): y
  masterPassword.check added. A backup of the properties file was saved to ../config/serverconfig.properties.2026.10.29.10.24.11.558
```

If the master password is not correct, you can try again, continue or exit:

```
  The master password is not correct (it does not match masterPassword.check)
  
    1. Try again
    2. Continue, e.g. to reset the passwords. Values encrypted with the correct master password
       will need to be set again
    3. Exit
  Choice:
```

Choose **2** only if the master password has been lost and the passwords are to be set again (see [Changing the Master Password](#changing-the-master-password))

The server makes the same check when it starts.  If the properties file has a ``masterPassword.check`` value and the master password does not match it, the server logs *The master password is incorrect* and does not start

<br>

Once the master password has been entered, the menu is displayed:

```
  Krestfield EzSign Management
  ----------------------------

  1.  Set Passwords

  2.  Generate CSR
  3.  Import Certificate
  4.  Import Existing HSM Keys

  5.  Set Signing Key

  6.  Display Certificates
  7.  Display Certificates Details
  8.  Delete Certificate

  9.  Generate AES Key
  10. Display AES Keys
  11. Delete AES Key

  12. Translate Keystore Objects
  13. Display All Channel Objects
  14. Set Authentication Code

  15. Set TLS Client Keystore Password
  16. Set TLS Trust Keystore Password

  17. REST API Users
  18. Set REST API Keystore Password
  19. Set REST API Trust Store Password

  20. Change Master Password

  21. Exit

Command:
```

When an option asks for the channel, the channel chosen last is shown as the default.  Press enter to choose it again, or enter another number:

```
  Channels
  --------

    1. SIGNING
    2. ENCRYPTION

Select Channel Number (1. SIGNING):
```

<br>

### Starting the CLI

To run an operation from the command line, give the command after the properties file.  For example, to list the channels:

```
ezsign-manage.sh ../config/serverconfig.properties channels list
```

```
1. SIGNING  type: PKI  token: SOFTWARE
2. ENCRYPTION  type: SYM  token: SOFTWARE
```

(On Windows run ``ezsign-manage.bat`` with the same parameters)

To list all the commands, use the ``--help`` parameter:

```
ezsign-manage.sh ../config/serverconfig.properties --help
```

```
Usage: ezsign-manage [-hV] [COMMAND]
Manages the ezsign-server configuration from the command line.

Commands that work on the server configuration follow the properties file:
  ezsign-manage <propertiesFile> <command> <subcommand> ...

If the properties file is left out, the file named by the EZSIGN_CONFIG
environment variable is used:
  ezsign-manage <command> <subcommand> ...

The master password is read from the file given with -f, the EZMASTERPASS
environment variable, or prompted for. Token passwords and new passwords are
always prompted for.

Start the interactive menu with:
  ezsign-manage <propertiesFile> [masterPassword | -f passwordFile]
  -h, --help      Show this help message and exit.
  -V, --version   Print version information and exit.
Commands:
  channels           List the channels
  certs              List, import and delete the certificates in a channel
  signing-key        Show or set the key a channel signs with
  csr                Generate a certificate signing request
  aes-keys           List, generate and delete the AES keys in a channel
  objects            List the objects (keys and certificates) in a channel
  hsm                Work with keys already in an HSM
  token-password     Set or change a channel's token password
  auth-code          Set the authentication codes clients and the control tool
                       use
  keystore-password  Set the TLS key store and trust store passwords
  master-password    Change the master password
  users              Manage the REST API users in the users file (server.
                       restapi.usersFile)
  roles              Manage the roles in the users file. A role is a named set
                       of permissions assigned to users
  sign-users-file    Sign a users file with the admin key, writing <usersFile>.
                       sig.
  help               Display help information about the specified command.
```

``--help`` also works on every command, to show its sub commands and parameters.  For example:

```
ezsign-manage.sh ../config/serverconfig.properties certs --help
ezsign-manage.sh ../config/serverconfig.properties certs import --help
```

```
Usage: ezsign-manage certs import [-hV] [--set-signer] [-f=<file>] <channel>
                                  <certFile>
Import a certificate file into a channel: a single certificate (PEM or DER), or
several - a PKCS#7 file (.p7b, .p7c, .p7) or PEM certificates one after another
- e.g. the certificate issued for a CSR with its issuing CAs.
In a file of several certificates, a root CA certificate is not imported:
import a root CA from a file that holds it alone, so it is never trusted by
accident. Prompts for the token password
      <channel>      The channel name
      <certFile>     The certificate or PKCS#7 file
  -f, --master-password-file=<file>
                     File containing the master password (the first line).
                       Otherwise the EZMASTERPASS environment variable is used,
                       or the password is prompted for
  -h, --help         Show this help message and exit.
      --set-signer   Make the key of the imported certificate the channel's
                       signing key. The channel must hold its private key
                       (generated with csr generate)
  -V, --version      Print version information and exit.
```

<br>

**Passwords**

Passwords are never passed to the CLI as parameters, so they are never visible in the process list or the shell history:

- The master password is read from the file given with ``-f``, otherwise the ``EZMASTERPASS`` environment variable, otherwise it is prompted for (as for the menu).  Commands that only manage the REST API users do not need it
- The token password is always prompted for.  As with the menu, it is required for operations that change a channel's keys or certificates
- New passwords (token passwords, authentication codes, keystore passwords and the master password) are always prompted for, twice

If the CLI is run without a terminal (e.g. from a script with its input redirected), each prompt reads one line from the standard input.  This allows a script to supply them without placing them on the command line e.g.

```
ezsign-manage.sh ../config/serverconfig.properties aes-keys generate ENCRYPTION --label key1 -f master.txt < token.txt
```

<br>

**Leaving out the Properties File**

If all operations are carried out on the same properties file, set the ``EZSIGN_CONFIG`` environment variable to it and leave the file out:

```
export EZSIGN_CONFIG=../config/serverconfig.properties             (Linux)
set EZSIGN_CONFIG=..\config\serverconfig.properties                (Windows)

ezsign-manage.sh certs list SIGNING
```

```
Using properties file ../config/serverconfig.properties (from EZSIGN_CONFIG)
Master password:
1. CN=EzSign Signer,O=Krestfield Ltd,C=GB  [signing certificate, has private key]
...
```

A properties file given on the command line is always used instead.  The command reports the file it is using, so that a change is not made to the wrong configuration by mistake.  The menu also uses ``EZSIGN_CONFIG`` when it is started without a properties file

To set a default for every session, remove the comment from the ``EZSIGN_CONFIG`` line in the ``ezsign-manage.sh`` or ``ezsign-manage.bat`` script and set the file.  As written, the path is relative to the ``bin`` folder.  A value already set in the environment is used instead of the script's

<br>

**Output and Exit Codes**

Results (such as lists and CSRs) are written to the standard output and messages to the standard error, so the results can be captured or redirected.  The exit code is 0 on success.  Anything else is an error, with the reason given on the standard error

<br>

## Setting Master and Token Passwords

To set the Master and Token passwords for a channel choose **option 1**.  You will then be prompted to choose the channel, enter the Master Password and Token Passwords and then whether you want to write the new data to the properties file.  This option must be run before the server is started in order to encrypt the Token Passwords

```
  Channels
  --------

    1. SIGNING
    2. ENCRYPTION

Select Channel Number: 1

  Master Password
  ---------------

  This is the password which is used to start the server
  It is used to encrypt other passwords (Token Passwords etc). It is not stored

 Enter Password:
Retype Password:

  Token Password
  --------------

  For software tokens, this is the password used to encrypt keys
  For PKCS#11 tokens, this is the token PIN/Password used to authenticate, also referred to as the operator password
  This password is stored in the configuration, encrypted under the master password

 Enter Password:
Retype Password:

  A backup of the original has been saved to ../config/serverconfig.properties.2026.10.29.10.24.12.448
  Ready to update properties file ../config/serverconfig.properties with the new passwords

Proceed? (y/n): y

  The properties file ../config/serverconfig.properties has been updated successfully.
```

The master password must be at least 8 characters.  If the master password entered is not the one the rest of the configuration uses, you will be asked whether to cancel or to make it the new master password (see [Changing the Master Password](#changing-the-master-password))

Note: For sensitive operations including:

- Generating CSRs
- Importing certificates
- Deleting certificates
- Setting the signing key 
- Generating AES keys 
- Deleting AES keys 

The channels token password will be required.  When required you will receive a prompt as follows:

```
  The token password is required for this operation.  Please enter the token password below
  
Token Password:
```

The token password must then be entered to proceed.  It is only asked for once per channel while the menu is running

<br>

### Setting the Token Password via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties token-password set SIGNING
```

```
Master password:
New token password:
Retype the new token password:
Set channel.1.token.password, encrypted with the master password. Backup saved to serverconfig.properties.2026.10.29.10.21.22.011
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

The properties file is backed up before every change.  If the master password does not decrypt the other values in the properties file, nothing is changed.  To reset the passwords with a new master password, use the menu

When the CLI prompts for a channel's token password, it names the channel:

```
Token password for channel SIGNING:
```

<br>

## Generating a CSR

To generate a CSR (Certificate Signing Request) choose **option 2**.  You will be prompted to enter the channel, then the requested DN (Distinguished Name) and the filename to store the CSR.  The key type and size are taken from the channel's signature settings (e.g. ``channel.1.signature.keySize``)

```
Select Channel Number (1. SIGNING): 
  
  Generating CSR for channel SIGNING
  
  The token password is required for this operation.  Please enter the token password below
  
Token Password: 
  
  Password verified OK

Distinguished Name: CN=EzSign Signer,O=Krestfield Ltd,C=GB

CSR Filename: ../certs/signing.p10

  Generated CSR Data:
-----BEGIN CERTIFICATE REQUEST-----
MIICgzCCAWsCAQAwPjELMAkGA1UEBhMCR0IxFzAVBgNVBAoMDktyZXN0ZmllbGQg
THRkMRYwFAYDVQQDDA1FelNpZ24gU2lnbmVyMIIBIjANBgkqhkiG9w0BAQEFAAOC
AQ8AMIIBCgKCAQEAkrsYgMRhi1dZ61YlcewaDek+OCB4n3YodGwXlUdbPdNp9u59
thmosYfnnjyg7H5+M2H5qakOz8W+n9/W/ibJRr+KFDq0raeHqSpf9myxfkiw/2KU
WgiH4WcjGfW3iJwJRNg69qcz6MUO3HzsyXYH+scEy8wKL5NljRYDb3K+P/cd//PA
yj5p2TetvMmINgZiMSD8yRbj2CXiEnbxCqktwbt7H6IskLQ72t5SDx/BhR/myYL+
3kyCTmq24I2EIOEbtI4CBcbmPOsSCIPIMGFLKhRXO5xejLzFirHEcNTDoiZzAxe4
nvsgcVVsIRjCZsnI+L3Zeu0bwoaBe8JirgykVQIDAQABoAAwDQYJKoZIhvcNAQEL
BQADggEBAGQklb9u/iTKr+EAaAGSjln5wh9ezh5gGmloF0tJX4oZtoNm72APKwCK
tunXIRROBLsKISeZ6M5sW/DdT9oy9QvqGTuwSJgdx2BBFJneLGAjb5ikEOK249Pk
NV5cicFiHZ07+YrBCsBu53+vEclxQXwWxUtfupnlr0rd011+lKwP9NnkC20zESo/
hljsx5dnN3zDHUP1fHGKC2Tu0SAgenv/ZZLUoV1bjRHVj5RmSWHAly0rBhnD4QVt
d0sTWlczUpkn+F03E/9xmhFjPEVjkUOwiK2/W0RrWO7MtNpSScHT8xq8wNUc9oTI
UHwa6nARtpDVymI1+VBBo5IJYNFnj0Y=
-----END CERTIFICATE REQUEST-----

  CSR written to ../certs/signing.p10
```

The CSR should then be processed by the CA who will issue the certificate.  Once the certificate has been issued the Import Certificate option can be chosen to import the certificates

<br>

### Generating a CSR via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties csr generate SIGNING --dn "CN=EzSign Signer,O=Krestfield Ltd,C=GB" -o ../certs/signing.p10
```

```
Master password:
Token password for channel SIGNING:
CSR written to ../certs/signing.p10
A new key pair was generated in channel SIGNING. Import the issued certificate with: certs import SIGNING <certFile> --set-signer
```

Without ``-o`` the CSR is written to the standard output.  An existing file is not overwritten unless ``--force`` is given

<br>

## Importing Certificates

To import root certificates or certificates issued from a CSR choose **option 3**.  You will then be prompted for the channel and a path to the certificate file.  The file can contain:

- A single certificate (PEM or DER)
- A PKCS#7 structure (``.p7b``, ``.p7c``, ``.p7``, PEM or DER) e.g. the issued certificate together with its issuing CA certificates
- Several PEM certificates, one after another

The certificates are imported in order, issuers first, regardless of their order in the file.  Certificates that are already in the channel are reported and are not imported again

```
Select Channel Number (1. SIGNING): 

  Enter a certificate file, or a PKCS#7 file (.p7b) holding the certificate and its issuing CAs

Path to certificate: ../certs/signing.p7b

  The file holds 3 certificates
  Imported: C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA
  Imported: CN=EzSign Signer,O=Krestfield Ltd,C=GB

  The file includes a root CA certificate, which was not imported:
    C=GB,O=Krestfield Ltd,CN=Krestfield Root CA
  A root CA certificate makes the channel trust everything it issues, so it is only imported from a
  file holding that certificate alone. If this root should be trusted, import it on its own

Press any key to continue
```

When a file contains several certificates, a root CA certificate is **not** imported.  This ensures that a root CA is never trusted by accident.  To import a root CA certificate, import it from a file containing only that certificate:

```
Path to certificate: ../certs/root.cer

  Imported: C=GB,O=Krestfield Ltd,CN=Krestfield Root CA
```

If the certificate is associated with a private key on the token, you will also be prompted if you wish to set this as the new signing certificate:

```
Do you wish to set CN=EzSign Signer,O=Krestfield Ltd,C=GB as the default signing certificate? (y/n): y

  A backup of the original has been saved to ../config/serverconfig.properties.2026.10.29.10.24.14.260
  Ready to update properties file ../config/serverconfig.properties with the new passwords

Proceed? (y/n): y

  The properties file ../config/serverconfig.properties has been updated successfully.
```

Choosing y will result in the properties file being updated.  If you do not wish to set this as the signing certificate now, you can do this later by running option **5. Set Signing Key**

Note that for signing certificates, all certificates in the path must be imported

<br>

### Importing Certificates via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties certs import SIGNING ../certs/signing.p7b --set-signer
```

```
Master password:
Token password for channel SIGNING:
The file holds 3 certificates
Imported C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA into channel SIGNING
Imported CN=EzSign Signer,O=Krestfield Ltd,C=GB into channel SIGNING
The file includes a root CA certificate, which was not imported:
  C=GB,O=Krestfield Ltd,CN=Krestfield Root CA
A root CA certificate makes the channel trust everything it issues, so it is only imported from a
file holding that certificate alone. If this root should be trusted, import it on its own
Signing key set to the key of CN=EzSign Signer,O=Krestfield Ltd,C=GB (channel.1.signature.keyId=1a1872dbf4a1911). Backup saved to serverconfig.properties.2026.10.29.10.21.27.865
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

``--set-signer`` makes the imported certificate (the one whose private key the channel holds) the signing certificate.  Without it, the certificates are imported and the signing key is not changed

To import the root CA certificate:

```
ezsign-manage.sh ../config/serverconfig.properties certs import SIGNING ../certs/root.cer
```

```
Master password:
Token password for channel SIGNING:
Imported C=GB,O=Krestfield Ltd,CN=Krestfield Root CA into channel SIGNING
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

<br>

## Importing Existing Keys and Certificates

If you are using a PKCS#11 HSM which has been used by another system you may import these objects into EzSign.  To do this choose option **4.Import Existing HSM Keys**

Choose the channel to import the objects to.  Note: the channel selected must be configured to use the HSM from which the objects are to be imported

If not previously entered, you will be prompted for the token password:

```
The token password is required for this operation.  Please enter the token password
below

Token Password:

Password verified OK

Importing objects from the HSM...

Objects imported from the HSM OK
```

The objects imported can be examined by running the **Display Certificates** or **Display all Channel Objects** options.  The signing key can be selected by running the **Set Signing Key** option

<br>

### Importing Existing Keys and Certificates via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties hsm import-keys HSMCHANNEL
```

```
Master password:
Token password for channel HSMCHANNEL:
Imported the objects from the HSM into channel HSMCHANNEL
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

The objects imported can then be examined with ``certs list`` or ``objects list`` and the signing key set with ``signing-key set``

<br>

## Setting the Signing Key

To set the default signing key (that is the key that will be used to sign data), choose **option 5**.  You will then be presented with a list of available certificates which have associated private keys and can therefore be used to sign data.  Note: a certificate will not be available for signing if there is not a complete path for that certificate

```
  Current Signing Certificate:
  ----------------------------

       Subject: CN=EzSign Signer, O=Krestfield Ltd, C=GB
       Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Issuing CA
       Valid From: Thu Oct 29 10:18:51 UTC 2026
       Valid To  : Sat Oct 28 10:18:51 UTC 2028
       Serial Number: 6de730050c7e13a2d99d2d0049034b21397cc8d3
       Type : End Entity


  Available Signing Certificates:
  -------------------------------
    1. Subject: CN=EzSign Signer, O=Krestfield Ltd, C=GB
       Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Issuing CA
       Valid From: Thu Oct 29 10:18:51 UTC 2026
       Valid To  : Sat Oct 28 10:18:51 UTC 2028
       Serial Number: 6de730050c7e13a2d99d2d0049034b21397cc8d3
       Type : End Entity


Select Certificate Number: 1
  A backup of the original has been saved to ../config/serverconfig.properties.2026.10.29.10.24.14.716
  Ready to update properties file ../config/serverconfig.properties with the new passwords

Proceed? (y/n): y

  The properties file ../config/serverconfig.properties has been updated successfully.
```

<br>

### Setting the Signing Key via the CLI

To show the current signing certificate and the certificates that can be used to sign:

```
ezsign-manage.sh ../config/serverconfig.properties signing-key show SIGNING
```

```
Master password:
Signing certificate:

1. CN=EzSign Signer,O=Krestfield Ltd,C=GB  [signing certificate, has private key]
   Issuer       : C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA
   Serial number: 6de730050c7e13a2d99d2d0049034b21397cc8d4
   Valid        : 2026-10-29 10:21:25 UTC to 2028-10-28 10:21:25 UTC
   Type         : End Entity
   SHA-1        : 6b36577526b0324868babce68b0fc551c2a9999f
   SHA-256      : 0ebdf919e9685f41d775100ecfe1e1de7a9a404bae407843c1d85e3d40ce3c2b

Certificates that can be used to sign (use the number with signing-key set):

1. CN=EzSign Signer,O=Krestfield Ltd,C=GB  [signing certificate, has private key]
   Issuer       : C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA
   Serial number: 6de730050c7e13a2d99d2d0049034b21397cc8d4
   Valid        : 2026-10-29 10:21:25 UTC to 2028-10-28 10:21:25 UTC
   Type         : End Entity
   SHA-1        : 6b36577526b0324868babce68b0fc551c2a9999f
   SHA-256      : 0ebdf919e9685f41d775100ecfe1e1de7a9a404bae407843c1d85e3d40ce3c2b

```

To set the signing key, choose the certificate by its number, serial number, SHA-1 thumbprint or SHA-256 thumbprint:

```
ezsign-manage.sh ../config/serverconfig.properties signing-key set SIGNING --number 1
ezsign-manage.sh ../config/serverconfig.properties signing-key set SIGNING --serial 6de730050c7e13a2d99d2d0049034b21397cc8d4
ezsign-manage.sh ../config/serverconfig.properties signing-key set SIGNING --sha1 6b36577526b0324868babce68b0fc551c2a9999f
ezsign-manage.sh ../config/serverconfig.properties signing-key set SIGNING --sha256 0ebdf919e9685f41d775100ecfe1e1de7a9a404bae407843c1d85e3d40ce3c2b
```

```
Master password:
Token password for channel SIGNING:
Signing key set to the key of CN=EzSign Signer,O=Krestfield Ltd,C=GB (channel.1.signature.keyId=1a1872dbf4a1911). Backup saved to serverconfig.properties.2026.10.29.10.21.38.962
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

Thumbprints may be given with colons or spaces, in upper or lower case (e.g. as copied from the Windows certificate viewer).  In scripts, a thumbprint is preferred as it cannot change between commands

<br>

## Displaying and Deleting Certificates

**Options 6, 7 and 8** are used to delete and display the available certificates.  When certificates are displayed they are shown in the following format

```
  Current Signing Certificates:
  -----------------------------
    1. Subject: CN=EzSign Signer, O=Krestfield Ltd, C=GB
       Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Issuing CA
       Valid From: Thu Oct 29 10:18:51 UTC 2026
       Valid To  : Sat Oct 28 10:18:51 UTC 2028
       Serial Number: 6de730050c7e13a2d99d2d0049034b21397cc8d3
       Type : End Entity

    2. Subject: C=GB, O=Krestfield Ltd, CN=Krestfield Issuing CA
       Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Root CA
       Valid From: Thu Oct 29 10:14:17 UTC 2026
       Valid To  : Mon Jan 15 10:14:17 UTC 2035
       Serial Number: 803819bb9042b256e6257f0e9320b2b53b3fe52
       Type : Intermediate CA

    3. Subject: C=GB, O=Krestfield Ltd, CN=Krestfield Root CA
       Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Root CA
       Valid From: Thu Oct 29 10:14:16 UTC 2026
       Valid To  : Sun Oct 26 10:14:16 UTC 2036
       Serial Number: 7b92dcc0fe5dcb0ec1eaecfbc7243abe0ee596ba
       Type : Root CA


  Other Certificates:
  -------------------
  There are no other certificates
```

The first section displays the *Current Signing Certificates*.  This is based on the selected signing key and displays the complete path.  

The second sections displays all other certificates which are stored but not included in the current signing path

Option 7 also displays each certificate's data (base64 encoded).  Option 8 displays the certificates and asks for the number of the certificate to delete

<br>

### Displaying and Deleting Certificates via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties certs list SIGNING
```

```
Master password:
1. CN=EzSign Signer,O=Krestfield Ltd,C=GB  [signing certificate, has private key]
   Issuer       : C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA
   Serial number: 6de730050c7e13a2d99d2d0049034b21397cc8d4
   Valid        : 2026-10-29 10:21:25 UTC to 2028-10-28 10:21:25 UTC
   Type         : End Entity
   SHA-1        : 6b36577526b0324868babce68b0fc551c2a9999f
   SHA-256      : 0ebdf919e9685f41d775100ecfe1e1de7a9a404bae407843c1d85e3d40ce3c2b

2. C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA  [signing path]
   Issuer       : C=GB,O=Krestfield Ltd,CN=Krestfield Root CA
   Serial number: 803819bb9042b256e6257f0e9320b2b53b3fe52
   Valid        : 2026-10-29 10:14:17 UTC to 2035-01-15 10:14:17 UTC
   Type         : Intermediate CA
   SHA-1        : 15122833d6bf464364ce4e9f5b2882f7c375e50a
   SHA-256      : 779ee087eec91d8ad880d50d6478378a2a4b4b2fe8fe3a8e85a0c120de5cfe21

3. C=GB,O=Krestfield Ltd,CN=Krestfield Root CA  [signing path]
   Issuer       : C=GB,O=Krestfield Ltd,CN=Krestfield Root CA
   Serial number: 7b92dcc0fe5dcb0ec1eaecfbc7243abe0ee596ba
   Valid        : 2026-10-29 10:14:16 UTC to 2036-10-26 10:14:16 UTC
   Type         : Root CA
   SHA-1        : 8409382b91e9d8d3585edc68f4cbb1315301e921
   SHA-256      : 8e0708efa1156d86f8a937006d7e08def35347ee917f51b2d644025ee3c78b77

```

The signing certificate path is listed first (the signing certificate, then its issuers), followed by all other certificates.  The signing certificate and those with a private key in the channel are marked.  Add ``--details`` to include each certificate's data (base64 encoded), or ``--json`` for JSON output

Reading a channel requires the master password, even when nothing is being changed.  This is because the channel's objects (including the certificates) are encrypted under the token password, which is itself stored encrypted under the master password

To delete a certificate, choose it by its number (from ``certs list``), serial number, SHA-1 thumbprint or SHA-256 thumbprint:

```
ezsign-manage.sh ../config/serverconfig.properties certs delete SIGNING --sha1 1d8e140d9b87bce569e907f630465d0c126b9bec
```

```
Master password:
Token password for channel SIGNING:
Deleted C=GB,O=Krestfield Ltd,CN=Finance App (serial number 6de730050c7e13a2d99d2d0049034b21397cc8d2) from channel SIGNING
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

<br>

## Generating AES Keys

Choose **option 9** to generate an AES key.  Enter the key size and the key label as follows:

```
Enter AES Key Size (128, 192 or 256): 256

Enter a unique label for this key: key1
  AES key generated OK
```

Once the key has been created it can be used to encrypt and decrypt data via the client, where the label set above must be specified to select this key

<br>

### Generating AES Keys via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties aes-keys generate ENCRYPTION --label key1
```

```
Master password:
Token password for channel ENCRYPTION:
Generated a 256 bit AES key key1 in channel ENCRYPTION
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

The key size is 256 bits unless ``--size`` is given e.g. ``--size 128``

<br>

## Displaying and Deleting AES Keys

AES keys can be displayed and deleted by choosing **options 10 and 11**

```
  Current AES Keys:
  -----------------------------
       #    Key Size   Date Created         Label
       ---  --------   -------------------  --------
         1  128bits    29-10-2026 10:18:52   key2
         2  256bits    29-10-2026 10:18:52   key1
```

Key details will be shown including the key size, date created and associated label

Note: AES keys cannot be deleted from software tokens

<br>

### Displaying and Deleting AES Keys via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties aes-keys list ENCRYPTION
```

```
Master password:
key2  128 bits  created 2026-10-29 10:21:49
key1  256 bits  created 2026-10-29 10:21:47
```

Add ``--json`` for JSON output:

```
[
  { "label": "key2", "size": 128, "created": "2026-10-29 10:21:49" },
  { "label": "key1", "size": 256, "created": "2026-10-29 10:21:47" }
]
```

To delete a key, give its label:

```
ezsign-manage.sh ../config/serverconfig.properties aes-keys delete ENCRYPTION key2
```

For a software token, this reports the following error, as for the menu:

```
Error: deleteAESKey has not been implemented for this token type
```

<br>

## Translate KeyStore Objects

If you wish to translate keystore objects from one token password to another.  For example, when refreshing passwords for software tokens or if an HSM’s objects have been translated to another operator cardset, choose **option 12**

You will be prompted to choose the channel and then enter the current token password

```
  Please enter the current token password

 Enter Password:
 Retype Password:
```

Then enter the new token password.  This is the new password or new operator cardset passphrase:

```
  Please enter the NEW token password

 Enter Password:
 Retype Password:

Objects have been translated to the new password successfully
A backup was made of the original objects and stored in the SIGNING keystore folder
```

The objects will be translated and re-encrypted under the new password.  The pre-translated objects will be backed up to a timestamped folder within the keystore directory e.g. /20261101_1015_BACKUP.  The new token password is then stored in the properties file, encrypted under the master password

Note: objects can only be translated in PKI channels

<br>

### Translating KeyStore Objects via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties token-password change SIGNING
```

```
Master password:
Current token password for channel SIGNING:
New token password:
Retype the new token password:
The objects in channel SIGNING are now encrypted with the new token password. A backup of the original objects was kept in the channel's key store folder
Set channel.1.token.password, encrypted with the master password. Backup saved to serverconfig.properties.2026.10.29.10.22.05.510
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

Note the difference between the two token password commands.  ``token-password set`` only stores a token password in the properties file (as for option 1), whereas ``token-password change`` re-encrypts the objects with a new token password and then stores it (as for option 12)

<br>

## Display KeyStore Objects

To display all the objects stored within a channel, select **option 13**, then enter the channel

All objects details will be displayed indicating what type of object they are (i.e. private key, certificate etc), the ID and filename e.g.

```
  Current Objects: 
  ----------------
  Object ID: 1a1872b69389232
  Created  : Thu Oct 29 10:18:51 UTC 2026
  Type     : CERTIFICATE
    Subject: C=GB, O=Krestfield Ltd, CN=Krestfield Root CA
    Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Root CA
    Serial Number: 7b92dcc0fe5dcb0ec1eaecfbc7243abe0ee596ba
  Filename : 1a1872b69389232.cer

  Object ID: 1a1872b65402461
  Created  : Thu Oct 29 10:18:50 UTC 2026
  Type     : PRIVATE KEY
  Filename : 1a1872b65402461.priv

  Object ID: 1a1872b65402461
  Created  : Thu Oct 29 10:18:50 UTC 2026
  Type     : PUBLIC KEY
  Filename : 1a1872b65402461.pub

  Object ID: 1a1872b65402461
  Created  : Thu Oct 29 10:18:51 UTC 2026
  Type     : CERTIFICATE
    Subject: CN=EzSign Signer, O=Krestfield Ltd, C=GB
    Issuer : C=GB, O=Krestfield Ltd, CN=Krestfield Issuing CA
    Serial Number: 6de730050c7e13a2d99d2d0049034b21397cc8d3
  Filename : 1a1872b65402461.cer
```

<br>

### Displaying KeyStore Objects via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties objects list SIGNING
```

```
Master password:
Object ID: 1a1872dbf4a1911
Created  : Thu Oct 29 10:21:25 UTC 2026
Type     : PRIVATE KEY
Filename : 1a1872dbf4a1911.priv

Object ID: 1a1872dbf4a1911
Created  : Thu Oct 29 10:21:25 UTC 2026
Type     : PUBLIC KEY
Filename : 1a1872dbf4a1911.pub

Object ID: 1a1872dcb454046
Created  : Thu Oct 29 10:21:27 UTC 2026
Type     : CERTIFICATE
  Subject: C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA
  Issuer : C=GB,O=Krestfield Ltd,CN=Krestfield Root CA
  Serial Number: 803819bb9042b256e6257f0e9320b2b53b3fe52
Filename : 1a1872dcb454046.cer
...
```

<br>

## Set Authentication Code

To set the authentication code which is used to encrypt traffic between the client and server, choose **option 14**

Enter the master password, followed by the authentication code:

```
  You will now be asked to enter the Master Password
  Followed by the Authentication Code Password

  Master Password
  ---------------

  This is the password which is used to start the server
  It is used to encrypt other passwords (Token Passwords etc). It is not stored

 Enter Password:
Retype Password:

  Enter the Authentication Code
  -----------------------------

  This is a password used to secure traffic from the client to the server
  Once this has been set, the client must provide this same password to the EzSign client

 Enter Password:
Retype Password:
```

You will now be prompted whether to set this as the server code only (i.e. securing comms between the client and the server when sending messages), as the server control code only (i.e. securing comms between the client utils scripts and the control server) or both:

```
  Do you want to set this password as the: 

  1. Server Authentication Code
  2. Server Control Authentication Code
  3. Both
  4. Cancel

Enter Choice: 3
  A backup of the original has been saved to ../config/serverconfig.properties.2026.10.29.10.24.16.759
```

The server configuration will be updated and a backup made

<br>

### Setting the Authentication Code via the CLI

Use ``--server`` to set the server authentication code, ``--ctrl`` to set the server control authentication code, or both:

```
ezsign-manage.sh ../config/serverconfig.properties auth-code set --server --ctrl
```

```
Master password:
New authentication code:
Retype the new authentication code:
Set server.authCode, server.ctrl.authCode, encrypted with the master password. Backup saved to serverconfig.properties.2026.10.29.10.22.07.683
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

<br>

## Setting TLS Keystore Passwords

If utilising TLS to communicate with an HSM (e.g. a payShield) then you will need to configure a Trust Key Store (a key store where the CA certificates are stored) and optionally a Client Key Store (that will hold the client authentication certificate)

Select **options 15 and 16** to set these passwords

If the REST API is enabled, it requires a key store holding the server's TLS certificate and, if client certificates are used to authenticate, a trust store holding the CA certificates that issue them.  Select **options 18 and 19** to set these passwords:

```
  You will now be asked to enter the Master Password
  Followed by the REST API Keystore Password

  Master Password
  ---------------

  This is the password which is used to start the server
  It is used to encrypt other passwords (Token Passwords etc). It is not stored

 Enter Password:
Retype Password:

  Enter the REST API Keystore Password
  ----------------------------------

  This is a password that protects the TLS REST API Keystore.
  This is only required if you are utilising TLS.

 Enter Password:
Retype Password:

  A backup of the original has been saved to ../config/serverconfig.properties.2026.10.29.10.24.17.650
  Ready to update properties file ../config/serverconfig.properties with the new data

Proceed? (y/n): y

  The properties file ../config/serverconfig.properties has been updated successfully.
```

<br>

### Setting TLS Keystore Passwords via the CLI

Give the key store whose password is to be set:

| Key store | Property | Menu option |
| --- | --- | --- |
| ``tls-client`` | ``tls.clientKeyStore.password`` | 15 |
| ``tls-trust`` | ``tls.trustStore.password`` | 16 |
| ``rest`` | ``server.restapi.tls.keyStore.password`` | 18 |
| ``rest-trust`` | ``server.restapi.tls.trustStore.password`` | 19 |

```
ezsign-manage.sh ../config/serverconfig.properties keystore-password set rest
```

```
Master password:
New rest key store password:
Retype the new rest key store password:
Set server.restapi.tls.keyStore.password, encrypted with the master password. Backup saved to serverconfig.properties.2026.10.29.10.22.09.677
Reload the server's configuration with the server control tool, or restart the server, to apply the change
```

<br>

## REST API Users

The users that may call the REST API are held in a users file, set by ``server.restapi.usersFile`` in the server properties.  Each user has one or more roles and one or more credentials:

- **API tokens** - the client sends the token as ``Authorization: Bearer <token>``.  Only a hash of the token is stored
- **Client certificates** - the client authenticates with the certificate over TLS.  The certificate must be issued by a CA in ``server.restapi.tls.trustStore``

Permissions take the form ``operation:channel/NAME`` e.g. ``sign:channel/SIGNING`` or ``verify:channel/*``.  The operations are ``sign``, ``verify``, ``verify.bypass``, ``encrypt``, ``decrypt``, ``random`` or ``*`` for all.  A role is a named set of permissions.  A user's permissions are those of their roles: permissions cannot be assigned to a user directly, so create a role for each set of permissions and assign it to the users that need it

The ``status`` permission, given on its own without a channel, allows the server status (``/v1/status``) to be read.  This returns the server's details and the number of calls made since it started, for monitoring.  It is only granted by ``status`` or by ``*`` on its own, so put it in its own role for a dedicated monitoring user rather than in the applications' roles e.g.

```
ezsign-manage.sh ../config/serverconfig.properties roles set monitor -p status
ezsign-manage.sh ../config/serverconfig.properties users add monitoring -d "Monitoring" -r monitor
```

<br>

### Signing the Users File

The users file is signed with an admin private key, so that someone able to change the file cannot grant themselves access.  The admin key should be kept separate from the server's master password and, ideally, off the server.  It is held in a password protected PKCS#12 (``.p12``, ``.pfx``) or JKS file.  RSA and EC keys are supported.  For example:

```
keytool -genkeypair -alias users-admin -keyalg RSA -keysize 3072 -validity 1095 -dname "CN=EzSign Users Admin,O=Example" -storetype PKCS12 -keystore users-admin.p12
keytool -exportcert -rfc -alias users-admin -keystore users-admin.p12 -file users-admin.cer
```

Copy only ``users-admin.cer`` to the server and set:

```
server.restapi.usersFile.signerCerts=../config/users-admin.cer
```

When ``signerCerts`` is set, the server only loads a users file that is signed by one of these certificates.  An unsigned, changed or older users file is refused

<br>

### Managing REST API Users via the Menu

Choose **option 17** to manage the users file.  If the users file does not exist you will be asked whether to create it.  The menu shows the users file, its version, the number of users and roles and whether the file's signature is valid:

```
  REST API Users
  --------------
  Users file: ../config/users.json
  Version 1, 1 user(s) (1 enabled), 1 role(s)
  Signature: valid, signed by CN=EzSign Users Admin,O=Krestfield Ltd
  
   1.  List users
   2.  Show user details
   3.  Add user
   4.  Enable or disable user
   5.  Delete user
   6.  Set user roles
   7.  Add API token to user
   8.  Add certificate to user
   9.  Remove token or certificate from user
  
   10. List roles
   11. Add or change role
   12. Delete role
  
   13. Save changes and sign
   14. Sign users file
   15. Discard unsaved changes
   16. Revert to a previous version
   17. Back
  
  Command:
```

Changes are checked as they are made and kept in memory until saved.  After each option the results are displayed until a key is pressed

A user's permissions come from their roles, so add the roles first.  To add a role, choose **option 11**:

```
  Role name: signer
  Permissions are operation:channel/NAME, e.g. sign:channel/FINANCE or verify:channel/*
  Operations: sign, verify, verify.bypass, encrypt, decrypt, random or * for all
  Use status on its own to allow the server status (/v1/status) to be read, e.g. by a monitoring user
  Permissions, comma separated (- for none, enter to keep none): sign:channel/SIGNING,verify:channel/SIGNING
  Role signer set to sign:channel/SIGNING, verify:channel/SIGNING
```

To add a user, choose **option 3**:

```
  User id (no spaces, e.g. finance-app): finance-app
  Description (optional): Finance system
  Available roles: signer
  Roles, comma separated (- for none, enter to keep none): signer
  User finance-app added. Add an API token (7) or certificate (8) so the user can authenticate
```

To add an API token to a user, choose **option 7**.  The token is displayed once and is not stored, so it must be copied and given to the client securely:

```
  User number or id: finance-app
  Label for the token, e.g. what uses it (optional): production
  
  API token for finance-app:
  
    ezs_XKMoerLT9U0udp_vDOV0fRA2hghZhaqD1g3NuNknwng
  
  Copy it now and give it to the client securely. It is not stored and cannot be shown again.
  The client sends it as: Authorization: Bearer <token>
  It can be used once the changes are saved, signed and loaded by the server.
```

To add a client certificate to a user, choose **option 8**.  Load the certificate file (PEM or DER) and choose how the server is to recognise it:

```
  User number or id: finance-app
  Certificate file (PEM or DER): ../certs/financeapp.cer
  Subject: C=GB,O=Krestfield Ltd,CN=Finance App
  Issuer:  C=GB,O=Krestfield Ltd,CN=Krestfield Issuing CA
  Serial:  6DE730050C7E13A2D99D2D0049034B21397CC8D2
  Expires: Fri Oct 29 10:14:18 UTC 2027
  
  How should the server recognise this certificate?
    1. SHA-256 fingerprint (only this certificate)
    2. SHA-1 thumbprint (only this certificate)
    3. Issuer and serial number (only this certificate)
    4. Subject and issuer (also renewed certificates with the same subject and issuer)
    5. Subject only (any trusted CA issuing a certificate with this subject)
  The certificate must also be issued by a CA in server.restapi.tls.trustStore
  Choice [1]: 1
  Label (optional): finance app cert
  Certificate added to finance-app: Certificate SHA-256 b900c1aa36266fef... - finance app cert
```

To view a user, choose **option 2**:

```
  User:        finance-app
  Description: Finance system
  Enabled:     yes
  Roles:       signer
  Permissions: sign:channel/SIGNING, verify:channel/SIGNING
  Credentials:
    1. API token (sha256 e31548e43cc8a401...) - production (created 2026-10-29)
    2. Certificate SHA-256 b900c1aa36266fef... - finance app cert
```

To save the changes, choose **option 13**.  The current users file is backed up, the new file is written with its version increased by one and you are offered to sign it with the admin key:

```
  Saved ../config/users.json (version 1)
  
  
  Sign the users file now with the admin key? (y/n): y
  Admin key store (.p12, .pfx or .jks): ../admin/users-admin.p12
  Admin key store password: 
  Admin certificate: CN=EzSign Users Admin,O=Krestfield Ltd (expires Sun Oct 28 10:14:22 UTC 2029)
  The users file has been signed. Signature written to ../config/users.json.sig
  Reload the server's users with the server control tool (reload), or restart the server, to apply the changes
```

The signature is written to ``users.json.sig``.  Then reload the server's users with the server control tool, or restart the server

**Option 16** lists the backups of previous versions and restores the one chosen.  The restored file is saved as a new version, because the server refuses a signed users file with a lower version than the one it has loaded.  The current file is backed up first, so a revert can itself be undone

<br>

### Managing REST API Users via the CLI

The users and roles commands do not need the master password.  Each change is saved straight away: the previous file is backed up, the version is increased by one and the file is checked as the server would

To add a role:

```
ezsign-manage.sh ../config/serverconfig.properties roles set signer -p sign:channel/SIGNING -p verify:channel/SIGNING
```

```
Creating a new users file ../config/users.json
Added role signer: sign:channel/SIGNING, verify:channel/SIGNING
Saved ../config/users.json (version 1)
The users file is not signed. The server will not load it until it is signed (users sign, or --sign with the change)
Reload the server's users with the server control tool, or restart the server, to apply the change
```

To add a user:

```
ezsign-manage.sh ../config/serverconfig.properties users add finance-app -d "Finance system" -r signer
```

```
Added user finance-app
Saved ../config/users.json (version 2). Previous version backed up to users.json.2026.10.29.10.22.11.718
The users file is not signed. The server will not load it until it is signed (users sign, or --sign with the change)
Reload the server's users with the server control tool, or restart the server, to apply the change
```

Roles are given with ``-r``, which may be repeated.  The user's permissions are those of their roles.  Add ``--disabled`` to add the user disabled

To add an API token to a user:

```
ezsign-manage.sh ../config/serverconfig.properties users add-token finance-app -l production
```

```
Added an API token to finance-app. The token is shown once and is not stored. The client sends it as: Authorization: Bearer <token>
Saved ../config/users.json (version 3). Previous version backed up to users.json.2026.10.29.10.22.12.454
The users file is not signed. The server will not load it until it is signed (users sign, or --sign with the change)
Reload the server's users with the server control tool, or restart the server, to apply the change
ezs_RtgiIhnL8fAP90FzrvlB05eF21QDu46z3Og7mDrR8LY
```

Only the token is written to the standard output, so that a script can capture it e.g.

```
TOKEN=$(ezsign-manage.sh ../config/serverconfig.properties users add-token finance-app -l batch 2>/dev/null)
```

To add a client certificate to a user:

```
ezsign-manage.sh ../config/serverconfig.properties users add-cert finance-app -c ../certs/financeapp.cer -l "finance app cert"
```

```
Added to finance-app: Certificate SHA-256 b900c1aa36266fef... - finance app cert
Saved ../config/users.json (version 5). Previous version backed up to users.json.2026.10.29.10.22.13.815
The users file is not signed. The server will not load it until it is signed (users sign, or --sign with the change)
Reload the server's users with the server control tool, or restart the server, to apply the change
```

By default the certificate is recognised by its SHA-256 fingerprint.  Use ``-m`` to choose another match: ``sha256``, ``sha1``, ``issuer-serial``, ``subject-issuer`` or ``subject``

To sign the users file with the admin key:

```
ezsign-manage.sh ../config/serverconfig.properties users sign --admin-keystore ../admin/users-admin.p12
```

```
Admin key store password:
Signed by CN=EzSign Users Admin,O=Krestfield Ltd. Signature written to ../config/users.json.sig
```

A change can also be signed in the same step by adding ``--sign --admin-keystore <file>`` e.g.

```
ezsign-manage.sh ../config/serverconfig.properties users disable finance-app --sign --admin-keystore ../admin/users-admin.p12
```

```
Disabled user finance-app
Saved ../config/users.json (version 6). Previous version backed up to users.json.2026.10.29.10.22.16.185
Admin key store password:
Signed by CN=EzSign Users Admin,O=Krestfield Ltd. Signature written to ../config/users.json.sig
Reload the server's users with the server control tool, or restart the server, to apply the change
```

The admin key store password is never passed on the command line.  It is read from the file given with ``--admin-password-file``, otherwise the ``EZSIGN_ADMIN_PASSWORD`` environment variable, otherwise it is prompted for.  Use ``--admin-key <alias>`` if the key store holds more than one key

To list the users, show a user and check the users file:

```
ezsign-manage.sh ../config/serverconfig.properties users list
ezsign-manage.sh ../config/serverconfig.properties users show finance-app
ezsign-manage.sh ../config/serverconfig.properties users status
```

```
finance-app (DISABLED)  roles: signer  tokens: 2  certificates: 1  - Finance system

User:        finance-app
Description: Finance system
Enabled:     NO
Roles:       signer
Permissions: sign:channel/SIGNING, verify:channel/SIGNING
Credentials:
  1. API token (sha256 305867b4440d3924...) - production (created 2026-10-29)
  2. API token (sha256 a0ef89bee4e21b32...) - batch (created 2026-10-29)
  3. Certificate SHA-256 b900c1aa36266fef... - finance app cert

Users file: ../config/users.json
Version:    6
Users:      1 (0 enabled)
Roles:      1
Signature:  valid, signed by CN=EzSign Users Admin,O=Krestfield Ltd
Backups:    5
```

``users list``, ``users show`` and ``roles list`` also accept ``--json`` for JSON output

To remove a token or certificate, give its number as shown by ``users show``:

```
ezsign-manage.sh ../config/serverconfig.properties users remove-credential finance-app 2
```

```
Removed from finance-app: API token (sha256 a0ef89bee4e21b32...) - batch (created 2026-10-29)
Saved ../config/users.json (version 8). Previous version backed up to users.json.2026.10.29.10.22.21.176
The users file is not signed. The server will not load it until it is signed (users sign, or --sign with the change)
Reload the server's users with the server control tool, or restart the server, to apply the change
```

To list the backups of previous versions and revert to one:

```
ezsign-manage.sh ../config/serverconfig.properties users backups
ezsign-manage.sh ../config/serverconfig.properties users revert 1
```

```
1. 2026.10.29.10.22.16.185  version 5, 1 user(s), saved 2026-10-29 10:22:13, replaced 2026-10-29 10:22:16, was signed
2. 2026.10.29.10.22.13.815  version 4, 1 user(s), saved 2026-10-29 10:22:13, replaced 2026-10-29 10:22:13, was not signed
...

Reverted to the backup 2026.10.29.10.22.16.185 (version 5). Saved as version 7. The previous file was backed up first
The users file is not signed. The server will not load it until it is signed (users sign, or --sign with the change)
Reload the server's users with the server control tool, or restart the server, to apply the change
```

``users revert`` with no backup lists the backups and asks which to restore.  As for the menu, the backup is saved as a new version and must then be signed

Every save keeps a backup, so they build up over time.  ``users prune-backups --keep N`` deletes all but the newest N backups.  Use ``--dry-run`` first to see what would be deleted:

```
ezsign-manage.sh ../config/serverconfig.properties users prune-backups --keep 2 --dry-run
```

```
Would delete 2026.10.29.10.22.13.815  version 4, 1 user(s), saved 2026-10-29 10:22:13, replaced 2026-10-29 10:22:13, was not signed
...
Would delete 4 of 6 backup(s), keeping the newest 2. Nothing was deleted (--dry-run)
```

The full set of users and roles commands is:

```
users list [--json]
users show <user> [--json]
users add <user> [-d <description>] [-r <role>]... [--disabled]
users enable|disable|delete <user>
users set-roles <user> [-r <role>]...
users add-token <user> [-l <label>]
users add-cert <user> -c <certFile> [-m sha256|sha1|issuer-serial|subject-issuer|subject] [-l <label>]
users remove-credential <user> <number>
users status
users sign --admin-keystore <file>
users backups [--json]
users revert [<number or timestamp>]
users prune-backups --keep <number> [--dry-run]
roles list [--json]
roles set <role> -p <permission> [-p <permission>]...
roles delete <role>
```

<br>

### Signing on Another Machine

So that the admin key can be kept off the server, the users file can be signed on another machine.  Copy ``users.json`` to that machine and run the following, which does not need the server properties file:

```
ezsign-manage.sh sign-users-file users.json --admin-keystore users-admin.p12 --trusted-cert users-admin.cer
```

```
Admin key store password:
Signed users.json (version 8, 1 user(s)) with CN=EzSign Users Admin,O=Krestfield Ltd. Signature written to users.json.sig
```

Then copy ``users.json`` and ``users.json.sig`` back to the server.  Passing the admin certificate with ``--trusted-cert`` checks that you are signing with the key the server trusts

To change the admin key, add the new certificate to ``signerCerts`` (comma separated), sign with the new key, then remove the old certificate

<br>

## Changing the Master Password

To change the master password choose **option 20**.  Every value encrypted with the master password (the token passwords, authentication codes and keystore passwords) is decrypted and re-encrypted with the new master password, and the ``masterPassword.check`` value is updated.  Nothing is changed unless every value decrypts with the current master password.  The new master password must be at least 8 characters

```
  Change Master Password
  ----------------------
  Every value encrypted with the master password is re-encrypted with the new one.
  
  New master password: 
  Retype the new master password: 
  
  The master password has been changed. Re-encrypted 5 value(s): channel.1.token.password, channel.2.token.password, server.authCode, server.ctrl.authCode, server.restapi.tls.keyStore.password
  A backup of the previous properties file was saved alongside it.
  
  Now update the master password used to start the server (the start script, password file or
  EZMASTERPASS environment variable), then restart the server.
```

Then update the master password used to start the server and restart it

If the master password has been lost, it cannot be changed this way.  Instead, start the menu with the new master password and choose to continue (see [Checking the Master Password](#checking-the-master-password)).  Then set each password again, e.g. with option 1.  When the first is set, you will be asked to confirm that the new master password should replace the old one:

```
  This is not the master password this configuration uses (masterPassword.check).
  It does not decrypt: channel.2.token.password, server.restapi.tls.keyStore.password
  To change the master password and keep the existing values, use Change Master Password instead.
  
    1. Cancel
    2. Make this the master password (reset). The values it does not decrypt must be set again
  Choice:
```

<br>

### Changing the Master Password via the CLI

```
ezsign-manage.sh ../config/serverconfig.properties master-password change
```

```
Master password:
Change Master Password
----------------------
Every value encrypted with the master password is re-encrypted with the new one.

New master password:
Retype the new master password:

The master password has been changed. Re-encrypted 5 value(s): channel.1.token.password, channel.2.token.password, server.authCode, server.ctrl.authCode, server.restapi.tls.keyStore.password
A backup of the previous properties file was saved alongside it.

Now update the master password used to start the server (the start script, password file or
EZMASTERPASS environment variable), then restart the server.
```

The current master password is checked first.  A password file given with ``-f`` must then be updated with the new master password
