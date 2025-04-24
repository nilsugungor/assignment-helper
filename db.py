

import os
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("COSMOS_ENDPOINT")
key = os.getenv("COSMOS_KEY")
database_name = os.getenv("COSMOS_DB_DATABASE")
container_name = os.getenv("COSMOS_DB_CONTAINER")

client = CosmosClient(url, credential=key)
database = client.create_database_if_not_exists(id=database_name)
container = database.create_container_if_not_exists(
    id=container_name,
    partition_key=PartitionKey(path="/user_id"),
    offer_throughput=400
)
