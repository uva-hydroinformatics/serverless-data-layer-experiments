# Experiment F: Data ingestion app using TTN's IoT Hub integration template and Azure Functions

This app implements cloud data ingestion through one Azure Function written in python and the Azure IoT Hub Integration template provided by TTN. Azure IoT Hub integration is connected to TTN and publishes uplink messages from TTN to an Azure Events Hubs topic. The az function is subscribed to the event hubs topic and it is triggered by new events. The function then reads the raw message, parses it and converts the data to a delta-table format, saving it in a Delta Lake. An aditional function is required to periodically optimizing the Delta Lake.

# App components

- Delta Lake storage account;
- Azure IoT Hub integration template components (IoT Hub Namespace, Application Insights, AZ Function, Storage Account, App Service Plan);
- AZ Function triggered by new messages published in the event hubs and ingesting to delta lake;
- Storage account for the AZ Function triggered by new messages published in the event hubs and ingesting to delta lake;
- App service plan for the AZ Function triggered by new messages published in the event hubs and ingesting to delta lake;