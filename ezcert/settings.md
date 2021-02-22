---
layout: default
title: Settings
parent: EzCert
nav_order: 19
---
# EzCERT Settings

The settings can be viewed by selecting the **Settings > Settings** option on the menu

<img src=".\images\settings.png" alt="image-20210222163700318" style="zoom:80%;" />

* Private Key Retention Period
  * If a user generates a certificate using the *Request DN* option, then EzCERT also generates the keys and CSR. This period defines for how long this data will be retained by the system
  * Whilst the key data is retained the owner of the certificate can return to the system and download the certificate as a PKCS#12, JKS or PEM file. Once this period has expired, this data will be purged from the system and will no longer be available
* API Key Total Lifetime
  * When a user logs in successfully, an authorisation token (or API key) is returned which the user (or user interface) uses to authenticate from then on
  * This value determines for how long that token/key can be used before it expires. When it expires a user will be required to re-authenticate - even if they are still using the system
  * It can be set to last for up to 24 hours (86400 seconds) but in reality this figure will not normally be reached as systems using the API will be logging in and logging off as they call the API and a user is unlikely to be continually using the UI for that period of time
  * If you want to enforce users or systems to authenticate more frequently (you may not want systems calling the API to retain a valid key for a long period), reduce this figure
* API Key Inactive Timeout
  * This is the period after which a user will be logged out of the system if they have not carried out any operation
  * The API Key Total Lifetime value will only be reached if the system is continually being called within the API Key Inactive Timeout value
* Certificate Request Timeout
  * When a certificate request is made to a Microsoft CA, this is the time the system will wait for a response before it assumes the CA is down or non-contactable
* Template Request Timeout
  * As above but this timeout occurs when attempting to obtain the list of templates from the CA
* Response Poll Interval
  * This is the time the API will wait (in milliseconds) before checking if the ADCS Agent has obtained a certificate. If you have a fast CA, this can be reduced for more responsiveness 

