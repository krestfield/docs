---
layout: default
title: Issuing Sub CA from Microsoft CA
parent: Certdog
nav_order: 111
---

# Issuing a Sub CA Certificate from a Microsoft CA

Certdog allows the generation of a CSR for a Sub CA which can then be signed by an existing CA. For example, from an existing Microsoft Root CA

To issue the certificate from a Microsoft CA, perform the following:  

  

Place the CSR as a file on the CA where you want to issue the certificate from. Name the file with a .req extension

From the Microsoft CA snapin, right click the CA and select **All Tasks** > **Submit new request...**

![image-20210903090559353](.\images\ms_ca_issue_sub_ca.png)

Browse to the file containing the CSR saved above and click **Open**

By default the request will be taken *under submission* and must be manually issued. Select the **Pending Requests** folder, locate and right-click your request and choose **All Tasks** > **Issue**

![image-20210903091903018](.\images\ms_ca_issue_sub_ca2.png)

The certificate will be issued and will appear in the **Issued Certificates** folder. Export this certificate to a file. Also export the CA certificate as both are required when importing back into Certdog  



<hr/>

If you see an error such as the following:  

![image-20210903093244573](.\images\ms_ca_issue_sub_ca3.png)

Or the certificate issued is an end-entity (rather than a CA certificate) then the template information must also be provided

On domain connected CAs it is possible to enable the Subordinate Certificate Authority which you may have duplicated, updated and renamed

Certdog doesn't know what templates the CA is hosting and this extension is therefore not included (this is also the case when tools such as OpenSSL are used)

But all we need to do is tell the Microsoft CA what template to use  



### Offline CA

For a standalone CA, run the following

```powershell
certreq -attrib "CertificateTemplate:SubCA" .\certdog.csr
```

Where certdog.csr is the CSR you generated from certdog

If you see an error warning that the SubCA template does not exist, click OK

You will be prompted for what CA to use to issue the certificate. To avoid this prompt you may specify the CA config in the request as follows:

```powershell
certreq -attrib "CertificateTemplate:SubCA" -config "RootCA.krestfield.int\Krestfield Root"
```

The certificate may be taken under submission (if the template is configured in this way), in which case follow the instructions above to issue the certificate



### Enterprise CA

If the CA is a domain connected enterprise CA, it may have other templates issued for the subordinate CAs. To discover what templates are available, run the following:

```powershell
certutil -catemplates -config "Machine\CAName"
```

e.g.

```powershell
certutil -catemplates -config "RootCA.krestfield.int\Krestfield Root"
```

Where the value for ``-config`` is obtained from the ``Config`` as displayed when you run

```powershell
certutil
```



Identify the template (e.g. *KrestfieldSubCA*) and the run the same commands as for the offline CA above e.g.

```powershell
certreq -attrib "CertificateTemplate:KrestfieldSubCA" .\certdog.csr
```

Again, the certificate may be taken under submission, so must be issued via the CA console. Otherwise, you will be prompted to save the issued certificate

