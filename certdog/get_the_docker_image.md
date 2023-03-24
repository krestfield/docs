---
layout: default
title: Get the Docker Image
parent: Certdog
nav_order: 5
---
# Get the Docker Image

Take a look here on the docker hub:

[https://hub.docker.com/r/krestfield/certdog](https://hub.docker.com/r/krestfield/certdog)

Or just grab the image:

```bash
docker pull krestfield/certdog
```

Start the image:

```bash
docker run -d -p 443:443 --name certdog krestfield/certdog
```

And when running, open a  browser and navigate to:  

[https://127.0.0.1](https://127.0.0.1)  

Making sure you don't have any other instances of IIS, Apache or Tomcat listening on port 443  

Login with username: **admin** password: **password**  



### Issue a Certificate

The image comes pre-configured with a Local CA and profiles for TLS and Code Signing - more can be easily added  

From the menu, choose **Request  > DN Request**

<img src=".\images\image-20210121134446386.png" alt="image-20210121134446386" style="zoom:67%;" />

Enter a value for the **DN** and enter a **password** (the issuer and CSR generator fields should be pre-populated for now). If you want to add any SANs (Subject Alternative Names, click the drop down and add). Then click **Request Certificate**  

<img src=".\images\first_cert_issued.png" alt="image-20210121134641020" style="zoom:67%;" />

Click **Download PKCS12** and save the file. Then click **More** to view further details about the certificate  

Browse the other documentation to set up more CAs, add users etc. Remember all operations can also be carried out via the REST API for scripting common tasks





