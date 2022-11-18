---
layout: default
title: Windows Uninstall
parent: Certdog
nav_order: 101
---

# Uninstalling Certdog (Windows)

 

The following steps outline the steps required to completely uninstall Certdog from a windows environment

If a reset is required (to remove all data and revert to a blank state e.g. if the admin password were lost). Simply, run ``reset-db.ps1`` 



> From Version 1.8.0



Open a **PowerShell** window as Administrator and navigate to the **.\install** folder within the certdog installation. Run: 

**.\uninstall.ps1**

Once the product has been uninstalled, you may remove all files by closing the PowerShell window and deleting the certdog folder (e.g. ``c:\certdog\``)





> For Versions before 1.8.0



1. Open the **Windows Services** snapin and stop the following services:

   1. **Krestfield CertDog Service**

   2. **Krestfield Certdog Database**

   3. **Krestfield Adcs Driver** (if present)

      

2. Click **Start** and type **Apps and Features** and select Apps and Features system settings

   

3. Search for **certdog** and uninstall the following

   1. **Certdog Service**
   2. **Certdog ADCS Driver** (if present)

   

4. Open a **PowerShell** window as Administrator and navigate to the **.\install** folder within the certdog installation. Run: 

   **uninstall-db.ps1**

   

5. Finally, to remove all files, simply delete the folder where the original files were unzipped e.g. c:\certdog

   If this fails due to a file being in use, it may be that the CertDog Service was uninstalled before stopping, leaving a java process running

   If this happens. from the PowerShell window, navigate to the **.\bin** folder within the certdog installation and run:

   **stop-tomcat.ps1**

   Then re-attempt the folder deletion

   
