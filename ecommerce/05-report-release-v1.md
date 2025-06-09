### **Report Tecnico - Architettura Applicativa & Scalabilità**

**Cliente:** Mellys Kombucha
**Data:** 04/05/2025
**Redatto da:** Alessandro Brillante
**Ruolo:** Developer / Consulente Tecnico

---

#### **1. Architettura attuale**

* **Frontend:**

  * SPA realizzata in **React + Vite**
  * Hosting su **Aruba Linux Basic** (shared hosting)
  * Deployment statico (HTML, JS, CSS) + HTTPS
  * Funzioni principali: catalogo, autenticazione, carrello, gestione ordini

* **Backend principale (dati e logica di business):**

  * **Firebase Firestore**: database NoSQL per utenti, prodotti e ordini
  * **Firebase Authentication**: gestione utenti
  * Scalabilità automatica gestita da Google

* **Backend secondario (pagamenti):**

  * **Node.js server su Heroku** (gestione `paymentIntent` con Stripe)
  * Collegamento sicuro tramite HTTPS
  * Heroku Hobby plan (dyno always-on, SSL incluso)

---

#### **2. Stato attuale e capacità stimata**

| Componente          | Carico stimato attuale | Limite stimato                   |
| ------------------- | ---------------------- | -------------------------------- |
| Aruba Linux Basic   | 5-10 utenti simultanei | \~15-20 max (non ottimizzato)    |
| Firebase Firestore  | \~50-100 req/min       | Scalabile (dipende da costo/uso) |
| Heroku (Stripe API) | \~10 req/min           | Hobby plan: \~100-200 req/min    |

---

#### **3. Roadmap di scalabilità**

| Milestone utenti simultanei | Considerazioni                   | Azioni richieste                                             |
| --------------------------- | -------------------------------- | ------------------------------------------------------------ |
| **100 utenti**              | Possibile, ma al limite su Aruba | - Passare frontend su \[Vercel/Netlify] (SPA CDN+Edge)       |
|                             |                                  | - Ottimizzare build Vite + lazy loading                      |
|                             |                                  | - Tenere Firebase e Heroku così                              |
| **1.000 utenti**            | Heroku Hobby satura              | - Passare Heroku a Standard-1X (2x dyno, \~50€/mese)         |
|                             |                                  | - Firebase ok (potrebbe aumentare costi letture)             |
|                             |                                  | - Monitoraggio e caching lato client                         |
| **10.000 utenti**           | Limitazioni Firebase/Heroku      | - Passaggio a Heroku Performance dyno o altra PaaS           |
|                             |                                  | - Cache distribuita (es. Redis Cloud, CDN)                   |
|                             |                                  | - Firebase: valutare Firestore in modalità Native + Sharding |
|                             |                                  | - Frontend CDN globale (es. Cloudflare Pages)                |

---

#### **4. Rischi & raccomandazioni**

* **Aruba Linux Basic** è inadatto per ambienti ad alto traffico. Rischio alto di downtime.
* **Stripe + Heroku**: sicuro ma da monitorare attentamente per scalabilità durante promozioni o picchi.
* **Costi Firebase**: aumentano linearmente con numero di operazioni; attento a query non ottimizzate.
* **Mancanza di logging avanzato** in alcuni punti critici (es. pagamento, gestione ordini) può ostacolare il debugging in produzione.

---

#### **5. Proposte tecniche a breve termine**

1. **Migrazione frontend statico** su Netlify o Vercel → costi bassi, performance ottime (CDN globale).
2. **Audit Firebase Firestore** → riduzione query e batch update
3. **Log centralizzato** via Logtail o Sentry → migliore tracciamento errori
4. **Stima costi mensili** e monitor per Firebase & Heroku

---

### Limitazioni del piano Hosting Linux Basic

Per un e-commerce sviluppato come Single Page Application (SPA) con React e Vite, integrato con Stripe per i pagamenti, il piano **Hosting Linux Basic** di Aruba, al costo di circa **32,99 € + IVA all'anno**, potrebbe non essere la soluzione più adatta, soprattutto se prevedi un traffico significativo o funzionalità avanzate.

* **Risorse condivise**: Essendo un hosting condiviso, le risorse del server (CPU, RAM, I/O) sono suddivise tra più utenti, il che può causare rallentamenti in caso di picchi di traffico.
* **Prestazioni limitate**: Per applicazioni SPA che richiedono una gestione efficiente delle risorse, questo piano potrebbe non garantire le prestazioni necessarie.
* **Supporto per applicazioni moderne**: Anche se è possibile configurare applicazioni React, l'ambiente potrebbe non essere ottimizzato per build e deployment di applicazioni moderne.

### Considerazioni sull'integrazione con Stripe

L'integrazione con Stripe per i pagamenti richiede un ambiente sicuro e affidabile. Sebbene il piano offra un certificato SSL, le limitazioni di performance e le risorse condivise potrebbero influire negativamente sull'esperienza dell'utente durante il processo di pagamento.

### Raccomandazioni

Per garantire un'esperienza utente fluida e sicura, considera le seguenti opzioni:

* **Upgrade a un piano superiore**: Aruba offre piani come l'**Hosting Linux Professional**, che forniscono risorse dedicate e migliori prestazioni.
* **Soluzioni VPS o server dedicati**: Per un controllo completo sull'ambiente di hosting e per gestire meglio le esigenze di un e-commerce, una VPS o un server dedicato potrebbero essere più appropriati.
* **Piattaforme specializzate**: Valuta l'utilizzo di piattaforme come Vercel o Netlify per il frontend React, abbinate a servizi backend scalabili come Firebase o Supabase.

### Conclusione

Mentre il piano Hosting Linux Basic di Aruba può essere sufficiente per siti web statici o a basso traffico, per un e-commerce SPA con React e integrazione Stripe, è consigliabile optare per soluzioni di hosting più robuste e scalabili per garantire prestazioni ottimali e sicurezza.
