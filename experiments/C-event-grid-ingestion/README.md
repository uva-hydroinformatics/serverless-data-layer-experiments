# Experiment C: Data ingestion app using Azure Event Grid and Azure Functions

This app implements cloud data ingestion through two Azure functions written in python and an Event Grid topic. One of the functions is triggered by an HTTP Post request from the TTN API and publishes the raw message to an Event Grid topic. The other function is subscribed to the Event Grid topic and it is triggered by new published events. The function then reads the raw message, parses it and converts the data to a delta-table format, saving it in a Delta Lake. An aditional function is required to periodically optimizing the Delta Lake.

# App components

- Delta Lake storage account;
- Azure Event Grid topic;
- AZ Function that publishes to an event grid topic;
- Storage account for the AZ Function publishing to an event grid topic;
- App service plan for the AZ Function publishing to an event grid topic;
- AZ Function reading from queue and ingesting to delta lake;
- Storage account for the AZ Function reading from queue and ingesting to delta lake;
- App service plan for the AZ Function reading from queue and ingesting to delta lake;