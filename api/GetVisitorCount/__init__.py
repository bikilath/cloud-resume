import logging
import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.core.exceptions import CosmosResourceNotFoundError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # Initialize Cosmos DB client
    try:
        client = CosmosClient.from_connection_string(os.getenv("AzureCosmosDBConnectionString"))
        database = client.get_database_client("resume-db")
        container = database.get_container_client("visitorCounts")
        
        # Handle CORS preflight
        if req.method == "OPTIONS":
            return func.HttpResponse(
                status_code=200,
                headers={
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                }
            )
        
        # Handle GET request
        if req.method == "GET":
            try:
                item = container.read_item(item="1", partition_key="1")
                count = item.get("count", 0)
            except CosmosResourceNotFoundError:
                count = 0
                container.upsert_item({
                    "id": "1",
                    "count": count,
                    "partitionKey": "1"
                })
            
            return func.HttpResponse(
                body=json.dumps({"count": count}),
                status_code=200,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        
        # Handle POST request
        elif req.method == "POST":
            try:
                item = container.read_item(item="1", partition_key="1")
                count = item.get("count", 0) + 1
                container.upsert_item({
                    "id": "1",
                    "count": count,
                    "partitionKey": "1"
                })
                
                return func.HttpResponse(
                    body=json.dumps({"count": count}),
                    status_code=200,
                    headers={
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                )
            
            except Exception as e:
                logging.error(f"POST error: {str(e)}")
                return func.HttpResponse(
                    body=json.dumps({"error": "Internal server error"}),
                    status_code=500,
                    headers={
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": "*"
                    }
                )
        
        else:
            return func.HttpResponse(
                "Method not allowed",
                status_code=405,
                headers={
                    "Access-Control-Allow-Origin": "*"
                }
            )
    
    except Exception as e:
        logging.error(f"Database connection error: {str(e)}")
        return func.HttpResponse(
            body=json.dumps({"error": "Database connection failed"}),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )
