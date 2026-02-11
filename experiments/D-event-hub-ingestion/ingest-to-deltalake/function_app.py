import azure.functions as func
from azure.core.credentials import AzureNamedKeyCredential
from azure.storage.blob import BlobServiceClient
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
    'endpoint': 'https://?????????.blob.core.windows.net/', # The endpoint value is hidden for security reasons. Please replace it with the actual endpoint value to run the code.
    'container_id_path': ["end_device_ids", "application_ids", "application_id"],
    'container_id': None,
    'timestamp_path': ["received_at"],
    'timestamp': None,
    'flatten_separator': '__',
    'data_content_path': ["uplink_message", "decoded_payload"],
    'data_content': None,
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

# This example uses SDK types to directly access the underlying EventData object provided by the Event Hubs trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-eventhub to your requirements.txt file
import azurefunctions.extensions.bindings.eventhub as eh
@app.event_hub_message_trigger(
    arg_name="event", event_hub_name="myeventhub", connection="ttneventhubs_FabricListenEventKey_EVENTHUB"
)
def eventhub_trigger(event: eh.EventData):
    try:
        # Loads request body as JSON
        input_json = json.loads(event.body_as_str())
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