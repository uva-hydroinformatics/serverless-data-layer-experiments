import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.eventgrid import EventGridPublisherClient, EventGridEvent
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

config_values= {
    'topic_key': '????????????????????????????????????????????', # The topic key value is hidden for security reasons. Please replace it with the actual topic key value to run the code.
    'endpoint': 'https://?????????.???????????.eventgrid.azure.net/api/events' # The endpoint value is hidden for security reasons. Please replace it with the actual endpoint value to run the code.
}

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """ HTTP triggered function to send messages to an Azure Event Grid Topic.
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
    
    try:

        # Loads configuration values for Event Grid
        credential = AzureKeyCredential(config_values["topic_key"])
        client = EventGridPublisherClient(config_values["endpoint"], credential)

        # Publishes the event to Event Grid
        client.send(
            [
                EventGridEvent(
                    event_type=input_json.get('name', 'unknown'),
                    data=input_json,
                    subject=input_json.get('end_device_ids', {}).get('application_ids', {}).get('application_id', 'unknown'),
                    data_version="1.0",
                )
            ]
        )
    except:
        # Error publishing to Event Grid
        return func.HttpResponse(
            "Error: Failed to publish to Event Grid.",
            status_code=400
        )        

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Message sent to the queue.",
            status_code=200
    )
