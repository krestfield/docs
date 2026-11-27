---
layout: default
title: Custom PKCS#11 Templates
parent: HSMs & Key Stores
nav_order: 20
grand_parent: EzSign
---

# EzSign: Custom PKCS11 Templates

>
> From version: 4.2.1
>

EsSign supports the PKCS#11 interface for a variety of HSMs  

However, there are occasions where the PKCS#11 interface for an HSM vendor requires something slightly different to the default implementations. EzSign can support this via Custom Templates  

To support a custom template a single class jar-file must be produced which will implement the various PKCS#11 templates required for the specific HSM  

Krestfield support can either develop this on your behalf or provide details on how this can be implemented. The process is fairly straightforward for anyone with a basic understanding of Java and only requires the implementation of a single file (e.g. ``CustomHsm.java`` - although the file can be named anything you wish)

Once this file has been compiled and packaged, the resulting jar file (e.g. ``CustomHsm.jar``) must then be placed in the ``[EzSignInstall]]\EzSignServer\lib`` folder of the EzSign installation  

To use this custom version the following properties from the server configuration file must then be updated:

The *model* must be set to **Custom** e.g. 

```properties
channel.1.token.pkcs11.model=Custom
```

The class-name must be specified in the ``customTemplateClass`` property e.g. 

```properties
channel.1.token.pkcs11.customTemplateClass=CustomHsm
```

Note: The name to provide here is the class name without any extensions. It is not the jar name (that can be called anything you like).  In this example it would just be ``CustomHsm`` and not ``CustomHsm.class``, ``CustomHsm.java`` or ``CustomHsm.jar``

Restarting the EzSign server will now pick up this custom implementation
