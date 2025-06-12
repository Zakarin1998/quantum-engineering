"""
End-to-End Pipeline with Modular Wrappers: OCR → Paragraph Chunking → Embedding → Storage → Index Ingestion → RAG
Example: University Course PDF
"""
import os
import json
import uuid
from typing import List, Dict, Any, Tuple

from google.cloud import aiplatform, documentai_v1 as documentai
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex
from google.oauth2 import service_account

from vertexai import Client as GenAIClient
from vertexai.types import TextPrompt

# ——————————————————————————————————————————————————————
#  CONFIGURATION
# ——————————————————————————————————————————————————————
KEY_PATH = "path/to/service-account.json"
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
PROCESSOR_ID = "your-docai-processor-id"
PDF_GCS_URI = "gs://your-bucket/course.pdf"
OCR_OUTPUT_URI = "gs://your-bucket/ocr-output/"
CHUNKS_OUTPUT_URI = "gs://your-bucket/paragraph-chunks/"
EMBEDDINGS_OUTPUT_URI = "gs://your-bucket/embeddings/"
INDEX_NAME = "courses-index"
EMBEDDING_MODEL = "embedding-model-1"

# ——————————————————————————————————————————————————————
#  CLASS WRAPPERS
# ——————————————————————————————————————————————————————

class DBStorage:
    """Handles saving and loading artifacts to GCS"""
    def __init__(self, bucket_uri: str):
        self.bucket_uri = bucket_uri.rstrip('/') + '/'

    def save_json(self, data: Any, prefix: str) -> str:
        local = f"/tmp/{prefix}_{uuid.uuid4()}.json"
        uri = os.path.join(self.bucket_uri, f"{prefix}_{uuid.uuid4()}.json")
        with open(local, 'w') as f:
            json.dump(data, f)
        os.system(f"gsutil cp {local} {uri}")
        print(f"Saved JSON to {uri}")
        return uri

    def save_jsonl(self, records: List[Dict[str, Any]], prefix: str) -> str:
        local = f"/tmp/{prefix}_{uuid.uuid4()}.jsonl"
        uri = os.path.join(self.bucket_uri, f"{prefix}_{uuid.uuid4()}.jsonl")
        with open(local, 'w') as f:
            for r in records:
                f.write(json.dumps(r) + '\n')
        os.system(f"gsutil cp {local} {uri}")
        print(f"Saved JSONL to {uri}")
        return uri

class DocaiWrap:
    """Wrapper around Document AI for OCR"""
    def __init__(self, project: str, location: str, processor_id: str, creds):
        self.client = documentai.DocumentProcessorServiceClient(credentials=creds)
        self.name = f"projects/{project}/locations/{location}/processors/{processor_id}"

    def run_ocr(self, gcs_pdf_uri: str) -> documentai.Document:
        request = documentai.ProcessRequest(
            name=self.name,
            raw_document=documentai.RawDocument(gcs_content_uri=gcs_pdf_uri, mime_type='application/pdf')
        )
        return self.client.process_document(request=request)

class ParagraphChunkingFunctions:
    """Functions to chunk OCR text into paragraphs"""
    def __init__(self, genai: GenAIClient, storage: DBStorage):
        self.genai = genai
        self.storage = storage

    def chunk(self, document: documentai.Document) -> Tuple[List[Dict[str, str]], str]:
        text = ''.join(page.text for page in document.pages)
        prompt = (
            "Split the following university course transcript into coherent paragraphs."
            " Return a JSON list of {'id', 'text'} objects.\n\n" + text
        )
        resp = self.genai.generate_text(TextPrompt(text=prompt))
        chunks = json.loads(resp.content)
        uri = self.storage.save_json(chunks, 'paragraph_chunks')
        return chunks, uri

class EmbeddingWrap:
    """Wrapper to generate embeddings via GenAI"""
    def __init__(self, genai: GenAIClient, storage: DBStorage, model: str):
        self.genai = genai
        self.storage = storage
        self.model = model

    def embed_chunks(self, chunks: List[Dict[str, str]]) -> str:
        records = []
        for chunk in chunks:
            emb_resp = self.genai.generate_embeddings(model=self.model, instances=[chunk['text']])
            records.append({
                'id': chunk['id'],
                'embedding': emb_resp.embeddings[0],
                'metadata': {'source': 'course_pdf'}
            })
        return self.storage.save_jsonl(records, 'embeddings')

class GenaiWrap:
    """Wrapper for GenAI RAG functionality"""
    def __init__(self, project: str, location: str):
        self.client = GenAIClient(project=project, location=location)

    def rag_query(self, index, query: str) -> Any:
        retrieval = self.client.augment_prompt(prompt=query, retrieval_corpus=index)
        return self.client.generate_text(retrieval)

class MEWrap:
    """Wrapper for Matching Engine Index operations"""
    def __init__(self, project: str, location: str, index_name: str, creds):
        aiplatform.init(project=project, location=location, credentials=creds)
        self.index = MatchingEngineIndex(
            index_name=f"projects/{project}/locations/{location}/indexes/{index_name}",
            project=project,
            location=location,
            credentials=creds
        )

    def update_embeddings(self, embeddings_uri: str, overwrite: bool = True):
        self.index.update_embeddings(contents_delta_uri=embeddings_uri, is_complete_overwrite=overwrite)
        print("Index embeddings updated.")

# ——————————————————————————————————————————————————————
#  PIPELINE FUNCTIONS
# ——————————————————————————————————————————————————————

def rag_ingestion():
    creds = service_account.Credentials.from_service_account_file(KEY_PATH)
    # Storage handlers
    ocr_storage = DBStorage(OCR_OUTPUT_URI)
    chunk_storage = DBStorage(CHUNKS_OUTPUT_URI)
    emb_storage = DBStorage(EMBEDDINGS_OUTPUT_URI)

    # Clients
    docai = DocaiWrap(PROJECT_ID, LOCATION, PROCESSOR_ID, creds)
    genai = GenaiWrap(PROJECT_ID, LOCATION)
    me = MEWrap(PROJECT_ID, LOCATION, INDEX_NAME, creds)

    # OCR
    ocr_doc = docai.run_ocr(PDF_GCS_URI)
    ocr_storage.save_json(json.loads(documentai.Document.to_json(ocr_doc)), 'ocr')

    # Paragraph chunking
    chunker = ParagraphChunkingFunctions(genai.client, chunk_storage)
    chunks, chunks_uri = chunker.chunk(ocr_doc)

    # Embeddings
    embedder = EmbeddingWrap(genai.client, emb_storage, EMBEDDING_MODEL)
    emb_uri = embedder.embed_chunks(chunks)

    # Ingest into Matching Engine
    me.update_embeddings(embeddings_uri=emb_uri, overwrite=True)

    return {'ocr': None, 'chunks': chunks_uri, 'embeddings': emb_uri}


def rag_generation(query: str):
    creds = service_account.Credentials.from_service_account_file(KEY_PATH)
    me = MEWrap(PROJECT_ID, LOCATION, INDEX_NAME, creds)
    genai = GenaiWrap(PROJECT_ID, LOCATION)
    response = genai.rag_query(me.index, query)
    print("RAG Response:", response.content)
    return response

if __name__ == "__main__":
    # Ingest pipeline
    rag_ingestion()

    # RAG generation
    q = (
        "Spiega cosa significa la Quantum Encryption Keys "  
        "e le basi di crittografia quantistica"
    )
    rag_generation(query=q)
    
