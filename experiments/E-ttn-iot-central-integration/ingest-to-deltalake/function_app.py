import azure.functions as func
from azure.core.credentials import AzureNamedKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from datetime import datetime, timezone
from functools import reduce 
import operator
import json
import pandas as pd
from flatten_json import flatten
from deltalake import write_deltalake


app = func.FunctionApp()

config_values= {
    'account_name': '?????????????', # The account name value is hidden for security reasons. Please replace it with the actual account name value to run the code.
    'account_key': '??????????????????????????????????????????????????????????????', # The account key value is hidden for security reasons. Please replace it with the actual account key value to run the code.
    'endpoint': 'https://?????????.blob.core.windows.net/',
    'container_id_path': ["end_device_ids", "application_ids", "application_id"],
    'container_id': None,
    'timestamp_path': ["received_at"],
    'timestamp': None,
    'flatten_separator': '__',
    'data_content_path': ["uplink_message", "decoded_payload"],
    'data_content': None,
    'blob_storage_key':"??????????????????????????????????????????????????????????????" # The blob storage key value is hidden for security reasons. Please replace it with the actual blob storage key value to run the code.,
}

def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def upload_to_delta_table(input_json, config_values):
    """ This function converts the input JSON to a delta table and uploads it to an azure container."""

    # Create Azure credentials
    account_credential = AzureNamedKeyCredential(config_values['account_name'], config_values['account_key'])

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(config_values['endpoint'], credential=account_credential)
    
    # Creates an Azure blob container if it already doesn't exist
    container = blob_service_client.get_container_client(config_values['container_id'])
    if not container.exists():
        try:
            container = blob_service_client.create_container(name=config_values['container_id'])
        except:
            # Error handling for creating the blob container
            return None

    # Create the dictionary for the delta table
    entity = {'input_json': str(input_json), 'received_at':config_values['timestamp']}

    for field in config_values['data_content']:
        entity[field] = config_values['data_content'][field]

    # Create dataframe from the dictionary
    df = pd.DataFrame([entity])

    # define credentials
    storage_options = {
        "ACCOUNT_NAME": config_values['account_name'],
        "ACCESS_KEY": config_values['account_key'],
    }

    try:
        # write Delta to ADLS
        write_deltalake(
            f"abfs://{config_values['container_id']}/delta_table",
            df,
            storage_options = storage_options,
            mode="append"
        )
    except:
        # Error handling for uploading JSON to the data lake
        return None
    
    return df

@app.function_name(name="eventGridTrigger")
@app.event_grid_trigger(arg_name="event")
def eventGridTrigger(event: func.EventGridEvent):
    """ This function is triggered by an Azure Event Grid event, processes the event data, and uploads it to a Delta table in Azure Data Lake Storage."""

    try:
        # Extracts the blob URL from the event data
        grid_event_json = event.get_json()
        blob_url = grid_event_json['url']

        # Create Azure blob client
        msg_blob_client = BlobClient.from_blob_url(blob_url, credential=config_values['blob_storage_key'])

        # Download the blob content and decode bytes (assuming UTF-8 encoding for text files)
        msg_blob_data = msg_blob_client.download_blob().readall().decode("utf-8")

    except:
        # Error handling for downloading the blob content
        raise ValueError("Error: Unable to process event and download the blob content from the provided URL.")

    try:
        # Loads request body as JSON
        msg_json = json.loads(msg_blob_data)
        input_json = msg_json['telemetry']
    except:
        # Error handling for invalid JSON format
        raise ValueError("Invalid JSON format in the request body.")

    
    try:
         # Extracts the container id value from the input JSON file using the config file 
        config_values['container_id'] = get_by_path(input_json, config_values['container_id_path'])

        # Extracts the timestamp value from the input JSON file using the config file
        config_values['timestamp'] = get_by_path(input_json, config_values['timestamp_path'])

        # Extracts the data contents value from the input JSON file using the config file
        data_content = get_by_path(input_json, config_values['data_content_path'])
        config_values['data_content'] = flatten(data_content,config_values['flatten_separator'])

    except:
        # Error handling for missing fields in the input JSON
        raise ValueError("Error: Missing required fields in the input JSON.")

    # Executes the function to upload input data to delta table
    df = upload_to_delta_table(input_json,config_values)

    if df is None:  
        # Error handling for invalid JSON format
        raise ValueError("Error: Unable to create df to upload JSON to the data lake.")

    else:
        if df.empty:
            # Error handling for uploading JSON to the data lake
            raise ValueError("Error: Unable to upload JSON to the data lake.")