---
layout: default
title: OAuth 2.0 and OIDC Integration
parent: Certdog
nav_order: 11
---

# OAuth 2.0 and OIDC Integration

Certdog supports authorization and authentication of users via OAuth 2.0 and OIDC services, including processing of group membership.

Currently, the following provider(s) are supported:
- Microsoft Entra ID (formerly Azure AD)

<br>

Details on how to enable this are given below. Enabling OAuth support does not disable the use of local or Active Directory accounts. I.e. all three authentication options can be enabled at the same time.

<br>

## Configuring OAuth

To enable OAuth support you must:

1. [Create an App Registration in Microsoft Entra ID](#create-an-app-registration-in-microsoft-entra-id)

2. [Update the API properties file](#update-the-api-properties-file)

3. [Update the UI config file](#update-the-ui-config-file)

These steps are detailed in the next sections.

<br>

### Create an App Registration in Microsoft Entra ID

From Azure, click on **Microsoft Entra ID** and navigate to **App registrations**

<br>

#### Create a New App Registration

1. Click **+ New registration**

2. Enter a name for the application, e.g. "Certdog"

3. For *Supported account types* select **Accounts in this organizational directory only**

4. Under *Redirect URI (optional)*, choose **Single-page application SPA** from the *Select a platform* drop down and enter the **Cert User Interface URL** in the form:

​	``https://[certdog hostname]/certdog/ui/`` 

​	E.g. if your instance is located at https://certdog.intserver.local the full URL to enter would be: 

​	``https://certdog.intserver.local/certdog/ui/`` 

7. Note this value as it is the **[REDIRECT-URI]** and will be required later
8. Click **Register**

<br>

#### Expose the API

1. From the new app registration, navigate to **Owners** (under *Manage*) and add your own account as an owner if not already listed

8. From the new app registration, navigate to **Expose an API** and click the **Add** link to the right of *Application ID URI* and click Save accepting the default value for the Application ID URI

9. Click **+ Add a scope** and for 

   1. *Scope name* enter **Certdog.Access**

   2. For *who can consent* select **Admins and users**

   3. for *Admin consent display name* enter something like **Access the Certdog API**

   4. for *Admin consent description* enter something like **Allows the app to access and modify certdog API data**

10. Note the value beneath the *Scope name* text box:

    <img src="./images/image-20250912165902693.png" alt="image-20250912165902693" style="zoom:80%;" />

    E.g. ``api://12720666-5016-408f-8691-0565a23faa3b/Certdog.Access`` which is made up of the Application ID URL and the Scope name

11. Note this value as it is the **[API-SCOPE]** and will be required later

12. Click **Add scope**

<br>

#### Add Permissions

1. Click **+ Add a permission**, select **My APIs** and select the name of the application (e.g. Certdog)

8. Under Select permissions select Certdog.Access and click Add Permissions

9. Click **+ Add a permission** again, select **Microsoft Graph**, then **Delegated permissions**

10. Search for and select **openid** and **profile** then click **Add permissions**

11. Click the **three dots** at the end of the *User.Read* permission uder *Microsoft Graph* and select **Remove permission**, then **Yes, remove**

    The permissions should look like this:

<img src="./images/image-20250912163322074.png" alt="image-20250912163322074" style="zoom:67%;" />

<br>

#### Enable the claims for user identification and group support

1. From the app registration, navigate to **Token Configuration** (under *Manage*)
19. Click **Add optional claim**, select **Access** and check **upn**. Click **Add**
20. Click **Add groups claim**, select **Security groups**, then click **Add**



#### Enable OAuth 2.0 Support

1. From the app registration, navigate to **Manifest** (under *Manage*)
19. Search for **accessTokenAcceptedVersion** and change the value from **null** to **2** and click **Save**

<br>

#### Obtain Required Values

1. From the app registration, navigate to **Overview**

2. Copy the value for Application (client) ID

   E.g. ``e02d66e2-ae76-479c-8383-dbd209088538``

3. This is the **[CLIENT-ID]** value we will need below

   

4. Copy the value for Application ID URI

   E.g. ``api://e02d66e2-ae76-479c-8383-dbd209088538``

5. And remove the ``api://`` part to just give the ID

   E.g. ``e02d66e2-ae76-479c-8383-dbd209088538``

6. This is the **[AUDIENCES]** value we will need below

   

7. From the top menu click on Endpoints

8. Copy the value for **Authority URL (Accounts in this organizational directory only)**

   E.g. ``https://login.microsoftonline.com/0d285301-66f1-496e-9915-2008a8603591`` 

9. Add ``/v2.0`` to the end of this string e.g.

   ``https://login.microsoftonline.com/0d285301-66f1-496e-9915-2008a8603591/v2.0``

10. This is your **[ISSUER-URI]** value we will need below

    

11. The **[REDIRECT-URL]** should have been noted in the setup steps above 

12. The **[API-SCOPE]** should also have been noted in the setup steps above

<br>

### Update the API properties file

On the certdog server, open the ``application.properties`` file located here:

``[certdog install]\config\application.properties``

E.g.

``c:\certdog\config\application.properties``

Add in the following two lines, substituting in the values for [ISSUER-URI] and [AUDIENCES] as obtained above:

```
spring.security.oauth2.resourceserver.jwt.issuer-uri=[ISSUER-URI]
spring.security.oauth2.resourceserver.jwt.audiences=[AUDIENCES]
```

E.g.

```
spring.security.oauth2.resourceserver.jwt.issuer-uri=https://login.microsoftonline.com/0d285301-66f1-496e-9915-2008a8603591/v2.0
spring.security.oauth2.resourceserver.jwt.audiences=e02d66e2-ae76-479c-8383-dbd209088538
```

Save the file



### Update the UI config file

On the certdog server, open the ``config.json`` file located here:

``[certdog install]\tomcat\webapps\certdog#ui\config.json``

E.g.

``C:\certdog\tomcat\webapps\certdog#ui\config.json``

It will either contain a configuration such as:

```
{
  "apiUrl" : "https://127.0.0.1/certdog/api/"
}
```

Or one with placeholders already in place for the values we need. E.g.

```
{
  "apiUrl" : "https://127.0.0.1/certdog/api/",
  "oauth": {
    "server": "[ISSUER-URI],
    "clientId": "[CLIENT-ID]",
    "redirectUri": "[REDIRECT-URL]",
    "scope": "[API-SCOPE]"
  }
}

```

Populate this file with the values for [ISSUER-URI], [CLIENT-ID], [REDIRECT-URI] and [API-SCOPE] as gathered above.



# WE ARE THIS FAR



```
{
  "apiUrl" : "https://certdogtest/certdog/api/",
  "oauth": {
    "server": "https://login.microsoftonline.com/0d285301-66f1-496e-9915-2008a8603591/v2.0",
    "clientId": "12720666-5016-408f-8691-0565a23faa3b",
    "redirectUri": "https://certdogtest/certdog/ui/",
    "scope": "api://12720666-5016-408f-8691-0565a23faa3b/Certdog.Access"
  }
}

```









```
{
  "oauth": {
    "server": "[ISSUER-URI]",
    "clientId": "[CLIENT-ID]",
    "redirectUri": "[REDIRECT-URI]",
    "scope": "<your-api-scope>"
  }
}
```









# BENS ORIGINAL BELOW




OAuth support is controlled by the presence of the `spring.security.oauth2.resourceserver.jwt.issuer-uri`
property in the `application.properties` file of the API, and the presence of the `oauth` section in the
UI's `config.json` file.

The API must be restarted for changes to `application.properties` to take effect.

The UI will dynamically pick up changes to `config.json`, however, the configuration is stored locally and may also be cached by the browser, so to ensure the new configuration is loaded, you may need to clear the browser's cache and stored data for the site.
This can be done through developer tools or the browser's settings.
See your browser's documentation for details.

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

You can find `your-v2-issuer-uri` by taking the "Authority URL (Accounts in this organizational directory only)" at the
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

## Common Issues

### "No PKCE code verifier found in session storage, cannot complete OAuth login"

The URL you use to access the website must match the redirect URIs configured in the UI's configuration and
your provider's (e.g. your Entra ID app's) configuration.
If these differ, you will be redirected to a different domain (redirecting from `localhost` to `127.0.0.1` or vice
versa usually causes this problem), and so the required verifiers will be missing from session storage, causing this
error.

**Solution:** Ensure you use the same domain in all places, including when accessing the UI.

### I've updated the OAuth configuration, but the changes don't seem to take effect

The API must be restarted for changes made to the `application.properties` file to take effect.
The UI will dynamically pick up changes, but the configuration is cached, so this may need to be cleared.

See the *Toggling OAuth* section above for more details.

**Solution:** Restart the API and clear the browser cache and stored data for the site.
