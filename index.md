---
layout: landing
title: Knowledge Base
nav_order: 1
hero:
  eyebrow: Krestfield Documentation
  title: Guides and references for Krestfield products
  text: Install, configure and integrate Certdog, EzSign and our PKI tools, with API references and fixes for known errors.
popular_searches:
  - Install Certdog
  - ACME
  - Renew a certificate
  - HSM
  - Errors and solutions
products:
  - title: Certdog
    url: /certdog/certdog.html
    icon: certificate
    description: Our certificate manager, interfacing to Microsoft ADCS and other CAs, with a full RESTful API and an intuitive UI for issuing, renewing and managing certificates.
    links:
      - title: Getting started
        url: /certdog/getting_started.html
      - title: Installation
        url: /certdog/section/installation/
      - title: REST API
        url: /certdog/rest_api_overview.html
  - title: EzSign
    url: /ezsign/ezsign.html
    icon: signature
    description: A digital signature generation and verification server, interfacing to all popular HSMs.
    links:
      - title: Overview
        url: /ezsign/section/overview/
      - title: HSMs & key stores
        url: /ezsign/section/hsms-key-stores/
      - title: Integration & APIs
        url: /ezsign/section/integration/
  - title: Signature Toolkit
    url: /signature%20toolkit/signaturetoolkit.html
    icon: document
    description: Create, verify and analyse PKCS#7/CMS based signatures. Supports PQC algorithms.
    links:
      - title: User guide
        url: /signature%20toolkit/signaturetoolkit_user_guide.html
      - title: Release note
        url: /signature%20toolkit/RELEASENOTE.html
  - title: CRL OCSP Monitor
    url: /ocsp-monitor/ocsp-monitor.html
    icon: pulse
    description: Monitor all your own and any external CRLs and OCSP responders that you depend on, and get early notice of potential issues.
    links:
      - title: Installation
        url: /ocsp-monitor/installation.html
      - title: Test case configuration
        url: /ocsp-monitor/test-case-configuration.html
guides:
  - title: Windows Installation
    url: /certdog/installation.html
    product: Certdog
  - title: Create an ADCS Certificate Issuer
    url: /certdog/create_adcs_certificate_issuer.html
    product: Certdog
  - title: ACME
    url: /certdog/acme.html
    product: Certdog
  - title: HSM Support
    url: /ezsign/hsm_support.html
    product: EzSign
  - title: Errors and Solutions
    url: /certdog/errors%20v%20solutions.html
    product: Certdog
support:
  title: Can't find what you need?
  text: Our support team can help with installation, integration and troubleshooting.
  button:
    title: Contact support
    url: https://www.krestfield.com/support
  link:
    title: Visit krestfield.com
    url: https://www.krestfield.com
---

## More resources

- [OCSP Responder](./certdog/ocsp.html): rapid deployment of an OCSP responder in Windows environments with no need for IIS. Interfaces directly with Microsoft ADCS.
- [General PKI](./pki/general_pki.html): tips and how-to guides for common PKI tasks, such as creating a PFX, exporting certificates and setting Microsoft ADCS template permissions.
- [Security Advisories](./security/): vulnerabilities that may affect Krestfield products, and what to do about them.

For more details on any of these products, contact [support@krestfield.com](mailto:support@krestfield.com).
