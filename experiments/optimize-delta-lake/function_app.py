import logging
import azure.functions as func
import configparser
import deltalake
from azure.core.credentials import AzureNamedKeyCredential
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 */6 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function started.')

    try:
        # Loads config.ini file
        config = configparser.ConfigParser()
        config.read('config.ini')

        # Read the config values from the config.ini file
        account_name = config['storage.account']['name']
        account_key = config['storage.account']['key']
        account_endpoint =  config['storage.account']['endpoint']

    except:
        logging.error('Error reading config.ini file.')
        raise

    # Create Azure credentials
    account_credential = AzureNamedKeyCredential(account_name, account_key)

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_endpoint, credential=account_credential)

    az_storage_options = {
        "AZURE_STORAGE_ACCOUNT_NAME": account_name,
        "AZURE_STORAGE_ACCOUNT_KEY": account_key,
    }

    # List all containers in the storage account
    list_of_containers = blob_service_client.list_containers(include_metadata=True)

    # Iterate through each container and check if it is a Delta table
    for account_container in list_of_containers:
        container_name = account_container['name']
        az_table_path = f"abfs://{container_name}/delta_table"

        # If it is a delta-table, optimize and vacuum it
        if deltalake.DeltaTable.is_deltatable(az_table_path,storage_options = az_storage_options):
            logging.info(f'{container_name} is a delta table!')
            dt = deltalake.DeltaTable(az_table_path,storage_options = az_storage_options)
            dt.optimize.compact()
            dt.vacuum()
            # Log the optimization and vacuuming message
            logging.info(f'{container_name} was optimized!')
        else:
            # If it is not a delta table, log the message
            logging.info(f'{container_name} is not a delta table!')


    logging.info('Python timer trigger function executed.')