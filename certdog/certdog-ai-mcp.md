---
layout: default
title: MCP AI Setup
parent: Certdog
nav_order: 30
---

<br>

# AI MCP Setup with Claude

<br>

This guide demonstrates how to configure the certdog MCP server with Claude Code and Claude Desktop. This allows natural language to be used to gather data on the certificate estate and the certdog configuration, e.g. *"how many certificates expire next month?"*

All of the commands are read-only. If you wish to also allow certificate requests, renewals and revocations then the optional write tools can also be enabled

<br>

There are two ways to run the MCP server:

| | Option 1: Hosted by certdog | Option 2: Run locally |
|---|---|---|
| **How** | Enabled when installing (or later). Runs inside certdog's Tomcat | Each user runs ``certdog-mcp.jar`` on their own machine |
| **Connect to** | ``https://{certdog host}/certdog/claude/mcp`` | The jar, which Claude starts itself |
| **Needs Java on the user's machine** | No | Yes (Java 21 or later) |
| **Claude Code** | Yes | Yes |
| **Claude Desktop** | Not yet (see below) | Yes |

Both use certdog API tokens, so each user only sees what their certdog account allows

<br>

## Option 1: Hosted by certdog

From certdog 1.18 the MCP server can run inside certdog itself, using certdog's own address and TLS certificate. It is served at:

```
https://{certdog host}/certdog/claude/mcp
```

This is referred to as ``{MCP URL}`` below, e.g. ``https://certdog.svr.local/certdog/claude/mcp``. If certdog listens on a port other than 443, include it, e.g. ``https://certdog.svr.local:8443/certdog/claude/mcp``

It is off by default and must be enabled. Each user then connects with their own certdog API token

<br>

### Enabling AI assistant access

**Windows**

When installing, the installer asks:

```
Do you wish to enable AI assistant access (MCP) (y/n)?
```

Answer ``y`` to enable it. To enable it without being asked, add ``-enableMcp`` to the install command:

```powershell
.\install.ps1 -enableMcp
```

For an unattended install (one given ``-listeningPort``) the question is not asked, and it is only enabled if ``-enableMcp`` is given

When upgrading, it stays enabled (with its settings) if it was enabled before. Otherwise the upgrade asks the same question

To enable or disable it at any other time, open a PowerShell window as Administrator in the certdog ``install`` folder (e.g. ``C:\certdog\install``) and run:

```powershell
.\configure-mcp.ps1 -enableMcp
```

or

```powershell
.\configure-mcp.ps1 -disableMcp
```

Tomcat starts (or stops) the MCP server within a few seconds, so certdog does not need to be restarted

<br>

**Linux**

``configure.sh`` asks the same question when run in a terminal. To answer in advance, set ``ENABLEMCP="y"`` (or ``"n"``) in the settings at the top of ``configure.sh``, or set the ``CERTDOG_ENABLE_MCP`` environment variable

To enable or disable it later, from the certdog ``install`` folder run:

```bash
./configure-mcp.sh enable
```

or

```bash
./configure-mcp.sh disable
```

When building the Docker image, the question is not asked and it is left disabled. To enable it, add ``ENV CERTDOG_ENABLE_MCP=y`` to the Dockerfile before the step that runs the installer

<br>

### Settings

Enabling it creates ``config\certdog-mcp.properties`` in the certdog installation folder (e.g. ``C:\certdog\config\certdog-mcp.properties``). An existing file is kept, so your changes are not lost when it is disabled and enabled again, or when upgrading

Restart the certdog service after changing these settings

| Setting | Description |
|---|---|
| ``certdog.url`` | The certdog API that the MCP server calls. Set by the installer to certdog's own API, e.g. ``https://127.0.0.1/certdog/api`` |
| ``certdog.server-max-results`` | Must match ``certs.maxtoreturn`` in ``application.properties``. Default 1000 |
| ``certdog.timezone`` | The timezone used for dates such as "next month", e.g. ``Europe/London``. Blank uses the server's timezone |
| ``certdog.write-tools.enabled`` | ``true`` to offer the certificate request, renew and revoke tools. Default ``false``. See [Write operations](#write-operations-with-option-1) below |
| ``certdog.write-tools.max-actions-per-hour`` | The most requests, renewals and revocations the server will carry out in an hour, across all users. Default 10 |
| ``certdog.allowed-origins`` | Leave blank. Requests from web pages in a browser are refused unless their origin is listed here (comma-separated). Claude does not send an origin |

The MCP server's log is ``logs\certdog-mcp.log`` in the certdog installation folder

<br>

### Connect Claude Code

Obtain an API token as described in [Obtain API Keys and Certdog Details](#obtain-api-keys-and-certdog-details) below. Then, from a command prompt, run:

```
claude mcp add --transport http -s user certdog {MCP URL} --header "Authorization: Bearer {API TOKEN}"
```

E.g.

```
claude mcp add --transport http -s user certdog https://certdog.svr.local/certdog/claude/mcp --header "Authorization: Bearer eyJhbGciOi...1S-J9Lk7A"
```

Start Claude Code and type ``/mcp``. The certdog instance should show as connected

<br>

Claude Code must trust certdog's TLS certificate. If it is issued by a CA that is not in your system's trusted roots (for example the default certificate created by the installer), point Claude Code at the root CA certificate (PEM) with the ``NODE_EXTRA_CA_CERTS`` environment variable before starting it. For the default certificate this is ``config\sslcerts\tls_root.cer`` in the certdog installation folder, e.g.

```
set NODE_EXTRA_CA_CERTS=C:\certdog\config\sslcerts\tls_root.cer
claude
```

<br>

### Write operations with Option 1

When ``certdog.write-tools.enabled=true``, the request, renew and revoke tools are offered to everyone who connects. Each action is still carried out as the certdog user whose token was given, and the tools refuse to run as an admin user or as a user that can bypass workflows

So, as with Option 2, create a dedicated user for write operations whose requests require approval (see [Obtain API Keys and Certdog Details](#obtain-api-keys-and-certdog-details)), and add a second connection with that user's token:

```
claude mcp add --transport http -s user certdog-write {MCP URL} --header "Authorization: Bearer {USER API TOKEN}"
```

<br>

### Claude Desktop

Claude Desktop (and claude.ai) adds remote MCP servers as *connectors*, which sign in with OAuth rather than an API token. The certdog-hosted MCP server does not support OAuth yet, so for Claude Desktop use Option 2

<br>

### Troubleshooting Option 1

* **404 Not Found** at ``{MCP URL}``: AI assistant access is not enabled, or the certdog service is not running. Enable it as described above
* **"No certdog token was supplied"**: the ``Authorization`` header is missing. Check the ``--header`` value in the ``claude mcp add`` command
* **"certdog refused the request ... (HTTP 401/403)"**: the API token is incorrect or has expired, or the user does not have permission
* **"Could not connect to certdog"**: the MCP server could not reach certdog's API at ``certdog.url``. If you have replaced certdog's TLS certificate, make sure ``certdog.url`` uses a name or IP address in the certificate, and that the certificate's root CA is in ``config\sslcerts\dbssltrust.jks`` (the trust store certdog's Tomcat uses)
* **Certificate errors in Claude Code**: see ``NODE_EXTRA_CA_CERTS`` above
* Check ``logs\certdog-mcp.log`` for details

<br>

## Option 2: Run locally

Each user runs the MCP server on their own machine, and Claude Code or Claude Desktop starts it

<br>

### Obtain the MCP server

Contact support to obtain the ``certdog-mcp.jar``

Copy this file to your certdog installation or ideally a folder with no spaces in the path e.g. ``c:\certdog-mcp``

<br>

### Obtain API Keys and Certdog Details

An API key will be required for the AI agent (Claude Code or Desktop) to provide to the MCP server in order to access the certdog API

An admin level user key will allow for searching across the entire certificate estate as well obtaining information on all configs, users and teams

A standard user account will be limited, but this may be preferred if the AI model is running locally (as in claude desktop) and the user operating it is only concerned with their own certificates

For write operations (making certificate requests etc.), it is advisable to create a separate user account that is limited to specific issuers and ideally included in an approval workflow, so that some admin intervention (or other human approver) is required when certificates are being requested/revoked

Create the required API tokens by following the guide [here](users.html#api-tokens). The same tokens are used with Option 1

The API keys obtained are referred to as ``{API TOKEN}`` and ``{USER API TOKEN}`` in the steps below

<br>

The following information is also required:

* Full path to the MCP Server jar
  * E.g. ``c:\certdog\certdog-mcp.jar``
  * This is ``{MCP JAR PATH}`` below
  
* The certdog API URL
  * The URL to the API
  * E.g. https://certdog.svr.local/certdog/api
  * This is ``{API URL}``below

<br>

### TLS Configuration

Claude and the MCP server must trust the TLS certificates presented by the certdog API end point  

If the TLS certificate are issued from a trusted root that is already included within the local java trust store then no additional arguments are required. In this case the following argument (as shown in the examples below):

```properties
-Djavax.net.ssl.trustStoreType=Windows-ROOT
```

Can be removed

On windows machines, if the trusted roots are not present in the java trust store, but are present in the windows trusted root store, then the following argument:

```properties
-Djavax.net.ssl.trustStoreType=Windows-ROOT
```

Will pick them up and the connection to the MCP server will be allowed. This is often the default case and has been included in the samples below  

However, on other systems (linux etc), or where the root certificates have not been imported, then the trusted store (containing the TLS root) must be provided as a pkcs#12 or JKS file.  For example, if the default certdog certificates were still in use, the following arguments would be required:

``` properties
-Djavax.net.ssl.trustStore=C:/certdog/config/sslcerts/dbssltrust.jks
-Djavax.net.ssl.trustStorePassword=...
-Djavax.net.ssl.trustStoreType=JKS
```

If the trusted certificates were included in a pkcs#12 store:

```properties
-Djavax.net.ssl.trustStore=C:/certdog/config/sslcerts/truststore.p12
-Djavax.net.ssl.trustStorePassword=...
```

<br>

These changes will alter the configuration set below. E.g. if the JKS file were used then the ``args`` section below would look something like this:

```properties
"args": [
        "-Djavax.net.ssl.trustStore=C:/certdog/config/sslcerts/dbssltrust.jks",
        "-Djavax.net.ssl.trustStorePassword=somepassword",
        "-Djavax.net.ssl.trustStoreType=JKS",
        "-jar",
        "{MCP JAR PATH}"
      ]
```

<br>

### Setup with Claude Desktop

Note that Java 21 or later is required. This must be configured on the environment (via JAVA_HOME and path settings) so that Claude Desktop picks up the correct version when starting

<br>

From *Claude Desktop*, click **your account** (usually bottom left) and select **Settings**. Click **Developer** from the left hand options and choose **Edit Config**. Open the file referenced (``claude_desktop_config.json``), if not opened automatically, and edit

<br>

Add the following ``mcpServers`` section at the top of the config, ensuring that you substitute in the correct values for ``{MCP JAR PATH}``, ``{API URL}``and ``{API TOKEN}``:

```json
{
  "mcpServers": {
    "certdog": {
      "command": "java",
      "args": [
        "-Djavax.net.ssl.trustStoreType=Windows-ROOT",
        "-jar",
        "{MCP JAR PATH}"
      ],
      "env": {
        "CERTDOG_URL": "{API URL}",
        "CERTDOG_API_TOKEN": "{API TOKEN}"
      }
    }
  },
  
  
}
```

E.g. so it looks something like this:

```json
{
  "mcpServers": {
    "certdog": {
      "command": "java",
      "args": [
        "-Djavax.net.ssl.trustStoreType=Windows-ROOT",
        "-jar",
        "C:\\certdog\\certdog-mcp.jar"
      ],
      "env": {
        "CERTDOG_URL": "https://certdog.svr.local/certdog/api",
        "CERTDOG_API_TOKEN": "eyJhbGciOiJ...X1-XUBWnKuYLv6"
      }
    }
  },  
  "coworkUserFilesPath": "C:\\Users\\certdog\\Claude",
  "preferences": {
  ...
}
```

Note that the ``coworkUserFilesPath``, ``preferences`` (as shown above) and ``other sections`` will already be present in the config

<br>

If you want to enable write operations (certificate requests, revocation etc.) then also add ``"CERTDOG_WRITE_TOOLS" : true`` to the ``env`` section e.g.

```json
{
  "mcpServers": {
    "certdog": {
      "command": "java",
      "args": [
        "-Djavax.net.ssl.trustStoreType=Windows-ROOT",
        "-jar",
        "C:\\certdog\\certdog-mcp.jar"
      ],
      "env": {
        "CERTDOG_URL": "https://certdog.svr.local/certdog/api",
        "CERTDOG_API_TOKEN": "eyJhbGciOiJ...X1-XUBWnKuYLv6",
        "CERTDOG_WRITE_TOOLS": true
      }
    }
  },  
  "coworkUserFilesPath": "C:\\Users\\certdog\\Claude",
  "preferences": {
  ...
}
```

<br>

If you have created a dedicated account for write operations (certificate requests, revocation etc.) and you only want that account to be used for write operations, then add a second certdog instance such as ``certdog-write``, giving that accounts API key. For example:

```json
{
  "mcpServers": {
    "certdog": {
      "command": "java",
      "args": [
        "-Djavax.net.ssl.trustStoreType=Windows-ROOT",
        "-jar",
        "C:\\certdog\\certdog-mcp.jar"
      ],
      "env": {
        "CERTDOG_URL": "https://certdog.svr.local/certdog/api",
        "CERTDOG_API_TOKEN": "{API TOKEN}"
      }
    },
    "certdog-write": {
      "command": "java",
      "args": [
        "-Djavax.net.ssl.trustStoreType=Windows-ROOT",
        "-jar",
        "C:\\certdog\\certdog-mcp.jar"
      ],
      "env": {
        "CERTDOG_URL": "https://certdog.svr.local/certdog/api",
        "CERTDOG_API_TOKEN": "{USER API TOKEN}",
        "CERTDOG_WRITE_TOOLS": true
      }
    }
  }
```

This will ensure that any write operations are carried out with that user (whose API key is ``{USER API TOKEN}``),  whereas read operations are carried out by an admin user

<br>

Restart Claude Desktop. Close the window and right click the start bar running icon and click **Exit**. Then start

<br>

### Setup with Claude Code

Note that Java 21 or later is required. If running from the command line, confirm this by running:

```
java -version
```

![image-20261022150008509](./images/image-20261022150008509.png)

<br>

Start Claude Code from the command line or Desktop app

![image-20261022144935463](./images/image-20261022144935463.png)

At the prompt, run the following command:

```
claude mcp add certdog 
	-s user 
	-e CERTDOG_URL={API URL} 
	-e CERTDOG_API_TOKEN={API TOKEN} 
	-- java -Djavax.net.ssl.trustStoreType=Windows-ROOT 
	-jar {MCP JAR PATH}
```

E.g.

```
claude mcp add certdog 
	-s user 
	-e CERTDOG_URL=https://certdog.svr.local/certdog/api 
	-e CERTDOG_API_TOKEN=eyJhbGciOi...1S-J9Lk7A 
	-- java -Djavax.net.ssl.trustStoreType=Windows-ROOT 
	-jar c:\certdog\certdog-mcp.jar
```

(Note, the new lines are added for readability and will need to be removed before running)

<br>

As above, to allow write operations, also provide the ``CERTDOG_WRITE_TOOLS=true`` environment variable:

```
claude mcp add certdog 
	-s user 
	-e CERTDOG_URL=https://certdog.svr.local/certdog/api 
	-e CERTDOG_API_TOKEN=eyJhbGciOi...1S-J9Lk7A 
	-e CERTDOG_WRITE_TOOLS=true
	-- java -Djavax.net.ssl.trustStoreType=Windows-ROOT 
	-jar c:\certdog\certdog-mcp.jar
```

<br>

And if you want to only allow the write operations to be carried out by a restricted user, you may add a second MCP configuration, providing that user's API token:

```
claude mcp add certdog-write 
	-s user 
	-e CERTDOG_URL={API URL} 
	-e CERTDOG_API_TOKEN={USER API TOKEN} 
	-e CERTDOG_WRITE_TOOLS=true
	-- java -Djavax.net.ssl.trustStoreType=Windows-ROOT 
	-jar {MCP JAR PATH}
```

<br>

From the prompt type:

```
/mcp
```

The instance should show as connected. If not, select and choose reconnect

Failure to start is often due to the API not being reachable (certdog service not running), the API key being incorrect or the wrong java version being used. Check these settings if connection fails

<br>

To remove an MCP server run:

```
claude mcp remove certdog
```



