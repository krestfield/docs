---
layout: default
title: Searching Certificates
parent: Certdog
nav_order: 18
---
# Searching Certificates

The default *Certificates* view shows all certificates issued in the last day. You can perform some filtering and searching by using the header options:  

![image-20210122133824835](.\images\search_headings.png)



For more advanced searches, click the Certificate Search bar:  

![image-20210122133945462](.\images\search_bar.png)

Which will open the available search options:  

<img src=".\images\search_options.png" alt="image-20210319175222870" style="zoom:67%;" />

Select the options you wish to search on. The top items (those with a check box beside them) will only be  included in the search if the check box is ticked  

The other items will always be included in the search but if left empty (or set to **All**) will return all possibilities  

The resulting query is an **AND** of all items (not an **OR**). For example, if  you selected *expiring in the next 5 days* and *subject contains CN=test* the search would be for all certificates that are expiring in the next 5 days that have a subject with contains *CN=test*  



### Examples

* Certificates expiring in the next 5 days:

<img src=".\images\expiring_next_5_days.png" alt="image-20210122134453299" style="zoom:67%;" />

​      Uncheck the Issued in the last option and check the Expiring in next option  

​      Choose 5 days from the drop down and click Search



* Certificates issued by the issuer **CN=Certdog Test CA,O=Krestfield** with a subject containing **CN=mydomain**

<img src=".\images\issuer_and_subject_filter.png" alt="image-20210122135124788" style="zoom:67%;" />



* Certificate Expiring in 2023

​      Uncheck all items and leave others at their default

​      Check **Expiring between** and set the dates as follows

![image-20210122135430648](.\images\expiring_2023.png)



## Saving Searches

If there is a particular search that you wish to easily recall, once configured, enter a name for this search and click Save:

<img src=".\images\saving_searches1.png" alt="image-20210319175444785" style="zoom:67%;" />

You may then select this search from the drop down list to populate the details

<img src=".\images\saving_searches2.png" alt="image-20210319175550798" style="zoom:67%;" />

If you wish one of these searches to be the initial search whenever you click Certificates, click the **Set as Default** button. This will then use this search by default