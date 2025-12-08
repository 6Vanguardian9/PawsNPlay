from celery import Celery
from services_util.ollama_embeddings import generate_embedding
from services_util.qdrant_services import insert_vector   # FIXED

app = Celery("worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@app.task
def process_ingestion(behavior_id: int, text: str, pet_id: int):
    vector = generate_embedding(text)

    payload = {"pet_id": pet_id, "text": text}

    insert_vector(
        behavior_id=behavior_id,
        vector=vector,
        payload=payload
    )

    return True
