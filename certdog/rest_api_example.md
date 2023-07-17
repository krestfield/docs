---
layout: default
title: REST API Examples
parent: Certdog
nav_order: 31
---



# REST API Examples

The following demonstrate how to make a simple API calls to obtain certificates and view certificate details  

For the full API refer to the documentation [here](rest_api_overview.html)



The online version of the API documentation (available 8am - 8pm UK time) is available [here](https://certdog.net/certdog/api/swagger-ui/index.html)

You may test against this version, using the following credentials:

* Username: ``certdogtest``

* Password: ``password``



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
Authorization: Bearer {token}
```

e.g.

```json
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9....sdUfWLrtZPRGiQSA
```

<br>

To run this via the Swagger UI available [here](https://certdog.net/certdog/api/swagger-ui/index.html), perform the following:

Locate the **login-controller** and click on the "**POST** ``/certdog/api/login``" entry. Click **Try it out**

For password, replace ``"string"`` with ``"password"``. For username, replace ``"string"`` with ``"certdogtest"`` i.e.:

<img src="./images/image-20230717095938562-1689584386402-1.png" alt="image-20230717095938562" style="zoom: 80%;" />

Click the **Execute** button. In the *Server response* section below, you will see the token:

<img src="./images/image-20230717100109248.png" alt="image-20230717100109248" style="zoom: 80%;" />

Copy the value for *token* (without the enclosing quotes), go to the top of the page and click **Authorize** and enter this value as the JWT (apiKey). Click **Authorize**, then **Close**.

Now you can go to any of the other API calls and click **Try it out**. E.g. go to certificates-controller, click "**GET** ``/certdog/api/certs``" and click **Execute**. This will return all certs in the system

<br>

### Get a Cert as PKCS12

Requests a certificate from the DN (Distinguished Name)  

Certdog generates a CSR and issues the certificate from the CA issuer referred to by the caName parameter

PKCS#12 data is returned as Base64 which contains the issued certificate and the generated private key

```json
POST: https://certdog.net/certdog/api/certs/request
{
    "caName" : "Certdog TLS",
    "dn"  : "CN=server1.com",
    "teamName" : "Test Team",
    "csrGeneratorName" : "RSA2048",
    "p12Password" : "password",
    "subjectAltNames" : ["DNS:server1.com", "DNS:server2.com"],
    "extraEmails" : ["certs@krestfield.com"],
    "extraInfo" : "Resides in datacentre 111"
}
```

* **caName** is the Certificate Issuer as displayed in the UI
* **dn** is the requested Distinguished Name
* **teamName** must be provided if the authenticated user is a member of more than one team. If only a member of one team then the certificate will be associated with that team
* **csrGeneratorName** the name of the CSR Generator
* **p12Password** must be ASCII
* **subjectAltNames** is optional. If required, supply as a string array. Types can be 
  * **DNS** for a DNS entry e.g. "DNS:server2.com"
  * **EMAIL** for an email address e.g. "EMAIL:certs@krestfield.com"
  * **IP** for an IP Address e.g. "IP:192.44.17.221"
  * **URI** for a URI address e.g. "URI:https://server2.com"
* **extraEmails** is optional. If included these email addresses will also be sent reminder emails
* **extraInfo** is optional

<br>

<u>Returns</u>

```json
{
    "certId": "608292ed7e87646928628cd2",
    "pemCert": "-----BEGIN CERTIFICATE-----MIIDVTCCA...RCMOT4=-----END CERTIFICATE-----\r\n",
    "p12Data": "MIINkQIBAzC...OIwsHbBgIDAYag"
}
```

The p12Data contains the keys and certificates, encrypted under the password provided in the call (p12Password), base64 encoded

<br>

### Get a Cert from a CSR

Issues a certificate from the provided CSR data

```json
POST: https://certdog.net/certdog/api/certs/requestp10
{
    "caName" : "Certdog TLS",
    "teamName" : "Test Team",
    "csr"  : ""-----BEGIN CERTIFICATE REQUEST-----MIIChz...XOM3c-----END CERTIFICATE REQUEST-----",
```

* **caName** is the Certificate Issuer as displayed in the UI
* **teamName** must be provided if the authenticated user is a member of more than one team. If only a member of one team then the certificate will be associated with that team
* **csr** is the PEM CSR data or base64 encoded CSR data
<br>
<u>Returns</u>

```json
{
    "certId": "61ee876f326d6e636e46306b",
    "pemCert": "-----BEGIN CERTIFICATE-----MIIDVTCCA...RCMOT4=-----END CERTIFICATE-----\r\n"
}
```

<br>

### Get Certificate Details

Returns the data stored for a certificate given the certificate ID (the *certId* returned from one of the previous calls)

```json
GET https://certdog.net/certdog/api/certs/61ee876f326d6e636e46306b
```

Returns

```json
{
    "id": "61f412f7778c854398f0c59d",
    "caId": "61ef0c0edd22dc42704cf380",
    "localCaId": "61ef0beedd22dc42704cf37c",
    "csrId": "61f412f7778c854398f0c59c",
    "pemCert": "-----BEGIN CERTIFICATE-----\r\nMIIDUzC...qPAISd\r\n-----END CERTIFICATE-----\r\n",
    "commonName": "test1.server1.com",
    "subjectDn": "CN=test1.server1.com, O=Krestfield, C=GB",
    "issuerDn": "CN=Krestfield Issuing CA, O=Krestfield, C=GB",
    "issuerCertId": "608292ed7e87646924626cd9",
    "serialNumber": "2bb767253fe02946013f72d39e886b80",
    "signatureAlgorithm": "RSA",
    "hashAlgorithm": "SHA-256",
    "keyUsages": [
        "Digital Signature",
        "Key Encipherment"
    ],
    "enhancedKeyUsages": [
        "Server Authentication"
    ],
    "subjectAlternativeNames": [],
    "validFrom": "2022-01-28T15:59:51.000+00:00",
    "validTo": "2023-01-28T15:59:51.000+00:00",
    "validFromStr": "2022-01-28 15:59:51",
    "validToStr": "2023-01-28 15:59:51",
    "ownerUserId": "61ef0b76ae9da81f540b9eda",
    "ownerUsername": "admin",
    "teamId": "61ef0b780031e41d5c95453f",
    "active": true,
    "renewed": false,
    "renewedByCertId": null,
    "renewsCertId": null,
    "revoked": false,
    "history": [
        {
            "timestamp": "2022-01-28T15:59:51.541+00:00",
            "timestampStr": "2022-01-28 15:59:51.541",
            "event": "created",
            "details": "Certificate created by user admin. A CSR was provided"
        }
    ],
    "extraDetails": null,
    "extraEmails": null,
    "trackExpiry": true,
    "isCa": false,
    "hasKeyData": false,
    "imported": false,
    "importTime": null,
    "aias": [],
    "cdps": [],
    "thumbprint": "5e34950586d8d2d73d7f8245441bb72879d33790",
    "policies": [],
    "keySize": "2048",
    "eccCurve": null,
    "msTemplateName": null,
    "daysToExpiry": 364.99988
}
```

