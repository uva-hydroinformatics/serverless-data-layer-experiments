# Data ingestion app using Azure Event Hubs and Azure Functions

This app implements cloud data ingestion through one az function written in python and the Azure IoT Hub Integration template provided by TTN. Azure IoT Hubs integration is connected to TTN and publishes uplink messages from TTN to an Azure Events Hubs topic. The az function is subscribed to the event hubs topic and it is trigerred by new events . The function then reads the raw message, parses it and converts the data to a delta-table format for saving in the data lake. An aditional function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- Azure IoT Central;
- AZ Function triggered by new messages published in the event hubs and ingesting to data lake;
- Storage account for the AZ Function triggered by new messages published in the event hubs and ingesting to data lake;
- App service plan for the AZ Function triggered by new messages published in the event hubs and ingesting to data lake;
- Optimize Delta Table Az Function;
- Storage account for the Optimize Delta Table Az Function;
- App service plan for the Optimize Delta Table Az Function;