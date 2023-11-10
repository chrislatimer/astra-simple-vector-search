from astrapy.db import AstraDB
import doc_chunker
import os
import uuid
import json
import embedding_create

ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.environ.get("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
COLLECTION_NAME = "town_content"


# Function to split the documents into batches of 20
def batch(documents, batch_size):
    for i in range(0, len(documents), batch_size):
        yield documents[i : i + batch_size]


# Initialize connection to Astra DB
db = AstraDB(
    token=ASTRA_DB_APPLICATION_TOKEN,
    api_endpoint=ASTRA_DB_API_ENDPOINT,
    namespace=ASTRA_DB_KEYSPACE,
)

# Chunk the sample file into paragraphs
paragraphs = doc_chunker.chunk_file("./towns/shadowfen.txt")

# Create embeddings for each paragraph
embeddings = embedding_create.create_embeddings(paragraphs)

documents = []  # Initialize an empty list to hold document dictionaries

for index, paragraph in enumerate(paragraphs):
    # Create a dictionary for the current document
    document = {
        "_id": str(uuid.uuid4()),  # Generate a unique ID for each document
        "text": paragraph,  # The text of the paragraph
        "$vector": embeddings[index].tolist(),  # The corresponding embedding vector
    }

    # Append the document dictionary to the list
    documents.append(document)

# Define the db collection
collection = db.collection(collection_name=COLLECTION_NAME)

# Insert the documents in batches
for batch_documents in batch(documents, 20):
    # Convert the batch of documents to a JSON array string
    json_array = json.dumps(batch_documents, indent=4)

    # Insert the batch of documents into the collection
    res = collection.insert_many(documents=batch_documents)
    print(f"Inserted batch with response: {res}")
