# Generative and Predictive Ai

Spiegazione dei concetti base di **machine learning**, **predictive AI** e **generative AI** dal testo che hai fornito, con particolare attenzione a GPT.

---

### Elementi di Machine Learning nel testo:

* **Pattern recognition:** L’IA predittiva identifica pattern (schemi) nei dati per stimare cosa accadrà, lavorando su una catena di eventi o dati.
* **Parametri:** Si parla di "parametri" come elementi fondamentali del modello che influenzano la capacità di riconoscere pattern e fare previsioni. Parametri di qualità migliore sono preferibili a una quantità enorme di parametri di qualità mediocre.
* **Contesto e coerenza:** Importanti qualità che un modello deve mantenere per fornire risposte accurate e sensate. La perdita di contesto o coerenza porta a risposte sempre meno pertinenti.
* **RAG (Retrieval-Augmented Generation):** Tecnica in cui un modello generativo accede a dati esterni memorizzati per migliorare la qualità e la pertinenza delle risposte.
* **LoRA (Low-Rank Adaptation):** Micro-modelli aggiuntivi che si combinano con il modello base per creare variazioni specifiche e migliorare risposte in contesti particolari.
* **Calcoli probabilistici:** Le IA predittive lavorano su stime probabilistiche, non su certezze assolute, quindi la qualità dei dati e la struttura del modello sono cruciali per la precisione.

---

### Predictive AI vs Generative AI:

* **Predictive AI:** Si basa sul riconoscimento di pattern e fa previsioni su "cosa accadrà" nel prossimo passo di una sequenza. È orientata a stimare eventi futuri basandosi su dati passati, spesso usando modelli probabilistici.

  * Esempio: Previsioni del clima, stime su dati numerici.

* **Generative AI:** Crea contenuti nuovi, come testi, immagini, audio, ecc., combinando e riformattando informazioni, ma senza necessariamente "prevedere" nel senso stretto.

  * GPT è un esempio di AI generativa: genera testo plausibile e coerente basato su input, ma non fa previsioni di eventi futuri come fa una AI predittiva.

---

### GPT e la distinzione:

* **GPT è una AI generativa.** Usa enormi modelli (miliardi di parametri) per generare testo coerente basato sui prompt ricevuti.
* Quando sono necessari dati o calcoli predittivi più precisi, GPT può appoggiarsi a modelli predittivi o dati esterni (es. RAG) per migliorare la risposta.
* La **qualità dei dati** e la capacità di mantenere **contesto e coerenza** sono cruciali per le prestazioni di GPT.
* GPT non fa previsioni con certezza assoluta ma risponde in modo probabilistico, basandosi su pattern appresi.
