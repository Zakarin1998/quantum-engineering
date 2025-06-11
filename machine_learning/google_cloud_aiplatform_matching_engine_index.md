# Google Cloud AiPlatform - MatchingEngineIndex

Ecco il report strutturato in tre sezioni:

1. **Panoramica e tabelle dei metodi**
2. **Esempi di utilizzo**
3. **Confronto e differenze implementative**

---

## 1. Panoramica e tabelle dei metodi

| Metodo                 | Parametri principali                                                                                                                                                                                                                  | Cosa fa (descrizione)                                                                                                                                                            | Note implementative                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| **upsert\_datapoints** | - `name: str` (resource name dell’index)<br>- `datapoints: Sequence[Datapoint]`<br>- (opzionali) `crowding_tag`, `timeout`, `retry`, `metadata`                                                                                       | Inserisce o aggiorna uno o più datapoint nell’index. Restituisce un LRO che gestisce l’operazione asincrona di upsert.                                                           | È parte di `IndexServiceClient` del client GAPIC di Vertex AI.         |
| **update\_metadata**   | - `display_name: Optional[str]`<br>- `description: Optional[str]`<br>- `labels: Optional[Dict[str,str]]`<br>- `request_metadata: Optional[Sequence[Tuple[str,str]]]`<br>- `update_request_timeout: Optional[float]`                   | Esegue una chiamata a `update_index` su `api_client` per modificare campi “top-level” dell’Index (nome visualizzato, descrizione, etichette).                                    | Usa un `FieldMask` costruito dinamicamente; invoca `update_index` LRO. |
| **update\_embeddings** | - `contents_delta_uri: str` (GCS URI che punta a directory con file di delta)<br>- `is_complete_overwrite: Optional[bool]`<br>- `request_metadata: Optional[Sequence[Tuple[str,str]]]`<br>- `update_request_timeout: Optional[float]` | Chiama `update_index` passando un metadata blob con i percorsi GCS e flag di overwrite. Serve a caricare (o sovrascrivere) in blocco l’intero embedding set tramite path su GCS. | Anche qui costruisce un `FieldMask` e richiama `update_index` LRO.     |

---

## 2. Esempi di utilizzo

### 2.1 upsert\_datapoints

```python
from google.cloud.aiplatform.gapic import IndexServiceClient
from google.cloud.aiplatform.gapic.schema.index_service import Datapoint

# Configurazione
client = IndexServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})
index_name = client.index_path(project="my-project", location="us-central1", index="my-index")

# Costruzione dei datapoint
datapoints = [
    Datapoint(id="doc1", feature_vector=[0.1,0.2,0.3], restricts=[], crowding_tag="", datapoint_metadata={"page": 1}),
    Datapoint(id="doc2", feature_vector=[0.4,0.5,0.6], restricts=[], crowding_tag="", datapoint_metadata={"page": 2}),
]

# Chiamata upsert
operation = client.upsert_datapoints(name=index_name, datapoints=datapoints)
print("Upsert LRO name:", operation.operation.name)
operation.result(timeout=300)  # attende la fine
print("Upsert completato")
```

---

### 2.2 update\_metadata

```python
from google.cloud.aiplatform import MatchingEngineIndex

# Supponendo di aver già istanziato l’oggetto Index
index = MatchingEngineIndex(index_name="projects/my-project/locations/us-central1/indexes/my-index")

# Aggiornamento di display_name, description e labels
index.update_metadata(
    display_name="Indice Documenti RAG",
    description="Index per pipeline RAG custom",
    labels={"team": "ml-eng", "env": "dev"},
    request_metadata=[("x-goog-user-project","my-project")],
    update_request_timeout=120.0,
)
print("Nuovo display_name:", index.resource.display_name)
print("Nuove labels:", index.resource.labels)
```

---

### 2.3 update\_embeddings

```python
from google.cloud.aiplatform import MatchingEngineIndex

# Instanzia l’Index client wrapper
index = MatchingEngineIndex(index_name="projects/my-project/locations/us-central1/indexes/my-index")

# Carica in GCS i file di delta (JSON o CSV) in gs://my-bucket/delta/
delta_uri = "gs://my-bucket/delta/"

# Sovrascrivi completamente l’index con i nuovi embeddings
index.update_embeddings(
    contents_delta_uri=delta_uri,
    is_complete_overwrite=True,
    request_metadata=[("x-goog-user-project","my-project")],
    update_request_timeout=300.0,
)
print("Embeddings aggiornati da:", delta_uri)
```

---

## 3. Differenze e compatibilità

| Aspetto                | `upsert_datapoints`                                  | `update_metadata`                                             | `update_embeddings`                                                      |
| ---------------------- | ---------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| **Tipo di operazione** | Vettoriale: inserimento/aggiornamento singolo o bulk | Metadati: cambia display\_name, description, labels           | Gestione bulk embeddings via file GCS (delta o full overwrite)           |
| **Endpoint GAPIC**     | `IndexServiceClient.upsert_datapoints`               | `IndexServiceClient.update_index` (usato tramite wrapper API) | `IndexServiceClient.update_index` (wrapper API)                          |
| **Payload**            | Lista di `Datapoint` in-memory                       | Resource `Index` con campi top-level                          | Resource `Index` con `metadata.contentsDeltaUri` e `isCompleteOverwrite` |
| **Supporta**           | Solo vettori già calcolati                           | Solo metadati “statici” (stringhe, mappe)                     | Solo caricamento via GCS URI, non API-direct a lista in-memory           |
| **Non supporta**       | Non cambia labels o nome                             | Non inserisce / modifica embeddings                           | Non modifica display\_name/labels o feature\_vector in linea             |
| **Caso d’uso ideale**  | Aggiornare o inserire dinamicamente nuovi vettori    | Rinomina, ridescrive, etichetta senza toccare embeddings      | Popolare o risincronizzare massivamente embeddings da un bucket GCS      |
| **Locking / LRO**      | Sì, LRO asincrono                                    | Sì, LRO asincrono                                             | Sì, LRO asincrono                                                        |

### Conclusioni

* **`upsert_datapoints`** è l’unico metodo che consente di inserire o aggiornare **direttamente** vettori in memoria via API.
* **`update_metadata`** serve solo a modificare attributi non-vettoriali (display name, labels, description).
* **`update_embeddings`** permette di caricare o sovrascrivere in bulk embeddings tramite file GCS: non viaggia vettore per vettore, ma punta a directory preformattate.

Se hai bisogno di modificare simultaneamente **vettori** e **labels**, devi combinare un `upsert_datapoints` per i vettori e un `update_metadata` per le etichette.
Se invece vuoi solo “rifare” da zero l’index con un nuovo set di embeddings, usa `update_embeddings` con `is_complete_overwrite=True`.
