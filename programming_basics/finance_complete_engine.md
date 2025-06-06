# Finance Document Intelligence Engine

Di seguito trovi un progetto “enterprise‐grade” per il controllo di coerenza (in particolare di contraddizioni) su una knowledge base finanziaria, sfruttando a pieno tutte le risorse di cui disponi:

1. **Possibilità di costruire un Knowledge Graph (KG) complesso** (budget e team di esperti a disposizione).
2. **Regole di dominio finanziario** scritte da analisti/esperti degli stessi documenti.
3. **Disponibilità di Azure e Google come fornitori di servizi** (OCR, NLP, ML, storage, DB, rule engine, ecc.).

L’idea è progettare una pipeline end‐to‐end che combina:

* Estrazione di entità e relazioni dai documenti
* Popolamento di un KG finanziario di riferimento (ontologia)
* Ragionamento logico/ontologico (OWL/DL, rule engine) per validare coerenze formali
* Controlli semantici “soft” basati su embedding/NLI per segnalare incongruenze di linguaggio non strettamente ontologico
* Integrazione fra servizi Google e Azure (Document AI, Vertex AI, Cognitive Services, Power BI, ecc.)
* Dashboard/report interattivi per i business stakeholder

---

## 1. Panorama generale dell’architettura

```
+----------------------+       +----------------------------+       +------------------------------+
|   Ingestion Layer    |  -->  |   NLP / IE Pipeline        |  -->  |   Knowledge Graph Platform  |
|  (OCR, Conversion)   |       |  (NER, RE, OpenIE, Normal.)|       |  (Ontologia + Triple Store) |
+----------------------+       +----------------------------+       +------------------------------+
           |                                 |                                   |
           v                                 v                                   v
+--------------------------------------------------------------+      +---------------------------+
|       Hybrid Reasoning Layer                                  |      |  Analytics & Reporting    |
|  (Rule Engine, Semantic Similarity, NLI, Graph Queries)      |      |  (Power BI, Looker, etc.) |
+--------------------------------------------------------------+      +---------------------------+
           |                                 |                                   |
           v                                 v                                   v
+----------------------+       +----------------------------+       +------------------------------+
|     Alerting &       |       |   Data Governance /        |       |  User Interface / Portal    |
|   Notification Bus   |       |   Audit Trail & Versioning |       | (Web App, API, Chatbot)     |
+----------------------+       +----------------------------+       +------------------------------+
```

**Perché questa architettura?**

1. **Multi-layer approach**: separa chiaramente ingestione (documenti grezzi), estrazione informazioni, ragionamento ontologico/semantico, e infine reportistica e interfaccia utente.
2. **Scalabilità e manutenibilità**: ogni layer può scalare in cluster (es. più nodi OCR, più istanze di ML, più repliche del triple store).
3. **Plug-and-play fra Azure e Google**: possiamo scegliere il fornitore migliore per ogni sotto‐servizio (es. Document AI vs. Azure Form Recognizer, Vertex AI vs. Azure ML, BigQuery RDF vs. Azure Cosmos DB Graph).
4. **Rise of hybrid reasoning**: combinare ragionamento simbolico (ontologico/regole) e ragionamento statistico (embedding/NLI) per coprire sia le contraddizioni “hard” (regole finanziarie) sia quelle “soft” (sfumature semantiche).

---

## 2. Layer 1: Ingestion Layer

**Obiettivo**: acquisire i documenti in formato PDF, Word, Excel, HTML o immagine, ed elaborarli affinché siano “leggibili” dalla pipeline NLP.

1. **Fonte documentale**

   * Documenti interni (PDF di report, contratti, specifiche tecniche, whitepaper, presentazioni PowerPoint).
   * Documenti esterni (file scaricati, feed RSS, repository S3/Blob Storage, servizi Web).

2. **OCR / Conversion**

   * **Google Document AI** (per PDF scansionati e immagini):

     * Configurare uno o più “Processor” (ad es. “Document OCR v1”, “Form Parser v1”) in base al tipo di documento.
     * Output: JSON strutturato con “pages”, “paragraphs”, “tables”, “visual defects”.
     * Possibilità di pipeline multi‐stage (ad esempio: OCR puro → Form Parser specifico per tabelle contrattuali → classification).
   * **Azure Form Recognizer** + **Cognitive Services Read API**:

     * Confrontare performance su documenti neri/bianco vs. colorati, tipologia di font.
     * Configurazioni avanzate per tabelle e layout complessi (ad es. tabelle annidate in contratti).
   * **Conversione di Word / PPT / HTML**:

     * Per file Office, usare la libreria `python-docx` o `python-pptx` per estrarre testo e tabelle.
     * In alternativa, usare **Azure Cognitive Services Multi‐Page Form Recognizer** anche su file Office.

3. **Staging dei file**

   * Caricare tutto quanto (PDF, immagini, Word) in uno storage scalabile:

     * **Google Cloud Storage (GCS)** o **Azure Blob Storage**.
   * Ogni documentazione va mappata con un `document_id` univoco e un insieme di metadati iniziali (data di pubblicazione, autore, versione, dominio/linea di business).
   * Si tiene traccia del flusso di ingest (log di quando è arrivato il file, chi lo ha inviato, checksum, versione).

4. **Event Bus per l’avvio della pipeline**

   * Ogni file caricato (o ogni batch) pubblica un evento su un bus (ad es. **Google Pub/Sub** o **Azure Event Grid**).
   * Una **Cloud Function** (Google Cloud Functions) o **Azure Function** si attiva sull’evento e monta/trasforma i documenti verso la pipeline NLP.

---

## 3. Layer 2: NLP / IE Pipeline

**Obiettivo**: prendere il testo grezzo (o semi‐strutturato dall’OCR) e trasformarlo in entità, relazioni e “asserzioni” di dominio.

### 3.1 Pre‐processing

1. **Cleaning**:

   * Rimozione di header/footer ripetuti, numeri di pagina, watermark, linguaggio “boilerplate” (ad es. “Confidenziale – Non condividere”).
   * Correzione di encoding, Unicode normalisation, rimozione di caratteri non stampabili.

2. **Line‐segmentation / Paragraph segmentation**:

   * Dal JSON di Document AI (o da Azure Form Recognizer), raggruppare righe in paragrafi basandosi su bbox e coordinate.
   * In caso di pagine multi‐colonna, fare riassemblaggio per “colonna”.

3. **Tokenization e Sentence Splitting** (Language‐dependent):

   * Per la lingua inglese, spaCy (`en_core_web_trf`) o Google Vertex Translation + spaCy per normalizzare la lingua.
   * Per la lingua italiana, spaCy (`it_core_news_lg`) o modelli Flair.
   * Riconoscimento di lingue miste (Italiano/English) con **langdetect** o **fastText**: in pipeline, decidere automaticamente quale modello spaCy applicare per frase.

### 3.2 Named‐Entity Recognition (NER) e Relation Extraction (RE)

1. **NER Generico + NER Domain‐Specific**

   * **NER Generico (open domain)**:

     * Modello spaCy pre‐addestrato per entità di base (DATE, MONEY, ORG, PERSON, etc.).
   * **NER Finanziario Custom**:

     * Usare **Google Vertex AI** per addestrare un modello custom NER (basato su BERT, transformers) con dataset annotato dai domain expert (es. entità come “Ticker Symbol”, “Indice”, “Livello di Rating”, “Leva Finanziaria”, “Quota Banca”, ecc.).
     * Oppure, usare **Azure Custom Named Entity Recognition** (parte dei Language Understanding Intelligenza Artificiale di Azure), annotando frasi di esempio e generando modelli su misura.

2. **Relation Extraction (RE)**

   * Estrarre relazioni chiave per il dominio:

     * “Company A acquista Company B”
     * “Entità X ha rating Y”
     * “ReportTrimestrale Z contiene ricavi pari a R”
   * WP‐OpenIE (tool Python) o **spaCy’s EntityRuler + Dependency Parsing** per disegnare pattern regex e grammatici.
   * **Vertex AI AutoML Natural Language** per RE supervisionato: si forniscono coppie annotate (es. “(Eni, acquista, Saipem)”) e il modello imparare a generalizzare.
   * **Azure Text Analytics for Healthcare** (estremamente efficace su entità specializzate, benché pensato per sanitario) può venire usato per entità complesse e relazioni se ri‐addestrato.

3. **OpenIE / Triple Extraction (Claim Extraction)**

   * Per ogni frase/paragrafo, usare una libreria tipo **Stanford OpenIE** (tramite wrapper Java‐Python) per estrarre triple (Soggetto, Predicato, Oggetto).
   * Se il predicato è “equals” o equivale a un confrontatore (“is”, “was”, “reached”), normalizzare con regole custom:

     ```
     ("Company A", "reported", "€10M revenue")  
     → “CompanyA:hasRevenue:10M”  
     ```
   * Le triple vengono trasformate in “asserzioni” (claims) che popoleranno il KG.

4. **Sentiment & Tone Classification (Opzionale)**

   * Per analizzare il “sentiment” di disclaimers (es. “This report is forward‐looking…”), usare **Azure Text Analytics** o **Vertex AI Sentiment Analysis**.
   * Utile per contestualizzare claim di natura “predittiva” o “pass‐attentive” nei contratti finanziari.

### 3.3 Normalizzazione e Linking a Glossario

1. **Linking delle entità**

   * Ogni entità finanziaria (es. “ENI”, “Eni S.p.A.”, “Eni SpA”) deve venire risolta a un **Unified Entity ID** (ad es. ISIN, CUSIP, o un codice interno).
   * Si usano servizi esterni come **Bloomberg API** o **Refinitiv Entity Database** per normalizzare.
   * Se entità non riconosciute, si creano “stubs” nel KG, da arricchire manualmente (c’è un team di esperti pronti a revisionare).

2. **Lexicon & Ontology Linking**

   * Caricare un ontology finanziaria di riferimento (ad es. **FIBO – Financial Industry Business Ontology**, sviluppata da EDM Council).
   * Mappare le entità estratte nel paragrafo ai concetti FIBO:

     * “Company” → `fibo-fnd-txt-lty-1:LegalEntity`
     * “Revenue” → `fibo-fbc-fct-fse:NetIncome`
     * “Leverage Ratio” → `fibo-fnd-arr-agr:FinancialRatio`
   * Se una nuova entità non è presente, si crea come `skos:Concept` temporaneo in un “KG sandbox” fino a revisione.

---

## 4. Layer 3: Knowledge Graph Platform

**Obiettivo**: immagazzinare tutte le triple RDF (entità, relazioni, asserzioni), le ontologie FIBO, e fornire un endpoint SPARQL/Gremlin per query e inferenza.

### 4.1 Scelta del Triple Store / Graph DB

– **Azure Cosmos DB (API Gremlin)**

* Supporta grafo property, scalabilità globale, integrazione nativa con Azure Functions e Azure Synapse.
* Ottimo per operazioni OLTP veloci, query Gremlin, e integrazione con Power BI tramite connettore.

– **Google Cloud Platform (GCP): Google Cloud BigQuery + RDF support**

* Ultimamente GCP ha esteso BigQuery per supportare dati RDF/SPARQL (BigQuery RDF).
* In alternativa, si può usare **GraphDB by Ontotext** (distribuito su GCP Marketplace) o **Amazon Neptune** su AWS se si preferisce multi-cloud.

– **Virtuoso / Blazegraph** (on-premise o su VM dedicate)

* Se richiedi OWL DL reasoning, Virtuoso con OWL2 RL support è una scelta collaudata.
* Blazegraph ha ottime prestazioni SPARQL e supporto a RDF\* per statement su statement, utile per annotare provenienza/versione.

### 4.2 Ontologia & Modello di dati

1. **Import FIBO (RDF/OWL)**

   * Scarica i moduli FIBO rilevanti (es. `fibo-fbc-fct-fse:FinancialStatement`, `fibo-fnd-acc:AccountingEvent`, `fibo-fnd-plc-PLA:Place`).
   * Carica le ontologie come grafi OWL nel triple store.
   * Assicurati che i prefissi e i nomi delle proprietà siano coerenti (ad es. `fibo-fnd-arr-agr:hasNumericalValue`).

2. **Schema Extension**

   * Estendi FIBO con classi custom se serve:

     * `:Document` su `dcterms:BibliographicResource`
     * `:Paragraph` come `:DocumentPart` con proprietà `:hasText`, `:hasConfidence`
     * `:Claim` come sottoclasse di `fibo-fnd-agr-typ:InformationalContent`
     * `:hasClaim` tra `:DocumentPart` e `:Claim`
   * Associa metadati come `prov:wasGeneratedBy` (es. “estratto da Document AI”), `prov:generatedAtTime`, `prov:wasAttributedTo`.

3. **Popolamento iniziale**

   * Ogni output dell’IE Pipeline (entità estratte, triple OpenIE, entità allineate a FIBO) diventa una serie di triple RDF.
   * Ad esempio, da un claim “Eni reported €10M revenue in Q1 2024”:

     ```
     :Claim_Eni_Q1_2024 rdf:type :Claim ;
         :claimText "Eni reported €10M revenue in Q1 2024" ;
         :refersToEntity :Eni ;
         :refersToMetric :Revenue ;
         :hasValue "10M"^^xsd:decimal ;
         :hasPeriod ":Period_Q1_2024" .
     ```
   * `:Eni rdf:type fibo-fnd-plc-PLA:LegalEntity ; :hasISIN "IT0003132476" .`
   * Ogni triple viene anche arricchita con metadati di “confidence” (es. float 0.92) e provenienza (`prov:wasGeneratedBy :IE_PipelineRun_20250610`).

4. **Gestione versioni e provenienza**

   * Se un claim esiste in più versioni (es. “Eni reported €9M” nel doc A e “Eni reported €10M” nel doc B), si mantengono due archi:

     ```
     :Claim_A_1 fibo-fnd-arr-agr:hasNumericalValue "9"^^xsd:decimal .
     :Claim_B_1 fibo-fnd-arr-agr:hasNumericalValue "10"^^xsd:decimal .
     ```
   * Ogni triple ha proprietà `:versionNumber`, `prov:wasDerivedFrom` (punta alla fonte) ed eventualmente `prov:wasGeneratedBy`.
   * Si possono usare **RDF-star** (triple annidate) per annotare direttamente ogni statement con la sua “confidence”.

---

## 5. Layer 4: Hybrid Reasoning Layer

Qui si fondono due grandi “moteur” di coerenza:

1. **Ragionamento Ontologico e Rule-Based (Symbolic Reasoning)**
2. **Controlli Semantici Soft-Reasoning (NLI, Embedding Similarity)**

### 5.1 Ragionamento Ontologico + Rule Engine

1. **OWL DL / OWL 2 RL Reasoner**

   * Se usi **Virtuoso** o **GraphDB**, puoi attivare un reasoner OWL 2 RL.
   * Vengono generate inferenze “hard” (class membership, property characteristics, consistenza TBox).
   * Esempio: se `:CashFlow rdf:type fibo-fbc-fct-fse:CashFlowStatement`, e `fibo-fbc-fct-fse:hasNetCashFlow` ha come `rdfs:range` `xsd:decimal`, allora un valore stringa “ten million” scatta un errore di tipo.

2. **Rule-Engine Declarative**

   * **Drools** (in esecuzione su Kubernetes) o **Azure Rules Engine** per scrivere regole finanziarie di dominio.
   * Esempi di regole di “contraddizione contabile”:

     * SE `:ReportX :hasPeriod ":Q1_2024"` E `:ReportY :hasPeriod ":Q1_2024"` E `:ReportX :hasEntity :Eni` E `:ReportY :hasEntity :Eni` E `:ReportX :hasRevenue ?r1` E `:ReportY :hasRevenue ?r2` E `?r1 != ?r2` ALLORA `WarningContraddizioneContabile(Eni, Q1_2024, r1, r2)`
     * Regole di “double‐entry accounting” (se un guadagno è esibito come attivo in un report e passivo in un altro).

3. **SPARQL Constraints (SHACL)**

   * Definire **SHACL shapes** per validare proprietà dei nodi del grafo.
   * Esempio di shape:

     ```turtle
     :RevenueShape
         a sh:NodeShape ;
         sh:targetClass fibo-fnd-arr-agr:FinancialMetric ;
         sh:property [
             sh:path fibo-fnd-arr-agr:hasNumericalValue ;
             sh:datatype xsd:decimal ;
             sh:minInclusive 0 ;
         ] ;
         sh:property [
             sh:path :hasPeriod ;
             sh:nodeKind sh:IRI ;
         ] .
     ```
   * Gli strumenti come **TopBraid SHACL** o **GraphDB** permettono di fare validazione batch con le SHACL shapes.

4. **Publishing of Inconsistency Triples**

   * Ogni volta che il reasoner (OWL/DL, Drools, SHACL) trova un pattern incoerente, viene creata una triple del tipo:

     ```
     :Inconsistency_123 a :ContraddictionContabile ;
         :involvesClaim :Claim_A_1 , :Claim_B_1 ;
         :detectedBy :RuleID_RevenueMismatch ;
         :severity "HIGH" .
     ```
   * Il workflow del motivo:

     1. Esegui reasoner su dump RDF (o incremental).
     2. Pubblica i risultati di “Inconsistency” nel grafo (chiamato “KG‐Inconsistency”).
     3. Gli step successivi della pipeline leggeranno queste triple per generare report/alert.

### 5.2 Controlli Semantici Soft (Embedding + NLI)

1. **Embedding dei Testi / Claims**

   * Ogni claim testuale (es. “Eni reported €10M revenue in Q1 2024”) viene trasformato in embedding vettoriale con **Sentence-Transformers** (es. modello `finance‐bert‐sentence‐transformers`).
   * Gli embeddings sono salvati in un sistema di ricerca ANN (es. **FAISS** su GCP o **Azure Cognitive Search vector store**) per query di similarità “nearby”.

2. **Raggruppamento e Clustering di Claim Simili**

   * Ogni claim ottiene un cluster ID: usiamo DBSCAN/K-Means nel vettoriale umano mots.
   * I cluster raccolgono claim simili ma potenzialmente diversi nei numeri (es. “Eni: 10M revenue” vs. “ENI: 10.5M revenue”).

3. **Natural Language Inference (NLI) Fine‐Grained**

   * Su ogni coppia di claim facenti parte dello stesso cluster, eseguiamo **NLI** (es. con modello `roberta-finetuned-on-financialNLI`) per stimare “Entailment vs. Contradiction vs. Neutral”.
   * Se la probabilità di “Contradiction” > soglia (es. 0.9), generiamo un nodo di “Soft Contradiction” in KG:

     ```
     :SoftContradiction_456 a :SoftContradiction ;
         :involvesClaim :Claim_C_3 , :Claim_D_7 ;
         :nliScore "0.92"^^xsd:decimal ;
         :clusterID "cluster_17" .
     ```
   * Questo approccio cattura differenze linguistiche non strettamente catturate da regole rigide (es. “Eni’s net income reached €10M” vs. “Eni’s profit was €12M”, pur contenendo la stessa nozione “profit/net income”).

4. **Query Composite per Incongruenze Cross-Doc**

   * Esempio SPARQL che unisce ragionamento ontologico e soft‐contradictions:

     ```sparql
     PREFIX : <http://example.org/fin#>
     SELECT ?claimA ?claimB ?ruleDetected ?nliScore
     WHERE {
       ?inc a :ContraddictionContabile ;
            :involvesClaim ?claimA , ?claimB ;
            :detectedBy ?ruleDetected .
       OPTIONAL {
         ?softInc a :SoftContradiction ;
                  :involvesClaim ?claimA , ?claimB ;
                  :nliScore ?nliScore .
       }
       FILTER (?nliScore > 0.85)
     }
     ```
   * Questa query restituisce tutte le “hard contradictions” rilevate dalle regole, insieme a eventuali punteggi NLI per “soft contradictions” dello stesso paio di claim.

---

## 6. Layer 5: Analytics & Reporting

**Obiettivo**: esporre i risultati in dashboard interattivi, reportistica schedulata e API per i vari stakeholder (analisti finanziari, compliance, risk management).

### 6.1 Data Warehousing e Integrazione BI

1. **Data Pipeline di ETL/ELT**

   * Estrarre le triple di “Inconsistency” e i metadati (entità coinvolte, periodi, punteggi NLI) dal triple store/contenitore Azure Cosmos DB
   * Caricare in un **Data Warehouse** (es. **BigQuery**, **Azure Synapse Analytics**, o **Azure SQL Data Warehouse**).
   * Normalizzare in tabelle relazionali:

     * `inconsistency_events` (id, tipo (hard/soft), rule\_id, timestamp)
     * `inconsistency_claims` (inconsistency\_id, claimA\_id, claimB\_id, nli\_score, rule\_score)
     * `claims_details` (claim\_id, document\_id, paragraph\_index, text, embedding\_vector (JSON/BLOB), claim\_type)

2. **Power BI / Looker / Tableau**

   * Creare report interattivi:

     * **Mappa delle incongruenze**: heatmap per entità (es. “Eni” vs. altre società), periodi (“Q1\_2024” vs. “Q2\_2024”), tipologia di regola infranta.
     * **Timeline di contraddizioni**: grafico a linee che mostra il numero di “hard contradictions” e “soft contradictions” nel tempo (aggiornato settimanalmente/mensilmente).
     * **Analisi drill-down**: click su una singola entità → elenco documenti coinvolti → click su un documento → visualizzazione del testo originale e del claim.

3. **Alerting e Notification**

   * Configurare **Azure Logic Apps** o **Google Cloud Functions** per monitorare il Data Warehouse:

     * Se il numero di “Hard Contradictions” supera una soglia (p.es. >10 in un giorno), inviare email a compliance.
     * Se una nuova contraddizione coinvolge una entità “High Priority” (es. “Già segnalata da controllo contabile precedente”), inviare messaggio Slack ai team finance.
   * Possibilità di **Push Notification** su dispositivi mobile (tramite Azure Notification Hubs, FCM).

---

## 7. Layer 6: Alerting & Notification Bus

**Obiettivo**: orchestrare notifiche in tempo reale/cadenza schedule per problemi di coerenza.

1. **Event Bus / Message Queue**

   * Ogni volta che il reasoner scrive una triple di tipo `:ContraddictionContabile` o `:SoftContradiction`, viene emesso un evento su:

     * **Azure Event Grid**
     * **Google Pub/Sub**
   * Questi eventi vengono intercettati da:

     * **Azure Function** o **Cloud Function** che filtra per gravità e tipo di regola
     * **Webhook** verso sistemi di ticketing (ServiceNow, Jira) per creare request di “fact‐checking”

2. **Regole di Notifica**

   * **Hard Contradiction High Severity** → Email/Slack immediato a Team Lead
   * **Soft Contradiction Media/Alta** → Daily Digest su Teams/Slack
   * **Contradiction su Entità ad alto impatto (es. Top10 Market Cap)** → SMS/Push Notification

3. **Dashboard Operativa**

   * Creare una pagina nel Portale interno (React/Vue) che mostri:

     * Grafico dei nodi del KG attorno all’entità selezionata (usando **D3.js** + endpoint SPARQL)
     * Lista degli eventi di coerenza non ancora “risolti” (flagged)
     * Pulsante “Mark as Reviewed” per ogni inconsistency, integrato con DB di metadata
   * Il portale può interrogare un’API in **FastAPI**/Node.js che legge dal triple store e restituisce i JSON per la UI.

---

## 8. Layer 7: Data Governance, Provenance e Audit Trail

**Obiettivo**: mantenere tracciabilità completa di tutte le trasformazioni, delle versioni dei documenti e delle revisioni delle regole.

1. **Provenance con PROV-O**

   * Ogni entità nel KG (anche i claim generati da NLP) ha proprietà PROV:

     * `prov:wasGeneratedBy :PipelineRun_20250610`
     * `prov:generatedAtTime "2025-06-10T12:34:56Z"`
     * `prov:wasDerivedFrom :DocumentRaw_123`
   * Le triple di inconsistency contengono a loro volta indici verso i claim “parent”.

2. **Versioning dei Documenti**

   * Se un documento viene aggiornato (es. nuovo report trimestrale in sostituzione di un precedente), si crea un nuovo nodo `:Document_V2` collegato da `prov:wasRevisionOf :Document_V1`.
   * Questo stratagemma consente di eseguire controlli di coerenza fra versioni diverse (il KG conserva entrambe).

3. **Audit Trail Regole**

   * Ogni regola di Drools o SHACL ha un identificativo univoco e una versione.
   * Ad ogni esecuzione di rule engine si salva un “rule run ID” collegato a data/ora, versione delle regole, versione dell’ontologia, e risultati.
   * In un eventuale contenzioso o controllo di compliance, è possibile ricostruire esattamente quale regola (e quale versione) ha generato un certo warning.

---

## 9. Flusso di Lavoro End-to-End (Step by Step)

1. **Upload/Ingest**

   * Un utente carica un PDF in **Azure Blob Storage** (o GCS).
   * Scatta un evento su **Event Grid / Pub/Sub**.
   * Azione di **Function**: recupera il blob e invia richiesta a **Google Document AI** (o Azure Form Recognizer).

2. **NLP Pipeline**

   * La risposta JSON di Document AI (con paragrafi, tabelle) viene salvata temporaneamente in **Cloud Storage**.
   * Una pipeline orchestrata (Apache Airflow o Cloud Composer) passa il JSON a un microservizio di **NER/RE** (Docker container su GKE/AKS).
   * Il microservizio NER/RE (custom model su Vertex AI) produce un elenco di entità e relazioni annotate.
   * Un altro componente (microservizio) richiama **Stanford OpenIE** per estrarre triple e normalizzarle secondo la ontologia FIBO.

3. **KG Load & Enrichment**

   * Tutte le triple (entità, relazioni, claim) vengono trasformate in RDF (TTL) e caricate in batch nel Triple Store (es. Virtuoso o Cosmos DB Gremlin).
   * Parallelamente, si esegue un processo di Alignment:

     * “Entity Linking” verso database Refinitiv/Bloomberg per ottenere codici univoci.
     * Collegamenti a risorse esterne (Linked Open Data – DBpedia, Wikidata) per arricchire i metadati.

4. **Reasoning & Contradiction Detection**

   * Trigger periodico (ad esempio ogni notte) o on‐demand: si esegue il **Reasoning OWL 2 RL + Drools + SHACL** sul grafo aggiornato.
   * Per le “soft contradictions”, si genera un lotto di query SPARQL per selezionare coppie di claim simili (cluster) → queste coppie vengono inviate a un cluster di GPU su **Vertex AI Endpoint** per NLI.
   * Tutti i risultati (hard/soft) vengono salvati nel grafo come nodi di tipo `:InconsistencyEvent`.

5. **Analytics & Notification**

   * Una funzione cloud “DataMover” estrae le inconsistency daily e popola il Data Warehouse.
   * Le dashboard BI (Power BI su Azure Synapse) vengono aggiornate automaticamente.
   * I flussi di alert (Logic Apps, Functions) inviano notifiche in base a priorità/regole personalizzate.

6. **Interfaccia Utente / Portal**

   * Gli utenti (analisti, compliance) utilizzano un portale Web (React + FastAPI) per:

     * Visualizzare elenco di inconsistency aperte (paginate, filtri per entità, data, severity).
     * Vedere il dettaglio di ogni inconsistency, con testo estratto, link al documento originale (salvato in storage), punteggio NLI e regola infranta.
     * Marcare come “Reviewed/Fixed” (questa azione aggiorna il grafo con `:status "RESOLVED"` e `prov:wasRevokedBy user123`).

---

## 10. Tecnologie Specifiche Azure vs. Google

| Funzionalità               | Azure                                                         | Google                                                                 |
| -------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Storage documenti          | Azure Blob Storage                                            | Google Cloud Storage (GCS)                                             |
| Event Bus / Messaging      | Azure Event Grid / Service Bus                                | Google Pub/Sub                                                         |
| OCR e Layout Parsing       | Azure Form Recognizer / Cognitive Services Read API           | Google Document AI (Document OCR, Form Parser)                         |
| NER / RE Custom            | Azure Cognitive Search + Custom NER (Language Service)        | Google Vertex AI AutoML Natural Language                               |
| Embedding & NLI            | Azure Machine Learning (modelli ONNX o Transformers su GPU)   | Google Vertex AI (Fine‐tuning BERT/MNLI)                               |
| Triple Store / Graph DB    | Azure Cosmos DB (API Gremlin) o Azure Synapse RDF + Lakehouse | GraphDB su GCP Marketplace o BigQuery RDF Extensions                   |
| Reasoner OWL / SHACL       | Blazegraph/Drools su VM Kubernetes                            | Virtuoso / GraphDB su GKE                                              |
| Rule Engine                | Azure Rules Engine (parte di Logic Apps) o Drools on AKS      | Drools su GKE oppure Google Cloud Workflows + rego (Open Policy Agent) |
| Data Warehouse / BI        | Azure Synapse Analytics + Power BI                            | BigQuery + Looker (o Data Studio)                                      |
| Monitoring & Alerting      | Azure Monitor / Log Analytics + Azure Functions Alerts        | Cloud Monitoring + Cloud Functions Alerts                              |
| Deployment & Orchestration | AKS + Azure DevOps CI/CD                                      | GKE + Cloud Build / Cloud Run CI/CD                                    |
| Logging & Observability    | Azure Application Insights                                    | Google Cloud Logging + Trace                                           |

---

## 11. Ruoli e Team Coinvolti

Per un progetto di questo livello, considera di organizzare i seguenti ruoli/skill:

1. **Data Engineers**

   * Progettano pipeline di ingest (ETL/ELT), data lake, orchestrazione Airflow/Composer, definizione di workflow su Event Grid/Pub-Sub.

2. **NLP Engineers / ML Engineers**

   * Addestrano e mantengono modelli NER/RE custom (Vertex AI AutoML o Azure Custom NER).
   * Sviluppano microservizi di estrazione triple (OpenIE wrapper), embedding (Sentence-Transformers), NLI (roberta/DeBERTa).

3. **Knowledge Engineers / Ontologists**

   * Definiscono/estendono l’ontologia finanziaria (FIBO), creano SHACL shapes, gestiscono versioni dell’ontologia.
   * Mappano entità a codici univoci (ISIN, Bloomberg, CIK).

4. **Backend Developers / DevOps**

   * Sviluppano microservizi (Docker, Kubernetes), configurano CI/CD (Azure DevOps/GitHub Actions), gestiscono la scalabilità (AKS/GKE).
   * Si occupano di disponibilità, failover, cost profiling, backup/restore del triple store e del data warehouse.

5. **Data Analysts / Business Stakeholders**

   * Definiscono le regole di dominio finanzario (“Se due report trimestrali di Eni mostrano ricavi diversi per lo stesso periodo, segnala incongruenza di tipo ‘Revenue Mismatch’”).
   * Annotano esempi per training NER/RE e creano ground‐truth per calibratura soglie NLI.
   * Progettano reportistica e dashboard (Power BI, Looker).

6. **Security / Compliance Officers**

   * Definiscono policy di accesso (chi può vedere inconsistency di “High Severity”).
   * Audiscono i log di provenienza (PROV), assicurano GDPR, SOX compliance nelle informazioni finanziarie.

---

## 12. Vantaggi e Punti Critici

### 12.1 Vantaggi

* **Copertura Completa**: unisce ragionamento simbolico (ontologie, regole) e statistico (embedding, NLI).
* **Alta Precisione**: regole finanziarie scritte da esperti + modelli NLI finemente tarati riducono falsi positivi.
* **Tracciabilità Totale**: ogni claim, ogni inconsistenza, ogni regola ha un audit trail completo (PROV).
* **Scalabilità Orizzontale**: ogni componente (OCR, ML, triple store, data warehouse) può scalare indipendentemente.
* **Flessibilità Multi-Cloud**: se un servizio Google non soddisfa, si può spostare su Azure o viceversa senza riscrivere la logica di business (grazie agli adapter).
* **Revisione Umana Integrata**: possibilità di gestire un workflow “semi‐automatico” dove ogni inconsistenza viene eventualmente approvata/rigettata da analisti.

### 12.2 Punti Critici / Sfide

1. **Cost & Complexity**

   * Gestire un’architettura così ibrida comporta costi di licenze, infrastruttura, licenze Vertex AI/Google Document AI e costi di Azure.
   * Il team dev’essere ben organizzato: Data Engineers, NLP Engineers, Ontologists, DevOps, tutti devono collaborare strettamente.

2. **Qualità dei Dati e Ontologia**

   * Definire un’ontologia finanziaria robusta (FIBO) e mantenere la coerenza tra i dataset è complesso.
   * Gli esperti di dominio (CFO, financial controllers) devono validare continuamente l’ontologia e le regole, aggiungendo revisioni e modifiche.

3. **Performance del Reasoning**

   * Eseguire OWL 2 DL completo su grandi triple store può diventare lento; probabilmente si rimarrà su OWL 2 RL / SHACL (subset più efficiente).
   * I controlli NLI su milioni di coppie di claim richiedono GPU cluster e batching intelligente (filtro preliminare con ANN).

4. **Manutenzione & Versioning**

   * Ogni volta che aggiorni i modelli NER/RE o le regole, serve test di regressione per assicurarsi di non generare nuovi falsi positivi/negativi.
   * La gestione delle versioni del KG, dei modelli e delle regole dev’essere centralizzata (per evitare conflitti tra team).

5. **Security & Privacy**

   * Controllo di accesso granulare su chi può leggere/annotare inconsistenze (RBAC).
   * Crittografia dei dati a riposo (Azure/Vault, GCP KMS) e in transito (TLS).
   * Possibile necessità di mascherare dati sensibili (ESG, ESG metrics) esposti nei report.

---

## 13. Roadmap di Implementazione

1. **Fase 0 – Preparazione e Kickoff (1–2 settimane)**

   * Reclutare team interfunzionali (Data Engineers, NLP Engineers, Ontologists, DevOps).
   * Definire casi d’uso primari di contraddizione (es. contraddizione contabile di ricavi, asset, pas­sività).
   * Scegliere i dataset iniziali (es. 50 documenti finanziari storici, estratti di bilanci).
   * Setup preliminare delle risorse cloud (GCP + Azure subscription, ruoli IAM).

2. **Fase 1 – Prototipo rapido NLI‐based (2–3 settimane)**

   * Replica del prototipo NLI in Python descritto prima, per validare quantità di “soft contradictions”.
   * Labeling manuale di \~500 coppie “contradictive vs. non-contradictive” per tarare soglia.
   * Benchmarking modelli NLI (BERT‐MNLI, DeBERTa, finetuned su dominio).

3. **Fase 2 – Ontologia + Popolamento KG (4–6 settimane)**

   * Selezionare subset FIBO rilevante (entità contabili, misure finanziarie, eventi societari).
   * Progettare modelli di dati RDF per `:Document`, `:Claim`, `:Entity`, `:Metric`, `:Period`.
   * Creare script di caricamento RDF (TTL) nel triple store (Virtuoso o Cosmos DB).
   * Realizzare almeno 10 regole Drools / SHACL per inconsistenze hard.

4. **Fase 3 – Integrazione OCR + IE Pipeline (4–6 settimane)**

   * Configurare Google Document AI + Azure Form Recognizer per estrarre testi e tabelle.
   * Sviluppare microservizio NER/RE (Vertex AI custom) e wrapper OpenIE.
   * Caricare output IE nel triple store, verificare mapping e provenance.

5. **Fase 4 – Hybrid Reasoning & Inconsistency Engine (6–8 settimane)**

   * Sviluppare microservizio di ragionamento (Drools + SHACL + SPARQL).
   * Configurare cluster GPU / Vertex AI Endpoint per NLI cross‐claim.
   * Test di performance: quanti claim/giorno, latenza, costi.
   * Salvare risultati inconsistency come triple nel grafo, revisionare con esperti.

6. **Fase 5 – Analytics & Reporting (4 settimane)**

   * Progettare Data Warehouse schema, pipeline ETL in BigQuery/Synapse.
   * Realizzare dashboard pilota in Power BI / Looker.
   * Configurare logiche di alert (Logic Apps, Cloud Functions).

7. **Fase 6 – User Portal & Governance (6 settimane)**

   * Sviluppare portale Web (React + FastAPI) per gestione inconsistency (review, comment, resolve).
   * Implementare RBAC e crittografia.
   * Mettere in piedi pipeline di CI/CD, rollback plan, backup/restore, disaster recovery.

8. **Fase 7 – Scalabilità & Ottimizzazione (continua)**

   * Ottimizzare query SPARQL/Gremlin, shard del triple store.
   * Ottimizzare pipeline di NLI (filtro ANN, batching).
   * Addestrare modelli NER/RE e NLI iterativamente con più dati annotati.
   * Test di carico, tuning costi, ottimizzazione spot instances / preemptible VMs.

---

## 14. Conclusione

Con risorse illimitate a disposizione, il design proposto unisce:

* **Symbolic AI** (Ontologie FIBO, SHACL, OWL reasoning, Rule‐Based Drools) per garantire coerenze finanziarie “rigide” e trasparenti
* **Statistical AI / NLP** (NER custom, OpenIE, Embeddings, NLI) per catturare sfumature semantiche e contraddizioni “soft” che non emergerebbero da regole rigide
* **Integrazione multi‐cloud** (Azure e Google) per sfruttare il meglio di entrambi i provider in ambito OCR, ML, dati e BI
* **Governance & Provenance** per mantenere tracciabilità, versioning e compliance anche a scopi legali/contabili

Questo approccio ti permette di:

1. Identificare automaticamente **contraddizioni contabili** e **incongruenze di linguaggio** in un vasto corpus di documenti finanziari
2. Fornire **dashboard interattivi** ai CFO, ai team di audit e compliance, ai business analyst
3. Mantenere un **audit trail completo**, con versioni di documenti/regole/motori, per soddisfare requisiti regolatori (ad es. SOX, IFRS)
4. Adattare e scalare la soluzione a migliaia di documenti mensili, aggiungere nuovi domini (es. ESG, Risk Management) semplicemente estendendo l’ontologia

In sintesi, stiamo parlando di un vero e proprio “Financial Consistency Engine” enterprise, capace di gestire sia le contraddizioni “hard” (numeri che non quadrano, clausole contrattuali incompatibili) sia quelle “soft” (sfumature di linguaggio che rivelano incongruenze di significato). Se desideri ulteriori dettagli su uno specifico componente (per es. come scrivere regole Drools per casi contabili particolari, o come ottimizzare query SPARQL con Virtuoso/GraphDB), fammi sapere e approfondiamo!
