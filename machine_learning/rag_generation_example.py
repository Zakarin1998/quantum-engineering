"""
End-to-End Pipeline: OCR → Paragraph Chunking → Embedding → Ingestion → RAG via GenAI
Example: University Course PDF
"""
from google.cloud import aiplatform, documentai_v1 as documentai
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex as MEIndex
from google.oauth2 import service_account
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
PROCESSOR_ID = "your-docai-processor-id"
PDF_GCS_URI = "gs://your-bucket/course.pdf"
OCR_OUTPUT_URI = "gs://your-bucket/ocr-output/"
CHUNKS_OUTPUT_URI = "gs://your-bucket/paragraph-chunks/"
EMBEDDINGS_OUTPUT_URI = "gs://your-bucket/embeddings/"
INDEX_NAME = "courses-index"
EMBEDDING_MODEL = "embedding-model-1"

class CoursePipeline:
    def __init__(self):
        # Credentials & client initialization
        self.creds = service_account.Credentials.from_service_account_file(KEY_PATH)
        aiplatform.init(project=PROJECT_ID, location=LOCATION, credentials=self.creds)
        self.me_index = MEIndex(
            index_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/indexes/{INDEX_NAME}",
            project=PROJECT_ID,
            location=LOCATION,
            credentials=self.creds,
        )
        self.docai_client = documentai.DocumentProcessorServiceClient(credentials=self.creds)
        self.genai_client = GenAIClient(project=PROJECT_ID, location=LOCATION)
        self.processor_name = (
            f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}"
        )

    def run_ocr(self):
        """Run OCR on PDF and save JSON to GCS"""
        request = documentai.ProcessRequest(
            name=self.processor_name,
            raw_document=documentai.RawDocument(
                gcs_content_uri=PDF_GCS_URI, mime_type="application/pdf"
            ),
        )
        result = self.docai_client.process_document(request=request)
        local_path = "/tmp/ocr.json"
        gcs_uri = os.path.join(OCR_OUTPUT_URI, f"ocr_{uuid.uuid4()}.json")
        with open(local_path, "w") as f:
            f.write(documentai.Document.to_json(result))
        os.system(f"gsutil cp {local_path} {gcs_uri}")
        print(f"OCR output saved to {gcs_uri}")
        return result, gcs_uri

    def chunk_paragraphs(self, document):
        """Chunk OCR result into paragraphs via GenAI, save chunks to GCS"""
        text = "".join(page.text for page in document.pages)
        prompt = (
            "Split the following university course transcript into coherent paragraphs."
            " Return a JSON list of {'id', 'text'} objects.\n\n" + text
        )
        response = self.genai_client.generate_text(TextPrompt(text=prompt))
        chunks = json.loads(response.content)
        local = "/tmp/chunks.json"
        uri = os.path.join(CHUNKS_OUTPUT_URI, f"chunks_{uuid.uuid4()}.json")
        with open(local, "w") as f:
            json.dump(chunks, f)
        os.system(f"gsutil cp {local} {uri}")
        print(f"Chunks saved to {uri}")
        return chunks, uri

    def generate_embeddings(self, chunks):
        """Generate embeddings for each chunk, save JSONL to GCS"""
        payload = []
        for c in chunks:
            emb = self.genai_client.generate_embeddings(
                model=EMBEDDING_MODEL, instances=[c['text']]
            )
            payload.append({
                "id": c['id'],
                "embedding": emb.embeddings[0],
                "metadata": {"source": "course_pdf"},
            })
        local = "/tmp/embeddings.jsonl"
        uri = os.path.join(EMBEDDINGS_OUTPUT_URI, f"embeddings_{uuid.uuid4()}.jsonl")
        with open(local, "w") as f:
            for item in payload:
                f.write(json.dumps(item) + "\n")
        os.system(f"gsutil cp {local} {uri}")
        print(f"Embeddings JSONL saved to {uri}")
        return uri

    def ingest_index(self, embeddings_uri):
        """Ingest embeddings into Matching Engine (complete overwrite)"""
        self.me_index.update_embeddings(
            contents_delta_uri=embeddings_uri,
            is_complete_overwrite=True
        )
        print("Matching Engine index embeddings updated.")

    def rag_query(self, question):
        """Perform RAG-style query using GenAI & Matching Engine index"""
        retrieval = self.genai_client.augment_prompt(
            prompt=question,
            retrieval_corpus=self.me_index
        )
        resp = self.genai_client.generate_text(retrieval)
        print("RAG Response:", resp.content)
        return resp

# ——————————————————————————————————————————————————————
#  PIPELINE METHODS
# ——————————————————————————————————————————————————————

def rag_ingestion():
    """Execute OCR → chunking → embeddings → ingestion into Matching Engine"""
    pipeline = CoursePipeline()
    ocr_doc, ocr_uri = pipeline.run_ocr()
    chunks, chunks_uri = pipeline.chunk_paragraphs(ocr_doc)
    emb_uri = pipeline.generate_embeddings(chunks)
    pipeline.ingest_index(emb_uri)
    return ocr_uri, chunks_uri, emb_uri


def rag_generation(query: str):
    """Perform RAG-generation given a query against the indexed content"""
    pipeline = CoursePipeline()
    return pipeline.rag_query(query)


if __name__ == "__main__":
    # 1) Build and ingest index
    rag_ingestion()

    # 2) Run RAG generation
    query = (
        "Spiega cosa significa la Quantum Encryption Keys "  
        "e le basi di crittografia quantistica"
    )
    rag_generation(query=query)
