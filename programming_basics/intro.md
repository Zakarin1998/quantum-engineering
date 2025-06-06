# Patterns GRASP e GoF

Eccoti un elenco completo e strutturato dei *pattern* GRASP e GoF. Li ho distinti chiaramente per aiutarti a studiarli e applicarli con efficacia.

---

## 🧠 GRASP (General Responsibility Assignment Software Patterns)

Fornisce 9 principi fondamentali per assegnare responsabilità in progettazioni OO ([en.wikipedia.org][1], [it.wikipedia.org][2], [kamilgrzybek.com][3]):

1. **Information Expert** – assegna la responsabilità all’oggetto che possiede le informazioni necessarie.
2. **Creator** – il compito di “creare” un oggetto va assegnato a chi già lo contiene, registra, o ha i dati per inizializzarlo.
3. **Controller** – un oggetto dedicato gestisce gli eventi del sistema (use-case), separando UI e logica.
4. **Low Coupling** – minimizza le dipendenze tra componenti per favorire la manutenibilità e il riuso.
5. **High Cohesion** – mantiene le classi focalizzate su compiti strettamente correlati.
6. **Polymorphism** – usa polimorfismo per gestire comportamenti varianti oltre l’istruzione if/else.
7. **Protected Variations** – isola le variazioni instabili dietro interfacce stabili con polimorfismo.
8. **Pure Fabrication** – introduce classi “artificiali” (es. servizi/factory) per preservare basso accoppiamento e alta coesione.
9. **Indirection** – utilizza oggetti intermedi per diminuire accoppiamento tra componenti.

---

## 🏗️ GoF (Gang of Four) Design Patterns

Sono 23 pattern organizzati in tre categorie, definiti nel libro *Design Patterns: Elements of Reusable Object‑Oriented Software* ([geeksforgeeks.org][4], [principles-wiki.net][5], [javaguides.net][6], [digitalocean.com][7]):

### 1. **Creational Patterns** (per la creazione di oggetti):

* Abstract Factory
* Builder
* Factory Method
* Prototype
* Singleton

### 2. **Structural Patterns** (per le relazioni e composizione):

* Adapter
* Bridge
* Composite
* Decorator
* Facade
* Flyweight
* Proxy

### 3. **Behavioral Patterns** (per l’interazione tra oggetti):

* Chain of Responsibility
* Command
* Interpreter
* Iterator
* Mediator
* Memento
* Observer
* State
* Strategy
* Template Method
* Visitor

---

### 🛠️ Tabella riassuntiva

| Categoria      | GRASP (9)                                                      | GoF (23)                                                                                                                        |
| -------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Creational** | Creator, Pure Fabrication                                      | Abstract Factory, Builder, Factory Method, Prototype, Singleton                                                                 |
| **Structural** | Indirection, Low Coupling, High Cohesion, Protected Variations | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy                                                                 |
| **Behavioral** | Controller, Polymorphism                                       | Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor |

---

Se vuoi approfondire applicazioni reali di ognuno o esempi in codice, fammelo sapere! Posso anche aiutarti a stabilire quando preferire GRASP rispetto ai pattern GoF e viceversa.

[1]: https://en.wikipedia.org/wiki/GRASP_%28object-oriented_design%29?utm_source=chatgpt.com "GRASP (object-oriented design)"
[2]: https://it.wikipedia.org/wiki/GRASP?utm_source=chatgpt.com "GRASP"
[3]: https://www.kamilgrzybek.com/blog/posts/grasp-explained?utm_source=chatgpt.com "GRASP - General Responsibility Assignment Software Patterns Explained"
[4]: https://www.geeksforgeeks.org/gang-of-four-gof-design-patterns/?utm_source=chatgpt.com "Gang of Four (GOF) Design Patterns - GeeksforGeeks"
[5]: https://principles-wiki.net/collections%3Agof_patterns?utm_source=chatgpt.com "GoF Patterns [Principles Wiki]"
[6]: https://www.javaguides.net/2024/11/cheat-sheet-for-gof-design-patterns.html?utm_source=chatgpt.com "Cheat Sheet for GoF Design Patterns - Java Guides"
[7]: https://www.digitalocean.com/community/tutorials/gangs-of-four-gof-design-patterns?utm_source=chatgpt.com "Gangs of Four (GoF) Design Patterns - DigitalOcean"
