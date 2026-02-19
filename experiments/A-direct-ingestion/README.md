# Experiment A: Direct data ingestion app using Azure Functions

This app implements cloud data ingestion through only one Azure function written in python that is triggered by an TTN webhook API HTTP Post event. This ingestion function parses and converts the data to a delta-table format, saving it in a Delta Lake. An aditional function is required to periodically optimizing the Delta Lake.

# App components

- Delta Lake storage account;
- Ingestion to delta lake AZ Function;
- Storage account for the ingestion to delta lake AZ Function;
- App service plan for the ingestion to delta lake AZ Function;