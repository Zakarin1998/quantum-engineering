**Riassunto di Extreme Programming (XP)**

---

### 1. Fondamenti e variabili

* **Origini**: XP nasce alla fine degli anni ’90 per opera di Kent Beck, inizialmente progettato nell’ambito di un progetto Chrysler.

* **Le quattro variabili** (Beck):

  1. **Portata** (scope): insieme delle funzionalità da implementare, variabile e ricalcolabile continuamente.
  2. **Tempo**: l’effort effettivo dedicabile al progetto (in XP non è rigidamente definito, si adatta in base alle necessità).
  3. **Qualità**: considerata costante (si punta sempre alla massima correttezza e affidabilità, per quanto possibile).
  4. **Costo**: risorse finanziarie e di personale; in XP è “orario” e si paga a consuntivo, non a progetto finito.

* **Principio di base**: la qualità non è negoziabile; cambiando le altre tre variabili (portata, tempo, costo) bisogna mantenere sempre alta la qualità.

* **Modello XP vs. modello tradizionale**:

  * Tradizionale → portata definita rigidamente dal cliente, costo forfettario, rilascio completo a fine sviluppo.
  * XP → costo a consumo (orario), portata continuamente ridefinita in base al feedback e alle priorità, rilascio incrementale di piccole porzioni di funzionalità.

---

### 2. Principi di XP (rispetto al modello classico)

1. **Feedback rapido**

   * Stand-up meeting quotidiani (brevi, in piedi): ciascuno riassume quanto fatto e cosa farà oggi.
   * Test automatici e continui (TDD), revisione del codice in coppie (pair programming), coinvolgimento costante del cliente.

2. **Presunzione di semplicità**

   * **“Carpe diem”** nel codice: si implementa solo ciò che serve **adesso**, non ciò che si pensa serva in un futuro remoto.
   * Architetture, design e relazioni di team restano semplici: nessuna gerarchia eccessiva, compiti omogenei fra sviluppatori.

3. **Accettazione del cambiamento**

   * Ci si aspetta che i requisiti evolvano durante lo sviluppo.
   * Il cliente fa parte attiva del team, rivede continuamente il backlog e può ridistribuire priorità o rimuovere/addere user stories.

4. **Modifica incrementale (baby steps)**

   * Iterazioni brevi: ogni sprint introduce poche funzionalità ben definite.
   * Anche l’organizzazione del team segue la stessa logica: non si introducono tante persone in una sola volta, ma “una per volta”, al massimo una nuova figura per iterazione.

5. **Lavoro di qualità e benessere del team**

   * Ambiente di lavoro salutare, orari sostenibili, turni ragionevoli: uno sviluppatore “in forma” produce codice più pulito e robusto.
   * Pair programming come pratica per migliorare la condivisione della conoscenza e ridurre gli errori.

6. **Eredità di principi classici di ingegneria del software**

   * XP **non scarta**:
     • Separazione degli interessi (concerns).
     • Astrazione e modularità (uso di giuste astrazioni per dominare la complessità).
     • Anticipazione del cambiamento (design for change), pur ridimensionandolo a favore della semplicità.
     • Generalità delle interfacce.
     • Incrementalità (già adottata).
     • Rigore e formalità nella comunicazione e nei requisiti (XP adotta user stories, test suite, criteri di accettazione molto formali).

---

### 3. Conflitto “presumere la semplicità” vs “anticipazione del cambiamento”

* **Scopo XP**: scrivere codice minimale e semplice, rifattorizzabile costantemente, anziché ipotizzare grandi esigenze future.
* **Studio di Boehm (1976)**: sosteneva che il costo di modifica cresce esponenzialmente man mano che il progetto avanza. XP ribalta l’assunto, ipotizzando che – grazie a tecniche moderne (refactoring, linguaggi più espressivi) – il costo di modifica si stabilizzi (curva logaritmica asintotica).
* **Critiche**: Boehm stesso ritrattò poi in parte la sua curva esponenziale, e in molti progetti tuttora un buon “design up-front” rimane importante per certe componenti core del sistema. XP consiglia di investire più in continue revisioni rapide che in un design esaustivo all’inizio.

---

### 4. Figure e responsabilità in XP

| **Ruolo**             | **Compiti e responsabilità**                                                                                                                                                                                                                                                                                                       | **Diritti**                                                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Manager/Cliente**   | • Definire portata (features) e priorità in base al valore di business<br> • Stabilire date di rilascio incrementali<br> • Valutare costi e tempi complessivi<br> • Fornire feedback continuo, definire i test di accettazione                                                                                                     | • Vedere lo stato di avanzamento (demo, test passati)<br> • Cambiare idea su priorità e features a iterazione finita<br> • Conoscere costi e tempistiche reali, o consultare la documentazione di test |
| **Sviluppatore**      | • Stimare tempi per ogni feature (non accetta deadline imposte in modo unilaterale)<br> • Scegliere tecnologie e strategia di implementazione<br> • Pianificare dettagli iterazione per iterazione<br> • Segnalare rischi, dipendenze, criticità tecniche<br> • Produrre codice di qualità<br> • Adattarsi ai cambiamenti continui | • Ricevere requisiti chiari (user stories) con priorità<br> • Modificare stime in corso d’opera se necessario<br> • Identificare feature particolarmente complesse o rischiose                         |
| **Tracker (rotante)** | • Tenere traccia delle metriche principali (numero di issue aperti, bug, story completate)<br> • Condividere giornalmente (o per iterazione) sui principali problemi riscontrati<br> • Aiutare il team a migliorare il processo in base ai dati raccolti                                                                           | • Accedere a tutti i dati di progresso (jira, board, metriche)<br> • Facilitare decisioni sui miglioramenti di processo                                                                                |

---

### 5. Criticità e quando **non** usare XP

**Beck stesso** sosteneva che, in teoria, si può tentare XP in qualsiasi progetto—purché si osservino i dodici principi fondamentali (visione basata su feedback continuo, semplicità, comunicazione, coraggio, rispetto). In pratica, però, ci sono casi in cui XP non si presta:

1. **Team dislocati geograficamente**

   * Avere più sedi che lavorano in fusi orari diversi rende difficile il feedback istantaneo (stand-up, pairing, revisione del codice).
   * La comunicazione asincrona tende ad allungare i tempi di risposta e vanificare l’idea di “feedback rapido”.

2. **Team troppo numerosi (>8–10 persone)**

   * XP funziona al meglio con team ristretti e coesi (4–10 membri).
   * Aumentando le persone, la complessità di coordinamento cresce notevolmente, vanificando i benefici di pair programming e stand-up giornalieri.

3. **Barriere tecnologiche o infrastrutturali**

   * Mancanza di strumenti per integrazione continua (CI) comune a tutti (macchine condivise per test, repository centralizzato, server di build).
   * Impossibilità di garantire ambienti di test riproducibili per ciascuna coppia di sviluppatori.

4. **Troppe parti interessate (stakeholder) con esigenze contrastanti**

   * Se sul progetto agiscono più comitati o gruppi decisionali con visioni divergenti, diventa difficile far convergere i feedback in iterazioni brevi.
   * La continua rivalutazione delle priorità rischia di generare confusione anziché trasparenza.

5. **Consegna incrementale impraticabile**

   * Sistemi safety-critical, come nel caso di software per centrali nucleari, dispositivi medici (certificazione FDA/CE), pilota automatico di aerei: non si può rilasciare “un pezzetto alla volta” senza violare normative o mettere a rischio la sicurezza.
   * A fronte di questi vincoli, un approccio waterfall controllato (V-Model, spirale) rimane più adatto.

---

### 6. Critiche principali (da Meyer)

Robert C. Meyer (autore di “Object-Oriented Software Construction”) muove alcune critiche nei confronti di XP:

1. **Sottovalutazione del “Up-Front Design”**

   * Secondo Meyer, un’analisi e un’architettura iniziale sono fondamentali: in quasi tutti i progetti (tranne i più piccoli o i più “da hackathon”), non si può delegare tutto al design incrementale e al refactoring continuo.
   * Se non si ha una base solida, le modifiche successive possono risultare molto costose.

2. **Sovrastima delle user stories come sostituto dei requisiti**

   * Le user stories, per loro natura, sono “brevi descrizioni” di funzionalità dal punto di vista dell’utente. Meyer ritiene che spesso non bastino a rappresentare la completezza di un requisito, soprattutto per sistemi complessi con molte interdipendenze.

3. **Mancanza di enfasi sulle dipendenze tra user stories**

   * XP richiede che le user stories siano indipendenti e “negabili” in ordine, ma in progetti reali le funzionalità si intrecciano: Meyer suggerisce che senza un’analisi di dipendenza (diagrammi di Gantt o Dependency Structure Matrix) si rischi di non accorgersi in tempo di vincoli fondamentali.

4. **Rischio di visione troppo ristretta con TDD (“Test-Driven Development”)**

   * TDD richiede di scrivere test prima del codice. Se non si ha una visione di alto livello, i test possono diventare migliaia di casi “punto a punto” che tappano buchi, ma non garantiscono coerenza architetturale.
   * Meyer avverte che senza una strategia di test di integrazione e di sistema, TDD potrebbe portare a un eccesso di test unitari isolati, che non catturano i problemi end-to-end.

5. **Team cross-functional troppo eterogenei**

   * XP suggerisce team “multi-skill” (ogni membro sa un po’ di tutto), ma nella realtà spesso si hanno specialisti molto focalizzati (database, network, sicurezza).
   * Costruire una coppia di lavoro “developer–security expert” o “designer–frontend specialist” può creare attriti o rallentare il pairing costante.

> **Nota**: Meyer non esclude a priori XP, ma invita a bilanciare sempre un minimo di upfront design (analisi, architettura) con il refactoring continuo e a non dare per scontata l’efficacia delle sole user stories.

---

### 7. “Mesi-uomo” e produttività

* **Errata convinzione comune**: più persone si aggiungono al progetto, più velocemente si conclude (curva “iperbolica”).

* **Realtà**:

  * Aggiungendo risorse, aumenta l’**overhead di comunicazione**: occorre più tempo per coordinarsi (riunioni, aggiornamenti, merging di codice, sincronizzazione).
  * Se il lavoro è strettamente sequenziale (es. attività non parallelizzabile come determinati step di validazione o “collaudo fisico”), aggiungere persone non velocizza affatto.
  * In casi estremi (“gravidanza”, “start-up di un reattore”), l’input umano aggiuntivo peggiora la situazione.

* **Alternative al “more hands” se si ritarda**:

  1. **Rinegoziare la deadline** con il cliente (se possibile).
  2. **Ridurre la portata** (scope): focalizzarsi solo su killer feature, tagliare funzionalità secondarie.
  3. **Ridurre la qualità** (es. diminuire il testing), sconsigliato ma a volte praticato; comporta rischi elevati.

* **Dimensione ideale di un team XP**:

  * In genere non dovrebbe superare le **8-10 persone**.
  * Se si deve andare oltre, occorre splittare in moduli ben definiti con interfacce chiare e “team di team” (in questo caso XP puro decade).

---

### 8. Ruoli XP sintetizzati

1. **Cliente (o Business Representative)**

   * Membro effettivo del team.
   * Stabilisce priorità delle user stories, controlla i test di accettazione, fornisce feedback continuo.
   * Può (e deve) cambiare idea su priorità o requisiti a ogni iterazione.

2. **Sviluppatore**

   * Responsabile di scelte tecniche, stima dei tempi, qualità del codice.
   * Partecipa a pair programming, scrive test secondo TDD, rifattorizza continuamente.
   * Riceve user stories prioritarie, le stima e le realizza in piccole iterazioni.

3. **Tracker (Ruolo Rotante)**

   * Tiene traccia delle metriche di sprint (numero di bug, storie completate, ostacoli).
   * Aggiorna il “tracking board” (lavagna fisica o kanban board) con lo stato di ogni item.
   * Aiuta a identificare colli di bottiglia e a proporre miglioramenti al processo.

4. **Manager (o Coach)**

   * Non “imprime” scelte tecniche, ma assicura rimozione impedimenti, facilita le discussioni, protegge il team da interferenze esterne.
   * Coordina le release incrementali, negozia risorse col cliente e garantisce che l’ambiente di lavoro resti sano.

---

### 9. Criticità aggiuntive di XP

* **Rigidità su piccoli contesti**: in progetti di poche settimane e team di 2-3 persone, XP può risultare eccessivo nella burocrazia (stand-up quotidiani, pair programming continuo, TDD via test suite).
* **Mancanza di “vision” a medio/lungo termine**: senza un’architettura di massima, progetti con molte integrazioni (microservizi, interfacce con terze parti) possono diventare difficilmente manutenibili se non si progetta qualcosa “upfront”.
* **Eccessiva dipendenza dal cliente**: se il cliente non è disponibile “sempre” o non ha competenze tecniche, l’interazione continua rischia di diventare un collo di bottiglia.
* **Costi iniziali di set-up**: quality‐environment (CI server, test framework, pair stations, strumenti di refactoring) richiede investimenti (tempo e denaro) all’inizio.
* **Complessità nel coordinare più team XP**: in grandi organizzazioni con più team che lavorano su microservizi diversi, l’allineamento fra backlog e dipendenze cross-team diventa complicato.

---

## Conclusione

Extreme Programming offre un modo estremamente iterativo e orientato al feedback per gestire lo sviluppo software, massimizzando qualità e adattabilità ai cambiamenti. Tuttavia, rispetto al modello “classico” di ingegneria del software, sposta la complessità verso:

* **Costante comunicazione** fra sviluppatori, cliente e manager
* **Semplicità costruttiva** evitando design eccessivi in fase iniziale
* **Iterazioni molto brevi** con rilascio incrementale

L’XP non è universale: non si adatta bene a team molto distribuiti, a progetti safety-critical o a contesti in cui non si può rilasciare gradualmente. Le critiche principali (Meyer e altri) invitano a non trascurare del tutto analisi e architettura iniziale, a gestire con attenzione le dipendenze fra storie e a collaborare in team cross-functional con professionalità diverse. Infine, l’uso dei “mesi-uomo” come metrica di stima dev’essere considerato con cautela, perché aggiungere risorse spesso comporta più overhead che vantaggi di produttività.
