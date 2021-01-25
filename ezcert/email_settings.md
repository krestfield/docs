---
layout: default
title: Email Settings
parent: EzCert
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
  * This may be a common ID e.g. apikey
* Password
  * The password provided by the SMTP service
  * This may be an API key provided as a long string of text
* Use TLS
  * If the provider supports TLS, check this
  * Note that this option may be tied to the port you use. E.g. port 25 may not support TLS
* From Email Address
  * The email address you want emails to appear to have been sent from
  * You may have to register this with your SMTP provider



### Send Emails on Certificate Issue

Check this box if you want an email to be sent whenever a certificate is issued  



![image-20210122150749792](C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\send_emails_on_issue.png)

You can set the email subject and body templates of the emails that will be sent. You can use standard html tags in the body as well as the following additional tags:

* [CERTDATA]
  * This will insert the issued certificate's data (PEM formatted)
* [CERTURL]
  * This will resolve to the URL that when entered into a browser will take the user to the details page for that certificate
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



**System URL**

In order for the [CERTURL] tag to be correct, you must enter a value for **System URL**. This must be the server name and location a user would use to access the system  

The server name will be the DNS name and the location will usually be **/ezcert** but this can be changed depending on how you host the system  

As an example, on initial setup you may access the login page here:  

https://127.0.0.1/ezcert/ui/#/login

In this case you would set the System URL to be:  

https://127.0.0.1/ezcert

Later, when you configure your DNS entries, you may access the server at:  

https://ezcert.corpdomain.com/ezcert/ui/#/login

So now the System URL would be:

https://ezcert.corpdomain.com/ezcert



### Send Emails on Certificate Expiry

If this option is checked users will get email reminders when certificates are nearing expiry  

Configure the email subject and body templates as before, utilising the available tags  

Then set the values for **Send Notification on Days**  

This value is simply a comma separated list which indicates how many days before expiry a reminder will be sent e.g. 5,10,15 indicates that reminders will be sent when certificates are expiring in 5, 10, or 15 days

See [Certificate Expiry Reminders](certificate_expiry_reminders.html) for more details





Once all settings have been configured click **Update**  

When emails are sent, logs will be added. It is a good idea to set emails to be sent on issue and then issue a test certificate to confirm all of the SMTP server settings etc. are correct. If there are any issues, check the logs and then verify your settings