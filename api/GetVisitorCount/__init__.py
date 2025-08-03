import azure.functions as func
from azure.data.tables import TableServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Connect to Table Storage
    connection_string = os.getenv("AzureWebJobsStorage")  # Uses Function App's storage
    table_client = TableServiceClient.from_connection_string(
        connection_string).get_table_client("VisitorCounts")
    
    # Ensure table exists
    table_client.create_table_if_not_exists()
    
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST"
    }

    try:
        entity = table_client.get_entity(
            partition_key="CounterPartition", 
            row_key="GlobalCounter"
        )
        count = entity['Count'] + 1 if req.method == "POST" else entity['Count']
    except:
        count = 1 if req.method == "POST" else 0

    # Update counter
    table_client.upsert_entity({
        "PartitionKey": "CounterPartition",
        "RowKey": "GlobalCounter",
        "Count": count
    })

    return func.HttpResponse(
        body=f'{{"count": {count}}}',
        status_code=200,
        headers=headers,
        mimetype="application/json"
    )
