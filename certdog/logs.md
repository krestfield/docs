---
layout: default
title: Logs
parent: Certdog
nav_order: 200
---

# Logs

 Certdog's main logs are stored in the database. To view the logs click **Logs** the **View Logs** from the menu. The logs will be displayed, time ordered with the most recent topmost

This log view can continually be refreshed to monitor events. Click **Log View** at the top of the view and click **Auto Refresh** to continually refresh the view 

<img src=".\images\logs1.png" alt="logs" style="zoom:80%;" />

To locate specific log entries, click **Search Logs** from under the **Logs** main menu

<img src=".\images\logs2.png" alt="Search Logs" style="zoom:80%;" />

Set a time span and optionally, username and source. Click **Search**

When *Search* is clicked the **Download** button will appear. Click this button to download the current filtered logs to a JSON file

<br>

## Additional Logs

### log4j2

Certdog also utilises [log4j2](https://logging.apache.org/log4j/2.x/). This enables logging to numerous sources including file, syslog, databases etc.  

The default configuration logs to a file located here:

``[certdog install]\logs\certdog.log``

This file is configured to rollover every day or when the file reaches 100Mb. This is configured in the **log4j2.xml** file here:

``[certdog install]\config\log4j2.xml``

This file may be updated as required. Refer to the [log4j2.xml documentation](https://logging.apache.org/log4j/2.x/) for more information

<br>

### Container Log

The default container used by Certdog is Apache Tomcat. This outputs several logs to ``[certdog install]\apache\logs``

The most useful in debugging Certdog related issues is the ``catalina.* `` log file (e.g. catalina.out or catalina.2021-12-22.log etc)

Refer to Tomcat documentation should you wish to configure this logging furter







