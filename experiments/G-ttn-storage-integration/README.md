# Experiment G:Ingestion using TTN Storage API and periodically trigerred Azure Functions

This app implements cloud data ingestion through the TTN storage API, with an Azure function periodically fetching from TTN applications all uplink messages from the last 13 hours. The same function parses and converts the data to a delta-table format, and saves it in a Delta Lake. The same function is responsible for periodically optimizing the delta lake. There is no need for an aditional function to optimize the Delta Lake.

# App components

- Delta Lake storage account;
- AZ Function to query TTN Storage API, ingest to delta lake and optimize it;
- Storage account for the AZ Function to query TTN Storage API, ingest to delta lake and optimize it;
- App service plan for the AZ Function to query TTN Storage API, ingest to delta lake and optimize it;