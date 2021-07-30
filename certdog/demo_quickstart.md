---
layout: default
title: Free Version Installation and Setup
parent: Certdog
nav_order: 2
---

# Certdog Free Installation and Setup

 

## Pre-Requisites

* .NET v4.8 runtime
* Administrator privileges  
* Windows Server 2016/2019
* Windows 10

If installing on Windows 10 and you require access to a Microsoft ADCS Certificate Authority the RSAT (Remote Server Administration Tools) for Windows 10 are also required



## Download

1. Download from [here](https://krestfield.s3.eu-west-2.amazonaws.com/certdog/certdogfree_v140_win.zip)

   File Hashes:

   * SHA1: ``9c44e13d2a115f07939ecf63d6ac8aabf62f6974``

   * SHA256: ``52192f8e339c2fae08a900a4a325296980d050de9a4162dd85d57739572cb6f2``

     

2. Unzip to a location on your drive e.g. if you unzip to C:\ you will end up with a directory **C:\certdogfree** (but you can place this anywhere on your system)



## Installation

1. Open a PowerShell as **Administrator**, navigate to the **certdogfree\install** directory and run:

   ``.\install.ps1``

   Note: if you do not have a component installed (VC++ runtime or the correct .NET version) the installer will halt at this point and prompt you to install these components

   

2. At the prompt `Download java (y/n)?` Enter **y** 

   

3. A  the prompt `Download the database binaries (y/n)?` Enter **y**

   

4. In the **Database User Admin Account Setup** section, at the prompt `Please enter the password for this account:` enter a *password*

   

5. In the **First Admin User Account Setup** section enter a *username*, *email* (this email will be used to send certificate renewal reminders - if configured) and *password* e.g.

   ``Enter the username:`` **admin**  
   ``Enter the email address:`` **me@myemail.com**  
   ``Please enter the password:`` **password**    

This is the account you will first log on to the app with 

   

8. In the **Available interfaces** section, choose **0.0.0.0 (Listen on all)** (or **127.0.0.1** if you want to limit to local machine access only)

   

9. In the **Installing Application Service** section, enter a password e.g.:

   ``Please enter the master password:`` **password**

   

10. At the prompt ``Do you wish to install the ADCS agent on this machine (y/n)?`` Enter **y**

    Note: This is required if you wish to interface to Microsoft ADCS instances



If installation was a success and no errors were observed, a browser should open at https://127.0.0.1/certdog. If local restrictions disallow this, manually navigate to that address from your chosen browser



Login with the *username* and *password* entered in step 5 above



Note that a default TLS certificate is configured for 127.0.0.1. You can issue a new TLS certificate to replace this or temporarily install the root from here: ``.\certdog\config\sslcerts\dbssl_root.cer`` 



If you hit any issues, see the troubleshooting guide [here](install_troubleshooting.html)



## Configuration



### 1. Create a Local CA

1. From the menu, select **Local CA > CA Configuration** and click **Add New CA**

2. Enter the details for a new Root CA - provide a **name**, **Subject DN** and **lifetime**, everything else can be left at the defaults. Note: CRL Distribution Points, AIA extensions and CRL generation options can be edited later, other settings (key size etc.) cannot (though you can generate new CAs with different settings)

3. Click **Create**

You can now Create more CAs (including Subordinate CAs) as required




### 2. Create a Certificate Profile

1. From the menu, select **Local CA > Profiles** and click **Add New Profile**

2. Give the Profile a **name**, a **lifetime** and select **usages**. E.g. For a TLS certificate profile, select the following Key Usages:

   * **digitalSignature**

   * **keyEncipherment**

3. And the following for Enhanced Key Usages:

   * **serverAuth** 

4. Click **Add**




### 3. Create a Certificate Issuer

1. From the menu, select **Certificate Issuers** and click **Add New Issuer**

2. Select **Local CA** from the drop down and click **Next**

3. Provide a **Name** for this issuer (this is the name you will reference when requesting certificates)

4. select the **Local *CA* Configuration** and the **Profile** created above

5. Select the **Admin Team** and click **Add**



### 4. Create a CSR Generator
1. From the menu, select **CSR Generators** and click **New CSR Generator**

2. Give the generator a **Name** and click **Add**

   

### 5. Issue a Certificate
1. Now select **Request > DN Request** from the menu
2. Enter a **Subject DN** (e.g. CN=First Cert) and a **P12 Password** and click **Request Certificate**  

Your certificate will be issued from the CA you just created. It will include the details you configured in the profile

3. Download the PKCS#12 if required  

4. For further details, click **More**  

You can now also issue certificates via the [REST API](https://127.0.0.1/certdog/api/swagger-ui.html), or by using the [.NET client](https://github.com/krestfield/certdog-dotnet-client) or the [Java client](https://github.com/krestfield/certdog-java-client). Use the [IIS Script](https://github.com/krestfield/certdog-iis) to automate IIS cert issuance and renewal or use the scripts to [manage windows machine certificates](https://github.com/krestfield/certdog-cert)



## Further Options
To allow the download of the PKCS#12 files (or JKS, PKCS#8) at a later time, from the menu, select **Settings > Settings**

Set **Private Key Retention Period** to a value greater than zero and click **Update**

If you now issue a certificate its key will be retained for this period and can be downloaded with the certificate in PKCS#12, JKS or PKCS#8 formats



If you installed the ADCS Agent, select **Agents** from the menu and you should see an agent entry for the host machine name, set as *Not Approved*. Select it and click **Approve**. You will now be able to configure a [Microsoft CA as a Certificate Issuer](create_adcs_certificate_issuer.html)



Full Documentation: [https://krestfield.github.io/docs/certdog/certdog.html](https://krestfield.github.io/docs/certdog/certdog.html)

