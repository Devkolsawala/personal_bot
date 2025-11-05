from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

COLLECTION_NAME = "documents"

def create_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
    )

def add_document(id: int, embedding: list, metadata: dict):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[models.PointStruct(id=id, vector=embedding, payload=metadata)]
    )

def query_similar(vector: list, top_k=5):
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k
    )
    return [hit.payload for hit in results]
