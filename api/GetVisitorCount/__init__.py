import logging
import os
import azure.functions as func
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    connection_string = os.getenv("AzureWebJobsStorage")
    table_name = "visitorcounts"
    
    try:
        table_service = TableService(connection_string=connection_string)
        
        try:
            entity = table_service.get_entity(table_name, "1", "1")
            count = entity.Count + 1
            entity.Count = count
            table_service.update_entity(table_name, entity)
        except Exception:
            entity = Entity()
            entity.PartitionKey = "1"
            entity.RowKey = "1"
            entity.Count = 1
            table_service.insert_entity(table_name, entity)
            count = 1
            
        return func.HttpResponse(
            body=f'{{"count": {count}}}',
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as ex:
        logging.error(f"Error: {ex}")
        return func.HttpResponse(
            body='{"count": 0}',
            mimetype="application/json",
            status_code=500
        )