import io
import os
from typing import List

from google.cloud import documentai_v1 as documentai
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import IndexServiceClient
from google.cloud.aiplatform.gapic.schema import index_service

from PyPDF2 import PdfReader


def load_pdf_bytes(path: str) -> bytes:
    """Load PDF file into bytes."""
    with open(path, "rb") as f:
        return f.read()


def parse_document(project_id: str, location: str, processor_id: str, pdf_bytes: bytes):
    """Call Document AI to parse PDF and return the full text."""
    client = documentai.DocumentProcessorServiceClient()
    name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    document = documentai.Document.from_proto(
        client.process_document(
            request={"name": name, "raw_document": {"content": pdf_bytes, "mime_type": "application/pdf"}}
        ).document
    )
    return document.text, document


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Chunk text into overlapping windows."""
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def embed_texts(texts: List[str], project: str, location: str, endpoint_id: str) -> List[List[float]]:
    """Get embeddings from Vertex AI Embedding Endpoint."""
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    instances = [{"content": t} for t in texts]
    endpoint = f"projects/{project}/locations/{location}/endpoints/{endpoint_id}"
    response = client.predict(endpoint=endpoint, instances=instances)
    embeddings = [pred.model_outputs["embeddings"] for pred in response.predictions]
    return embeddings


def create_matching_engine_index(
    project: str,
    location: str,
    index_id: str,
    embeddings: List[List[float]],
    metadatas: List[dict],
):
    """Create or update a Matching Engine index with datapoints."""
    client = IndexServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    index_name = client.index_path(project=project, location=location, index=index_id)

    datapoints = []
    for idx, vector in enumerate(embeddings):
        datapoints.append(
            index_service.Datapoint(
                id=str(idx),
                feature_vector=vector,
                restricts=[],
                crowding_tag="",
                datapoint_metadata=metadatas[idx],
            )
        )

    operation = client.upsert_datapoints(name=index_name, datapoints=datapoints)
    print("Upsert operation:", operation.operation.name)
    return operation


def main():
    # Configuration
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    location = "us-central1"
    documentai_processor_id = "YOUR_DOCUMENT_AI_PROCESSOR_ID"
    embedding_endpoint_id = "YOUR_EMBEDDING_ENDPOINT_ID"
    matching_engine_index_id = "YOUR_INDEX_ID"
    pdf_path = "path/to/your/document.pdf"

    # 1. Load PDF
    pdf_bytes = load_pdf_bytes(pdf_path)

    # 2. Parse with Document AI
    full_text, document = parse_document(project_id, location, documentai_processor_id)

    # 3. Chunk text
    chunks = chunk_text(full_text)

    # 4. Embed chunks
    embeddings = embed_texts(chunks, project_id, location, embedding_endpoint_id)

    # 5. Prepare metadata
    metadatas = [{"text_snippet": chunk} for chunk in chunks]

    # 6. Create/update Matching Engine index
    operation = create_matching_engine_index(
        project=project_id,
        location=location,
        index_id=matching_engine_index_id,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print("Indexing started, check the operation status in the console.")


if __name__ == "__main__":
    main()
