# Ingestion using TTN Storage API and periodically trigerred Azure Functions

This app implements cloud data ingestion through the TTN storage API, with an az function periodically fetching uplink messages of TTN applications from the last 13h. The same function parses and converts the data to a delta-table format to save it in a data lake. The same function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- AZ Function to query TTN Storage API, ingest to delta lake and optimize delta tables;
- Storage account for the AZ Function to query TTN Storage API, ingest to delta lake and optimize delta tables;
- App service plan for the AZ Function to query TTN Storage API, ingest to delta lake and optimize delta tables;