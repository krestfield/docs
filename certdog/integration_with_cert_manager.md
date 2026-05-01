---
layout: default
title: Integration with cert-manager
parent: Certdog
nav_order: 1111
---

# Integration with cert-manager

> From version: 1.17.0

Whether running standalone or within a cluster, Certdog's ACME server can be used with cert-manager
to issue certificates from any of its connected issuers.

This guide covers creating and using a cert-manager ACME issuer connected to Certdog.

## Prerequisites

Before starting this guide, you will need the following

* A running Certdog instance with an enabled ACME server
* A running cluster with cert-manager
* `kubectl` to deploy the issuer resource

## Creating an ACME issuer

To create an ACME issuer linked to Certdog, simply create a cert-manager Issuer resource
with the URL of the ACME service you want to use to issue certificates.
Usually, this URL will end with `/acme/<alias>/directory`, where `<alias>` is the alias
you have set when configuring the ACME service in Certdog.

You may additionally need to provide the `caBundle`, if your instance of Certdog uses
a certificate for TLS which is not trusted by default.
This should be a base 64 encoded CA bundle in PEM format.

The `privateKeySecretRef.name` field tells cert-manager where to keep the key for the
ACME account it will autogenerate when connecting for the first time.
You can also use [external account bindings](https://cert-manager.io/docs/configuration/acme/#external-account-bindings)
with Certdog.

```yaml
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: certdog-k8s-acme-issuer
spec:
  acme:
    server: your-hostname.example/acme/alias/directory
    caBundle: ""
    privateKeySecretRef:
      name: acme-account-key
```

To successfully issue certificates with a given DNS name, the ACME issuer must be able
to prove to the ACME server it has access to this domain.
This is done by configuring it to solve either HTTP01 or DNS01 challenges.
For example, an ACME issuer can be configured to solve HTTP01 challenges by exposing the
key required by the ACME server on a gateway, which should be accessible via the domain being
validated.

```yaml
# ...
spec:
  acme:
    # ...
    solvers:
    - http01:
        gatewayHTTPRoute:
          parentRefs:
          - name: acme-gateway
            namespace: default
            kind: Gateway
```

See the [cert-manager documentation](https://cert-manager.io/docs/configuration/acme/) for
more details.

## Using the ACME issuer

Certificates can be requested from the ACME issuer as with any other cert-manager issuer.

## Issuing certificates from an internal Certdog instance

Using a Certdog instance running in the same cluster as cert-manager is identical to
using an external Certdog instance.
The ACME server must still be behind HTTPS otherwise the client (ACME issuer) will not
be able to request certificates.
As a result, you will need to set up something to provide this HTTPS connection, such
as a gateway or proxy pod providing TLS termination.
