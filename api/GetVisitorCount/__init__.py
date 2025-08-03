import azure.functions as func
from azure.data.tables import TableServiceClient, TableTransactionError
import os
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Initialize response headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Content-Type": "application/json"
    }

    # Handle CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers=headers
        )

    try:
        # Connect to Table Storage
        connection_string = os.getenv("AzureWebJobsStorage")
        if not connection_string:
            raise ValueError("Missing AzureWebJobsStorage configuration")
            
        table_client = TableServiceClient.from_connection_string(
            connection_string).get_table_client("VisitorCounts")
        
        # Ensure table exists (auto-create if not)
        table_client.create_table_if_not_exists()

        # Transactional update for counter
        try:
            entity = table_client.get_entity(
                partition_key="CounterPartition",
                row_key="GlobalCounter"
            )
            current_count = entity.get('Count', 0)
        except Exception as get_error:
            logging.warning(f"Counter not found, initializing: {str(get_error)}")
            current_count = 0

        # Increment only on POST requests
        if req.method == "POST":
            current_count += 1
            table_client.upsert_entity({
                "PartitionKey": "CounterPartition",
                "RowKey": "GlobalCounter",
                "Count": current_count
            })

        return func.HttpResponse(
            body=f'{{"count": {current_count}}}',
            status_code=200,
            headers=headers
        )

    except TableTransactionError as e:
        logging.error(f"Table transaction failed: {str(e)}")
        return func.HttpResponse(
            body='{"error": "Counter update failed"}',
            status_code=500,
            headers=headers
        )
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return func.HttpResponse(
            body='{"error": "Internal server error"}',
            status_code=500,
            headers=headers
        )
