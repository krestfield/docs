The master password

The API service use an AES key to encrypt data it stores. A master secret is then used to protect this AES key. This master secret/password must be entered when the API service starts

To enable the API service to start without requiring manual intervention, the following options are available:

The master password can be provided in an environment variable called:

cmmasterpassword

If this mechanism is used, then the environment variable should be set for the API service application only (i.e. not system wide). This can be acheived by 

 

The cmmasterpassword variable can also be set to contain the location of a file which contains the master password. To configure this the cmmasterpassword variable should be set as follows:

file:[file containing the master password]

e.g.

cmmasterpassword=file:/opt/cmuser/masterpwd.txt

Where the masterpwd.txt file will contain the master password on the first line of the file