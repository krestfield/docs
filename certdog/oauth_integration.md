---
layout: default
title: OAuth 2.0 and OIDC Integration
parent: Certdog
nav_order: 11
---

# OAuth 2.0 and OIDC Integration

Certdog supports authorization and authentication of users via OAuth 2.0 and OIDC services, and processing of group membership where available.

Currently, the following provider(s) are supported:
- Microsoft Entra ID (formerly Azure AD)

## Microsoft Entra ID

Entra ID users do not have to be explicitly registered in Certdog.
Their permissions are managed by their security group membership in Entra ID.
To achieve this, the security groups must be configured against Teams in Certdog.

### Initial Configuration

Before editing the Certdog configuration, an application registration for Certdog must be made in the Entra ID tenant.

1. Create a new App Registration
   1. In the Entra admin centre, navigate to "Azure Entra ID" > "App registrations".
   2. Click "New registration".
   3. Enter a name for the application, e.g. "Certdog".
   4. Set "Supported account types" to "Accounts in this organizational directory only".
   5. Set "Redirect URI" to "SPA" and enter the URL of your UI.
   6. Click "Register".
   7. Under your new app registration, navigate to "Owners" and add yourself as an owner if not already listed.
2. Expose Certdog as an API
   1. Navigate to "Expose an API".
   2. Click "Add" next to "Application ID URI" then "Save".
   3. Click "Add a scope". Name the scope "Certdog.Access", set the consent option as desired,
   and add a reasonable description such as "Access to Certdog". Click "Add scope".
3. Enable the correct permissions for the API
   1. Navigate to "API permissions".
   2. Click "Add a permission", select "My APIs", then select your new app.
   3. Select the "Certdog.Access" scope, then click "Add permissions".
   4. Click "Add a permission" again, select "Microsoft Graph", then "Delegated permissions".
   5. Search for and select "openid" and "profile" then click "Add permissions".
   6. You can remove any other default permissions such as "User.Read".
4. Enable the required claims for user identification and group support.
   1. Under your new app registration, navigate to "Token configuration".
   2. Click "Add optional claim", select "Access", check "upn", then click "Add".
   If prompted, add the MS Graph profile permission to the API permissions, if not already added. 
   3. Click "Add groups claim", select "Security groups", then click "Add".
5. Enable OAuth 2.0 support
   1. Navigate to "Manifest".
   2. Under "api" change "requestedAccessTokenVersion" from `null` to `2`.
   3. Click "Save".

Once the application registration is complete, the Certdog API must be configured to use it.
To do this, set the following properties in the `application.properties` configuration file.

```properties
spring.security.oauth2.resourceserver.jwt.issuer-uri=<your-v2-issuer-uri>
spring.security.oauth2.resourceserver.jwt.audiences=<your-audience-id>
```

If `spring.security.oauth2.resourceserver.jwt.issuer-uri` is missing, OAuth will be disabled for the application.

You can find `your-v2-issuer-uri` by taking the "Authority URL (Accounts in this organizational directory only" at the
top of the "Endpoints" in the "Overview" section of your app registration.
Note you must add `/v2.0` to the end of this URL to use the correct version.

You can find `your-audience-id` in the "Overview" section of your app registration as the identifier after "api://" in
"Application ID URI".

Finally, the Certdog UI must be configured to use the same application registration.
To do this, add the following section to the `config.json` file under `<certdog-install-path>/tomcat/webapps/certdog#ui`.

```json
{
  "oauth": {
    "server": "<your-v2-issuer-uri>",
    "clientId": "<your-client-id>",
    "redirectUri": "<your-redirect-uri>",
    "scope": "<your-api-scope>"
  }
}
```

`your-v2-issuer-uri` is the same as above.

To find `your-client-id`, copy the "Application (client) ID" from the "Overview" section of your app registration.

To find `your-redirect-uri`, find the "Single-page application" section under the "Authentication" section.

To find `your-api-scope`, copy the scope you created earlier, found under "Expose an API".

### Granting Permissions

In Certdog, permissions to specific Certificate Issuers are granted via [Teams](teams.html).
A Team is configured to allow access to issuers.
Users are then made members of this Team.

To allow access for Entra ID users, simply map the Entra ID security groups to the Certdog Teams.
Make sure to use the Object ID of the security group, not the display name.

The processing then completes as follows:

1. User authenticates with their Entra ID account
2. Map the users OAuth Group Memberships to the Certdog Teams that have been configured with those Groups
3. The user obtains the permissions and restrictions as imposed by those Teams

Note that when an Entra ID user authenticates their account will then appear in the Users list in Certdog.
This will show what Certdog Teams the user is a member of (based on their Entra ID group membership).
None of the details for Entra ID accounts can be managed via Certdog - they continue to be managed via Entra ID only

If an Entra ID user is not a member of any group mapped to a Team, they can still login to Certdog but will have no access to any Certificate Issuers.
If the Setting _Users can see_ is set to **All Certificates** then they will also be able to view certificates in the system but will not be able to carry out any operations on them.
