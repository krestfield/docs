---
layout: default
title: EzSign Service - version 1.4
parent: EzSign
nav_order: 26
---

# EzSign Service - Version 1.4



### Updates from V1.3

* Bundles a supported java runtime
  * There is no need to install this separately although you may use an alternative runtime if preferred. Note that this must be 8u241 or later  

* Key Store Location removed from the Configuration Utility
  * Previously this could be set via the UI but generating CSRs requires this parameter to be present in the properties file anyway. To avoid confusion (of mismatched locations) this now only resides in the properties file and must be set there
* SHA-3 and ECDSA support added
* PayShield support improved
  * Support for Key Block and Variant LMKs added and the ability to choose which LMK to use

