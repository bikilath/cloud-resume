import logging
import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.core.exceptions import ResourceNotFoundError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Initialize Cosmos DB Table API client
    client = CosmosClient.from_connection_string(os.getenv("COSMOS_CONNECTION_STRING"))
    database = client.get_database_client("resume-db")
    container = database.get_container_client("visitorCounts")
    
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if req.method == "GET":
        try:
            item = container.read_item(item="1", partition_key="counter")
            return func.HttpResponse(
                body=json.dumps({"count": item["count"]}),
                status_code=200,
                headers=headers,
                mimetype="application/json"
            )
        except ResourceNotFoundError:
            # Initialize counter if not exists
            container.upsert_item({
                "id": "1",
                "partitionKey": "counter",
                "count": 0
            })
            return func.HttpResponse(
                body=json.dumps({"count": 0}),
                status_code=200,
                headers=headers,
                mimetype="application/json"
            )

    elif req.method == "POST":
        try:
            item = container.read_item(item="1", partition_key="counter")
            current_count = item["count"] + 1
            container.upsert_item({
                "id": "1",
                "partitionKey": "counter",
                "count": current_count
            })
            return func.HttpResponse(
                body=json.dumps({"count": current_count}),
                status_code=200,
                headers=headers,
                mimetype="application/json"
            )
        except Exception as e:
            logging.error(f"POST error: {str(e)}")
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
