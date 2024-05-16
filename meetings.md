# Meetings notes

## Meeting 1.
* **DATE:** 2024-01-31
* **ASSISTANTS:** Ivan Sanchez Milara

### Minutes

The meeting focused on the project plan, specifically addressing the quality of descriptions. It was noted that the current functionality is somewhat limited, with the main concepts suggesting potential for expanded capabilities. The architecture diagram was reviewed.
Additionally, the discussion covered the application of APIs and their clients, along with a review of related work.

### Action points

* Expand the system's features to overcome current limitations.
* Refine the architecture diagram by removing the 'Request' element, recognizing it as an action rather than a static feature.
* Provide references for API usage, specifically pointing out actual applications or clients that integrate these APIs.


## Meeting 2.
* **DATE:** 2024-02-20
* **ASSISTANTS:** Mika Oja

### Minutes
This meeting focused on the database design and code with Mika. The database design was appreciated. In wiki, there were relationships added in the table which were asked to be removed. On the code side, we were asked to add the on_delete behavior for the tables. Lastly we were asked to move the code for populating the DB to a CLI handler instead of implementing it in app main function.

### Action points
* relationships are not part of database table
* no on_delete behavior defined explicitly
* move database population from main() to a CLI handler


## Meeting 3.
* **DATE:** 2024-03-25
* **ASSISTANTS:** Mika Oja

### Minutes
Discussed about the API basic implantation. Mentioned some issues in the implementation. 
Discussed on code quality, documentation and running instructions. 

### Action points
* URLs should not have actions as verbs, actions are defined by method
```
    /identities/register changed to /identities  with POST
    /identities/{user_id}/delete to /identities/{user_id}  with DELETE
    /identities/{user_id}/update to /identities/{user_id}  with PUT
```
* Fix PUT since it seems to support partial which is not fully RESTful
* clean up pylint, move complex code from app to utility functions etc
* document API related functions
* Include instructions for running tests
* Fix the app coverage issue 
* Fix identity updating API bug  


## Meeting 4.
* **DATE:** 2024-04-11
* **ASSISTANTS:** Mika Oja

### Minutes
Discussed about hypermedia documentation, test coverage, request bodies. And evaluate hypermedia design and implementation 

### Action points

* show hypermedia in examples
* update missing response codes; 415 missing, 401/403 missing in some endpoints
* State diagram syntactically correct, but the current URL map is not restful enough for this to make sense. make it restful enough 
* Connectedness cannot validate fully since function complicity. make it simple by moving support functions using utils
* requests that need a request body, should include schemas


## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*




