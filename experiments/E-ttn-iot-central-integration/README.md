# Experiment E: Data ingestion app using IoT Central and Azure Functions

This app implements cloud data ingestion through one Azure function written in python and the Azure IoT Central. Azure IoT Central is connected to TTN and periodically dumps received uplink messages from TTN to a blob storage. The az function is triggered by new blobs being written in the storage account. The function then reads the raw message blobs, parses it and converts the data to a delta-table format, saving in a Delta Lake. An aditional function is required to periodically optimizing the Delta Lake.

# App components

- Delta Lake storage account;
- Azure IoT Central;
- AZ Function triggered by new blobs written by IoT Central and ingesting to delta lake;
- Storage account for the AZ Function triggered by new blobs written by IoT Central and ingesting to delta lake;
- App service plan for the AZ Function triggered by new blobs written by IoT Central and ingesting to delta lake;