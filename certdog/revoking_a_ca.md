---
layout: default
title: Revoking a CA
parent: Certdog
nav_order: 117
---

# Revoking a CA

An Internal (Local) CA can be revoked if it meets the following criteria:

* It has been issued from an Internal CA i.e. not from an external CA
  * When a CA has been issued from an external CA, that CA must perform the revocation step

* It is a Subordinate CA. I.e. not a Root CA. 
  * Root CAs cannot be revoked as these CAs are self-signed. Hence, there is no issuer from where valid revocation status can be obtained.

<br>

CA revocation is a last resort operation, normally only employed in cases such as CA key compromise. Once performed all certificates issued under this CA will fail validation

<br>

When a CA is revoked, the following occurs:

* The CA certificate is revoked and its serial number will be added to the issuing CA's CRL. OCSP responses from the issuer will return REVOKED.

* The CA will be disabled and no further certificates can be issued from the CA.

<br>

<p align="center"><b>WARNING: This operation cannot be undone!</b></p>

<br>

## Steps to Revoke

To revoke a CA perform the following steps:

1. From the menu, choose **Local CAs** then **CA Configuration**
2. Right click the **CA to be revoked** and click **View/Edit**
   1. Note that this must be a Subordinate CA as Root CAs cannot be revoked
3. Scroll to the bottom of the page and click the **Revoke CA** button

![image-20250605160923718](./images/image-20250605160923718.png)

4. Select the **Revocation Reason** and click **Revoke This CA**

<img src="./images/image-20250605161104546.png" alt="image-20250605161104546" style="zoom:80%;" />

5. Click **Revoke Now** to confirm you wish to continue

<img src="./images/image-20250605161131891.png" alt="image-20250605161131891" style="zoom:80%;" />

6. Click **Revoke Now** to finalise the revocation process

<img src="./images/image-20250605161225109.png" alt="image-20250605161225109" style="zoom:80%;" />

The CA is now revoked

<img src="./images/image-20250605161319187.png" alt="image-20250605161319187" style="zoom:80%;" />

<br>

## Final Steps

Although any revocation from this CA will now be invalid (as the CA itself is revoked) it is good practise to tidy up any connected artifacts

<u>OCSP</u>

If the CA has an associated OCSP server, delete it. If the OCSP server remains, responses from it will not be deemed valid. Once the OCSP signer certificate has expired it will not be able to renew

<u>CRL</u>

Locate where the CRLs are published and remove them. As above, their status will no longer be valid and they will expire without being renewed but this will ensure no clients can use them