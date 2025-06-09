### Report Interno - Task Urgenti per Release Produzione

Data: 04/05/2025
Deadline release: 09/05/2025 (venerdì)
Redatto da: Alessandro Brillante
Ruolo: Developer / Coordinatore Tecnico

---

#### 1. Frontend (React + Vite su Aruba)

| Task                   | Descrizione                                                                                        | Urgenza   | Impatto                            |
| ---------------------- | -------------------------------------------------------------------------------------------------- | --------- | ---------------------------------- |
| Migrazione hosting | Spostare build statico su Netlify o Vercel per supporto CDN e fallback SPA (risolve errore F5) | Alta  | Critico (blocco UX su refresh) |
| SPA fallback routing   | Configurare _redirects su Netlify o vercel.json per supporto alle rotte SPA                    | Alta  | Critico                        |
| Ottimizzazione build   | Verificare lazy loading, code splitting e compressione asset (vite.config.js)                | Media | Migliora performance               |

---

#### 2. Backend (Heroku + Stripe)

| Task                        | Descrizione                                                                          | Urgenza   | Impatto                 |
| --------------------------- | ------------------------------------------------------------------------------------ | --------- | ----------------------- |
| Verifica variabili ambiente | Confermare corretta configurazione STRIPE_SECRET_KEY solo lato server              | Alta  | Sicurezza pagamenti |
| Limitare permessi API key   | Passare a Restricted Key su Stripe per test e produzione (solo paymentIntent)  | Media | Aumenta sicurezza       |
| Logging pagamenti           | Aggiungere logging lato server per pagamento riuscito/fallito (senza loggare la key) | Media | Debug + Audit           |
| Verifica deploy sicuro      | Rimuovere qualsiasi console.log(process.env) o simili dal codice                   | Alta  | Sicurezza               |

---

#### 3. Firebase

| Task                       | Descrizione                                                        | Urgenza   | Impatto                       |
| -------------------------- | ------------------------------------------------------------------ | --------- | ----------------------------- |
| Audit query Firestore      | Controllare e ottimizzare letture multiple o query non indicizzate | Alta  | Riduzione costi + performance |
| Test carico autenticazione | Simulare 50+ utenti login per validare scalabilità Firebase Auth   | Media | Robustezza auth               |
| Aggiungere logging Sentry  | Integrazione con Sentry o Logtail per tracciare errori runtime     | Media | Debug + Monitoraggio          |

---

#### 4. QA & Stress Test

| Task                           | Descrizione                                                                                   | Urgenza   | Impatto           |
| ------------------------------ | --------------------------------------------------------------------------------------------- | --------- | ----------------- |
| Test refresh su tutte le route | Validare comportamento SPA dopo migrazione su Netlify/Vercel                                  | Alta  | UX finale         |
| Simulazione carico utenti      | Usare tool come k6 o Lighthouse CI per simulare utenti simultanei (checkout, login, catalogo) | Alta  | Prevenzione crash |
| Test mobile                    | Controllare interazioni come "pull to refresh" su Android/iOS                                 | Media | Consistenza UX    |

---

#### 5. Organizzazione e tempistiche suggerite

Alexei, [04/05/2025 17:44]
| Giorno              | Obiettivo principale                                         |
| ------------------- | ------------------------------------------------------------ |
| Domenica (oggi) | Migrazione frontend + redirect SPA + audit backend sicurezza |
| Lunedì          | Logging backend + audit Firestore + deploy Netlify/Vercel    |
| Martedì         | Test mobile + test carico + Sentry                           |
| Mercoledì       | Fix QA + chiusura ticket + test utente reale                 |
| Giovedì         | Hardening + piano rollback + comunicazione release           |
| Venerdì         | Release ufficiale (mattina) + monitoraggio h24               |

---

### Nota finale

Le basi ci sono. Serve solo mettere in sicurezza, spostare il frontend e testare tutto bene. Nessun blocco strutturale, ma non possiamo permetterci incidenti di base (F5 rotte, chiavi esposte o timeout pagamenti).
