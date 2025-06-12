"""
End-to-End Pipeline: OCR → Paragraph Chunking → Embedding → Ingestion → RAG via GenAI
Example: University Course PDF
"""
from google.cloud import aiplatform
from google.cloud import documentai_v1 as documentai
from google.cloud.aiplatform import MatchingEngineIndex
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex as MEIndex
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2
from vertexai import Client as GenAIClient
from vertexai.types import TextPrompt
import os
import json
import uuid

# ——————————————————————————————————————————————————————
#  CONFIGURATION
# ——————————————————————————————————————————————————————
KEY_PATH = "path/to/service-account.json"
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
PROCESSOR_ID = "your-docai-processor-id"  # e.g., "ocr_processor"
PDF_GCS_URI = "gs://your-bucket/course.pdf"
OCR_OUTPUT_URI = "gs://your-bucket/ocr-output/"
CHUNKS_OUTPUT_URI = "gs://your-bucket/paragraph-chunks/"
EMBEDDINGS_OUTPUT_URI = "gs://your-bucket/embeddings/"
INDEX_NAME = "courses-index"

# Initialize credentials & clients
creds = service_account.Credentials.from_service_account_file(KEY_PATH)

aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=creds)
me_index = MEIndex(
    index_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/indexes/{INDEX_NAME}",
    project=PROJECT_ID,
    location=LOCATION,
    credentials=creds,
)

docai_client = documentai.DocumentProcessorServiceClient(credentials=creds)
parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"

genai_client = GenAIClient(project=PROJECT_ID, location=LOCATION)

# ——————————————————————————————————————————————————————
#  1) OCR with Document AI → save JSON to GCS
# ——————————————————————————————————————————————————————
request = documentai.ProcessRequest(
    name=parent,
    raw_document=documentai.RawDocument(
        gcs_content_uri=PDF_GCS_URI, mime_type="application/pdf"
    ),
)
result = docai_client.process_document(request=request)

gcs_uri = os.path.join(OCR_OUTPUT_URI, f"ocr_{uuid.uuid4()}.json")
# Save entire OCR JSON to GCS
with open("/tmp/ocr.json", "w") as f:
    f.write(documentai.Document.to_json(result))
os.system(f"gsutil cp /tmp/ocr.json {gcs_uri}")
print(f"OCR output saved to {gcs_uri}")

# ——————————————————————————————————————————————————————
#  2) Paragraph Chunking
# Option A: use GenAI prompt for chunking
# ——————————————————————————————————————————————————————
# Load OCR text
text = "".join([page.text for page in result.pages])
chunk_prompt = (
    f"Split the following university course transcript into coherent paragraphs."
    f" Return a JSON list of objects {{'id':..., 'text':...}}."
    f"\n\nDocument:\n{text}"
)
response = genai_client.generate_text(TextPrompt(text=chunk_prompt))
chunks = json.loads(response.content)
print(f"Generated {len(chunks)} chunks via GenAI.")

# Save chunk JSON to GCS
chunks_uri = os.path.join(CHUNKS_OUTPUT_URI, f"chunks_{uuid.uuid4()}.json")
with open("/tmp/chunks.json", "w") as f:
    json.dump(chunks, f)
os.system(f"gsutil cp /tmp/chunks.json {chunks_uri}")
print(f"Chunks saved to {chunks_uri}")

# ——————————————————————————————————————————————————————
#  3) Embeddings Generation & Save to GCS
# ——————————————————————————————————————————————————————
embeddings_payload = []
for c in chunks:
    embed_resp = genai_client.generate_embeddings(
        model="embedding-model-1",  # specify suitable embedding model
        instances=[c['text']]
    )
    vec = embed_resp.embeddings[0]
    embeddings_payload.append({
        "id": c['id'],
        "embedding": vec,
        "metadata": {"source": "course_pdf"}
    })

emb_uri = os.path.join(EMBEDDINGS_OUTPUT_URI, f"embeddings_{uuid.uuid4()}.jsonl")
with open("/tmp/embeddings.jsonl", "w") as f:
    for item in embeddings_payload:
        f.write(json.dumps(item) + "\n")
os.system(f"gsutil cp /tmp/embeddings.jsonl {emb_uri}")
print(f"Embeddings JSONL saved to {emb_uri}")

# ——————————————————————————————————————————————————————
#  4) Ingest into Matching Engine (full overwrite)
# ——————————————————————————————————————————————————————
me_index.update_embeddings(
    contents_delta_uri=emb_uri,
    is_complete_overwrite=True
)
print("Matching Engine index embeddings updated.")

# ——————————————————————————————————————————————————————
#  5) RAG Query via GenAI Client
# ——————————————————————————————————————————————————————
query = "Explain the grading criteria for the final exam."
rag_retrieval = genai_client.augment_prompt(
    # illustrate using RAG augmentPrompt underlying API
    prompt=query,
    retrieval_corpus=me_index
)
rag_response = genai_client.generate_text(rag_retrieval)
print("RAG Response:", rag_response.content)
