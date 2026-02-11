import azure.functions as func
from azure.storage.queue import  QueueClient, TextBase64EncodePolicy
from azure.core.credentials import AzureNamedKeyCredential
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

config_values= {
    'account_name': '?????????????', # The account name value is hidden for security reasons. Please replace it with the actual account name value to run the code.
    'account_key': '??????????????????????????????????????????????????????????????', # The account key value is hidden for security reasons. Please replace it with the actual account key value to run the code.
    'endpoint': 'https://?????????????.queue.core.windows.net/',# The endpoint value is hidden for security reasons. Please replace it with the actual endpoint value to run the code.
    'queue_id': '?????????????', # The queue id value is hidden for security reasons. Please replace it with the actual queue id value to run the code.
}

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """ HTTP triggered function to send messages to an Azure Storage Queue.
    It expects a JSON payload in the request body.
    """
    
    # Tries to load the request body as JSON
    try:
        # Loads request body as JSON
        input_json = json.loads(req.get_body())
    except:
        # Error handling for invalid JSON format
        return func.HttpResponse(
            "Error: Invalid JSON format in the request body.",
            status_code=400
        )

    # Create Azure credentials
    account_credential = AzureNamedKeyCredential(config_values['account_name'], config_values['account_key'])

    # Get the queue client
    queue_client = QueueClient(
        account_url=config_values['endpoint'],
        queue_name=config_values['queue_id'],
        credential=account_credential,
        message_encode_policy=TextBase64EncodePolicy()
    )

    # Prepare the message to be sent to the queue
    queue_client.send_message(json.dumps(input_json))

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Message sent to the queue.",
            status_code=200
    )
