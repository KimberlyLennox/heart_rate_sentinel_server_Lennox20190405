# heart_rate_sentinel_server_Lennox20190405

This server can be found at:
http://vcm-9030.vm.duke.edu:5000/


This server stores heart rate data on a database for multiple patients. It can return the following:
*The latest heart rate
*All heart rates since the initialization of the patient
*The average of all heart rates
*The average of all heart rates since a given timestamp

The client function has been added to Github in case of any syntax discrepancies

NOTE: The virtual machine has been tested using the patient_id of 1. Some extraneous data may still be stored on the database.

NOTE 2: The MongoDB password has been removed, along with the Sendgrid API key. This has affected the Travis integration and sends back a syntax error. If you download the code to run on your own machine, please use your own Sendgrid API key and Mongo username and password to get the code to run.
