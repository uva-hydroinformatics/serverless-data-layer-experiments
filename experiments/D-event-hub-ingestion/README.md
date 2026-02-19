# Experiment D: Data ingestion app using Azure Event Hubs and Azure Functions

This app implements cloud data ingestion through one Azure function written in python and the Azure Event Hubs service. The event hubs API receives HTTP Post requests from TTN that are then published under a topic. The az function is subscribed to the Event Hubs topic and it is triggered by new published events. The function then reads the raw message, parses it and converts the data to a delta-table format, saving it in a Delta Lake. An aditional function is required to periodically optimizing the Delta Lake.

# App components

- Delta Lake storage account;
- Azure Event Hubs;
- AZ Function triggered by new messages of the event hub topic and ingesting to delta lake;
- Storage account for the AZ Function triggered by new messages of the event hub topic and ingesting to delta lake;
- App service plan for the AZ Function triggered by new messages of the event hub topic and ingesting to delta lake;