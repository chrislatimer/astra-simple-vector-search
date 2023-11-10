from astrapy.db import AstraDB
import embedding_create
import os
import json

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
COLLECTION_NAME = "town_content"

# Create a list of queries
queries = []
queries.append("What are the locations within Shadowfen?")
queries.append("Who is Eldermarsh Thorne?")
queries.append("Who is Brom Stoutfist?")
queries.append("What is The Gloomwater Brewery?")
queries.append("What is the terrain like surrounding Shadowfen?")
queries.append("Who created Shadowfen?")
queries.append("What is the climate of Shadowfen?")
queries.append("What is the population of Shadowfen?")
queries.append("What is the history of Shadowfen?")
queries.append("Where can I get a drink in Shadowfen?")

# Create embeddings for each query
embeddings = embedding_create.create_embeddings(queries)

# Initialize connection to Astra DB
db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    namespace=ASTRA_DB_KEYSPACE,
)

# Define the db collection
collection = db.collection(collection_name=COLLECTION_NAME)

# Perform a similarity search for each query and print the results
for index, query in enumerate(queries):
    embedding = embeddings[index].tolist()
    query = queries[index]
    sort = {"$vector": embedding}
    options = {"limit": 2}
    projection = {"$similarity": 1, "text": 1}
    document_list = collection.find(sort=sort, options=options, projection=projection)

    print(f"Query: {query}")
    proper_json_string = str(document_list).replace("'", '"')
    parsed_json = json.loads(proper_json_string)
    print(json.dumps(parsed_json, indent=4, sort_keys=True))

    # # Specify the filename
    # filename = "output.txt"

    # # Open the file in write mode ('w') and write the contents
    # with open(filename, "w") as file:
    #     file.write(str(document_list))
