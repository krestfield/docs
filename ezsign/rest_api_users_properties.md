---
layout: default
title: EzSign REST API Users File
parent: EzSign
nav_order: 11
---

# EzSign REST API Users File

<br>

> Note: The REST API is only available in version 4.6.0 onwards

<br>

The users that may call the [REST API](rest-api/index.html) are held in a users file.  It lists each user, the credentials they authenticate with (API tokens or client certificates) and the roles that give them their permissions.  The file is set by ``server.restapi.usersFile`` in the server properties (see [EzSign Properties](ezsign_properties.html))

The file is normally created and changed with the [EzSign Management Tool](ezsign_management_tool.html#rest-api-users) (the browser UI, the menu or the CLI), which validates it with exactly the rules the server uses and signs it with the admin key.  This page describes the format, for reviewing the file or creating it by other means

<br>

## Example

```json
{
  "version": 3,
  "roles": {
    "finance-signer": [
      "sign:channel/FINANCE",
      "verify:channel/FINANCE"
    ],
    "batch-crypto": [
      "verify:channel/*",
      "random:channel/BATCH",
      "encrypt:channel/BATCH",
      "decrypt:channel/BATCH"
    ],
    "monitor": [
      "status"
    ]
  },
  "users": [
    {
      "id": "finance-app",
      "description": "Finance application",
      "enabled": true,
      "roles": ["finance-signer"],
      "credentials": [
        { "type": "certificate", "sha256": "3f:5a:...:9c", "label": "production" },
        { "type": "certificate", "issuer": "CN=Example Issuing CA,O=Example Ltd", "serialNumber": "3A:4B:5C:6D" }
      ]
    },
    {
      "id": "batch-service",
      "enabled": true,
      "roles": ["batch-crypto"],
      "credentials": [
        { "type": "apiToken", "sha256": "<SHA-256 of the token>", "label": "batch jobs", "created": "2026-10-28" }
      ]
    },
    {
      "id": "monitoring",
      "enabled": true,
      "roles": ["monitor"],
      "credentials": [
        { "type": "apiToken", "sha256": "<SHA-256 of the token>" }
      ]
    },
    {
      "id": "partner-gateway",
      "enabled": false,
      "roles": ["batch-crypto"],
      "credentials": [
        { "type": "certificate", "subject": "CN=partner-gateway,O=Example Ltd", "issuer": "CN=Example Issuing CA,O=Example Ltd" }
      ]
    }
  ]
}
```

<br>

## The File

The file is a JSON object, encoded as UTF-8.  It must not be larger than 10 MB

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| version | Whole number (0 or more) | No | The version of the file.  The management tool increases it by one on every change.  When the file is signed, the server refuses a file with a lower version than the one it has loaded (see [Signing](#signing)).  *If omitted defaults to 1* |
| roles | Object | No | The roles, by name.  Each value is an array of [permissions](#permissions) |
| users | Array | Yes | The [users](#users) |

Fields not listed on this page are ignored, and are not kept when the management tool writes the file

<br>

## Roles

Each entry in ``roles`` is a role name and the array of permissions it grants e.g.

```json
"roles": {
  "finance-signer": ["sign:channel/FINANCE", "verify:channel/FINANCE"]
}
```

A user's permissions are those of all their roles.  Permissions cannot be assigned to a user directly: create a role for each set of permissions and assign it to the users that need it

<br>

## Permissions

A permission takes the form ``operation:channel/NAME``

| Operation | Allows |
|-----------|--------|
| sign | Signing with the channel |
| verify | Verifying with the channel |
| verify.bypass | Asking for revocation checking or path building to be bypassed when verifying.  Needed in addition to ``verify`` |
| encrypt | Encrypting with the channel |
| decrypt | Decrypting with the channel |
| random | Generating random data with the channel |
| * | All of the above |

The channel name may contain ``*`` as a wildcard, matching any characters.  Names are compared exactly, including case.  For example:

| Permission | Allows |
|------------|--------|
| sign:channel/FINANCE | Signing with the FINANCE channel |
| verify:channel/* | Verifying with any channel |
| \*:channel/TEST* | Every operation with any channel whose name starts with TEST |
| \*:\* | Every operation with any channel |

There are also two permissions written on their own, without a channel:

| Permission | Allows |
|------------|--------|
| status | Reading the server status (``/v1/status``): the server's details and the number of calls made since it started, for monitoring.  It is only granted by ``status`` or ``*`` on its own, not by any channel permission, so give it to a dedicated monitoring user rather than to the applications |
| * | Everything, including ``status`` |

A file with a permission that is not in one of these forms is refused

<br>

## Users

Each entry in ``users`` is an object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | String | Yes | The user's id.  It is written to the server log with each request.  Must not be empty and must be unique in the file |
| description | String | No | A description of the user e.g. the application it is |
| enabled | true or false | No | A disabled user cannot authenticate.  Their credentials are kept so the server can log why a request was refused, and so they can be enabled again.  *If omitted defaults to true* |
| roles | Array of strings | No | The names of the user's roles.  Each must be in ``roles``.  A user with no roles can authenticate but is not permitted to do anything |
| credentials | Array | Yes | The [credentials](#credentials) the user authenticates with.  May be empty, in which case the user cannot authenticate |

A user with a ``permissions`` field is refused rather than ignored, so a user does not silently lose (or keep) access.  Move the permissions to a role and assign the role to the user

<br>

## Credentials

Each credential is an object with a ``type`` of ``apiToken`` or ``certificate``.  A credential can belong to only one user: a file with the same token or certificate on two users, or twice on the same user, is refused

Both types may also have:

| Field | Type | Description |
|-------|------|-------------|
| label | String | A description e.g. what the token is used for, or which system holds the certificate |
| created | String | When the credential was added.  The management tool writes the date e.g. ``2026-10-28`` |

<br>

### API Tokens

```json
{ "type": "apiToken", "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08", "label": "batch jobs" }
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sha256 | String | Yes | The SHA-256 hash of the token (of its UTF-8 bytes), as 64 hex characters |

The token itself is never stored, only its hash.  The client sends the token in the ``Authorization`` header:

```
Authorization: Bearer ezs_Q2xhdWRlIGdlbmVyYXRlZCB0aGlzIGV4YW1wbGU...
```

Tokens generated by the management tool are ``ezs_`` followed by 32 random bytes, base64url encoded.  The tool shows the token once, when it is created.  If it is lost, add a new token and remove the old one

An API token credential must not have any of the certificate fields

<br>

### Client Certificates

```json
{ "type": "certificate", "sha256": "3F:5A:...:9C" }
```

The client authenticates with its certificate over TLS.  The server first validates the certificate against ``server.restapi.tls.trustStore`` (see [EzSign Properties](ezsign_properties.html)), then finds the user it belongs to.  A certificate credential identifies the certificate with exactly one of:

| Fields | Matches |
|--------|---------|
| sha256 | The SHA-256 fingerprint of the whole certificate, as 64 hex characters.  Only this certificate |
| sha1 | The SHA-1 fingerprint (thumbprint) of the whole certificate, as 40 hex characters.  Only this certificate |
| issuer and serialNumber | The issuer's distinguished name and the certificate's serial number, in hex.  Only this certificate |
| subject and issuer | The subject and issuer distinguished names.  Also matches a renewed certificate with the same subject and issuer |
| subject | The subject distinguished name only.  Matches a certificate with this subject from any CA in the trust store, so only use it when the trust store holds only CAs you control |

Hex values (``sha256``, ``sha1`` and ``serialNumber``) may be in upper or lower case, and may contain colons and spaces e.g. ``3f5a...``, ``3F:5A:...`` and ``3F 5A ...`` are all accepted.  The invisible characters Windows adds when a thumbprint is copied from the certificate dialog are ignored.  Leading zeros in a serial number are ignored

Distinguished names are given as in RFC 2253 e.g. ``CN=finance-app,O=Example Ltd``.  They are compared as distinguished names, so differences in spacing and case that do not change the name are ignored

The certificate is matched in this order: ``sha256``, ``sha1``, ``issuer`` and ``serialNumber``, ``subject`` with ``issuer``, then ``subject`` alone.  The first match decides the user

<br>

## Signing

If ``server.restapi.usersFile.signerCerts`` is set, the users file must be signed with the private key of one of these admin certificates, so that someone who can change the file cannot give themselves access.  See [Signing the Users File](ezsign_management_tool.html#signing-the-users-file) for creating the admin key and signing with the management tool

The signature is held in a second file, next to the users file, with ``.sig`` added to its name e.g. ``users.json.sig``:

```json
{
  "format": "ezsign-users-signature",
  "formatVersion": 1,
  "algorithm": "SHA256withRSA",
  "signedAt": "2026-10-28T13:00:00Z",
  "signer": "CN=EzSign Users Admin,O=Example",
  "signerCertificate": "<base64 DER of the admin certificate>",
  "contentSha256": "<hex SHA-256 of users.json>",
  "signature": "<base64 signature over the exact bytes of users.json>"
}
```

| Field | Description |
|-------|-------------|
| format | Always ``ezsign-users-signature`` |
| formatVersion | Always ``1`` |
| algorithm | One of ``SHA256withRSA``, ``SHA384withRSA``, ``SHA512withRSA``, ``SHA256withECDSA``, ``SHA384withECDSA`` or ``SHA512withECDSA``.  The management tool uses SHA256withRSA or SHA256withECDSA |
| signedAt | When the file was signed.  For information only |
| signer | The admin certificate's subject.  For information only |
| signerCertificate | The admin certificate, base64 encoded DER |
| contentSha256 | The SHA-256 of the users file, in hex.  If present and it does not match, the server reports that the file was changed after it was signed |
| signature | The signature over the exact bytes of the users file, base64 encoded |

When the users file must be signed, the server only loads it if:

- The signature file exists and is in the format above
- ``signerCertificate`` is one of the certificates in ``server.restapi.usersFile.signerCerts``.  The certificate is pinned, not validated against a CA, so list more than one certificate to change the admin key without a break
- The signature verifies over the exact bytes of the users file.  Any change to the file, even to spacing, needs a new signature
- The file's ``version`` is not lower than the version already loaded, so an older signed file cannot be put back while the server is running

If ``signerCerts`` is not set, the signature is not checked and the server logs a warning each time it loads the file

<br>

## Loading the File

The server loads the users file when it starts, and again when it is reloaded with the server control tool (see [EzSign Control](ezsign_control.html)) or from the management tool.  If the new file cannot be read, is not valid, is not correctly signed or has a lower version, it is refused, the reason is logged and the server keeps the users it has

The server logs the number of enabled users and the version loaded e.g.

```
REST: Loaded 3 enabled user(s) from ../config/users.json (version 3)
```

A file is refused as a whole if any part of it is not valid, for example:

- It is not valid JSON, or has no ``users`` array
- A user has an empty or repeated ``id``, no ``credentials``, a ``permissions`` field or a role that is not in ``roles``
- A permission is not in one of the forms above
- A credential has an unknown ``type``, a hex value of the wrong length, an invalid distinguished name or serial number, or not exactly one way of identifying a certificate
- The same credential is assigned more than once
