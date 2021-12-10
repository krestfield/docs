---
layout: default
title: Email Settings
parent: Certdog
nav_order: 20
---
# Email Settings

The settings can be viewed by selecting the **Settings > Email Settings** option on the menu  

<img src=".\images\email_settings.png" alt="image-20210122142648429" style="zoom:67%;" />

Emails can be configured to be sent when:

* A certificate is issued
* A certificate is nearing its expiry date



But before any emails can be sent you must configure your email server settings. This is the SMTP server that will send the emails to the recipients



> If this is the first time you are testing emails - ensure you have created a new user or have updated the default admin user's email address. Otherwise emails will be sent to the default bogus email address 

<br>

### Server Settings

The email server can be a local SMTP gateway or an internet provided service. This service should be able to provide the details required below  

Click on Server Settings to expand:  

<img src=".\images\email_server_settings.png" alt="image-20210122145623039" style="zoom:67%;" />

Populate the following settings

* Host Server
  * The SMTP server
* Host Port
  * The port. For non TLS connections this may be 25, for TLS connections it may be 465 or 587
* Authentication Required
  * Most provided services will require this. When checked you must populate the username and password fields
* Username
  * The username provided by the SMTP service
  * This may be a common ID e.g. apikey or a username
* Password
  * The password provided by the SMTP service
  * This may be an API key provided as a long string of text
* Use TLS
  * If the provider supports TLS, check this
  * Note that this option may be tied to the port you use. E.g. port 25 may not support TLS
* From Email Address
  * The email address you want emails to appear to have been sent from
  * You may have to register this with your SMTP provider

<br>

**System URL**

In order for the [CERTURL] tag to be correct, you must enter a value for **System URL**. This must be the server name and location a user would use to access the system  

The server name will be the DNS name and the location will usually be **/certdog** but this can be changed depending on how you host the system  

As an example, on initial setup you may access the login page here:  

https://127.0.0.1/certdog/ui/#/login

In this case you would set the *System URL* to be:  

https://127.0.0.1/certdog

Later, when you configure your DNS entries, you may access the server at:  

https://certdog.corpdomain.com/certdog/ui/#/login

So now the *System URL* would be:

https://certdog.corpdomain.com/certdog

<br>

### Send Emails on Certificate Issue

Check this box if you want an email to be sent whenever a certificate is issued  

<img src=".\images\send_emails_on_issue.png" alt="Send On Issue" style="zoom:80%;" />



You can set the email subject and body templates of the emails that will be sent. You can use standard html tags in the body as well as the following additional tags:

* [CERTDATA]
  * This will insert the issued certificate's data (PEM formatted)
* [CERTURL]
  * This will resolve to the URL that when entered into a browser will take the user to the details page for that certificate
* [CERTRENEWURL]
  * This is the URL that can be accessed to renew this certificate

* [CERTSUBJECT]
  * The certificate subject e.g. CN=mydomain.com,O=krestfield
* [CERTISSUER]
  * The certificates issuer DN
* [VALIDFROM]
  * The valid from date of the certificate
* [VALIDTO]
  * The expiry date of the certificate
* [SERIALNUM]
  * The certificates serial number
* [DAYSTOEXPIRY]
  * The number of days until the certificate expires

<br>

**Always Send To**

If you wish to send an email to an address (or addresses) in addition to the one being sent to the requester, enter the email address(es) here. For multiple email addresses enter as a comma separated list e.g.

```
casupport@krestfield.com, ca@krestfield.com
```

For emails in this field, every time an email is sent to a user the same email will also sent to these email addresses

This option can be used as a notification - when certificates or issued, or as an additional audit record (in addition to the logs)  

Leave this field blank to not send additional emails

<br>

<br>

### Send Emails on Certificate Expiry

If this option is checked users will get email reminders when certificates are nearing expiry  

<img src=".\images\send_emails_on_expiring1.png" alt="Expiry Reminders" style="zoom:80%;" />

Configure the email subject and body templates as before, utilising the available tags  

<br>

**Send Notification on Days**  

This value is simply a comma separated list which indicates how many days before expiry a reminder will be sent e.g. 5,10,15 indicates that reminders will be sent when certificates are expiring in 5, 10, or 15 days

See [Certificate Expiry Reminders](certificate_expiry_reminders.html) for more details

  <br>

**Always Send To**

As above, for every reminder email sent, the same email will be sent to these additional addresses. This can be useful for another team to also obtain reminders for all certificates or as an audit to validate that emails are being sent

  

Once all settings have been configured click **Update**  

When emails are sent, logs will be added. It is a good idea to set emails to be sent on issue and then issue a test certificate to confirm all of the SMTP server settings etc. are correct. If there are any issues, check the logs and then verify your settings
<br>

### Suppression

Emails can be suppressed for individual certificates as well as teams  

Expiry monitoring can be disabled for a specific certificate. This means no expiry reminder emails will be sent for that certificate  

A Team can suppress *cert issued* and *cert expiring* emails. If a certificate is within a team that has one of both of these items checked, emails will not be sent for that certificate. See the [teams documentation](teams.html) for more information

<br>

### Additional Settings

It is possible to setup multiple Certdog API services all using the same database. If you have more than one server configured you may set just one of these servers to manage the email sending

Sending of emails can be switched off for specific servers by editing the ``application.properties`` file located at ``[Certdog Install]\config`` e.g.

```shell
c:\certdog\config\application.properties
```

Set the following setting to false as shown below:

```properties
# If set to true, this server will send emails, otherwise no emails will be sent from this server
# Set this to false if you have multiple servers running as you will only want one to send emails
email.thisserver.send=false
```

Once restarted, the server will no longer send any emails

<br>

If the sending of an email fails (due to incorrect SMTP server configuration or connectivity issues etc.), an attempt to re-send the same email will be made at a a later time. This time is set to 6 hours (360 minutes) by default. If you wish to change this period, edit the ``application.properties`` file and update the following

```properties
# If an email fails to send, this is the time the server will wait before retrying
email.resenddelay.minutes=360
```

Note that whenever the server settings are updated, an attempt will be made to re-send failed emails. E.g. if the incorrect SMTP host, username or password were entered, when these are corrected emails will be sent
