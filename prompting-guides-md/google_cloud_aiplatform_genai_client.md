# Google Cloud AiPlatform - 1.97.0 Update

Here’s a structured overview of the  **1.97.0 (2025-06-11)** release, focusing on the code-level additions and changes:

---

## 1. New Features

### 1.1 GenAI Client (Experimental)

* **Added** a new GenAI client under `vertexai._genai.client`

  * Lazy-loads the `evals` module to avoid requiring heavy deps (`pandas`, `tqdm`) unless used.
  * Introduces both `AsyncClient` and `Client` wrappers around the underlying `google.genai.client.Client`.
  * Exposes `e vals` via an experimental warning decorator (`@_common.experimental_warning`).
  * Ensures that importing `vertexai.Client` now gives you a GenAI-capable client.

### 1.2 URL Context Metadata API

* **Exposed** `UrlContextMetadata` (and its nested `UrlMetadata`) in both

  * `google.cloud.aiplatform_v1`
  * `google.cloud.aiplatform_v1beta1`
* These additions allow Vertex AI’s content-generation outputs to include structured metadata about URLs retrieved during grounding.

  * Definitions live in `types/content.py` under each versioned package.

### 1.3 Vertex AI Multimodal Datasets Integration

* **Updated** the docstring for `sft.train()` to list “Vertex Multimodal Dataset” as a valid source for `train_dataset` and `validation_dataset`.
* This is purely documentation, but formalizes support for training on rich multimodal data.

### 1.4 RAG Corpus Configuration

* **Introduced** new configuration options for Retrieval-Augmented Generation (RAG):

  * `DocumentCorpus`
  * `MemoryCorpus`
* These allow clients to specify the type of corpus when constructing a RAG pipeline, improving flexibility around what data is retrieved and how “memory” stores are managed.

---

## 2. Bug Fixes & Enhancements

* **Default Auth Scope**

  * Added a default scope so that clients don’t accidentally omit required OAuth scopes.

* **ADK Agents Support**

  * `agent_engine` now recognizes “ADK Agents” as a valid engine type.

* **Memory Corpus Wiring**

  * Fixed an issue where the RAG memory-corpus setting wasn’t getting propagated into the internal `RagCorpus` object.

---

## 3. Client Initialization & Lazy Loading Overhaul

* **`vertexai/__init__.py`**

  * Expanded `__getattr__` to lazily expose both `Client` and `types` at the top level.
  * Ensures that importing `vertexai.types` or `vertexai.Client` triggers the underlying `_genai` imports exactly once.

* **`vertexai/_genai/__init__.py`**

  * Wrapped access to `evals` behind a custom `__getattr__`, with a clear error if pandas/tqdm aren’t installed.

* **`vertexai/_genai/client.py`**

  * Simplified constructor logic: removed eager assignment of `self._evals` and replaced with lazy-loading methods.
  * Both `AsyncClient` and `Client` now guard against missing dependencies and only import `evals` when accessed.

---

## 4. Unit Test Updates

Across **8** test files, the diffs show:

1. **Import Alignment**

   * Switched many imports from `from google.genai import types` to `from vertexai._genai.types` (aliased as `vertexai_genai_types`).
   * Ensures tests hit the new top-level API surface rather than the old direct GenAI SDK.

2. **Lazy-Load Assertions**

   * New tests to verify that importing `vertexai._genai.client` **does not** pull in heavy deps (e.g. `"pandas"` absent, `"pydantic"` present).
   * Added checks that the `evals` module itself *does* import `pandas` once triggered.

3. **Eval-API Behavior**

   * Consolidated duplicate `@pytest.mark.usefixtures("google_auth_mock")` decorators.
   * Merged and removed redundant test methods (`test_eval_batch_eval` appeared twice).
   * Updated expected call patterns to use the new `vertexai_genai_types` for all input objects.

4. **Client Instantiation**

   * Simplified the “genai client” smoke test to just assert that `vertexai.Client(...)` yields a non-null object with the right project set.

---

## 5. Version Bump in Samples

* **Sample metadata files** (`snippet_metadata_*.json`) now list `"version": "0.1.0"` instead of `"1.96.0"`, aligning samples with the new release’s codebase expectations.

---

### Impact & Next Steps

* **Upgrading** to 1.97.0 will **not** break existing Vertex AI users, but:

  * You should install the extra evaluation dependencies if you use `client.e vals` (`pip install google-cloud-aiplatform[evaluation]`).
  * Review any scripts that imported GenAI types directly—update to use `vertexai.types`.
* **Try out** the experimental GenAI client by doing:

  ```python
  from vertexai import Client
  client = Client(project="…", location="…")
  # now client.e vals is available!
  ```
* **Explore** the new RAG corpus options and URL metadata to enrich your retrieval and grounding pipelines.


## 🧠 6. Using the New Experimental GenAI Client

Here are some concrete examples demonstrating the new features available in **google‑cloud‑aiplatform 1.97.0**:

```python
# Install: pip install google-cloud-aiplatform[evaluation]
from vertexai import Client

# Initialize Vertex AI with your GCP project and region
client = Client(project="my-project", location="us-central1")

# Access the experimental GenAI evals client
e = client.evals  # triggers lazy loading of evals (loads pandas/tqdm)
print(e)  # <vertexai._genai.evals.Evals object>

# Example: Evaluate a simple BLEU instance
from vertexai.types import BleuInput
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("always")
    e.evaluate_instances(bleu_input=BleuInput())  # triggers ExperimentalWarning
```

* This shows how to use the new `Client` to access `evals` features—lazy-loaded only when needed.
* If you don't install evaluation dependencies (`pandas`, `tqdm`), attempting to access `client.evals` will raise a descriptive `ImportError`.

---

## 🌐 7. Using URL Context Metadata with GenAI (Grounding)

You can now pass URLs directly into the GenAI prompt and get back structured `UrlContextMetadata`, showing which URLs were actually retrieved and used.

```python
from vertexai import Client
from vertexai.types import TextPrompt

client = Client(project="my-project", location="us-central1")
prompt = TextPrompt(
    text="Summarize the key milestones in this NATO press release:",
    url_context=["https://www.nato.int/cps/en/natohq/news_123456.htm"]
)

response = client.chat.send(prompt)
print(response.content)

# Inspect which URLs were accessed in grounding
for m in response.url_context_metadata.url_metadata:
    print(m.retrieved_url, m.url_retrieval_status)
    # Example output:
    # https://.../news_123456.htm SUCCESS
```

This matches the documented pattern: GenAI includes a `url_context_metadata` field listing each URL retrieved and its status ([pypi.org][1], [ai.google.dev][2], [cloud.google.com][3], [github.com][4]).

---

## 🔁 8. Configuring RAG with Document vs Memory Corpus

The RAG features now differentiate between short-term document search and longer-term memory stores.

```python
from google.cloud.aiplatform import RagRetriever, RagGenerator
from google.cloud.aiplatform.types import DocumentCorpus, MemoryCorpus

# Build a retriever that sources from a document store
retriever = RagRetriever(corpus=DocumentCorpus(gcs_uri="gs://my-bucket/docs/"))
generator = RagGenerator(corpus=MemoryCorpus(gcs_uri="gs://my-bucket/memory/"))

# Run RAG pipeline
result = generator.generate_with_retrieval(
    question="What's the ROI of renewable energy projects?",
    retriever=retriever
)
print(result.text)
```

* `DocumentCorpus` is used for immediate retrieval.
* `MemoryCorpus` handles ongoing memory for future prompts.

---

## 🧩 9. Integrating URL Context + RAG + GenAI (Full Workflow)

Combine file/document retrieval, URL-context grounding, and memory-based RAG in a complete example:

```python
from vertexai import Client
from vertexai.types import TextPrompt
from google.cloud.aiplatform import RagRetriever, RagGenerator
from google.cloud.aiplatform.types import DocumentCorpus, MemoryCorpus

client = Client(project="...", location="...")

# Setup retriever and generator pipelines
retriever = RagRetriever(corpus=DocumentCorpus(gcs_uri="gs://my-bucket/news-articles/"))
generator = RagGenerator(corpus=MemoryCorpus(gcs_uri="gs://my-bucket/conversation-memory/"))

# Compose a grounded prompt
prompt = TextPrompt(
    text="Analyze recent trends in European energy policy.",
    url_context=["https://ec.europa.eu/energy/topics/energy-strategy_en"]
)

# Generate answer leveraging RAG and URL grounding
response = generator.generate_with_retrieval(
    question=prompt,
    retriever=retriever
)

print(response.text)
# URL metadata shows grounding success:
for u in response.url_context_metadata.url_metadata:
    print(u.retrieved_url, u.url_retrieval_status)
```

---

## ✨ Summary

* **`Client` with `.evals`**: Try experiments or run evaluations easily.
* **Grounding with URLs**: Get precise insights via URL metadata on what was used.
* **Corpus configuration**: Choose between document vs memory for RAG pipelines.

Let me know if you'd like additional examples—e.g., async GenAI client usage, memory persistence, or deeper evaluation scenarios!

[1]: https://pypi.org/project/google-cloud-aiplatform/?utm_source=chatgpt.com "google-cloud-aiplatform · PyPI"
[2]: https://ai.google.dev/gemini-api/docs/url-context?utm_source=chatgpt.com "URL context | Gemini API | Google AI for Developers"
[3]: https://cloud.google.com/python/docs/reference/aiplatform/1.23.0/google.cloud.aiplatform?utm_source=chatgpt.com "Package aiplatform (1.23.0) | Python client library - Google Cloud"
[4]: https://github.com/GoogleCloudPlatform/applied-ai-engineering-samples?utm_source=chatgpt.com "GoogleCloudPlatform/applied-ai-engineering-samples - GitHub"
