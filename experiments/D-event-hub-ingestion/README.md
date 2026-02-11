# Data ingestion app using Azure Event Hubs and Azure Functions

This app implements cloud data ingestion through one az function written in python and the Azure Event Hubs service. The event hubs API receives http post requests from TTN that are then published under a topic. The az function is subscribed to the Event Hubs topic and it is triggered by new published events. The function then reads the raw message, parses it and converts the data to a delta-table format for saving in the data lake. An aditional function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- Azure Event Hubs;
- AZ Function triggered by new messages of the event hub topic and ingesting to data lake;
- Storage account for the AZ Function triggered by new messages of the event hub topic and ingesting to data lake;
- App service plan for the AZ Function triggered by new messages of the event hub topic and ingesting to data lake;
- Optimize Delta Table Az Function;
- Storage account for the Optimize Delta Table Az Function;
- App service plan for the Optimize Delta Table Az Function;