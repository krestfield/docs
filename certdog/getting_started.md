---
layout: default
title: Getting Started
parent: Certdog
nav_order: 6
---

# Certdog - Getting Started

<br>

Once certdog has been successfully installed you are now ready to start the configuration.

<br>

<u>STEP 1</u>

First steps are to carry out any [Post Installation steps](post-Installation.html)

<br>

<u>STEP 2</u>

If you wish to interface to an existing Microsoft AD CS instance. Follow the [steps here](create_adcs_certificate_issuer.html).

If you wish to interface to an existing EJBCA instance. Follow the [steps here](create_ejbca_issuer.html).

To create an internal PKI, first [create a Key Store](keystores.html), then follow the [steps here](create_local_certificate_issuer.html) to create a CA.

<br>

<u>STEP 3</u>

Issue a certificate as [described here](issuing-a-certificate.html)

<br>

### Next Steps

<u>Users</u>

Consider how you want users to authenticate to the system. You can use:

* [Local Users](users.html), and manage permissions via [Teams](teams.html)
* [Integrate with Active Directory](active_directory_integration.html)
* [Use OAuth 2.0 and OIDC with Azure EntraID](oauth_integration.html)

<br>

<u>Integration Options</u>

Consider integrating your applications for automation using the following options:

* [REST API](rest_api_overview.html)

* [PowerShell](powershell_module.html)

* [ACME](acme.html)

* [SCEP](scep.html)

* [.NET Client](dotnet_client.html)

* [Java Client](https://github.com/krestfield/certdog-java-client)

<br>

You can browse the [documentation located here](https://krestfield.github.io/docs/certdog/certdog.html) and search for any terms. Also, see our [YouTube channel](https://www.youtube.com/channel/UC1uScLlevNOXHS51oGnQlSg) for video guides.

