---
layout: default
title: REST API
parent: Certdog
nav_order: 16
---

# The Certdog REST API

All functions (including all administrative operations) can be carried out via the REST API  

These functions are described in the Swagger UI  

See [here for examples of calling the API](rest_api_example.html)



### Swagger

The available REST API functions can be viewed using the Swagger UI as follows:  

 <br> Ensure that certdog is running. Open a browser and navigate to:  

​    https://*endpoint*/certdog/api/swagger-ui/index.html  

Note: For versions before 1.7.0, it was located here:

​    https://*endpoint*/certdog/api/swagger-ui.html  

The online version is available [here](https://certdog.net/certdog/api/swagger-ui/index.html). This test instance is available during 8am and 8pm UK time

​     

E.g.  

​    [https://127.0.0.1/certdog/api/swagger-ui/index.html](https://127.0.0.1/certdog/api/swagger-ui/index.html)  

​    (Previously: [https://127.0.0.1/certdog/api/swagger-ui.html](https://127.0.0.1/certdog/api/swagger-ui.html))





If you see something like the following: 

<img src=".\images\swaggere_main.png" alt="Swagger API" style="zoom:80%;" />



Then everything should be working OK  

Scroll down and all of the API methods should be presented



### Trying out the API

Scroll down to the **login-controller** and expand the tab. Click **Try it out**

<img src=".\images\login_restapi.png" alt="image-20210121153238903" style="zoom: 67%;" />

Enter values for the **username** and **password** and click **Execute**. Scroll down to the response:  

<img src=".\images\login_restapi_result.png" alt="image-20210121153421520" style="zoom:67%;" />

Copy the value returned for *token*, scroll up to the top of the page and click <img src=".\images\auth_button.png" alt="image-20210121153547479" style="zoom:80%;" />

<img src=".\images\authorise_window.png" alt="image-20210121153646947" style="zoom:67%;" />

Paste in the value for *token* copied from the response above and click **Authorize** then **Close**  

You can now try out the other methods (that require authorization)