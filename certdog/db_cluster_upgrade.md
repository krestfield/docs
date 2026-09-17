---
layout: default
title: Database Cluster Upgrade
parent: Certdog
nav_order: 1201
---

# Database Cluster Upgrade

> From Version: 1.16.0

<br>

If running the databases in a cluster (using the setup described [here](certdog_ha_config.html)) and have been instructed to update the database then follow the steps below

<br>

## Pre-requisites

This configuration is supported on Certdog from version 1.16 onwards.

The certmanadmin database admin password is available. This password would have been configured during initial installation

The cluster has been configured as described in [High Availability Configuration](certdog_ha_config.html) and is healthy. To confirm the status from ``.\certdog\mongodb\bin`` run

```
mongo.exe mongodb://certmanadmin@node1.krestfield.local/admin?tls=true
```

Replacing ``node1.krestfield.local`` with the FQDN of a node in your cluster

(For later versions of mongo - e.g. if you have previously upgraded - use ``mongosh.exe`` instead of ``mongo.exe``)

Type:

```
rs.status()
```

If you receive unauthorised, first run:

```
db.grantRolesToUser("certmanadmin", [ { role: "clusterAdmin", db: "admin" } ])
```

Then retry. You may need to reconnect

The output from ``rs.status()`` should show each node, which is primary and which are secondary and their health. E.g.

```
  members: [
    {
      _id: 0,
      name: 'node1.krestfield.local:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      ...
    },
    {
      _id: 1,
      name: 'node2.krestfield.local:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      ...
    },
    {
      _id: 2,
      name: 'node3.krestfield.local:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      ...
    }
  ]
```

Ensure that the health of all nodes is 1

Note that the environment will be out of service during this upgrade

<br>

## Steps

We will be performing the following steps:

1. Obtain the new database binaries
2. Identify the primary node in the cluster
3. Grant the clusterAdmin role
4. Shutdown the Certdog Service on all nodes
5. Take a dump of the current data from the primary node

4. Stop all database service on all nodes and upgrade the binaries

5. On the primary node, disable database authentication and re-create the cluster
6. On the primary node, restore the data
7. On the primary node, re-enable authentication
8. Start the other nodes
9. Start the Certdog Service on all nodes

<br>

### 1. Obtain the new database binaries

Download the new database from:

https://krestfield.s3.dualstack.eu-west-2.amazonaws.com/certdog/components/mongodb.zip

Create a folder within the ``certdog`` installation called ``mongodb.new`` and unzip the contents of the zip there

Do this on each of the nodes

You should have a file structure something like this:

```
.\certdog
	\bin
	\config
	\java
	\logs
	\mongodb      <== The existing binaries
		\bin
		...
	\mongodb.new  <== The new binaries
		\mongodb
			\bin
			...
```

<br>

### 2. Identify the primary node in the cluster

From any node, open a command prompt as Admin and navigate to ``.\certdog\mongodb.new\mongodb\bin``. Run the following command:

```
mongosh.exe mongodb://certmanadmin@[SERVER]/admin?tls=true
```

E.g. if we are on node1.krestfield.local, the command would be:

```cmd
mongosh.exe mongodb://certmanadmin@node1.krestfield.local/admin?tls=true
```

Enter the database admin password when prompted

*Note: If you see the message ``MongoNetworkError: unable to get local issuer certificate`` this usually indicates that the certificates protecting the DB end points - as configured in the ``tls`` sectrion of the ``mongod.cfg`` file - are not fully trusted. Ensure the root and intermediate certificates are included in the local machines store. Alternatively, to ignore this message, at the end of the connection string replace ``tls=true`` with ``tls=true&tlsAllowInvalidCertificates=true``*

If the prompt shows:

```
replocal [direct: primary] admin>
```

Then you are on the primary server and we can continue with this connection. Skip to **3. Grant the clusterAdmin role** below

NOTE: For the purposes of this document, we will assume that **node1.krestfield.local is the *primary* node**, with node2.krestfield.local and node3.krestfield.local being the *secondary* nodes

<br>

If the prompt shows:

```
replocal [direct: secondary] admin>
```

Then we are on a secondary. In this case run:

```
db.hello{}
```

Which will display information such as the following:

```
replocal [direct: secondary] admin> db.hello()
{
  topologyVersion: {
    processId: ObjectId('6aa409e8e43871a69eb415d6'),
    counter: Long('4')
  },
  hosts: [
    'node1.krestfield.local:27017',
    'node2.krestfield.local:27017',
    'node3.krestfield.local:27017'
  ],
  setName: 'replocal',
  setVersion: 7,
  isWritablePrimary: false,
  secondary: true,
  primary: 'node1.krestfield.local:27017',  <=== THIS IS THE PRIMARY
  me: 'node3.krestfield.local:27017',
  ...
```

Note the value for primary (in this example ``node1.krestfield.local``). This is the primary node and the one we need to connect to

Type ``exit`` to exit this connection and reconnect to the primary node e.g. in this example ``node1.krestfield.local``:

```
.\mongosh.exe mongodb://certmanadmin@node1.krestfield.local/admin?tls=true
```

Now continue to **3. Grant the clusterAdmin role** below

<br>

### 3. Grant the clusterAdmin role

From the mongosh prompt, run the following to grant the cluster admin role:

```
db.grantRolesToUser("certmanadmin", [ { role: "clusterAdmin", db: "admin" } ])
```

Type ``exit`` to exit the connection

<br>

### 4. Shutdown the Certdog Service on all nodes

From each of node, stop the **Krestfield Certdog Service** service:

<img src="./images/image-20260916163403396.png" alt="image-20260916163403396" style="zoom:67%;" />

<br>

### 5. Take a dump of the current data from the primary node

Navigate to the ``.\certdog\mongodb.new\mongodb\dbtools\bin`` and run the following command:

```
mongodump.exe /uri:mongodb://certmanadmin@node1.krestfield.local /ssl /tlsInsecure /out:..\..\..\dump
```

Ensuring you enter your primary server instead of node1.krestfield.local

This should create a folder under ``mongodb.new`` called ``dump``

<br>

### 6. Stop all database service on all nodes and upgrade the binaries

Starting with secondary and  finishing on the primary node, stop the **Krestfield Certdog Database** service on all servers

Rename the existing ``.\certdog\mongodb`` to ``.\certdog\mongodb.bak`` thus creating a backup

Then copy ``.\certdog\mongodb.new\mongodb`` to ``.\certdog\mongodb``

This places the new binaries at the correct location

<br>

Copy the ``mongod.cfg`` file from the backup to the new files location i.e. copy ``.\certdog\mongodb.bak\bin\mongod.cfg`` to ``.\certdog\mongodb\bin\mongod.cfg``

<br>

### 7. On the primary node, disable database authentication and re-create the cluster

Open ``.\certdog\mongodb\bin\mongod.cfg`` and comment out the TLS and security sections (using the ``#`` character at the start of the line) as shown below:

```
...
net:
   bindIp: 127.0.0.1,node2.krestfield.local
   port: 27017
#   tls:
#        mode: requireTLS
#        certificateKeyFile: C:\certdog\mongodb\..\config\sslcerts\dbssl.pem
#        CAFile: C:\certdog\mongodb\..\config\sslcerts\dbssl_root.pem
#        allowConnectionsWithoutCertificates: true
setParameter:
   enableLocalhostAuthBypass: false
replication:
   replSetName: replocal
#security:
#   authorization: "enabled"
#   clusterAuthMode: x509
```

Save the file

<br>

Start the database on this node

<br>

Open a command prompt and connect using mongosh (now located in ``.\certdog\mongodb\bin``) but this time, we connecting to the localhost (``127.0.0.1``) address and authentication is not required:

```
mongosh.exe mongodb://localhost:27017
```

Run the following commands, to initialise the cluster with this single node:

```
rs.initiate({_id: "replocal", members: [{_id: 0, host: "127.0.0.1:27017"}] })
```

Then

```
rs.status
```

And

```
rs.status()
```

And then type ``exit`` to close the connection

<br>

### 8. On the primary node, restore the data

Navigate to ``.\certdog\mongodb\dbtools\bin`` and run:

```
mongorestore.exe /uri:"mongodb://localhost:27017" "..\..\..\mongodb.new\dump"
```

There will be a lot of output but the final line should report something such as:

```
2026-09-11T23:17:46.770+0100    8740 document(s) restored successfully. 0 document(s) failed to restore.
```

<br>

### 9. On the primary node, re-enable authentication

Now uncomment the sections that were commented out in ``mongod.cfg`` above by removing the ``#`` characters from the start of the lines

Restart the database

Connect to this upgraded DB by navigating to ``.\certdog\mongodb\bin`` and running:

```
mongosh "mongodb://certmanadmin@node1.krestfield.local/admin?tls=true
```

Enter the certmanadmin DB password when prompted

If you see:

``MongoNetworkError: unable to get local issuer certificate``

Then include the ``tlsAllowInvalidCertificates=true``. i.e.

```
mongosh "mongodb://certmanadmin@node1.krestfield.local/admin?tls=true&tlsAllowInvalidCertificates=true"
```

Note: This is temporary and is caused as this node in the cluster is referenced as 127.0.0.1 but certificates will reference the full FQDN of the node. We will change this in the next steps

And run:

```
rs.status()
```

You should see that this is the only node in the cluster:

```
members: [
    {
      _id: 0,
      name: '127.0.0.1:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 97,
      optime: { ts: Timestamp({ t: 1789165257, i: 1 }), t: Long('2') },
      optimeDate: ISODate('2026-09-11T22:20:57.000Z'),
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: 'Could not find member to sync from',
      electionTime: Timestamp({ t: 1789165167, i: 1 }),
      electionDate: ISODate('2026-09-11T22:19:27.000Z'),
      configVersion: 1,
      configTerm: 2,
      self: true,
      lastHeartbeatMessage: ''
    }
  ]
```

<br>

Run the following commands ensuring that the specified node (node1) is the primary:

```
cfg = rs.conf()
cfg.members[0].host = "node1.krestfield.local:27017"
rs.reconfig(cfg)
```

This updates the node in the cluster to use the FQDN, as other nodes will need to connect. You can confirm the changes by running ``rs.status()`` again

<br>

### 10. Start the other nodes

Start the Krestfield Certdog Database on the other nodes and wait for them to start

Then back on the primary node, from the same prompt used above, add in the other nodes to the cluster by running the following commands:

```
rs.add("node2.krestfield.local:27017");
rs.add("node3.krestfield.local:27017");
```

Run the following command:

```
rs.status()
```

This time, under members you should see all three nodes with one is showing as the PRIMARY and the others as SECONDARY:

```
  members: [
    {
      _id: 0,
      name: 'node1.krestfield.local:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      ...
    },
    {
      _id: 1,
      name: 'node2.krestfield.local:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      ...
    },
    {
      _id: 2,
      name: 'node3.krestfield.local:27017',
      health: 1,
      state: 2,
      stateStr: 'SECONDARY',
      ...
    }
  ]
```

<br>

### 11. Start the Certdog Service on all nodes

On each node, start the Krestfield Certdog Service

<br>

Optionally, you may revoke the clusterAdmin from the certmanadmin user (that was added at the start of this process), using the following command from mongosh:

```
db.revokeRolesFromUser("certmanadmin", [{ role: "clusterAdmin", db: "admin" }])
```

