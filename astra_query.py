from astrapy.db import AstraDB
import embedding_create
import os

# Fetching necessary environment variables for AstraDB configuration
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
COLLECTION_NAME = "town_content"

# Preparing a list of queries about the town Shadowfen
queries = [
    "What are the locations within Shadowfen?",
    "Who is Eldermarsh Thorne?",
    "Who is Brom Stoutfist?",
    "What is The Gloomwater Brewery?",
    "What is the terrain like surrounding Shadowfen?",
    "Who created Shadowfen?",
    "What is the climate of Shadowfen?",
    "What is the population of Shadowfen?",
    "What is the history of Shadowfen?",
    "Where can I get a drink in Shadowfen?",
]

# Generating embeddings for each query using a custom embedding creation function
embeddings = embedding_create.create_embeddings(queries)

# Establishing a connection to Astra DB with the provided credentials and keyspace
db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    namespace=ASTRA_DB_KEYSPACE,
)

# Accessing the specified collection in the Astra DB
collection = db.collection(collection_name=COLLECTION_NAME)

# Iterating through each query to perform a similarity search in the database
for index, query in enumerate(queries):
    # Converting the embedding to a list for the query
    embedding = embeddings[index].tolist()

    # Defining the sorting, options, and projection for the database query
    sort = {"$vector": embedding}
    options = {"limit": 2}
    projection = {"$similarity": 1, "text": 1}

    # Executing the find operation on the collection with the specified parameters
    document_list = collection.find(sort=sort, options=options, projection=projection)

    print(query)
    # Iterating through the retrieved documents to print their content
    for document in document_list["data"]["documents"]:
        print(document["text"])
        print(document["$similarity"])
        print("\n\n")
