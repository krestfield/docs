---
layout: default
title: High Availability Configuration
parent: Certdog
nav_order: 1200
---

# High Availability Configuration

> From Version: 1.16.0

<br>

The following steps outline a sample how to deploy a multi-instance Certdog installation for high availability use cases.

This is achieved by using a MongoDB replica set to maintain data consistency across all instances. This provides automatic failover of the database.

In this example, we will deploy a three node database replica-set. Two of the nodes will also run the certdog services and can then be load-balanced or referenced via DNS.

The following is the example setup described in this guide:

* node1.krestfield.local
  * Initial Primary DB. Full Certdog installation.

* node2.krestfield.local
  * Initial Secondary DB. Full Certdog installation.

* node3.krestfield.local
  * Initial Secondary DB. Certdog components not running.

Note that this is the initial setup. The databases will adopt the Primary or Secondary roles as required.

<br>

### Pre-requisites

This configuration is supported on Certdog from version 1.16 onwards.

Ensure that three servers are available for the deployment. They must be able to communicate with each other over port 27017.

It is recommended to have a DNS record for each server, as this allows the cluster to continue working even if individual machine IP addresses change, IP addresses may be used but they must be static.

The same version of Certdog must be installed on all nodes.

<br>

### 1. Install certdog on each system

Install certdog on the first node (e.g. node1.krestfield.local). Ensure this is running as expected.

When that installation is stable, install certdog onto node2 and node3 using the same passwords as for node1.

Backup node1 by stopping the Krestfield services and making a copy of the entire installation (e.g. ``c:\certdog``). Once backed up, restart the services.

<br>

For node2 and node3 perform the following additional steps:

1. Obtain the master password from the first node (node1.krestfield.local)

   This is initially written to the protected file called: ``.\certdog\install\MasterSecret.txt`` although it is advised that this file be removed and the secret stored securely.

2. On the second and third nodes (e.g. node2.krestfield.com and node3.krestfield.com), open a PowerShell window as Administrator and run the following command:

   ``.\certdog\install\start-certdog-service.ps1``

   Enter the *master password* when prompted.
   
   E.g.
   
    ```powershell
    PS C:\Program Files\Krestfield\certdog\install> .\start-certdog-service.ps1
   
    Starting Certdog Service
   
    A Master Password is required to start this service the first time
    Store this password securely as it may be needed if changes are made to the configuration
   
    Please enter the master password: *******************************************
    Please confirm the master password: *******************************************
   
    Starting the service...
   
    Service started OK
    ```

Note: node2 and node3 will not be operational until we synchronise the databases.

<br>

### 2. Update the Database Config

On a single instance setup, the database only listens on the localhost address (127.0.0.1). When in a cluster, it will also be accessed from the other nodes. We therefore need to make it available to an interface other than localhost.

For each of the nodes, locate the FQDN of the server (e.g. node1.krestfield.local) or IP Address. It is recommended to use the FQDN but if using an IP Address, it should be static (not dynamic).

Edit the ``.\certdog\mongodb\bin\mongod.cfg`` file.

Update the following section, from:

```
net:
   bindIp: 127.0.0.1
```

to:

```
net:
	bindIp: 127.0.0.1,[FQDN or IP Address]
```

E.g. On node1 this would become:

```
net:
   bindIp: 127.0.0.1,node1.krestfield.local
```

And on node2 this would become:

```
net:
   bindIp: 127.0.0.1,node2.krestfield.local
```

And on node3:

```
net:
   bindIp: 127.0.0.1,node3.krestfield.local
```

<br>

Once applied to all nodes and saved, restart the *Krestfield Certdog Database* service.

<br>

<u>Optional: Test the Connection</u>

The connection between nodes can be tested before proceeding further. In this example we simply attempt to connect to node2 from node1.

From node1, open a PowerShell window and navigate to:

```powershell
.\certdog\mongodb\bin
```

Run the following command:

```powershell
.\mongosh.exe <node2 FQDN or IP Address> -u certmanadmin -p <DB ADMIN PASSWORD> --tls --tlsAllowInvalidCertificates --authenticationDatabase admin
```

Where ``<node2 FQDN or IP Address>`` are the details of the other node (e.g. node2) and ``DB ADMIN PASSWORD`` is the password of the database admin (where username is always ``certmanadmin``)

Note we are bypassing TLS certificate checks with the ``-tlsAllowInvalidCertificates`` at this point as we only wish to verify connectivity. Certificate setup is dealt with in the next section.

e.g.

```powershell
..\mongodb\bin> .\mongosh.exe node2.krestfield.local -u certmanadmin -p complexpassword -tls -tlsAllowInvalidCertificates -authenticationDatabase admin
```

Note that the same DB Admin password should have been used for all installations. If this is not the case, ensure that the correct ``<DB ADMIN PASSWORD>`` is used for the instance being targetted.

This should connect with output as shown below:

```powershell
Current Mongosh Log ID: 69c51384152f64f0a51e2620
Connecting to:          mongodb://<credentials>@node2.krestfield.local:27017/?directConnection=true&tls=true&tlsAllowInvalidCertificates=true&authSource=admin&appName=mongosh+2.5.10
Using MongoDB:          8.0.16
Using Mongosh:          2.5.10
mongosh 2.8.1 is available for download: https://www.mongodb.com/try/download/shell

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

replocal [direct: primary] test>
```

If a connection cannot be made, an output such as the following will be seen instead:

```powershell
Current Mongosh Log ID: 69c5156406dd574ba01e2620
Connecting to:          mongodb://<credentials>@node2.krestfield.local:27017/?directConnection=true&tls=true&tlsAllowInvalidCertificates=true&authSource=admin&appName=mongosh+2.5.10
MongoNetworkError: getaddrinfo ENOTFOUND node2.krestfield.local
```

In this case examine the firewall settings and confirm that port 27017 is open.

Type ``exit`` to close the shell.

<br>

### 3. Update the DB Certificates

There are some additional certificate requirements when forming a cluster. They are:

* The certificates must have both the *Client Authentication* and *Server Authentication* Enhanced Key Attributes.

* They must have the *Digital Signature* and *Key Encipherment* Key Usages.

A single certificate can be issued and deployed to each of the database nodes or separate certificates issued. The certificate DN can be anything but if separate certificates are used, their O, OU and DC components must match (if present). These requirements can be found in the [Mongo DB documentation](https://www.mongodb.com/docs/manual/tutorial/configure-x509-member-authentication/#certificate-requirements).

* The certificate(s) must have *Subject Alternative Names* matching the DB hosts it is protecting.

<br>

In this example, we will issue a single certificate, deploy to node1 then copy to the other nodes.

Note: If issuing from a Certdog CA, then a profile created from the *TLS (Client and Server Auth)* common profile can be used. 

Ensure the CA this certificate is issued from is trusted by all machines in the cluster

<br>

From certdog on node1, place a DN request for a certificate with the following details:

DN: ``CN=Database Cluster,O=My Org,C=GB`` (but can be anything you choose)

SANS: ``IP:127.0.0.1, DNS:node1.krestfield.local, DNS:node2.krestfield.local, DNS: node3.krestfield.local`` - ensuring the FQDNs match the names of your servers

Enter a strong password and issue the certificate.

Follow the [guide here](https://krestfield.github.io/docs/certdog/update_the_db_certificate.html) to set this as the new DB password.



From node1, copy the following files located in ``.\certdog\config\tlscerts\`` :

* dbssl.pem

* dbssl_root.pem

* dbssl_trust.jks

To node2 and node3 at the same location.

<br>

### 4. Prepare the primary

Next, we configure node1 as the primary.

Open a PowerShell window and navigate to:

```powershell
.\certdog\mongodb\bin
```

Run the following command to start the mongo shell:

```powershell
.\mongosh.exe node1.krestfield.local -u certmanadmin -p complexpassword -tls -tlsAllowInvalidCertificates -authenticationDatabase admin
```

Then run the following commands:

```javascript
// switch to the admin database
use admin;
// grant the certmanadmin user the clusterAdmin role to configure the replica set
db.grantRolesToUser("certmanadmin", [{ role: "clusterAdmin", db: "admin" }]);
```

Next, type the following commands to add this node as the primary:

```javascript
// the replica set currently contains one member, 127.0.0.1:27017
// replica sets must use either all localhost references, or none
// so first update the host of the current single member
const cfg = rs.conf();
cfg.members[0].host = "node1.krestfield.local:27017"
rs.reconfig(cfg);
```

Now we add the secondary nodes to the cluster:

```javascript
// next, add the other member(s) to the replica set
rs.add("node2.krestfield.local:27017");
rs.add("node3.krestfield.local:27017");
```

Verify the configuration and remove the clusterAdmin role:

```javascript
// verify the configuration has been updated
// you should see the other members listed
rs.conf();
// you can also check the current status
// ignore any errors listed under members for now
rs.status();

// optionally remove the clusterAdmin role
db.revokeRolesFromUser("certmanadmin", [{ role: "clusterAdmin", db: "admin" }]);
```

There may be errors seen in the output at this time that can be ignored until we configure the secondary nodes.

For an example of output see Appendix A - Primary DB Output below.

<br>

### 5. Prepare the secondaries 

For node2 and node3, stop the *Krestfield Certdog Database* service and delete the contents of this folder:

```
.\certdog\mongodb\dbfiles
```

Do not delete the folder itself, only the contents.

Start the *Krestfield Certdog Database* service on node2 and node3.

<br>

### 6. Update the database URIs

On node1, edit the following file:

```
.\certdog\config\application.properties
```

Locate the following line:

```properties
spring.data.mongodb.uri=mongodb://certmanuser:hkZ2IoHSkQiLAroe3SLA@127.0.0.1/certman?tls=true
```

Replace the existing localhost value of ``127.0.0.1`` with a comma separated list of all the nodes FQDNs. E.g.

```properties
spring.data.mongodb.uri=mongodb://certmanuser:hkZ2IoHSkQiLAroe3SLA@node1.krestfield.local,node2.krestfield.local,node3.krestfield.local/certman?tls=true
```

Ensuring your server FQDNs are used.

<br>

Copy this URL to the ``.\certdog\config\application.properties`` file on node2 and node3 so that all nodes are now using the same database URL.

<br>

If you are using the ADCS driver, open a PowerShell window as Administrator, navigate to ``.\certdog\install`` and run:

```powershell
configure-adcs-service.ps1
```

This configures the ADCS service to use the same URL as just configured.

<br>

## Final Steps

On node3 stop and disable the following services:

* Krestfield Certdog Service

* Krestfield Adcs Driver

This will leave node1 and node2 as the Certdog instances providing the API and UI services with node3 acting as the database node only.

<br>

If using the AD CS driver with a Microsoft CA you will now have two drivers available. Register them both and allow both to be used by the Certificate Issuer.

<br>



---

<br>

## Appendix A - Primary DB Output

The following is an example of the output seen when configuring the database to be a primary, as described in step 4 above.

```javascript
replocal [direct: primary] test> use admin
switched to db admin

replocal [direct: primary] admin> db.grantRolesToUser("certmanadmin", [{ role: "clusterAdmin", db: "admin" }]);
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1774531075, i: 1 }),
    signature: {
      hash: Binary.createFromBase64('AOZ1HaUNM/gfhTr/k8/enVMoCYg=', 0),
      keyId: Long('7621505237248901127')
    }
  },
  operationTime: Timestamp({ t: 1774531075, i: 1 })
}

replocal [direct: primary] admin> const cfg = rs.conf();

replocal [direct: primary] admin> cfg.members[0].host = "node1.krestfield.local:27017"
server1.krestfield.local:27017

replocal [direct: primary] admin> rs.reconfig(cfg);
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1774532495, i: 1 }),
    signature: {
      hash: Binary.createFromBase64('wavfgfGXP/gjDiFUav9Mo+Gbn9Q=', 0),
      keyId: Long('7621505237248901127')
    }
  },
  operationTime: Timestamp({ t: 1774532495, i: 1 })
}

replocal [direct: primary] admin> rs.add("node2.krestfield.local:27017");
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1774532563, i: 1 }),
    signature: {
      hash: Binary.createFromBase64('Inyw5kayz74wHqoVmLbUKtag0s8=', 0),
      keyId: Long('7621505237248901127')
    }
  },
  operationTime: Timestamp({ t: 1774532563, i: 1 })
}

replocal [direct: primary] admin> rs.add("node3.krestfield.local:27017");
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1774532568, i: 2 }),
    signature: {
      hash: Binary.createFromBase64('/DbwvzbSwhZm+fKbzFXCEKgPepE=', 0),
      keyId: Long('7621505237248901127')
    }
  },
  operationTime: Timestamp({ t: 1774532568, i: 2 })
}

replocal [direct: primary] admin> rs.conf();
{
  _id: 'replocal',
  version: 4,
  term: 6,
  members: [
    {
      _id: 0,
      host: 'node1.krestfield.local:27017',
      arbiterOnly: false,
      buildIndexes: true,
      hidden: false,
      priority: 1,
      tags: {},
      secondaryDelaySecs: Long('0'),
      votes: 1
    },
    {
      _id: 1,
      host: 'node2.krestfield.local:27017',
      arbiterOnly: false,
      buildIndexes: true,
      hidden: false,
      priority: 1,
      tags: {},
      secondaryDelaySecs: Long('0'),
      votes: 1
    },
    {
      _id: 2,
      host: 'node3.krestfield.local:27017',
      arbiterOnly: false,
      buildIndexes: true,
      hidden: false,
      priority: 1,
      tags: {},
      secondaryDelaySecs: Long('0'),
      votes: 1
    }
  ],
  protocolVersion: Long('1'),
  writeConcernMajorityJournalDefault: true,
  settings: {
    chainingAllowed: true,
    heartbeatIntervalMillis: 2000,
    heartbeatTimeoutSecs: 10,
    electionTimeoutMillis: 10000,
    catchUpTimeoutMillis: -1,
    catchUpTakeoverDelayMillis: 30000,
    getLastErrorModes: {},
    getLastErrorDefaults: { w: 1, wtimeout: 0 },
    replicaSetId: ObjectId('69c506a24a4d9e0f04cf42ad')
  }
}

replocal [direct: primary] admin> rs.status();
{
  set: 'replocal',
  date: ISODate('2026-03-26T13:43:04.897Z'),
  myState: 1,
  term: Long('6'),
  syncSourceHost: '',
  syncSourceId: -1,
  heartbeatIntervalMillis: Long('2000'),
  majorityVoteCount: 1,
  writeMajorityCount: 1,
  votingMembersCount: 1,
  writableVotingMembersCount: 1,
  optimes: {
    lastCommittedOpTime: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
    lastCommittedWallTime: ISODate('2026-03-26T13:42:55.951Z'),
    readConcernMajorityOpTime: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
    appliedOpTime: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
    durableOpTime: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
    writtenOpTime: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
    lastAppliedWallTime: ISODate('2026-03-26T13:42:55.951Z'),
    lastDurableWallTime: ISODate('2026-03-26T13:42:55.951Z'),
    lastWrittenWallTime: ISODate('2026-03-26T13:42:55.951Z')
  },
  lastStableRecoveryTimestamp: Timestamp({ t: 1774532531, i: 1 }),
  electionCandidateMetrics: {
    lastElectionReason: 'electionTimeout',
    lastElectionDate: ISODate('2026-03-26T13:15:20.979Z'),
    electionTerm: Long('6'),
    lastCommittedOpTimeAtElection: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
    lastSeenWrittenOpTimeAtElection: { ts: Timestamp({ t: 1774530909, i: 1 }), t: Long('5') },
    lastSeenOpTimeAtElection: { ts: Timestamp({ t: 1774530909, i: 1 }), t: Long('5') },
    numVotesNeeded: 1,
    priorityAtElection: 1,
    electionTimeoutMillis: Long('10000'),
    newTermStartDate: ISODate('2026-03-26T13:15:20.982Z'),
    wMajorityWriteAvailabilityDate: ISODate('2026-03-26T13:15:21.082Z')
  },
  members: [
    {
      _id: 0,
      name: 'node1.krestfield.local:27017',
      health: 1,
      state: 1,
      stateStr: 'PRIMARY',
      uptime: 1664,
      optime: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
      optimeDate: ISODate('2026-03-26T13:42:55.000Z'),
      optimeWritten: { ts: Timestamp({ t: 1774532575, i: 1 }), t: Long('6') },
      optimeWrittenDate: ISODate('2026-03-26T13:42:55.000Z'),
      lastAppliedWallTime: ISODate('2026-03-26T13:42:55.951Z'),
      lastDurableWallTime: ISODate('2026-03-26T13:42:55.951Z'),
      lastWrittenWallTime: ISODate('2026-03-26T13:42:55.951Z'),
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      electionTime: Timestamp({ t: 1774530920, i: 1 }),
      electionDate: ISODate('2026-03-26T13:15:20.000Z'),
      configVersion: 4,
      configTerm: 6,
      self: true,
      lastHeartbeatMessage: ''
    },
    {
      _id: 1,
      name: 'node2.krestfield.local:27017',
      health: 0,
      state: 8,
      stateStr: '(not reachable/healthy)',
      uptime: 0,
      optime: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
      optimeDurable: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
      optimeWritten: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
      optimeDate: ISODate('1970-01-01T00:00:00.000Z'),
      optimeDurableDate: ISODate('1970-01-01T00:00:00.000Z'),
      optimeWrittenDate: ISODate('1970-01-01T00:00:00.000Z'),
      lastAppliedWallTime: ISODate('1970-01-01T00:00:00.000Z'),
      lastDurableWallTime: ISODate('1970-01-01T00:00:00.000Z'),
      lastWrittenWallTime: ISODate('1970-01-01T00:00:00.000Z'),
      lastHeartbeat: ISODate('2026-03-26T13:43:04.779Z'),
      lastHeartbeatRecv: ISODate('1970-01-01T00:00:00.000Z'),
      pingMs: Long('0'),
      lastHeartbeatMessage: "replica set IDs do not match, ours: 69c506a24a4d9e0f04cf42ad; remote node's: 69c50aba30e2840c742a0b36",
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      configVersion: -1,
      configTerm: -1
    },
    {
      _id: 2,
      name: 'node3.krestfield.local:27017',
      health: 0,
      state: 8,
      stateStr: '(not reachable/healthy)',
      uptime: 0,
      optime: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
      optimeDurable: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
      optimeWritten: { ts: Timestamp({ t: 0, i: 0 }), t: Long('-1') },
      optimeDate: ISODate('1970-01-01T00:00:00.000Z'),
      optimeDurableDate: ISODate('1970-01-01T00:00:00.000Z'),
      optimeWrittenDate: ISODate('1970-01-01T00:00:00.000Z'),
      lastAppliedWallTime: ISODate('1970-01-01T00:00:00.000Z'),
      lastDurableWallTime: ISODate('1970-01-01T00:00:00.000Z'),
      lastWrittenWallTime: ISODate('1970-01-01T00:00:00.000Z'),
      lastHeartbeat: ISODate('2026-03-26T13:43:04.779Z'),
      lastHeartbeatRecv: ISODate('1970-01-01T00:00:00.000Z'),
      pingMs: Long('0'),
      lastHeartbeatMessage: "replica set IDs do not match, ours: 69c506a24a4d9e0f04cf42ad; remote node's: 69c534cbc8edaae50aaed39a",
      syncSourceHost: '',
      syncSourceId: -1,
      infoMessage: '',
      configVersion: -1,
      configTerm: -1
    }
  ],
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1774532578, i: 1 }),
    signature: {
      hash: Binary.createFromBase64('Or3a7clRzkZhQt+bRSPoFeJED1A=', 0),
      keyId: Long('7621505237248901127')
    }
  },
  operationTime: Timestamp({ t: 1774532575, i: 1 })
}

replocal [direct: primary] admin> db.revokeRolesFromUser("certmanadmin", [{ role: "clusterAdmin", db: "admin" }]);
{
  ok: 1,
  '$clusterTime': {
    clusterTime: Timestamp({ t: 1774532603, i: 1 }),
    signature: {
      hash: Binary.createFromBase64('vf009Bps3VXGjxgjUvrvd1YPWJg=', 0),
      keyId: Long('7621505237248901127')
    }
  },
  operationTime: Timestamp({ t: 1774532603, i: 1 })
}
replocal [direct: primary] admin>
```

