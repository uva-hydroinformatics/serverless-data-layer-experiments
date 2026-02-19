# Optimize Delta Lake

This app implements Delta lake optimization through only one Azure function written in python that is periodically triggered every 6 hours. This function reads Azure Storage Account contents, finds Delta Lakes, and optimizes the tables consolidating small parquet files in large ones.

# App components

- Optimize delta lake AZ Function;
- Storage account for the optimize delta lake AZ Function;
- App service plan for the optimize delta lake AZ Function;