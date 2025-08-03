import logging
import os
import json
import azure.functions as func
from azure.data.tables import TableClient
from azure.core.exceptions import ResourceNotFoundError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    connection_string = os.getenv("COSMOS_CONNECTION_STRING")
    if not connection_string:
        return func.HttpResponse("Database connection not configured", status_code=500)
    
    try:
        table_client = TableClient.from_connection_string(
            conn_str=connection_string,
            table_name="VisitorCounts"
        )
        
        if req.method == "GET":
            return handle_get(table_client)
        elif req.method == "POST":
            return handle_post(table_client)
        else:
            return func.HttpResponse("Method not allowed", status_code=405)
            
    except Exception as ex:
        logging.error(f"Error: {str(ex)}")
        return func.HttpResponse("Internal server error", status_code=500)

def handle_get(table_client):
    try:
        entity = table_client.get_entity(partition_key="1", row_key="1")
        count = entity.get('Count', 0)
    except ResourceNotFoundError:
        count = 0
    return func.HttpResponse(
        json.dumps({"count": count}),
        mimetype="application/json"
    )

def handle_post(table_client):
    try:
        entity = table_client.get_entity(partition_key="1", row_key="1")
        count = entity.get('Count', 0) + 1
    except ResourceNotFoundError:
        count = 1
        
    table_client.upsert_entity({
        "PartitionKey": "1",
        "RowKey": "1",
        "Count": count
    })
    
    return func.HttpResponse(
        json.dumps({"count": count}),
        mimetype="application/json"
    )
