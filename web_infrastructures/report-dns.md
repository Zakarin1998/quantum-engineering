## Report sui Sistemi DNS

### 1. Introduzione ai DNS

Il **Domain Name System (DNS)** è un sistema distribuito che mappa i nomi di dominio (es. `mellyskombucha.com`) agli indirizzi IP (es. `23.227.38.65`) e viceversa. Funziona come una rubrica telefonica di Internet e si basa su una gerarchia di server:

* **Root Servers**: punto di partenza per ogni ricerca DNS.
* **TLD (Top-Level Domain) Servers**: gestiscono domini di primo livello come `.com`, `.org`, `.it`.
* **Authoritative Name Servers**: detengono i record DNS effettivi di un dominio.

### 2. Tipi di Record DNS

| Tipo      | Descrizione                                                          |
| --------- | -------------------------------------------------------------------- |
| **A**     | IPv4 address record: associa un nome host a un indirizzo IPv4.       |
| **AAAA**  | IPv6 address record: associa un nome host a un indirizzo IPv6.       |
| **CNAME** | Canonical Name record: alias che punta ad un altro nome di dominio.  |
| **MX**    | Mail Exchange: specifica i server di posta per il dominio.           |
| **NS**    | Name Server: indica i server autoritativi per il dominio.            |
| **TXT**   | Testo libero: spesso usato per SPF, DKIM, verifiche di dominio, ecc. |
| **SRV**   | Service locator: identifica servizi e porte (es. per VoIP, XMPP).    |

### 3. Risoluzione DNS

1. **Query Iterativa/Ricorsiva**: Il client (resolver) invia richieste ricorsive al server DNS locale.
2. **Cache**: i resolver memorizzano le risposte per un certo TTL (Time To Live).
3. **Propagazione**: quando si modificano record, la nuova informazione si propaga in tutto il mondo in base ai TTL.

### 4. Piattaforme di Gestione DNS (es. Aruba)

* Alcuni provider, come Aruba, hanno interfacce web per aggiungere/modificare record.
* **Limite CNAME**: non può convivere con altri record (A, AAAA, MX…) per lo stesso nome.
* **Pratiche comuni**:

  * `@` per il dominio radice (es. `mellyskombucha.com`)
  * `www` per il sottodominio (es. `www.mellyskombucha.com`)
  * Interfacce che richiedono campi come “Nome host”, “Tipo”, “Valore”, TTL.

---

## Prototipo Python a Grafo per Knowledge Base

Di seguito uno **scheletro** Python che:

1. Definisce nodi e relazioni del dominio DNS.
2. Permette di aggiungere conoscenza estratta dalla chat.
3. Esporta la struttura a grafo per navigazione e analisi.

```python
import networkx as nx

class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, key, **attrs):
        # Aggiunge un nodo con attributi
        self.graph.add_node(key, **attrs)

    def add_edge(self, src, dst, **attrs):
        # Aggiunge un arco diretto
        self.graph.add_edge(src, dst, **attrs)

    def from_chat(self, entries):
        '''Converti una lista di tuple (categoria, elemento, relazione) in nodi/arcs.'''
        for cat, elem, rel, target in entries:
            self.add_node(cat)
            self.add_node(elem)
            self.add_edge(cat, elem, type=rel)
            if target:
                self.add_node(target)
                self.add_edge(elem, target, type=rel)

    def export_graphml(self, path):
        nx.write_graphml(self.graph, path)
        print(f"Esportato grafo in {path}")

# Esempio d'uso:
if __name__ == '__main__':
    kg = KnowledgeGraph()
    # Struttura minima
    entries = [
        ('INFRASTRUTTURE_WEB', 'DNS', 'include', None),
        ('DNS', 'DNS_Records', 'composizione', None),
        ('DNS_Records', 'CNAME', 'tipo', None),
        ('DNS_Records', 'A', 'tipo', None),
        ('DNS_Records', 'AAAA', 'tipo', None),
        ('DNS_Records', 'MX', 'tipo', None),
        ('DNS_Records', 'Aruba', 'esempio', None),
    ]
    kg.from_chat(entries)
    kg.export_graphml('dns_knowledge.graphml')
```

**Spiegazioni:**

* **NetworkX**: libreria Python per grafi.
* **DiGraph**: grafo diretto, utile per rappresentare gerarchie e relazioni.
* **Estrarre Chat**: il metodo `from_chat` potrebbe essere esteso per fare parsing automatico di log di conversazione.
* **Export**: formato GraphML per import in strumenti di visualizzazione (Gephi, Cytoscape).

---

### Prossimi Passi

1. **Estrazione automatica**: implementare parser che leggono la chat e generano `entries`.
2. **Arricchimento nodi**: aggiungere attributi come descrizione, link a documentazione.
3. **Interfaccia di navigazione**: usare librerie web (es. D3.js) per un front-end interattivo.

Spero che questo report e il prototipo ti aiutino a organizzare e approfondire il sistema DNS! 🚀
