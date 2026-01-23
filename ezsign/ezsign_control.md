---
layout: default
title: EzSign - Control
parent: EzSign
nav_order: 6
---
# EzSign Control

<br>

The Control utility connects to the running server on the specified control port and enables the live monitoring of the server status (running or stopped), the pausing and resuming of the server and the ability to alter the logging level whilst the server is running

Run the ``ezsign-server-ctrl`` script to start the EzSign Control utility

The script requires two parameters: the **IP Address** and **Control Port** of the server e.g:

```
ezsign-server-ctrl 127.0.0.1 5657
```

These are the values set by the following properties in the server properties file:

```
server.ctrl.bindIpAddress
server.ctrl.port
```

If an *Authentication Code* is being used on the server’s control interface, this should also be provided at startup via the authCode parameter e.g.

```
ezsign-server-ctrl 127.0.0.1 5657 authCode=1f84-66c2-29f5-a60b
```

In this case the Authentication Code is ``1f84-66c2-29f5-a60b``

Starting the utility in this way will display the menu, enabling the user to select the option required

This script may also be called with an action supplied to carry out the operation with no further interaction required e.g.

To obtain the running status of the server:

```
ezsign-server-ctrl 127.0.0.1 5657 status
```



To pause the server:

```
ezsign-server-ctrl 127.0.0.1 5657 pause
```



To resume the server

```
ezsign-server-ctrl 127.0.0.1 5657 resume
```



To shut down the server process

```
ezsign-server-ctrl 127.0.0.1 5657 stopdaemon
```



To change the log level

```
ezsign-server-ctrl 127.0.0.1 5657 loglevel=3
```



