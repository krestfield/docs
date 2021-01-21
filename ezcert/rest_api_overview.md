---
layout: default
title: REST API
parent: EzCert
nav_order: 16
---

# The EzCert REST API

All functions (including all administrative operations) can be carried out via the REST API  



### Swagger

The available REST API functions can be viewed using the Swagger UI as follows  

  



Ensure that EzCERT is running. Open a browser and navigate to:  

   https://*endpoint*/ezcert/api/swagger-ui.html  

E.g.  

   [https://127.0.0.1/ezcert/api/swagger-ui.html](https://127.0.0.1/ezcert/api/swagger-ui.html)  

If you see something like the following: 

<img src=".\images\swaggere_main.png" alt="image-20210121152518748" style="zoom:80%;" />

Then everything should be working OK  

Scroll down and all of the API methods should be presented



### Try out the API

Scroll down to the **login-controller** and expand the tab. Click **Try it out**

<img src="C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\login_restapi.png" alt="image-20210121153238903" style="zoom: 67%;" />

Enter values for the **username** and **password** and click **Execute**. Scroll down to the response:  

<img src="C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\login_restapi_result.png" alt="image-20210121153421520" style="zoom:67%;" />

Copy the value returned for *token*, scroll up to the top of the page and click <img src="C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\auth_button.png" alt="image-20210121153547479" style="zoom:80%;" />

<img src="C:\Users\darre\Documents\_mystuff\development\_Krestfield Products\docs\ezcert\images\authorise_window.png" alt="image-20210121153646947" style="zoom:67%;" />

Paste in the value for *token* copied from the response above and click **Authorize** then **Close**  

You can now try out the other methods (that require authorization)