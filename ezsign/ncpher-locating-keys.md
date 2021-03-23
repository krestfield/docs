---
layout: default
title: nCipher HSM - Locating Keys
parent: EzSign
nav_order: 40
---

# Locating Keys on nCipher HSMs



EzSign stores references to keys on an HSM locally within the channel folder of the keystore directory.  A typical listing of files in a channel folder may yield:

>   **15acca536498950**.cer  
>   **15acca536498950**.priv  
>   **15acca536498950**.pub  
>   15adcb5a5bc0779.cer  
>   15adcb5fb0e2532.cer  
>   15adcb61fef5373.cer   


(The bold text is explained later)

 

The Thales nCipher HSM stores keys within its own local keystore on the filesystem e.g. at ``/opt/nfast/kmdata/local/`` and a listing of files in this directory will show many files e.g.:

> card_725e1d27135c1b5dbb296f63be079fa827cf65fd_1  
> card_725e1d27135c1b5dbb296f63be079fa827cf65fd_2  
> cards_725e1d27135c1b5dbb296f63be079fa827cf65fd  
> key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-287c2f4c7d0cbfc2baa0dd0bc5a37e98c32b07e5  
> key_pkcs11_**uc725e1d27135c1b5dbb296f63be079fa827cf65fd-c17a0a33699c0f123c25525ce741cee8aeaca9bd**  
> key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-e3f641fea6ea9dcabc7a9d53fc671c468eddf05a  
> key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-f87af6c580d76302635be9c04bf16af3e113a17d  
> key_pkcs11_ucd4be65d640abecaf94668b3d96a5255ea58965eb-2bb6488690c6d721c3c4d6f817c6b08972e700ff  
> key_pkcs11_ucd4be65d640abecaf94668b3d96a5255ea58965eb-500b030ebb6bc2ddd7f2ac625d92c38bbe6b14da  
> key_pkcs11_ucd4be65d640abecaf94668b3d96a5255ea58965eb-569bc7bde55ca9bb0503358b4deb0fdd6362056a  
> key_pkcs11_ucd4be65d640abecaf94668b3d96a5255ea58965eb-b6183678323e8af7076beb58609b74e01576ee9b  
> key_pkcs11_ucd4be65d640abecaf94668b3d96a5255ea58965eb-d8fd60032c7324e2ed773882419c41d3fbbbba0e  
> module_DF21-826F-BCFD  
> world  

(Note the bold section)



It is possible to determine what each file in the keystore relates to what key on the HSM by running the following commands

 

## Commands
To determine what key an HSM file contains run this command from the ``nfast/bin`` directory:

```shell
/opt/nfast/bin/cklist
```

Or on windows:

```shell
C:\Program Files (x86)\nCipher\nfast\bin\cklist.exe
```

You will be prompted to enter the operator cardset passphrase (if using an operator cardset)

 

This will output a list of keys together with their details (the output can be quite long)

> CKA_CLASS CKO_PRIVATE_KEY  
> CKA_TOKEN true  
> CKA_PRIVATE true  
> CKA_MODIFIABLE true  
> CKA_LABEL "**15acca536498950**"  
> CKA_NFKM_APPNAME "pkcs11"  
> CKA_NFKM_ID "**uc725e1d27135c1b5dbb296f63be079fa827cf65fd-c17a0a33699c0f123c25525ce741cee8aeaca9bd**"  
> CKA_NFKM_HASH length 20  
> { 36B58085 0F01F349 6177AF40 1B5F3730 434974BE }  
> CKA_KEY_TYPE CKK_RSA  
> CKA_ID length 20  
> { D019A879 EF8ABF30 8C6BE3F4 EC574CD2 0B43D555 }  
> ...  
>
> CKA_CLASS CKO_PUBLIC_KEY  
> CKA_TOKEN true  
> CKA_PRIVATE false  
> CKA_MODIFIABLE true  
> CKA_LABEL "**15acca536498950**"  
> CKA_NFKM_APPNAME "pkcs11"  
> CKA_NFKM_ID "**uc725e1d27135c1b5dbb296f63be079fa827cf65fd-c17a0a33699c0f123c25525ce741cee8aeaca9bd**"  
> CKA_NFKM_HASH length 20  
> { 36B58085 0F01F349 6177AF40 1B5F3730 434974BE }  
> CKA_KEY_TYPE CKK_RSA  
> CKA_ID length 20  
> { 85CF8C06 525BD109 584983CF 89AE8B75 A31B67B7 }  
> ...  



Notice that the CKA_LABEL values match the EzSign channel keystore filenames i.e.

> **15acca536498950**.cer  
> **15acca536498950**.priv  
> **15acca536498950**.pub  

And the CAK_NFKM_ID text matches the filenames in the ``/kmdata/local`` directory i.e.

>  key_pkcs11_**uc725e1d27135c1b5dbb296f63be079fa827cf65fd-c17a0a33699c0f123c25525ce741cee8aeaca9bd**  



### Making the Connection 

This highlights the connection between the nCipher file and the EzSign keystore files, in that the nCipher file: 

> key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-c17a0a33699c0f123c25525ce741cee8aeaca9bd  

contains the public and private keys referenced by these EzSign keystore files:

> 15acca536498950.priv  
> 15acca536498950.pub  

The other files in the EzSign keystore, i.e.:  

> **15acca536498950**.cer  
> 15adcb5a5bc0779.cer  
> 15adcb5fb0e2532.cer  
> 15adcb61fef5373.cer  

Relate to certificates.  Note that one of the entries (highlighted above) contains the same name (15acca536498950) as the .priv and .pub files (but with the .cer extension). 

This indicates that this is the signing certificate - the certificate which is associated with the public (.pub file) and private (.priv file) key pair with the same name  

The other files may relate to other certificates (e.g. intermedaite CA and root CA certificates) that would have also been imported  

 

## Verifying Keystores 

You can use this method to confirm that your local nCipher installation includes all of the required keys that are being referenced by EzSign  

If you are copying configurations between servers, forgetting to also copy the required HSM files can result in errors such as:  

```shell
ERROR EzSignLog - There was an error checking a certificate for an associated key. 
Could not get public key.  There was an error obtaining the public key.  
Could not locate stored key ID on the HSM.  The key object may have been removed from the HSM  
```



Using the filenames from the example above, this would indicate that EzSign has the following files in its keystore e.g.   

> 15acca536498950.cer  
> 15acca536498950.priv  
> 15acca536498950.pub  

But the nCipher file:

> key_pkcs11_uc725e1d27135c1b5dbb296f63be079fa827cf65fd-c17a0a33699c0f123c25525ce741cee8aeaca9bd  

Is not present (has not been copied across or been deleted)

This can also be caused when generating a CSR on one machine and attempting to import the certificate into another without first copying the nCipher files across

 

To avoid errors such as this, always backup or copy the EzSign keystore files together with the nCipher security world files

When migrating to another machine, ensure it references the same HSM or the HSM is in the same Security World

