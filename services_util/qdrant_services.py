from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
qdrant = QdrantClient(url=QDRANT_URL)


qdrant.recreate_collection(
    collection_name="pet_behavior",
    vectors_config=VectorParams(size=1024, distance="Cosine")
)

def insert_vector(behavior_id: int, vector: list[float], payload: dict):
    qdrant.upsert(
        collection_name="pet_behavior",
        points=[
            PointStruct(
                id=behavior_id,
                vector=vector,
                payload=payload
            )
        ],
    )
