# ADCS Driver

To interface with ADCS (Active Directory Certificate Services) 

The ADCS Driver 



```java
EzCertClient client = new EzCertClient("127.0.0.1", "username", "password");
String b64CertData = client.requestCertP10(csr, "testca1");

```



`EzCertClient client = new EzCertClient("127.0.0.1", "username", "password");`

`client.getCert()`





## Requirements

- Windows Server 2016
- Windows Server 2019
- .NET Framework 4.8





## Installation

Download the installer from [here](https://www.krestfield.com) 

Unzip onto a location on a supported server (see [Requirements](## Requirements)).  This server must be in the domain for the CA you wish to connect to.  

Run the .msi installer

Ensure that port 4474 is open to wherever the database is hosted



