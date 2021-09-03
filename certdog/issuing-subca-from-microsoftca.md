---
layout: default
title: Issuing Sub CA from Microsoft CA
parent: Certdog
nav_order: 111
---

# Issuing a Sub CA Certificate from a Microsoft CA

Certdog allows the generation of a CSR for a Sub CA which can then be signed by an existing CA. For example, from an offline Microsoft Root CA

To issue the certificate from a Microsoft CA, perform the following:  

  

Place the CSR as a file on the CA where you want to issue the certificate from. Name the file with a .req extension

From the Microsoft CA snapin, right click the CA and select **All Tasks** > **Submit new request...**

![image-20210903090559353](.\images\ms_ca_issue_sub_ca.png)

Browse to the file containing the CSR saved above and click **Open**

By default the request will be taken *under submission* and must be manually issued. Select the **Pending Requests** folder, locate and right-click your request and choose **All Tasks** > **Issue**

![image-20210903091903018](.\images\ms_ca_issue_sub_ca2.png)

The certificate will be issued and will appear in the **Issued Certificates** folder. Export this certificate to a file. Also export the CA certificate as both are required when importing back into Certdog  



<hr/>

If your issuing CA is not an offline root, when attempting to issue the certificate the Microsoft CA may display an error such as:  

![image-20210903093244573](.\images\ms_ca_issue_sub_ca3.png)

In this case, as the CA is domain joined, it is expecting the CSR to include a Microsoft specific extension telling it what template to use to issue the certificate  

Certdog doesn't know what templates the CA is hosting and this extension is therefore not included (this is also the case when tools such as OpenSSL are used)

But all we need to do is tell the Microsoft CA what template to use. As follows:

* On the CA (or on a machine in the same domain as the CA), open a command prompt as Administrator  
* Ensure that the account you are using has permissions to issue certificates from the CA and from template being targeted

To discover what templates are available, at the prompt, type

```powershell
certutil -catemplates -config "Machine\CAName"
```

e.g.

```powershell
certutil -catemplates -config "RootCA.krestfield.int\Krestfield Root"
```



To discover what CAs are available (in order to obtain the *-config* information required in the command above), just type:

```powershell
certutil
```

and extract the config information  



* At the prompt, type:

```powershell
certreq -attrib "CertificateTemplate:KrestfieldSubCA"
```

and press **Enter**

You will be prompted to browse to your request file (that you saved earlier with the .req extension)

If there are multiple CAs in the domain, you will also be prompted for what CA to use to issue the certificate. To avoid this prompt you may specify the CA config in the request as follows:

```powershell
certreq -attrib "CertificateTemplate:KrestfieldSubCA" -config "RootCA.krestfield.int\Krestfield Root"
```



The certificate may be taken under submission (if the template is configured in this way), in which case follow the instructions above to issue the certificate

