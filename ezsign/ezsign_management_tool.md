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
- Importing Certificates
- Importing existing HSM keys
- Deleting Certificates
- Displaying Certificates
- Generating AES Keys
- Displaying AES Keys
- Deleting AES Keys
- Translating Keystore Objects from an old password to new
- Setting the Authentication Code
- Setting TLS Passphrases

<br>

The server will not start until the token passwords have been set and you will be unable to sign or verify signatures until the required keys and certificates have been generated and imported.  Encrypting and decrypting requires an AES key to be generated.  Therefore, the Management tool must usually be run before the server can be started (if you are duplicating configurations there is no need to re-run the tool)

<br>

## Starting

To start the management utility, run the following script which requires that the server properties file is passed as a parameter e.g.

```
ezsign-manage.sh server.properties
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



Type the *Master Password* and press enter.  This will then display the menu:

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
    10.  Display AES Keys
    11.  Delete AES Key

    12.  Translate Keystore Objects
    13.  Display all Channel Objects
    14.  Set Authentication Code

    15.  Set TLS Client Keystore Password
    16.  Set TLS Trust Keystore Password

    17.  Exit

Command:
```

<br>

## Setting Master and Token Passwords

To set the Master and Token passwords for a channel choose **option 1**.  You will then be prompted to choose the channel, enter the Master Password and Token Passwords and then whether you want to write the new data to the properties file.  This option must be run before the server is started in order to encrypt the Token Passwords

```
  Channels
  --------

    1. TEST
    2. TechTest1
    3. TechTest2

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
  For PKCS#11 tokens, this is the token PIN/Password used to authenticate, 
      also referred to as the operator password
  For HSM9000 tokens, this is password is used to re-encrypt the local keys 
     (although they are already encrypted under the HSM Master Key)
  This password is stored in the configuration, encrypted under the master password

 Enter Password:
 Retype Password:

  A backup of the original has been saved to ..\test.properties.2026.01.12.09.03
  Ready to update properties file ..\test.properties with the new passwords

Proceed? (y/n): y

  The properties file ..\test.properties has been updated successfully.
```

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

The token password must then be entered to proceed

<br>

## Generating a CSR

To generate a CSR (Certificate Signing Request) choose **option 2**.  You will be prompted to enter the selected channel again, then requested DN (Distinguished Name), key size and the filename to store the CSR

```
Generating CSR for channel TEST

Distinguished Name: CN=Test,O=Krestfield Ltd,C=GB

CSR Filename: krestfield.p10

Generated CSR Data:
-----BEGIN CERTIFICATE REQUEST-----
MIICYTCCAUkCAQAwHjEPMA0GA1UEAwwGVGVzdC5PMQswCQYDVQQGEwJHQjCCASIwDQYJKoZIhvcN
AQEBBQADggEPADCCAQoCggEBAIMvY7RaJtHTz2jB7Nfqb2OLANmjOqACybd5FSlwFxvCSjTzoRoG
Y97aFWldDHueyVLmKKJtYMScTIs1gZSvm9guUpOhVsvQ0KaX58ZFMmRvlmeBlP2rbQIe0F1Fp724
XggI/5dXr9OKVbdIWrJkZTsFYn8bXU7nY1MAuRl5NK6CSkl6XZTvODRezL9ioFmkE09EWP4wIKyQ
zQW0Z/mn7a51eiJA+utBf3MgtUkmEzTc8Z73xrGflwt0fCnghs1gXnHNlZMkiR3l1iOPV/ppQ9l2
FsVv85JFk4eMJxP1cp+niEtoTFIc49JF/nB4u+B1aslnBBimn2oMzD/gItOdCc0CAwEAATANBgkq
hkiG9w0BAQsFAAOCAQEAYh4erwAkHL+ZuHMRcOmufK9ZJCxLXgbF2DjCgCC53xMuNwiQ7wIL6at6
N1jK8v4WlIaRE1WRSOO7k7OG3MwXBtDy3oVmr5NWEKu0WSVbwM/7mVjkczuBxLXdr/pEeyH9Nm02
h3kH0sO25xt5BjoCzcoHIYmmHxa5tyzjchqTE5Fw68S/7rusodvAbEwNKYQQhHTCwAzuusGDxb0D
+JHNTk63zenDHw56pcURsvmA16BSXF30MatVcoTd7elqmAho+yUm0c0CVOfGoH2zFv7jcyl8jDtm
w3Kg45sND7L2A9hII0QGy3L+seE/GpMaoxhhDBPxbIfAkqecxyapA+aX3w==
-----END CERTIFICATE REQUEST-----

CSR written to krestfield.p10
```

The CSR should then be processed by the CA who will issue the certificate.  Once the certificate has been issued the Import Certificate option can be chosen to import the certificates

<br>

## Importing Certificates

To import root certificates or certificates issued from a CSR choose option 3.  You will then be prompted for the channel and a path to the certificate.  

```
  Channels
  --------

    1. TEST

Select Channel Number: 1

Path to certificate: /opt/ezsign/certs/signing.cer

Certificate imported successfully
```

if the certificate is associated with a private key on the token, you will also be prompted if you wish to set this as the new signing certificate:

```
Do you wish to set this as the default signing certificate? (y/n): y
  A backup of the original has been saved to ..\samples\test.properties.2026.01.12.11.00
  Ready to update properties file ..\samples\test.properties with the new passwords
Proceed? (y/n): y

The properties file ..\samples\test.properties has been updated successfully.
```

Choosing y will result in the properties file being updated.  If you do not wish to set this as the signing certificate now, you can do this later by running option **5. Set Signing Key**

Note that for signing certificates, all certificates in the path must be imported

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

## Setting the Signing Key

To set the default signing key (that is the key that will be used to sign data), choose **option 5**.  You will then be presented with a list of available certificates which have associated private keys and can therefore be used to sign data.  Note: a certificate will not be available for signing if there is not a complete path for that certificate

```
  Current Signing Certificate:
  ----------------------------

       Subject: CN=Test Cert 1, O=Krestfield Ltd, C=GB
       Issuer : CN=Krestfield Test CA, OU=Engineering, O=Krestfield Ltd, C=GB
       Valid From: Wed Oct 12 08:12:48 BST 2026
       Valid To  : Thu Oct 12 08:12:48 BST 2027
       Serial Number: 5b000000348a17f73059f07217000000000034


  Available Signing Certificates:
  -------------------------------

    1. Subject: CN=Test Cert 2, O=Krestfield Ltd, C=GB
       Issuer : CN=Krestfield Test CA, OU=Engineering, O=Krestfield Ltd, C=GB
       Valid From: Wed Nov 12 18:12:48 BST 2026
       Valid To  : Thu Nov 12 18:12:48 BST 2027
       Serial Number: 5b000000348a17f73059f07217000002010F13


Select Certificate Number: 1

  A backup of the original has been saved to ..\test.properties.2016.10.12.09.28
  Ready to update properties file ..\test.properties with the new passwords

Proceed? (y/n): y

  The properties file ..\test.properties has been updated successfully.
```

<br>

## Displaying and Deleting Certificates

**Options 6, 7 and 8** are used to delete and display the available certificates.  When certificates are displayed they are shown in the following format

```
Current Signing Certificates:
  -----------------------------

    1. Subject: CN=Test 1, O=Krestfield Ltd, C=GB
       Issuer : CN=Krestfield Test CA2, OU=Engineering, O=Krestfield Ltd, C=GB
       Valid From: Wed Oct 12 08:12:48 BST 2016
       Valid To  : Thu Oct 12 08:12:48 BST 2017
       Serial Number: 5b000000348a17f73059f07217000000000034
    
    2. Subject: CN=Krestfield Test CA2, OU=Engineering, O=Krestfield Ltd, C=GB
       Issuer : CN=Krestfield Test Root CA2, OU=Engineering, O=Krestfield Ltd, C=GB
       Valid From: Fri Dec 04 08:22:54 GMT 2015
       Valid To  : Thu Nov 29 08:22:54 GMT 2035
       Serial Number: 3e00000002254212210f37d14f000000000002
    
    3. Subject: CN=Krestfield Test Root CA2, OU=Engineering, O= Krestfield Ltd, C=GB
       Issuer : CN=Krestfield Test Root CA2, OU=Engineering, O= Krestfield Ltd, C=GB
       Valid From: Thu Dec 03 09:13:47 GMT 2015
       Valid To  : Wed Dec 03 09:23:47 GMT 2036
       Serial Number: 5de549fbaf4b14b141d63d3c631b27c0


  Other Certificates:
  -------------------

    4. Subject: CN=Krestfield Test Root CA1, OU=Engineering, O=Krestfield Ltd, C=GB
       Issuer : CN=Krestfield Test Root CA1, OU=Engineering, O=Krestfield Ltd, C=GB
       Valid From: Thu Nov 03 09:13:47 GMT 2015
       Valid To  : Wed Nov 03 09:23:47 GMT 2036
       Serial Number: 5de549abaf4b14b141d63d3c631bde54


```

The first section displays the *Current Signing Certificates*.  This is based on the selected signing key and displays the complete path.  

The second sections displays all other certificates which are stored but not included in the current signing path

<br>

## Generating AES Keys

Choose **option 9** to generate an AES key.  Enter the key size and the key label as follows:

```
Enter AES Key Size (128, 192 or 256): 256

Enter a unique label for this key: key10

AES key generated OK
```

Once the key has been created it can be used to encrypt and decrypt data via the client, where the label set above must be specified to select this key

<br>

## Displaying and Deleting AES Keys

AES keys can be displayed and deleted by choosing **options 10 and 11**

```
  Current AES Keys:
  -----------------------------

       #    Key Size   Date Created         Label
       ---  --------   -------------------  --------
         1  128bits    11-3-2017 17:16:45   key2
         2  256bits    13-3-2017 21:33:00   testkey5
         3  192bits    11-3-2017 17:14:52   key1
         4  256bits    19-3-2017 09:20:26   key10
         5  256bits    11-3-2017 17:17:05   key3
```

Key details will be shown including the key size, date created and associated label

<br>

## Translate KeyStore Objects

If you wish to translate keystore objects from one token password to another.  For example, when refreshing passwords for software tokens or if an HSM’s objects have been translated to another operator cardset, choose **option 12**

You will be prompted to choose the channel and then enter the current token password

```
  Please enter the current token password

 Enter Password:
 Retype Password:


Then enter the new token password.  This is the new password or new operator cardset passphrase:

  Please enter the NEW token password

 Enter Password:
 Retype Password:

Objects have been translated to the new password successfully
A backup was made of the original objects and stored in the SIGN keystore folder
```

The objects will be translated and re-encrypted under the new password.  The pre-translated objects will be backed up to a timestamped folder within the keystore directory e.g. /20261101_1015_BACKUP

<br>

## Display KeyStore Objects

To display all the objects stored within a channel, select option 13, then enter the channel

All objects details will be displayed indicating what type of object they are (i.e. private key, certificate etc), the ID and filename e.g.

```
  Current Objects:
  ----------------

  Object ID: 15fbc93ade39910
  Created  : Tue Nov 14 22:08:35 GMT 2026
  Type     : CERTIFICATE
    Subject: CN=Krestfield CA, OU=PKI Services, O=Krestfield Ltd, C=GB
    Issuer : CN=Krestfield Root, OU=PKI Services, O=Krestfield Ltd, C=GB
    Serial Number: 380000000e3308b4434ca3142100000000000e
  Filename : 15fbc93ade39910.cer

  Object ID: 15fbc93956f0472
  Created  : Tue Nov 14 22:08:29 GMT 2026
  Type     : CERTIFICATE
    Subject: CN=Krestfield Root, OU=PKI Services, O=Krestfield Ltd, C=GB
    Issuer : CN=Krestfield Root, OU=PKI Services, O=Krestfield Ltd, C=GB
    Serial Number: 5f0609d62d60709e45c1051774a13021
  Filename : 15fbc93956f0472.cer

  Object ID: PRVK:CC035985F170B51460A3B659523A8D757AD0CBCD
  Created  : Thu Apr 05 22:03:12 BST 2026
  Type     : PRIVATE KEY
  Filename : PRVK_CC035985F170B51460A3B659523A8D757AD0CBCD.priv

  Object ID: PUBK:13996A889E52A844660D083D631EE0F30405C576
  Created  : Tue Nov 14 22:08:35 GMT 2026
  Type     : CERTIFICATE
    Subject: CN=SSAS Cert, O=Krestfield, C=GB
    Issuer : CN=Krestfield CA, OU=PKI Services, O=Krestfield Ltd, C=GB
    Serial Number: 450000000716edae60376f2200000000000007
  Filename : PUBK_13996A889E52A844660D083D631EE0F30405C576.cer
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

Enter Choice: 1
  A backup of the original has been saved to ..\config\config.properties.2026.01.05.12.23
```

The server configuration will be updated and a backup made

<br>

## Setting TLS Keystore Passwords

If utilising TLS to communicate with an HSM (e.g. a payShield) then you will need to configure a Trust Key Store (a key store where the CA certificates are stored) and optionally a Client Key Store (that will hold the client authentication certificate)

Select **options 15 and 16** to set these passwords

