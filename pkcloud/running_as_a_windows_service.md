---
layout: default
title: PkCloud - Running as a Windows Service
parent: PkCloud
nav_order: 10

---



# Running as a Windows Service



The Tomcat server may be installed as a Service (rather than as a stand-alone application which requires the startpkcloud.bat and stoppkcloud.bat scripts to be run)  

The Service requires the following environment variables to be set:  
### CATALINA_HOME
``CATALINA_HOME = [PKCloud Installation]\apache-tomcat-[version]``
e.g.
``CATALINA_HOME = C:\Program Files\Krestfield\PKCloud\apache-tomcat-9.0.34``

### JAVA_HOME
``JAVA_HOME = [PKCloud Installation]\openjdk-[version]``
e.g.
``JAVA_HOME = C:\Program Files\Krestfield\PKCloud\openjdk-11.0.1``

### JRE_HOME
``JRE_HOME = %JAVA_HOME%``  

  

These variables may be set by performing the following steps:

1. Press Window Keys+R, or select Run from the start menu, type **sysdm.cpl** and click **OK**  

 <img src=".\images\sys_props.png" alt="image-20210324071108801" style="zoom:67%;" />  

2. Select the **Advanced** tab and click the **Environment Variables** button

3. Under *System Variables*, click **New…**

     For the *Variable Name*, enter **CATALINA_HOME**

     For the *Variable Value*, enter the full path to the tomcat directory in the PKCloud installation e.g.
     ``C:\Program Files\Krestfield\PKCloud\apache-tomcat-9.0.34``

4. Click **OK**

5. Repeat for **JAVA_HOME** and **JRE_HOME**  

  

Once the variables have been set correctly, the service may be installed by performing these steps:

1. Open a command prompt, as Administrator

2. Navigate to the tomcat bin directory in the PKCloud installation e.g. 

   ``C:\Program Files\Krestfield\PKCloud\apache-tomcat-9.0.34\bin``

13. At the prompt, type: 

    ``service.bat install PkCloud`` and press **Enter**

    This will install the Service

14. To check that the Service has installed, from the Start menu, type **Services** and press **Enter**

15. Ensure that the *Apache Tomcat PKCloud* service is now present. Right click the service and set the Start-up type to be **Automatic** (leave at Manual if this service should not auto-start on reboot)
    
16. Also confirm that the Logon is **Local System** Account (occasionally the tomcat install script sets this incorrectly) e.g.  

<img src=".\images\service_props.png" alt="image-20210324071517675" style="zoom:67%;" />

The service can be run under another account if required but if this is done, ensure the permissions for that account allow write to the install location files

8. Click **OK**