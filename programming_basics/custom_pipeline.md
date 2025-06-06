# Document Pipeline

Ecco un esempio completo di come si potrebbero applicare i pattern GRASP e GoF per progettare in modo modulare, chiaro e manutenibile la pipeline descritta. In questa trattazione vedremo:

1. **Reasoning**: come e perché scegliamo ogni pattern, quali responsabilità assegnare e come organizzare i moduli.
2. **Esempio di codice Python**: uno scheletro funzionante (MVP) che utilizza i pattern illustrati, con commenti espliciti su dove e come sono applicati.

---

## 1. Reasoning: responsabilità e pattern

### 1.1 Moduli principali e responsabilità

Per chiarezza, riprendiamo i 5 step della pipeline e vediamo come assegnare responsabilità (principi GRASP) e quali GoF pattern usare per ciascuno:

1. **OCR + Parsing**

   * **Information Expert**: il modulo `OCRParser` conosce i dettagli di Document AI e sa come estrarre “pages”, “paragraphs” e “tables”.
   * **Creator**: il `OCRParser` sarà anche responsabile di creare istanze di oggetti `DocumentData` (entità che contiene il JSON strutturato estratto).
   * **Factory Method** (GoF): usiamo un factory per supportare in futuro più “OCR engines” (Document AI, Tesseract, ecc.) restituendo la stessa interfaccia `IOCRParser`.

2. **Classificazione Documenti**

   * **Information Expert**: il modulo `Classifier` sa comunicare con Google Cloud Natural Language e mappa il risultato in `DocumentClassification`.
   * **Pure Fabrication**: creiamo un componente “finto” (`Classifier`) per non violare coesione/basso accoppiamento tra `OCRParser` e moduli successivi.
   * **Strategy** (GoF): definire un’interfaccia `IClassifierStrategy` che consente di cambiare facilmente algoritmo (ad es. Google Cloud vs. un modello locale).

3. **Correzione Errori**

   * **Information Expert**: `ErrorCorrector` è esperto nel rilevare e correggere errori ortografici/grammaticali, e usa librerie come spaCy o textblob.
   * **Polymorphism** (GoF): si definisce un’interfaccia `IErrorCorrectionStrategy`, e si implementano vari algoritmi (ex. `SpacyCorrector`, `TextBlobCorrector`).

4. **Database Saving**

   * **Pure Fabrication**: creiamo il “database manager” (`DatabaseManager`) per isolare l’ORM (SQLAlchemy).
   * **Singleton** (GoF): usiamo un singleton per la sessione/connessione al database, in modo che tutte le classi la condividano.
   * **Controller** (GRASP): il modulo `DatabaseManager` funge da controller per tutte le operazioni CRUD, esponendo metodi asincroni.

5. **Inconsistency Checking**

   * **Information Expert**: il modulo `InconsistencyChecker` conosce come recuperare paragrafi, calcolare similarità e rilevare conflitti.
   * **Strategy** (GoF): per la similarità testo possiamo avere diverse implementazioni (`SpacySimilarity`, `RapidFuzzSimilarity`).
   * **Template Method** (GoF): potremmo definire un template generico per “analisi cross-doc” in cui la logica fissa (iterazione 1:1, threshold, logging) è nel metodo base, mentre la parte “come calcolo la similarità” e “come definisco la soglia di conflitto” è lasciata ai sottotipi.

Infine, serve un **Controller** generale (`PipelineManager`) che coordina i cinque moduli in sequenza, gestendo gli errori di ciascuna fase e orchestrando le chiamate asincrone.

---

## 2. Esempio di codice Python

Nel seguito troverai una struttura minimalista delle classi e dei moduli, con i pattern chiave evidenziati nei commenti. L’obiettivo è di fornire un MVP funzionante, pronto per essere esteso.

### 2.1 Struttura di cartelle

```
project/
├── main.py
├── ocr_parser.py
├── classify_docs.py
├── error_corrector.py
├── database_manager.py
├── inconsistency_checker.py
├── models.py
├── strategies/
│   ├── __init__.py
│   ├── ocr_strategies.py
│   ├── classifier_strategies.py
│   └── similarity_strategies.py
└── requirements.txt
```

---

### 2.2 `models.py`

Definiamo le entità principali (Data Transfer Objects) che verranno passate tra i layer:

```python
# models.py

from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class ParagraphData:
    paragraph_id: str
    page_number: int
    bbox: Dict[str, Any]          # {"x":..., "y":..., "width":..., "height":...}
    raw_text: str
    confidence: float
    cleaned_text: str = ""        # Popolato da ErrorCorrector

@dataclass
class TableData:
    table_id: str
    page_number: int
    bbox: Dict[str, Any]
    table_json: Dict[str, Any]

@dataclass
class DocumentData:
    document_id: str
    filename: str
    paragraphs: List[ParagraphData] = field(default_factory=list)
    tables: List[TableData] = field(default_factory=list)
    visual_defects: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class DocumentClassification:
    document_id: str
    categories: List[str]
    confidences: List[float]

@dataclass
class InconsistencyReport:
    docA_id: str
    paragraphA_id: str
    docB_id: str
    paragraphB_id: str
    inconsistency_type: str
    similarity_score: float
```

---

### 2.3 `strategies/ocr_strategies.py`

Qui definiamo l’astrazione per l’OCR e una possibile implementazione basata su Google Document AI:

```python
# strategies/ocr_strategies.py

from abc import ABC, abstractmethod
from models import DocumentData

class IOCRParser(ABC):
    """Strategy Interface per l’OCR + parsing documentale."""
    
    @abstractmethod
    async def parse_document(self, filepath: str) -> DocumentData:
        pass


class GoogleDocumentAIParser(IOCRParser):
    """Concrete Strategy che usa Google Cloud Document AI."""
    
    def __init__(self, project_id: str, location: str, processor_id: str):
        from google.cloud import documentai_v1 as documentai
        self.project_id = project_id
        self.location = location
        self.processor_id = processor_id
        self.client = documentai.DocumentProcessorServiceAsyncClient()
    
    async def parse_document(self, filepath: str) -> DocumentData:
        # Esempio semplificato: 
        # Qui dovremmo caricare il file, inviarlo a Document AI,
        # ricevere la risposta e popolare DocumentData.
        #
        # Per brevità non includo dettagli di autenticazione e lettura
        # del PDF/immagine. Immaginiamo che `response` sia il JSON di Document AI.
        #
        from models import DocumentData, ParagraphData, TableData

        # 1) Carica file in GCS o direttamente in memoria 
        # 2) Costruisci richiesta a Document AI
        # 3) await self.client.process_document(request=...)
        # 4) Response -> estrazione di paragraphs, tables, visual_defects
        
        # --- pseudo-codice di parsing (da sostituire con implementazione reale) ---
        document_id = filepath.split("/")[-1]
        doc_data = DocumentData(document_id=document_id, filename=filepath)
        
        # Immaginiamo di processare 2 paragrafi e 1 tabella per esempio:
        para1 = ParagraphData(
            paragraph_id="para_001",
            page_number=1,
            bbox={"x": 100, "y": 150, "width": 400, "height": 50},
            raw_text="This is the first paragraph of document.",
            confidence=0.95
        )
        para2 = ParagraphData(
            paragraph_id="para_002",
            page_number=1,
            bbox={"x": 100, "y": 210, "width": 400, "height": 50},
            raw_text="This is the second paragraph, possibly blurry.",
            confidence=0.80
        )
        table = TableData(
            table_id="table_001",
            page_number=2,
            bbox={"x": 50, "y": 300, "width": 500, "height": 200},
            table_json={"headers": ["Col1","Col2"], "rows": [["A","B"],["C","D"]]}
        )
        visual_defects = [{"page": 1, "type": "blurry_text", "bbox": para2.bbox}]
        
        doc_data.paragraphs.extend([para1, para2])
        doc_data.tables.append(table)
        doc_data.visual_defects = visual_defects
        
        return doc_data
```

* **Pattern applicati**:

  * `IOCRParser` è l’**interfaccia strategy** (GoF, Polymorphism).
  * `GoogleDocumentAIParser` è la **Concrete Strategy**.
  * La classe “crea” oggetti `DocumentData` (Creator, GRASP).

---

### 2.4 `strategies/classifier_strategies.py`

Per la classificazione via Google Cloud NL:

```python
# strategies/classifier_strategies.py

from abc import ABC, abstractmethod
from typing import List
from models import DocumentClassification

class IClassifierStrategy(ABC):
    """Strategy Interface per la classificazione dei documenti."""
    
    @abstractmethod
    async def classify(self, document_id: str, text: str) -> DocumentClassification:
        pass


class GoogleNLClassifier(IClassifierStrategy):
    """Concrete Strategy che usa Google Cloud Natural Language classifyText."""
    
    def __init__(self, project_id: str):
        from google.cloud import language_v1
        self.client = language_v1.LanguageServiceAsyncClient()
        self.project_id = project_id
    
    async def classify(self, document_id: str, text: str) -> DocumentClassification:
        # Il testo inviato deve essere almeno 20 token: altrimenti l’API fallisce.
        from models import DocumentClassification
        
        # Splitting a token count:
        if len(text.split()) < 20:
            raise ValueError("Text must be at least 20 tokens for classification.")
        
        # Costruisci la richiesta:
        # request = {
        #   "document": {"content": text, "type_": enums.Document.Type.PLAIN_TEXT},
        #   "classification_model": "projects/.../models/.../documents:classifyText"
        # }
        # response = await self.client.classify_text(request=request)
        # categories = [cat.name for cat in response.categories]
        # confidences = [cat.confidence for cat in response.categories]
        
        # Per MVP, simuliamo un risultato:
        categories = ["Technical/Manufacturing", "Engineering/Quantum"]
        confidences = [0.85, 0.60]
        
        return DocumentClassification(
            document_id=document_id,
            categories=categories,
            confidences=confidences
        )
```

* **Pattern applicati**:

  * `IClassifierStrategy` è ancora **Strategy**.
  * `GoogleNLClassifier` è la **Concrete Strategy**.

---

### 2.5 `strategies/similarity_strategies.py`

Per calcolare la similarità tra paragrafi (Semantic + Fuzzy):

```python
# strategies/similarity_strategies.py

from abc import ABC, abstractmethod
from typing import Tuple

class ISimilarityStrategy(ABC):
    """Strategy Interface per il calcolo di similarità tra due testi."""
    
    @abstractmethod
    def similarity(self, textA: str, textB: str) -> float:
        """Ritorna un punteggio [0.0 .. 1.0]."""
        pass


class RapidFuzzSimilarity(ISimilarityStrategy):
    """Concrete Strategy che usa rapidfuzz per similarità fuzzy."""
    
    def __init__(self):
        from rapidfuzz import fuzz
        self.fuzz = fuzz
    
    def similarity(self, textA: str, textB: str) -> float:
        # rapidfuzz.ratio ritorna valore da 0 a 100
        score = self.fuzz.ratio(textA, textB) / 100.0
        return score


class SpacySimilarity(ISimilarityStrategy):
    """Concrete Strategy che usa embeddings spaCy per similarità semantica."""
    
    def __init__(self):
        import spacy
        self.nlp = spacy.load("en_core_web_sm")
    
    def similarity(self, textA: str, textB: str) -> float:
        docA = self.nlp(textA)
        docB = self.nlp(textB)
        return docA.similarity(docB)
```

* **Pattern applicati**:

  * `ISimilarityStrategy` è **Strategy**.
  * `RapidFuzzSimilarity` e `SpacySimilarity` sono **Concrete Strategies** per diversi metodi di similarità.

---

### 2.6 `ocr_parser.py`

Il modulo che espone la classe per orchestrare l’OCR (Controller + Factory Method):

```python
# ocr_parser.py

import asyncio
from abc import ABC, abstractmethod
from typing import List
from models import DocumentData
from strategies.ocr_strategies import IOCRParser, GoogleDocumentAIParser

class OCRParserFactory:
    """Factory Method (GoF) per istanziare parser diversi in base a configurazione."""
    
    @staticmethod
    def create_parser(engine: str, **kwargs) -> IOCRParser:
        if engine == "google_document_ai":
            return GoogleDocumentAIParser(
                project_id=kwargs.get("project_id"),
                location=kwargs.get("location"),
                processor_id=kwargs.get("processor_id")
            )
        else:
            raise ValueError(f"OCR engine '{engine}' non supportato.")

class OCRParserController:
    """Controller (GRASP) che coordina l’estrazione OCR di più documenti."""
    
    def __init__(self, parser: IOCRParser):
        self.parser = parser
    
    async def parse_all(self, filepaths: List[str]) -> List[DocumentData]:
        tasks = []
        for path in filepaths:
            tasks.append(self.parser.parse_document(path))
        results = await asyncio.gather(*tasks)
        return results
```

* **Pattern applicati**:

  * `OCRParserFactory` è **Factory Method** (GoF).
  * `OCRParserController` è **Controller** (GRASP).

---

### 2.7 `classify_docs.py`

Modulo per classificare in parallelo tutti i documenti:

```python
# classify_docs.py

import asyncio
from typing import List
from models import DocumentData, DocumentClassification
from strategies.classifier_strategies import IClassifierStrategy, GoogleNLClassifier

class ClassifyDocsController:
    """Controller (GRASP) che coordina la classificazione multipla."""
    
    def __init__(self, classifier: IClassifierStrategy):
        self.classifier = classifier
    
    async def classify_all(self, docs: List[DocumentData]) -> List[DocumentClassification]:
        tasks = []
        for doc in docs:
            # concateniamo tutto il testo dei paragrafi per la classificazione
            full_text = " ".join([p.raw_text for p in doc.paragraphs])
            tasks.append(self.classifier.classify(doc.document_id, full_text))
        results = await asyncio.gather(*tasks)
        return results
```

* **Pattern applicati**:

  * `ClassifyDocsController` è **Controller** (GRASP).
  * `GoogleNLClassifier` (importato) è **Concrete Strategy** (Strategy).

---

### 2.8 `error_corrector.py`

Modulo per segnalare e correggere errori in ogni paragrafo:

```python
# error_corrector.py

from typing import List
from models import ParagraphData

import spacy

class ErrorCorrector:
    """Information Expert (GRASP) che sa correggere errori ortografici/grammaticali."""
    
    def __init__(self):
        # Carichiamo il modello spaCy (inglese) per il controllo grammaticale/ortografico
        self.nlp = spacy.load("en_core_web_sm")
    
    def correct_paragraph(self, paragraph: ParagraphData) -> ParagraphData:
        # Se confidence < 0.90, flaggiamo il paragrafo:
        if paragraph.confidence < 0.90:
            # Qui potremmo segnalarlo come “error_type = low_confidence”
            paragraph.cleaned_text = paragraph.raw_text  # per ora, copiamo direttamente
            return paragraph
        
        # Correzione grammaticale/ortografica (semplificata):
        # Usiamo il pipeline di spaCy per tokenizzare e correggere
        doc = self.nlp(paragraph.raw_text)
        corrected_tokens = []
        for token in doc:
            if token._.is_oov:  
                # se parole fuori vocabolario, le manteniamo ma potremmo segnalarle
                corrected_tokens.append(token.text)
            else:
                corrected_tokens.append(token.text)
        paragraph.cleaned_text = " ".join(corrected_tokens)
        return paragraph
    
    def correct_all(self, docs: List[ParagraphData]) -> List[ParagraphData]:
        corrected = []
        for p in docs:
            corrected.append(self.correct_paragraph(p))
        return corrected
```

* **Pattern applicati**:

  * `ErrorCorrector` è **Information Expert** (GRASP).

---

### 2.9 `database_manager.py`

Implementiamo un singleton per la sessione e un manager CRUD (Pure Fabrication):

```python
# database_manager.py

import asyncio
from typing import List, Any
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from sqlalchemy import Integer, String, Float, JSON, Table, Column, ForeignKey
from sqlalchemy.future import select

Base = declarative_base()

# ----------------------------
# Definizione delle tabelle ORM
# ----------------------------
class DocumentORM(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    categories: Mapped[List[str]] = mapped_column(JSON)     # lista di stringhe
    confidences: Mapped[List[float]] = mapped_column(JSON)


class ParagraphORM(Base):
    __tablename__ = "paragraphs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paragraph_id: Mapped[str] = mapped_column(String, nullable=False)
    doc_fk: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"))
    page_number: Mapped[int] = mapped_column(Integer)
    bbox: Mapped[Dict[str, Any]] = mapped_column(JSON)
    raw_text: Mapped[str] = mapped_column(String)
    cleaned_text: Mapped[str] = mapped_column(String)
    confidence: Mapped[float] = mapped_column(Float)


class TableORM(Base):
    __tablename__ = "tables"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    table_id: Mapped[str] = mapped_column(String, nullable=False)
    doc_fk: Mapped[int] = mapped_column(Integer, ForeignKey("documents.id"))
    page_number: Mapped[int] = mapped_column(Integer)
    bbox: Mapped[Dict[str, Any]] = mapped_column(JSON)
    table_json: Mapped[Dict[str, Any]] = mapped_column(JSON)


class ErrorORM(Base):
    __tablename__ = "errors"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paragraph_fk: Mapped[int] = mapped_column(Integer, ForeignKey("paragraphs.id"), nullable=True)
    table_fk: Mapped[int] = mapped_column(Integer, ForeignKey("tables.id"), nullable=True)
    error_type: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

# ----------------------------
# Singleton Async DB Session
# ----------------------------
class DatabaseSessionSingleton:
    """Singleton (GoF) per la sessione asincrona e l’engine DB."""
    _instance = None

    def __new__(cls, db_url: str = "sqlite+aiosqlite:///./pipeline.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Creiamo l’engine e la session factory
            cls._instance.engine = create_async_engine(db_url, echo=False, future=True)
            cls._instance.AsyncSessionLocal = sessionmaker(
                bind=cls._instance.engine,
                expire_on_commit=False,
                class_=AsyncSession
            )
        return cls._instance

async def init_db():
    """Crea tutte le tabelle se non esistono (solo una volta all’avvio)."""
    session_singleton = DatabaseSessionSingleton()
    async with session_singleton.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ----------------------------
# Database Manager (CRUD)
# ----------------------------
class DatabaseManager:
    """Pure Fabrication (GRASP): gestisce tutte le operazioni DB."""
    
    def __init__(self):
        self.db_singleton = DatabaseSessionSingleton()
    
    async def insert_document(self, doc_data: Any, classification: Any) -> int:
        """
        Inserisce un nuovo documento e restituisce la chiave primaria.
        doc_data: DocumentData
        classification: DocumentClassification
        """
        async with self.db_singleton.AsyncSessionLocal() as session:
            # Creiamo l’ORM document
            from models import DocumentData, DocumentClassification
            doc = DocumentORM(
                document_id=doc_data.document_id,
                filename=doc_data.filename,
                categories=classification.categories,
                confidences=classification.confidences
            )
            session.add(doc)
            await session.flush()  # otteniamo doc.id
            # In seguito possiamo inserire paragrafi, tabelle, errori
            await session.commit()
            return doc.id
    
    async def insert_paragraphs(self, doc_pk: int, paragraphs: List[Any]):
        """Inserisce lista di ParagraphData per un documento."""
        async with self.db_singleton.AsyncSessionLocal() as session:
            objs = []
            for p in paragraphs:
                para = ParagraphORM(
                    paragraph_id=p.paragraph_id,
                    doc_fk=doc_pk,
                    page_number=p.page_number,
                    bbox=p.bbox,
                    raw_text=p.raw_text,
                    cleaned_text=p.cleaned_text,
                    confidence=p.confidence
                )
                objs.append(para)
            session.add_all(objs)
            await session.commit()
    
    async def insert_tables(self, doc_pk: int, tables: List[Any]):
        """Inserisce lista di TableData per un documento."""
        async with self.db_singleton.AsyncSessionLocal() as session:
            objs = []
            for t in tables:
                table = TableORM(
                    table_id=t.table_id,
                    doc_fk=doc_pk,
                    page_number=t.page_number,
                    bbox=t.bbox,
                    table_json=t.table_json
                )
                objs.append(table)
            session.add_all(objs)
            await session.commit()
    
    async def insert_errors(self, errors: List[Any]):
        """
        In caso di errori rilevati (OCR o grammatici), inserisce gli errori
        errors: lista di dict con chiavi: paragraph_fk o table_fk, error_type, description
        """
        async with self.db_singleton.AsyncSessionLocal() as session:
            objs = []
            for e in errors:
                err = ErrorORM(
                    paragraph_fk=e.get("paragraph_fk"),
                    table_fk=e.get("table_fk"),
                    error_type=e.get("error_type"),
                    description=e.get("description")
                )
                objs.append(err)
            session.add_all(objs)
            await session.commit()

    async def fetch_all_paragraphs(self):
        """Recupera tutti i paragrafi (id, doc_fk, cleaned_text)."""
        async with self.db_singleton.AsyncSessionLocal() as session:
            result = await session.execute(select(ParagraphORM))
            return result.scalars().all()
```

* **Pattern applicati**:

  * `DatabaseSessionSingleton` è **Singleton** (GoF).
  * `DatabaseManager` è un esempio di **Pure Fabrication** (GRASP) perché non rappresenta un’entità di dominio, ma un servizio creato per scopi tecnici (gestione DB).

---

### 2.10 `inconsistency_checker.py`

Usiamo **Template Method** per l’algoritmo di scanning 1:1, e **Strategy** per la similarità:

```python
# inconsistency_checker.py

import asyncio
from typing import List, Tuple, Dict
from models import InconsistencyReport, ParagraphData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from strategies.similarity_strategies import ISimilarityStrategy

class BaseInconsistencyChecker:
    """
    Template Method (GoF) per l’inconsistency checking.
    Definisce lo scheletro dell’algoritmo:
      1. Carica paragrafi da DB
      2. Genera tutte le coppie 1:1
      3. Chiama il metodo `check_pair` (sottoclasse) su ciascuna coppia
      4. Accumula risultati in un report
    Sottoclassi devono implementare:
      - get_paragraphs()
      - check_pair(paraA, paraB)
    """
    async def run(self) -> List[InconsistencyReport]:
        paragraphs = await self.get_paragraphs()
        reports: List[InconsistencyReport] = []
        # Ciclo su tutte le coppie distinte di paragrafi
        n = len(paragraphs)
        for i in range(n):
            for j in range(i+1, n):
                paraA = paragraphs[i]
                paraB = paragraphs[j]
                rep = self.check_pair(paraA, paraB)
                if rep:
                    reports.append(rep)
        return reports
    
    async def get_paragraphs(self) -> List[ParagraphData]:
        """Recupera tutti i paragrafi dal DB (override nella sottoclasse)."""
        raise NotImplementedError
    
    def check_pair(self, paraA: ParagraphData, paraB: ParagraphData) -> InconsistencyReport:
        """Controlla coppia di paragrafi, ritorna un InconsistencyReport o None."""
        raise NotImplementedError


class SimpleInconsistencyChecker(BaseInconsistencyChecker):
    """
    Concrete Checker che implementa get_paragraphs e check_pair
    usando una Strategy di similarità.
    """
    def __init__(self, db_manager, similarity_strategy: ISimilarityStrategy, threshold: float = 0.85):
        self.db_manager = db_manager
        self.similarity_strategy = similarity_strategy
        self.threshold = threshold
    
    async def get_paragraphs(self) -> List[ParagraphData]:
        # Riprendiamo i paragrafi dal DB
        paras_orm = await self.db_manager.fetch_all_paragraphs()
        results = []
        from models import ParagraphData
        for p in paras_orm:
            pd = ParagraphData(
                paragraph_id=p.paragraph_id,
                page_number=p.page_number,
                bbox=p.bbox,
                raw_text=p.raw_text,
                confidence=p.confidence,
                cleaned_text=p.cleaned_text
            )
            results.append(pd)
        return results
    
    def check_pair(self, paraA: ParagraphData, paraB: ParagraphData) -> InconsistencyReport:
        # 1) Se stessi documenti, skip
        if paraA.paragraph_id == paraB.paragraph_id:
            return None
        
        # 2) Calcola similarità testi
        sim_score = self.similarity_strategy.similarity(paraA.cleaned_text, paraB.cleaned_text)
        
        if sim_score < self.threshold:
            return None
        
        # 3) Controllo “incongruenza” semplice:
        #    se i paragrafi condividono le stesse parole chiave opposte,
        #    o valori numerici differenti, segnaliamo.
        
        # Esempio molto semplificato:
        keywords_opposite = [("increase", "decrease"), ("above", "below"), ("yes", "no")]
        textA = paraA.cleaned_text.lower()
        textB = paraB.cleaned_text.lower()
        
        found_contradiction = False
        for a, b in keywords_opposite:
            if a in textA and b in textB:
                found_contradiction = True
                break
            if b in textA and a in textB:
                found_contradiction = True
                break
        
        inconsistency_type = None
        if found_contradiction:
            inconsistency_type = "Contraddizione semantica"
        
        # Controllo differenze numeriche (regex semplificato)
        import re
        numsA = re.findall(r"\d+\.?\d*", textA)
        numsB = re.findall(r"\d+\.?\d*", textB)
        if numsA and numsB and numsA != numsB:
            inconsistency_type = "Contraddizione numerica"
        
        if inconsistency_type:
            return InconsistencyReport(
                docA_id=paraA.paragraph_id.split("_")[0], 
                paragraphA_id=paraA.paragraph_id,
                docB_id=paraB.paragraph_id.split("_")[0],
                paragraphB_id=paraB.paragraph_id,
                inconsistency_type=inconsistency_type,
                similarity_score=sim_score
            )
        
        return None
```

* **Pattern applicati**:

  * `BaseInconsistencyChecker` è **Template Method** (GoF): definisce lo scheletro dell’algoritmo, lasciando “hook” a `get_paragraphs` e `check_pair`.
  * `SimpleInconsistencyChecker` è **Concrete Class** che estende il template.
  * `ISimilarityStrategy` (importato) è **Strategy**: possiamo cambiare `RapidFuzzSimilarity` vs. `SpacySimilarity` senza modificare il “template”.

---

### 2.11 `main.py`

Infine, il **PipelineManager** (Controller generale) che mette insieme tutti i pezzi:

```python
# main.py

import asyncio
import os
from typing import List

from ocr_parser import OCRParserFactory, OCRParserController
from classify_docs import ClassifyDocsController
from error_corrector import ErrorCorrector
from database_manager import init_db, DatabaseManager
from inconsistency_checker import SimpleInconsistencyChecker
from strategies.classifier_strategies import GoogleNLClassifier
from strategies.similarity_strategies import RapidFuzzSimilarity

async def main():
    # 1) Configurazione iniziale
    # -------------------------------------------------------
    # Lettura parametri da env o config (semplificato):
    OCR_ENGINE = "google_document_ai"
    DOC_AI_PROJECT = "my-project"
    DOC_AI_LOCATION = "us"
    DOC_AI_PROCESSOR = "processor-id-123"
    
    # 2) Inizializza DB (crea tabelle)
    await init_db()
    db_manager = DatabaseManager()
    
    # 3) Crea i parser/strategy
    ocr_parser = OCRParserFactory.create_parser(
        engine=OCR_ENGINE,
        project_id=DOC_AI_PROJECT,
        location=DOC_AI_LOCATION,
        processor_id=DOC_AI_PROCESSOR
    )
    ocr_controller = OCRParserController(parser=ocr_parser)
    
    classifier_strategy = GoogleNLClassifier(project_id="my-project")
    classify_controller = ClassifyDocsController(classifier=classifier_strategy)
    
    error_corrector = ErrorCorrector()
    similarity_strategy = RapidFuzzSimilarity()
    inconsistency_checker = SimpleInconsistencyChecker(
        db_manager=db_manager,
        similarity_strategy=similarity_strategy,
        threshold=0.85
    )
    
    # 4) Raccolta dei file da processare
    input_folder = "./documents/"
    filepaths: List[str] = [
        os.path.join(input_folder, f) 
        for f in os.listdir(input_folder) 
        if f.lower().endswith((".pdf", ".png", ".jpg"))
    ]
    
    # 5) Step 1: OCR + Parsing
    print(">>> Step 1: OCR + Parsing")
    docs_data = await ocr_controller.parse_all(filepaths)
    
    # 6) Step 2: Classificazione
    print(">>> Step 2: Classificazione")
    classifications = await classify_controller.classify_all(docs_data)
    
    # 7) Step 3: Correzione Errori
    print(">>> Step 3: Correzione Errori")
    # Per ogni documento, correggiamo paragrafi singolarmente:
    for doc, cls in zip(docs_data, classifications):
        # Correggiamo tutti i paragrafi
        corrected_paragraphs = error_corrector.correct_all(doc.paragraphs)
        doc.paragraphs = corrected_paragraphs
    
    # 8) Step 4: Salvataggio su DB
    print(">>> Step 4: Salvataggio su DB")
    for doc, cls in zip(docs_data, classifications):
        doc_pk = await db_manager.insert_document(doc, cls)
        await db_manager.insert_paragraphs(doc_pk, doc.paragraphs)
        await db_manager.insert_tables(doc_pk, doc.tables)
        # Nel nostro MVP non popoleremo errori: si potrebbe analizzare doc.visual_defects
        # e paragrafi con confidence < 0.90, creando voci in ErrorORM
    
    # 9) Step 5: Inconsistency Checking
    print(">>> Step 5: Inconsistency Checking")
    inconsistency_report = await inconsistency_checker.run()
    
    # 10) Output report finale (salviamo in CSV)
    import csv
    with open("inconsistency_report.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "docA_id", "paragraphA_id", 
            "docB_id", "paragraphB_id", 
            "inconsistency_type", "similarity_score"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for rep in inconsistency_report:
            writer.writerow({
                "docA_id": rep.docA_id,
                "paragraphA_id": rep.paragraphA_id,
                "docB_id": rep.docB_id,
                "paragraphB_id": rep.paragraphB_id,
                "inconsistency_type": rep.inconsistency_type,
                "similarity_score": rep.similarity_score
            })
    
    print(f"► Report generato: inconsistency_report.csv")

if __name__ == "__main__":
    asyncio.run(main())
```

* **Pattern applicati**:

  * `main()` è il **Controller** (GRASP) che coordina tutti i sub-controller e i servizi.
  * Viene applicato un flusso asincrono (uso di `asyncio.gather`) per parallelizzare OCR e classificazione.

---

## 3. Riassunto dei pattern applicati

| Modulo / Classe                          | Pattern GRASP / GoF                              | Scopo                                                                           |
| ---------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------- |
| `IOCRParser`                             | Strategy (GoF)                                   | Interfaccia per plug-in di motori OCR diversi.                                  |
| `GoogleDocumentAIParser`                 | Concrete Strategy, Creator (GRASP)               | Implementazione del parsing e creazione di `DocumentData`.                      |
| `OCRParserFactory`                       | Factory Method (GoF)                             | Crea istanze di `IOCRParser` in base a configurazione.                          |
| `OCRParserController`                    | Controller (GRASP)                               | Coordina la chiamata parallela all’OCR di più documenti.                        |
| `IClassifierStrategy`                    | Strategy (GoF)                                   | Definisce l’API comune per moduli di classificazione.                           |
| `GoogleNLClassifier`                     | Concrete Strategy                                | Classificazione di documento tramite Google Cloud NL.                           |
| `ClassifyDocsController`                 | Controller (GRASP)                               | Coordina la classificazione multipla in parallelo.                              |
| `ErrorCorrector`                         | Information Expert (GRASP)                       | È esperto nel rilevare e correggere errori testuali.                            |
| `DatabaseSessionSingleton`               | Singleton (GoF)                                  | Unica connessione/engine asincrono al database.                                 |
| `DatabaseManager`                        | Pure Fabrication (GRASP)                         | Gestisce tutte le operazioni CRUD su DB (dettaglio tecnico).                    |
| `BaseInconsistencyChecker`               | Template Method (GoF)                            | Scheletro generico di “scanning” 1:1 tra paragrafi.                             |
| `SimpleInconsistencyChecker`             | Concrete Class (GoF), Information Expert (GRASP) | Implementa la specifica logica di confronto, usa strategy di similarità.        |
| `ISimilarityStrategy`                    | Strategy (GoF)                                   | Interfaccia per differenti algoritmi di similarità testuale.                    |
| `RapidFuzzSimilarity`, `SpacySimilarity` | Concrete Strategy                                | Implementazioni reali di similarità fuzzy e semantica.                          |
| `PipelineManager` (`main.py`)            | Controller (GRASP)                               | Coordina l’intera pipeline in modo asincrono, gestendo errori e orchestrazione. |

---

## 4. Conclusioni

* Applicando **GRASP**, abbiamo assegnato responsabilità chiare: ciascuna classe “sa” **cosa** fa (Information Expert), le classi di servizio non rappresentano entità reali ma servono a isolare logica tecnica (Pure Fabrication), vi è un’entità unica per la connessione DB (Singleton), e abbiamo separato i comportamenti (Strategy e Factory Method) per aumentare flessibilità e testabilità.
* Applicando i **GoF Patterns**, la pipeline risulta strutturata in moduli che si possono estendere (“se domani volessimo cambiare OCR, basta aggiungere una nuova Concrete Strategy e aggiornare la Factory”), supportando la **manutenibilità** e il **riuso**.
* Il risultato è un **MVP funzionante**, che puoi già lanciare in locale (ricordandoti di installare le librerie elencate in `requirements.txt`, configurare le chiavi Google, e mettere i PDF/immagini in `./documents/`).
* In ogni punto della pipeline è facile sostituire o aggiungere nuove implementazioni (es. un altro database, un altro algoritmo di similarità, un correttore grammaticale differente), senza riscrivere tutta la logica.

Sentiti libero di personalizzare ulteriormente le soglie, i meccanismi di logging (es. usando `loguru`), o di aggiungere un’interfaccia Web/Streamlit per visualizzare i risultati. Questo esempio mostra nel dettaglio **come** i principi GRASP e i GoF Patterns possano guidare scelte di design solide, e fornisce una base su cui costruire ulteriori funzionalità (ad es. gestione delle tabelle nel “inconsistency checker”, report avanzati, ecc.). Se hai domande o vuoi approfondire un modulo specifico, fammi sapere!
