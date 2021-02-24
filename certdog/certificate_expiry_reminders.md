---
layout: default
title: Certificate Expiry Reminders
parent: Certdog
nav_order: 21
---

# Certificate Expiry Reminders

A reminder email can be sent to the certificate owner informing them of upcoming expiry of their certificate  

This is configured in the **Settings > Email Settings** section  

Refer to [Email Settings](email_settings.html) for more information on configuring the emails  



### Reminder Days

You can configure how many days before expiry a user is notified  

For example, you may want to inform users that their certificate is expiring 30 days before expiry and that's all  

In this case, in the Email Settings, you would set the *Send Notification on Day(s)* value to **30**

With this configuration a user will receive one email when their certificate has 30 days left before expiring and then no others



If you also wanted to reminder them closer the time e.g. 10 days before expiry, you would set *Send Notification on Day(s)* value to **30,10**



### Check Schedule

By default, certificates are checked for expiry once a day at 2:15am  

To change this, you must update the following file:  

``[install location]/config/application.properties``

Within this file, locate the following section:  

```properties
# Check for cert expiry at 2:15AM every day
# It you want to change this ensure the cron setting is correct else, you could produce
# many unwanted emails - or none at all...
certexpirycheck.cron=0 15 2 * * ?
```

And update the ``certexpirycheck.cron`` value

Some knowledge of cron settings is required but as an example to change this to 10:15 am every day you would set the following:  

```properties
certexpirycheck.cron=0 15 10 * * ?
```



> Do not set the cron value to run more than once per day as this will result in multiple emails being sent per day

> Always double check and verify any changes. Incorrect changes can result in missed reminders or many unwanted emails being sent

