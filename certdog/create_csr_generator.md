---
layout: default
title: Create a CSR Generator
parent: Certdog
nav_order: 11
---

# certdog - Create a CSR Generator

A CSR Generator is required if you want certdog to generate CSRs on your behalf. If you will only be submitting pre-generated CSRs, you will not need a CSR Generator.  But if you wish to generate a certificate from a DN and download a PFX containing the certificate and associated keys, a CSR Generator is required  

A CSR Generator is configured with an algorithm, the key size (or elliptic curve name) and a hash algorithm. A CSR Generator is also assigned a name and it is this name that is then specified when requesting a certificate when the system will also be generating the CSR  

To create a CSR Generator:

1. From the UI click on the **CSR Generators** menu item and click **New CSR Generator**  
2. Provide a name for the generator and specify the algorithm, key size (or curve if ECDSA is chosen) and the hash algorithm  
<img src=".\images\csr_generator.png" alt="image-20210116150109796" style="zoom:67%;" />   
3. Click **Add**





