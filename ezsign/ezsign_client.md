---
layout: default
title: EzSign - Client
parent: EzSign
nav_order: 5
---
# EzSign Client

<br>

The EzSign client is a lightweight java (or .NET) component which exposes a simple interface enabling applications to quickly utilise the PKI and encryption functions offered by the EzSign Server

The client can communicate with the server using either of the server's interfaces:

* The socket API
  * This is the default, and is used by all versions of the client
* The REST API (from client version 4.6.0)
  * The client calls the server's REST API over HTTPS and authenticates with an API token or a TLS client certificate

The server name (or IP Address) and the port the server is listening on must be specified at the client

The calls made by an application are the same whichever interface is used, so an application can move from the socket API to the REST API (and back again) by changing only how the client is created

When the socket API is used, the communications between the client and server can be protected by using:

* An authentication code
  * This is a passphrase which is provided at the client and also configured at the server
* TLS
  * This can be server based or also configured for client side authentication 

When the REST API is used:

* The communications are protected by TLS
* Each application authenticates as its own REST API user, with an API token or a TLS client certificate
* Each user is only permitted the operations and channels it has been granted

<br>
For further details see the [Client Integration Guide](ezsign_client_integration_guide.html)

For the .NET client. See the [.Net Client Integration Guide](ezsign_dotnet_client_integration_guide.html)

