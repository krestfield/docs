---
layout: default
title: EzSign - REST API
parent: EzSign
nav_order: 12
---

# REST API

<br>

From version 4.6.0 the EzSign Server can offer a REST API alongside the socket interface.  Applications can sign, verify, encrypt, decrypt and generate random data by calling the server over HTTPS with JSON, without the EzSign client

The REST API runs inside the server process.  No separate web server or additional software is needed

**[Open the REST API Reference](rest-api/index.html)** for every endpoint, request and response field, error code and example.  The reference can also be downloaded as an [OpenAPI 3.1 file](rest-api/openapi.yaml), which can be imported into Postman, Swagger Editor or other OpenAPI tools

<br>

## Endpoints

| Method and path | Permission | Description |
| --- | --- | --- |
| ``POST /v1/channels/{channel}/sign`` | ``sign`` | Sign data |
| ``POST /v1/channels/{channel}/verify`` | ``verify`` | Verify a PKCS#7 or raw signature |
| ``POST /v1/channels/{channel}/encrypt`` | ``encrypt`` | Encrypt data with an AES key |
| ``POST /v1/channels/{channel}/decrypt`` | ``decrypt`` | Decrypt data |
| ``POST /v1/channels/{channel}/random`` | ``random`` | Generate random data |
| ``GET /v1/health`` | none | Check the REST API is running |
| ``GET /v1/whoami`` | any user | Show the authenticated user and their permissions |
| ``GET /v1/status`` | ``status`` | The server status and the number of calls made on each channel |

Request and response bodies are JSON, with binary values (data, signatures and certificates) base64 encoded.  Requests must have the header ``Content-Type: application/json``

Every response includes an ``X-Transaction-Id`` header.  The same ID is written to the server log, so a request can be traced from the client to the server

<br>

## Enabling the REST API

The REST API is configured in the server properties file:

| Property | Default | Description |
| --- | --- | --- |
| ``server.restapi.enabled`` | ``false`` | Enables the REST API |
| ``server.restapi.port`` | (required) | The port to listen on e.g. ``8443`` |
| ``server.restapi.bindIpAddress`` | all addresses | The address to listen on |
| ``server.restapi.allowedSourceIpAddresses`` | any | Comma separated client addresses permitted to connect |
| ``server.restapi.threadPoolSize`` | ``server.threadPoolSize`` | The number of requests processed at once |
| ``server.restapi.waitTimeoutIfAllBusy`` | ``server.waitTimeoutIfAllBusy`` | Milliseconds to wait for a free instance before returning 503 (busy) |
| ``server.restapi.maxRequestSize`` | ``10485760`` | The largest request body in bytes |
| ``server.restapi.usersFile`` | (required) | The users file, which holds the users that may call the API |
| ``server.restapi.usersFile.signerCerts`` | none | Comma separated admin certificate files.  If set, the users file must be signed by one of these certificates |
| ``server.restapi.stateFile`` | ``ezsign-rest-state.properties`` | Written by the server to record the trusted admin certificates, so a change between restarts is reported |
| ``server.restapi.logRequests`` | ``true`` | Log one line per request.  Request bodies are never logged |
| ``server.restapi.useTls`` | ``true`` | Use HTTPS.  Only disable for testing |
| ``server.restapi.tls.keyStore.filename`` / ``.type`` / ``.password`` | type ``PKCS12`` | The server's TLS certificate and key.  The password is encrypted with the master password using the Management Tool |
| ``server.restapi.tls.trustStore.filename`` / ``.type`` / ``.password`` | none | Only the CA(s) that issue client certificates |
| ``server.restapi.tls.clientAuth`` | ``optional`` with a trust store, otherwise ``none`` | ``none``, ``optional`` or ``required`` |
| ``server.restapi.tls.protocols`` | ``TLSv1.3,TLSv1.2`` | The TLS protocols enabled |

Client certificates are only checked against the configured trust store, never the Java ``cacerts`` file

<br>

## Authentication and Permissions

Each request is authenticated with either:

* **An API token** - sent in the header ``Authorization: Bearer <token>``
* **A TLS client certificate** - presented when the connection is made.  The certificate must be issued by a CA in the server's trust store

The users, their API tokens and certificates, and their roles are held in the users file and managed with the [Management Tool](ezsign_management_tool.html).  A user's permissions are those of their roles.  A permission takes the form ``operation:channel/NAME`` e.g. ``sign:channel/FINANCE`` or ``verify:channel/*``

<br>

## Example

To sign data with an API token (held in ``$TOKEN``):

```shell
curl --cacert server-ca.pem \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"data":"SGVsbG8gV29ybGQ=","isDigest":false}' \
     https://ezsign.example.com:8443/v1/channels/FINANCE/sign
```

```json
{"signature":"MIIGxQYJKoZIhvcNAQcCoIIGtjCCBrICAQExDzANBglghkgBZQMEAgEFADALBgkqhkiG9w0BBwE..."}
```

To use a client certificate instead of a token, replace the ``Authorization`` header with ``--cert client.pem --key client.key``

If the request fails, the response contains an error code and message, e.g.

```json
{"error":{"code":"FORBIDDEN","message":"User finance-app does not have the sign permission on channel FINANCE"}}
```

The error codes are listed in the [REST API Reference](rest-api/index.html)

<br>

## Java Applications

Java applications can also use the REST API through the EzSign client, with the same calls as the socket interface.  See the [Client Integration Guide](ezsign_client_integration_guide.html)
