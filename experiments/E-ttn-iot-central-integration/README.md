# Data ingestion app using Azure Event Hubs and Azure Functions

This app implements cloud data ingestion through one az function written in python and the Azure IoT Central. Azure IoT Central is connected to TTN and periodically dumps received uplink messages from TTN to a blob storage. The az function is trigerred by new blobs being written in the storage account. The function then reads the raw message blobs, parses it and converts the data to a delta-table format for saving in the data lake. An aditional function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- Azure IoT Central;
- AZ Function triggered by new blobs written by IoT Central and ingesting to data lake;
- Storage account for the AZ Function triggered by new blobs written by IoT Central and ingesting to data lake;
- App service plan for the AZ Function triggered by new blobs written by IoT Central and ingesting to data lake;
- Optimize Delta Table Az Function;
- Storage account for the Optimize Delta Table Az Function;
- App service plan for the Optimize Delta Table Az Function;