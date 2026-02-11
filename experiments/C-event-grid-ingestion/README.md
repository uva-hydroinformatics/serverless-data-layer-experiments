# Data ingestion app using Azure Event Grid and Azure Functions

This app implements cloud data ingestion through two az function written in python and a Event Grid topic. One of the az functions is triggered by an http post request from the TTN API and publishes the raw message to an Event Grid topic. The other az function is subscribed to the Event Grid topic and it is triggered by new published events. The function then reads the raw message, parses it and converts the data to a delta-table format for saving in the data lake. An aditional function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- Azure Event Grid topic;
- AZ Function that publishes to an event grid topic;
- Storage account for the AZ Function publishing to an event grid topic;
- App service plan for the AZ Function publishing to an event grid topic;
- AZ Function reading from queue and ingesting to data lake;
- Storage account for the AZ Function reading from queue and ingesting to data lake;
- App service plan for the AZ Function reading from queue and ingesting to data lake;
- Optimize Delta Table Az Function;
- Storage account for the Optimize Delta Table Az Function;
- App service plan for the Optimize Delta Table Az Function;