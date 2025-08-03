import logging
import os
import json
import azure.functions as func
from azure.data.tables import TableClient, UpdateMode
from azure.core.exceptions import ResourceNotFoundError

TABLE_NAME = 'ResumeVisits'
PARTITION_KEY = 'counter'
ROW_KEY = 'visits'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request for resume visit counter.')
    
    cosmos_conn_str = os.getenv('COSMOSDB_CONNECTION_STRING')
    if not cosmos_conn_str:
        return func.HttpResponse("Missing DB connection", status_code=500)

    try:
        table_client = TableClient.from_connection_string(
            conn_str=cosmos_conn_str,
            table_name=TABLE_NAME
        )
        
        if req.method == "GET":
            return handle_get(table_client)
        elif req.method == "POST":
            return handle_post(table_client)
        else:
            return func.HttpResponse("Method not allowed", status_code=405)
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse("Server error", status_code=500)

def handle_get(table_client):
    try:
        entity = table_client.get_entity(PARTITION_KEY, ROW_KEY)
        count = entity.get('Count', 0)
    except ResourceNotFoundError:
        count = 0
    return func.HttpResponse(json.dumps({'count': count}), mimetype="application/json")

def handle_post(table_client):
    try:
        entity = table_client.get_entity(PARTITION_KEY, ROW_KEY)
        current = entity.get('Count', 0)
    except ResourceNotFoundError:
        current = 0
    
    new_count = current + 1
    table_client.upsert_entity({
        'PartitionKey': PARTITION_KEY,
        'RowKey': ROW_KEY,
        'Count': new_count
    }, mode=UpdateMode.REPLACE)
    
    return func.HttpResponse(json.dumps({'count': new_count}), mimetype="application/json")
