# Experiment B: Data ingestion app using Queue data buffer and Azure Functions

This app implements cloud data ingestion through two Azure functions written in python and a queue data buffer storage. One of the functions is triggered by an HTTP Post request from the TTN API and stores the raw message in a queue data buffer. The other function is triggered by the queue insertion, reads the raw message, parses it and converts the data to a delta-table format, saving it in a Delta Lake. An aditional function is required to periodically optimizing the Delta Lake.

# App components

- Delta Lake storage account;
- AZ Function ingesting to queue;
- Storage account for the AZ Function ingesting to queue;
- App service plan for the AZ Function ingesting to queue;
- AZ Function reading from queue and ingesting to delta lake;
- Storage account for the AZ Function reading from queue and ingesting to delta lake;
- App service plan for the AZ Function reading from queue and ingesting to delta lake;