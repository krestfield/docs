---
layout: default
title: EzSign - Client
parent: EzSign
nav_order: 5
---
# EzSign Client

<br>

The EzSign client is a lightweight java (or .NET) component which exposes a simple interface enabling applications to quickly utilise the PKI and encryption functions offered by the EzSign Server

The communication between the client and server is socket based. The server name (or IP Address) and the port the server is listening on must be specified at the client

The communications between the client and server can be protected by using:

* An authentication code
  * This is a passphrase which is provided at the client and also configured at the server
* TLS
  * This can be server based or also configured for client side authentication 

<br>
For further details see the [Client Integration Guide](ezsign_client_integration_guide.html)

