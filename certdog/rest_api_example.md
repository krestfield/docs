---
layout: default
title: REST API Example
parent: Certdog
nav_order: 31
---



# REST API Example

The following demonstrates how to make a simple API call to obtain a certificate as a PKCS#12

### Login

Before any operations can be performed a user must authenticate

```json
POST: https://certdog.net/certdog/api/login
{
    "username": "certdogtest",
    "password": "password"
}
```

Returns:

```json
{
    "username": "certdogtest",
    "token": "eyJhbG...BJnNA"
}
```

The *token* value returned must be added to the *Authorization* header of subsequent calls:

```json
Authorization: Bearer {{token}}
```





### Get a Cert as PKCS12

```json
POST: https://certdog.net/certdog/api/certs/request
{
    "caName" : "Certdog TLS",
    "dn"  : "CN=server1.com",
    "teamName" : "Test Team",
    "csrGeneratorName" : "RSA2048",
    "p12Password" : "password",
    "extraInfo" : "Resides in datacentre 111"
}
```

Returns

```json
{
    "certId": "608292ed7e87646928628cd2",
    "p12Data": "MIINkQIBAzC...OIwsHbBgIDAYag"
}
```

The p12Data contains the keys and certificates, encrypted under the password provided in the call (p12Password), base64 encoded



### Get the Certificate Details

```json
GET https://certdog.net/certdog/api/certs/608292ed7e87646928628cd2
```

Where 608292ed7e87646928628cd2 is the *certId* returned from the previous call

Returns

```json
{
    "id": "608292ed7e87646928628cd2",
    "caId": "6081c3ba7e87646928628c6e",
    "csrId": "608292ed7e87646928628cd1",
    "pemCert": "-----BEGIN CERTIFICATE-----\nMIIDSDCCA...NnykrKqyy+wA==\n-----END CERTIFICATE-----\n",
    "commonName": "server1.com",
    "subjectDn": "CN=server1.com",
    "issuerDn": "CN=Certdog Test CA, O=Krestfield",
    "serialNumber": "23c64ca9f566ad2545c03ea9ed992cc4",
    "signatureAlgorithm": "RSA",
    "hashAlgorithm": "SHA-256",
    "keyUsages": [
        "Digital Signature",
        "Key Encipherment"
    ],
    "enhancedKeyUsages": [
        "Server Authentication",
        "Client Authentication"
    ],
    "subjectAlternativeNames": [],
    "validFrom": "2021-03-23T09:27:09.000+0000",
    "validTo": "2022-03-23T09:27:09.000+0000",
    "validFromStr": "2021-03-23 09:27:09",
    "validToStr": "2022-03-23 09:27:09",
    "ownerUserId": "604ba413edd31279d221aa80",
    "ownerUsername": "certdogtest",
    "teamId": "604ba427edd31279d221aa82",
    "status": 1,
    "history": [
        {
            "timestamp": "2021-03-23T09:27:09.159+0000",
            "event": "created",
            "details": "Certificate created by user certdogtest. The system generated a CSR on the user's behalf"
        }
    ],
    "extraDetails": "Resides in datacentre 111",
    "extraEmails": null,
    "daysToExpiry": 364.99884
}
```

