# Data ingestion app using Queue data buffer and Azure Functions

This app implements cloud data ingestion through two az function written in python and a queue data buffer storage. One of the az functions is triggered by an http post request from the TTN API and stores the raw message in a queue data buffer. The other az function is triggered by the queue insertion, reads the raw message, parses it and converts the data to a delta-table format for saving in the data lake. An aditional function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- AZ Function ingesting to queue;
- Storage account for the AZ Function ingesting to queue;
- App service plan for the AZ Function ingesting to queue;
- AZ Function reading from queue and ingesting to data lake;
- Storage account for the AZ Function reading from queue and ingesting to data lake;
- App service plan for the AZ Function reading from queue and ingesting to data lake;
- Optimize Delta Table Az Function;
- Storage account for the Optimize Delta Table Az Function;
- App service plan for the Optimize Delta Table Az Function;
