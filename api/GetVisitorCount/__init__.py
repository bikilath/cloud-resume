import azure.functions as func
from azure.data.tables import TableServiceClient
import os

app = func.FunctionApp()

@app.function_name(name="GetVisitorCount")
@app.route(route="visitor", methods=["GET", "POST", "OPTIONS"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    # Handle CORS preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "https://lively-dune-0dcea4703.1.azurestaticapps.net",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        )
    
    # Initialize Table Storage
    table_client = TableServiceClient.from_connection_string(
        os.environ["AzureWebJobsStorage"]
    ).get_table_client("VisitorCounts")
    
    try:
        # Counter logic
        try:
            entity = table_client.get_entity(partition_key="1", row_key="1")
            count = entity['Count'] + 1 if req.method == "POST" else entity['Count']
        except:
            count = 1 if req.method == "POST" else 0

        # Update on POST
        if req.method == "POST":
            table_client.upsert_entity({
                "PartitionKey": "1",
                "RowKey": "1",
                "Count": count
            })

        return func.HttpResponse(
            body=f'{{"count": {count}}}',
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "https://lively-dune-0dcea4703.1.azurestaticapps.net",
                "Content-Type": "application/json"
            }
        )

    except Exception as e:
        return func.HttpResponse(
            body='{"error": "Counter unavailable"}',
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            }
        )
