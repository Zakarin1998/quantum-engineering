# Google Cloud AiPlatform - MatchingEngineIndex

Ecco il confronto dettagliato fra le tre operazioni disponibili su un indice Matching Engine (upsert, update\_metadata, update\_embeddings), un esempio di utilizzo reale e un’analisi delle differenze.

---

## Introduzione

Ecco una panoramica dei termini chiave nel contesto di Google Vertex AI Matching Engine, così da chiarire i “ruoli” e le relazioni tra **risorsa**, **indice** e **datapoint**.

---

| Termine       | Cosa indica                                                                                                                            | Ruolo / Scopo                                                                                                                 |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Risorsa**   | Qualunque oggetto gestito dalle API di Google Cloud. Ha un *resource name* univoco (es. `projects/.../locations/.../indexes/...`).     | Ogni operazione (creazione, aggiornamento, cancellazione) agisce su una risorsa. Ad es., l’indice stesso è una risorsa.       |
| **Indice**    | Risorsa di tipo „Index“ all’interno di Matching Engine. Contiene metadati (nome, descrizione, labels) e punta a un insieme di vettori. | È il contenitore principale: definisce *dove* i datapoint vengono organizzati e *come* verranno cercati (configurazioni).     |
| **Datapoint** | Un singolo “punto” nel tuo spazio vettoriale: un record composto da un ID, un vettore (embedding) e metadati/restrizioni opzionali.    | È l’unità atomica di ricerca: ogni datapoint è indicizzato nell’indice e potrà essere restituito come risultato di una query. |

---

### 🔍 Dettaglio delle relazioni

1. **Risorsa**

   * Ogni indice (`MatchingEngineIndex`) è una risorsa Cloud, identificata da un nome come

     ```
     projects/{PROJECT}/locations/{LOCATION}/indexes/{INDEX_ID}
     ```
   * Su questa risorsa puoi chiamare metodi come `create_index`, `delete_index`, `update_index`, `upsert_datapoints`.

2. **Indice**

   * Ha un layer “statale” (metadati) e un layer “dati” (i datapoint).
   * Metadati di indice includono `display_name`, `description`, `labels`, e parametri di configurazione (es. algoritmo di ricerca).
   * Dati dell’indice sono i **datapoint**: il vero contenuto vettoriale.

3. **Datapoint**

   * Ogni datapoint è un record JSON simile a:

     ```python
     {
       "id": "dp123",
       "feature_vector": [0.12, 0.98, …],
       "datapoint_metadata": {"category": "news", …},
       "restricts": {"lang": "en"},
       "crowding_tag": "tag1"
     }
     ```
   * Viene indicizzato nell’indice tramite operazioni come:

     * **Upsert**: crea o aggiorna singoli datapoint in tempo reale.
     * **Update\_embeddings**: ricarica in blocco embedding via GCS.
   * Al momento della **query**, Matching Engine calcola distanze tra vettori di query e i datapoint presenti nell’indice.

---

### 📝 Esempio

```txt
Risorsa (Index)
 ├─ Metadati: display_name="Prod Index", labels={"env":"prod"}
 └─ Datapoints:
     ├─ {id="dp1", feature_vector=[…], metadata={…}}
     ├─ {id="dp2", feature_vector=[…], metadata={…}}
     └─ …
```

* Quando esegui **update\_metadata**, modifichi solo i metadati dell’oggetto `Index` (risorsa).
* Quando esegui **upsert\_datapoints**, aggiungi o aggiorni singoli record all’interno della sezione “Datapoints” dell’indice.
* Quando esegui **update\_embeddings**, fornisci un GCS URI da cui Matching Engine ricarica in massa tutti (o un sottoinsieme) dei vettori dei datapoint.

---

Con questa distinzione:

* **Risorsa** = “l’oggetto Cloud” su cui fai chiamate API;
* **Indice** = specifica risorsa di tipo Index, che raccoglie metadati e datapoint;
* **Datapoint** = singolo record vettoriale immesso nell’indice per la ricerca.

Speriamo che con questa introduzione, il modello concettuale dietro queste funzionalità sia più chiaro!

---

## 1. Panoramica a confronto

| Operazione            | Metodo a livello client                                                                       | Parametri principali                                                                                                                                              | Cosa fa                                                                                                                        | FieldMask usato                                                     |
| --------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **Upsert datapoints** | `IndexServiceClient.upsert_datapoints` <br>(wrapper: `MatchingEngineIndex.upsert_datapoints`) | - `name` (resource name dell’indice)<br>- `datapoints: List[Datapoint]`<br>- *opzionale* `validate_only`, `skip_head_request`                                     | Inserisce o aggiorna singoli datapoint (id, vettore, metadata, restrizioni). Se l’id esiste, sovrascrive embedding e metadata. | Nessun field mask (tutta la risorsa “datapoints” viene considerata) |
| **Update metadata**   | `IndexServiceClient.update_index` <br>(wrapper: `MatchingEngineIndex.update_metadata`)        | - `gapic_index: Index(name=…, display_name?, description?, labels?)`<br>- `update_mask: FieldMask(paths=[…])`<br>- *metadati di RPC*                              | Modifica solo le proprietà di *index* (nome utente, descrizione, etichette). Non tocca datapoints né embedding.                | `["display_name","description","labels"]`                           |
| **Update embeddings** | `IndexServiceClient.update_index` <br>(wrapper: `MatchingEngineIndex.update_embeddings`)      | - `gapic_index: Index(name=…, metadata={"contentsDeltaUri":…, "isCompleteOverwrite":…})`<br>- `update_mask: FieldMask(paths=["metadata"])`<br>- *metadati di RPC* | Informa il servizio di prendere da GCS nuovi file di embedding (delta o full), associati all’indice.                           | `["metadata"]`                                                      |

---

## 2. Esempio realistico di utilizzo

Supponiamo di voler:

1. Creare un indice vuoto.
2. Upsertare un paio di datapoint (due vettori e metadati).
3. Aggiornare solo le etichette dell’indice.
4. Forzare un completa sovrascrittura degli embedding via GCS.

```python
from google.cloud.aiplatform.gapic import IndexServiceClient
from google.cloud.aiplatform.gapic.schema import index_service
from google.cloud.aiplatform import init
from google.cloud.aiplatform.matching_engine import MatchingEngineIndex
from google.protobuf import field_mask_pb2

# Inizializzazione
init(project="mio-progetto", location="us-central1")
client = IndexServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})

# 1) Upsert datapoints
datapoints = [
    index_service.Datapoint(
        id="dp1",
        feature_vector=[0.1, 0.2, 0.3],
        datapoint_metadata={"tag": "prima versione"},
    ),
    index_service.Datapoint(
        id="dp2",
        feature_vector=[0.5, 0.4, 0.9],
        datapoint_metadata={"tag": "prima versione"},
    ),
]
upsert_op = client.upsert_datapoints(
    name="projects/mio-progetto/locations/us-central1/indexes/mio-indice",
    datapoints=datapoints,
)
upsert_op.result()  # blocca fino al completamento

# 2) Update metadata (solo labels e display_name)
index = MatchingEngineIndex(
    index_name="projects/mio-progetto/locations/us-central1/indexes/mio-indice"
)
index.update_metadata(
    display_name="Indice di prova",
    labels={"env": "dev", "team": "ricerca"}
)

# 3) Update embeddings via GCS (full overwrite)
index.update_embeddings(
    contents_delta_uri="gs://bucket/embeddings/full_overwrite/",
    is_complete_overwrite=True
)

print("Operazioni completate con successo")
```

---

## 3. Differenze e casi d’uso

| Aspetto           | Upsert                                                                                                              | Update metadata                                                        | Update embeddings                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Ambito**        | Singoli datapoint all’interno dell’indice                                                                           | Proprietà dell’indice (nome, etichette, descrizione)                   | Contenuto embedding dell’indice (da GCS)                                                    |
| **FieldMask**     | nessuno (affronta direttamente “datapoints”)                                                                        | specifici campi metadata dell’indice                                   | `metadata`                                                                                  |
| **Uso tipico**    | Aggiungere o correggere singoli vettori/metadati <br>– utile hot-fix su poche righe di dati                         | Cambiare display\_name/labels/description senza toccare vectordb       | Caricare in blocco file vettoriali (delta o full) tramite GCS                               |
| **Limiti**        | - **Non** modifica labels o description<br>- Payload in request si paga e scala linearmente con numero di datapoint | - **Non** modifica embedding o datapoints <br>- Solo campi index-level | – Non consente upsert puntuale di singoli datapoint;<br>– Richiede struttura e permessi GCS |
| **Performance**   | Buono per aggiornamenti puntuali (batch <1000)                                                                      | Istantaneo (piccola update LRO)                                        | Ottimo per dataset molto grandi (parallelismo interno GCS)                                  |
| **Compatibilità** | Disponibile in tutte le versioni API                                                                                | Disponibile in tutte le versioni API                                   | Richiede IAM e formati GCS compatibili                                                      |

### Cosa posso fare **solo** con ciascuno:

* **Solo upsert**:

  * Aggiungere o sostituire singoli datapoint o piccoli batch senza creare file GCS esterni.
  * Esempio: correggere embedding sbagliato per l’id `dp123`.

* **Solo update\_metadata**:

  * Modificare etichette, descrizione o nome visualizzato dell’indice in modo atomico, senza influenzare i data points.
  * Esempio: marcare l’indice come “production” via label senza toccare i vector.

* **Solo update\_embeddings**:

  * Caricare gigabyte di vettori in bulk tramite GCS, con opzione di full overwrite (utile per refresh totale periodico).
  * Esempio: rimpiazzare tutti i vettori con una nuova estrazione da un corpus aggiornato, senza dover upsertare manualmente migliaia di record.

---

## 4. Tabella Alternativa per Differenze e compatibilità

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
* **Upsert** è ideale per interventi “ad hoc” su singoli o piccoli gruppi di datapoint.
    
* **`update_metadata`** serve solo a modificare attributi non-vettoriali (display name, labels, description).
* **Update metadata** serve esclusivamente a cambiare proprietà dell’indice (es. naming, organizzazione).

* **`update_embeddings`** permette di caricare o sovrascrivere in bulk embeddings tramite file GCS: non viaggia vettore per vettore, ma punta a directory preformattate.
* **Update embeddings** è la via più efficiente per operazioni massicce su vettori, in particolare quando si ha già un dump su GCS.

Se hai bisogno di modificare simultaneamente **vettori** e **labels**, devi combinare un `upsert_datapoints` per i vettori e un `update_metadata` per le etichette.
Se invece vuoi solo “rifare” da zero l’index con un nuovo set di embeddings, usa `update_embeddings` con `is_complete_overwrite=True`.
