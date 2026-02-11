import azure.functions as func
from azure.core.credentials import AzureNamedKeyCredential
from azure.storage.blob import BlobServiceClient, ContainerClient
from functools import reduce 
import operator
import pandas as pd
from flatten_json import flatten
import deltalake
import pyarrow as pa
import requests
from io import StringIO

app = func.FunctionApp()

config_values= {
    'account_name': '????????????????????',
    'account_key': '???????????????????????????????????????????????????????????????',
    'endpoint': 'https://?????????.blob.core.windows.net/',
    'download_params': [
        {
            'container_id': '?????????',
            'url': 'https://nam1.cloud.thethings.network/api/v3/as/applications/???????/packages/storage/uplink_message',
            'key': 'NNSXS.????????????????????????????????????????????????????????????????'
        },
        {
            'container_id': '?????????',
            'url': 'https://nam1.cloud.thethings.network/api/v3/as/applications/?????????/packages/storage/uplink_message',
            'key': 'NNSXS.????????????????????????????????????????????????????????????????'
        },
        {
            'container_id': '?????????',
            'url': 'https://nam1.cloud.thethings.network/api/v3/as/applications/?????????/packages/storage/uplink_message',
            'key': 'NNSXS.????????????????????????????????????????????????????????????????'
        }
    ],
    'download_query_param': "last=13h",
    'timestamp_path': ["received_at"],
    'flatten_separator': '__',
    'data_content_path': ["uplink_message", "decoded_payload"]
}


def get_by_path(root, items):
    """Access a nested object in root by item sequence."""
    return reduce(operator.getitem, items, root)


def upload_to_delta_table(df,container_id,config_values):
    """ This function converts the input JSON to a delta table and uploads it to an azure container."""

    # Create Azure credentials
    account_credential = AzureNamedKeyCredential(config_values['account_name'], config_values['account_key'])

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(config_values['endpoint'], credential=account_credential)

    # Azure data storage account parameters
    az_table_path = f"abfs://{container_id}/delta_table"
    az_storage_options = {
        "ACCOUNT_NAME": config_values['account_name'],
        "ACCESS_KEY": config_values['account_key'],
    }

    # Creates an Azure blob container if it already doesn't exist
    container = blob_service_client.get_container_client(container_id)
        
    # If container exists, updates the Delta table, otherwise creates a new one
    if container.exists():

        # Loads the existing Delta table       
        dt = deltalake.DeltaTable(az_table_path,storage_options = az_storage_options)

        # Merges the new data into the existing Delta table
        dt.merge(
            source=pa.table(df),
            predicate="target.received_at = source.received_at",
            source_alias="source",
            target_alias="target").when_not_matched_insert_all().execute()
        
        # Optimize and vacuum the Delta table
        dt.optimize.compact()
        dt.vacuum()

    else:
        # Create a new container and write the Delta table
        container = blob_service_client.create_container(name=container_id)
        
        # write Delta to ADLS
        deltalake.write_deltalake(
            az_table_path,
            pa.table(df),
            storage_options = az_storage_options
        )
    

@app.timer_trigger(schedule="0 0 */6 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:

    for download_param in config_values['download_params']:
        # Extracts the container ID, URL, and key from the download parameters
        container_id = download_param['container_id']
        url = download_param['url']+ '?' + config_values['download_query_param']    
        key = download_param['key']

        # Makes a GET request to the URL with the provided key and payload
        headers = {'Authorization': f'Bearer {key}', 'Accept': 'text/event-stream'}

        response = requests.get(url, headers=headers)
        input_json_df = pd.read_json(StringIO(response.text), lines=True)

        entity_list = []
        for index, row in input_json_df.iterrows():
            input_json = row.to_dict()['result']

            # Extracts the timestamp value from the input JSON file using the config file
            timestamp_value = get_by_path(input_json, config_values['timestamp_path'])

            # Extracts the data contents value from the input JSON file using the config file
            data_content = get_by_path(input_json, config_values['data_content_path'])
            flatten_data_content = flatten(data_content,config_values['flatten_separator'])

            # Create the dictionary for the delta table
            entity = {'input_json': str(input_json), 'received_at':timestamp_value}

            for field in flatten_data_content:
                entity[field] = flatten_data_content[field]
            entity_list.append(entity)

        # Create dataframe from the dictionary
        df = pd.DataFrame(entity_list)

        # Upload the JSON data to the delta table
        upload_to_delta_table(df, container_id, config_values)