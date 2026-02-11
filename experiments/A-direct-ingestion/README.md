# Direct data ingestion app using Azure Functions

This app implements cloud data ingestion through only one az function written in python that is triggered by an TTN webhook API post event. This ingestion function parses and converts the data to a delta-table format to save it in a data lake. An aditional function is responsible for periodically optimizing the delta table.

# App components

- Data Lake storage account;
- Ingestion to data lake AZ Function;
- Storage account for the ingestion to data lake AZ Function;
- App service plan for the ingestion to data lake AZ Function;
- Optimize Delta Table Az Function;
- Storage account for the Optimize Delta Table Az Function;
- App service plan for the Optimize Delta Table Az Function;

