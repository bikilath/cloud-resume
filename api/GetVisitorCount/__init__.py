import logging
import os
import json
import azure.functions as func
from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceNotFoundError

# Initialize table client
def get_table_client():
    connection_string = os.getenv("AzureWebJobsStorage")  # Uses your Function App storage
    table_service = TableServiceClient.from_connection_string(connection_string)
    table_client = table_service.get_table_client("VisitorCounts")
    
    try:
        table_client.create_table()
        logging.info("Table created or already exists")
    except Exception as e:
        logging.info(f"Table creation check: {str(e)}")
    
    return table_client

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers=headers
        )

    table_client = get_table_client()
    
    try:
        if req.method == "GET":
            try:
                entity = table_client.get_entity(partition_key="counter", row_key="main")
                return func.HttpResponse(
                    body=json.dumps({"count": entity["Count"]}),
                    status_code=200,
                    headers=headers,
                    mimetype="application/json"
                )
            except ResourceNotFoundError:
                # Initialize if not exists
                table_client.upsert_entity({
                    "PartitionKey": "counter",
                    "RowKey": "main",
                    "Count": 0
                })
                return func.HttpResponse(
                    body=json.dumps({"count": 0}),
                    status_code=200,
                    headers=headers,
                    mimetype="application/json"
                )

        elif req.method == "POST":
            try:
                entity = table_client.get_entity(partition_key="counter", row_key="main")
                current_count = entity["Count"] + 1
            except ResourceNotFoundError:
                current_count = 1
            
            table_client.upsert_entity({
                "PartitionKey": "counter",
                "RowKey": "main",
                "Count": current_count
            })
            
            return func.HttpResponse(
                body=json.dumps({"count": current_count}),
                status_code=200,
                headers=headers,
                mimetype="application/json"
            )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Internal server error"}),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )

    return func.HttpResponse(
        "Method not allowed",
        status_code=405,
        headers=headers
    )
