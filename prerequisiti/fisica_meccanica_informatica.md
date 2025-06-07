# **Report Scientifico: Fondamenti di Fisica, Meccanica e Informatica Quantistica**

---

## 1. Principi Fondamentali della Meccanica Quantistica

### 1.1 Principio di Indeterminazione di Heisenberg

* Formula:

$$
\sigma_x\,\sigma_p \;\ge\; \frac{\hbar}{2}
$$

dove

* $\sigma_x$ = deviazione standard della posizione
* $\sigma_p$ = deviazione standard dell’impulso
* $\hbar = \dfrac{h}{2\pi}$ costante di Planck ridotta




### 1.2 Equazione di Schrödinger

* **Dipendente dal tempo**:

$$
i\hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t) 
= \hat H\,\Psi(\mathbf{r},t)
$$

* **Stazionaria** (autovalori dell’Hamiltoniana):

$$
\hat H\,\psi_n(\mathbf{r}) = E_n\,\psi_n(\mathbf{r})
$$

con
$\hat H = -\dfrac{\hbar^2}{2m}\nabla^2 + V(\mathbf{r})$

### 1.3 Sovrapposizione e Collasso di Stato

* Stato generico di sovrapposizione:

$$
|\Psi\rangle = \sum_{n} c_n \,|n\rangle,
\quad \sum_n |c_n|^2 = 1
$$

* Probabilità di outcome $n$: $P(n) = |c_n|^2$
* Postulato di misura (collasso): al momento della misura, lo stato proietta su $|n\rangle$.

### 1.4 Entanglement

* Stato entangled di due particelle (Bell):

$$
|\Phi^+\rangle = \frac{1}{\sqrt{2}}\bigl(|00\rangle + |11\rangle\bigr)
$$

Proprietà: non fattorizzabile in prodotti di stati singoli.

---

## 2. Struttura Matematica e Operatori

### 2.1 Spazio di Hilbert

* Vettori di stato $|\Psi\rangle$ in uno spazio vettoriale completo con prodotto scalare.
* Norma: $\langle\Psi|\Psi\rangle = 1$.

### 2.2 Operatori Lineari Hermitiani

* Osservabili $\hat A = \hat A^\dagger$
* Autovalori reali $a$ e autostati $|a\rangle$ con ortonormalità $\langle a|a'\rangle = \delta_{aa'}$.

### 2.3 Operatori Unitari

* Evoluzione temporale:
  $\hat U(t) = e^{-\frac{i}{\hbar}\hat H\,t}$,
  con $\hat U^\dagger \hat U = \mathbb{I}$.

---

## 3. Decoerenza e Misura

### 3.1 Decoerenza Quantistica

* Descrive la perdita di coerenza tra i termini di sovrapposizione a causa dell’interazione con l’ambiente.
* Modello di canale di decoerenza (es. canale di dephasing):

$$
\rho \;\mapsto\; (1-p)\,\rho \;+\; p\,\sigma_z\,\rho\,\sigma_z
$$

### 3.2 Postulati della Misura

* Proiezione su uno dei proiettori $P_n$:

$$
\rho \;\mapsto\; \frac{P_n\,\rho\,P_n}{\mathrm{Tr}\bigl(P_n\,\rho\bigr)},
\quad P_n = |n\rangle\langle n|
$$

* Probabilità di ottenere l’esito $n$: $\mathrm{Tr}(P_n\,\rho)$.

---

## 4. Informatica Quantistica

### 4.1 Qubit e Spazio di Stato

* Stato generico di un qubit:

$$
|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle,
\quad |\alpha|^2 + |\beta|^2 = 1
$$

* Rappresentazione sulla sfera di Bloch: coordinate $(\theta,\phi)$.

### 4.2 Porte Quantistiche (Operatori Unutari)

* **Porte fondamentali**:

  * Pauli–X: $X = \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}$
  * Pauli–Z: $Z = \begin{pmatrix}1 & 0\\0 & -1\end{pmatrix}$
  * Hadamard: $H = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1\\1 & -1\end{pmatrix}$
  * CNOT (controllo-bersaglio su 2 qubit)

### 4.3 Algoritmi Quantistici di Base

* **Algoritmo di Deutsch-Jozsa**: distingue funzioni bilanciate da costanti in un’unica valutazione.
* **Algoritmo di Grover**: ricerca non-ordinata in $O(\sqrt{N})$ con iterazioni di amplificazione.
* **Algoritmo di Shor**: fattorizzazione in tempo polinomiale basato su trasformata discreta di Fourier quantistica.

### 4.4 Teorema di No-Cloning

* Non esiste operatore unitario $U$ tale che

$$
U\bigl(|\psi\rangle\otimes|0\rangle\bigr)
= |\psi\rangle\otimes|\psi\rangle
$$

per ogni $|\psi\rangle$.

---

## 5. Conclusioni

Questo report riassume i **concetti chiave e le formulazioni matematiche** che connettono la meccanica quantistica alla futura pratica del quantum engineering e dell’informatica quantistica. La relazione tra **osservazione**, **sovrapposizione**, **entanglement** e **misura** crea il fondamento sia per la ricerca teorica sia per lo sviluppo di **quantum hardware** e **algoritmi** avanzati.


Di seguito un’esposizione **estensiva** e dettagliata sui punti 1.1 e 1.2, con tutti i riferimenti storici, matematici e le connessioni con teoria dei segnali e Fisica II.

---

## 1. Principio di Indeterminazione di Heisenberg

### 1.1 Definizione e contesto storico

* **Origine (1927)**: Werner Heisenberg introdu­ce il principio per spiegare perché non si può misurare contemporaneamente con precisione arbitrar­ia posizione e quantità di moto di una particella.
* **Significato fisico**: c’è un limite intrinseco alla nostra capacità di conoscere simultaneamente certe coppie di osservabili (posizione – momento, energia – tempo, fase – numero di particelle, ecc.).

### 1.2 Deviazione standard in statistica

Per un operatore $\hat A$ (es. posizione $\hat x$ o impulso $\hat p$) in uno stato $|\Psi\rangle$, definiamo:

1. **Valore medio**

   $$
     \langle\hat A\rangle \;=\; \langle\Psi|\hat A|\Psi\rangle
   $$
2. **Varianza**

   $$
     \mathrm{Var}(A) 
     = \langle(\hat A - \langle\hat A\rangle)^2\rangle
     = \langle\hat A^2\rangle - \langle\hat A\rangle^2
   $$
3. **Deviazione standard**

   $$
     \sigma_A = \sqrt{\mathrm{Var}(A)}.
   $$

Qui $\sigma_x$ misura la “dispersione” delle misure di posizione, $\sigma_p$ quella dell’impulso.

### 1.3 Derivazione del principio

1. **Commutatore**

   $$
     [\hat x,\hat p] = \hat x\,\hat p - \hat p\,\hat x = i\hbar.
   $$
2. **Disuguaglianza di Robertson–Schrödinger**
   Per due operatori Hermitiani generici $\hat A$, $\hat B$:

   $$
     \sigma_A\,\sigma_B
     \;\ge\;
     \frac{1}{2}\bigl|\langle[\hat A,\hat B]\rangle\bigr|.
   $$

   Sostituendo $\hat A=\hat x$, $\hat B=\hat p$ otteniamo

   $$
     \sigma_x\,\sigma_p \;\ge\; \frac{1}{2}\bigl|\langle i\hbar\rangle\bigr|
     = \frac{\hbar}{2}.
   $$

### 1.4 Interpretazione e analogia in teoria dei segnali

* **Dualismo tempo–frequenza**:
  un segnale $f(t)$ e la sua trasformata di Fourier
  $\tilde f(\omega)=\int e^{-i\omega t}f(t)\,dt$ soddisfano

  $$
    \sigma_t\,\sigma_\omega \;\ge\; \frac{1}{2}.
  $$
* **Correlazione**:

  * $\displaystyle \omega\leftrightarrow k$ (numero d’onda)
  * $\displaystyle p=\hbar k\implies k=p/\hbar$
  * Dividendo per $\hbar$ si passa da $\sigma_p$ a $\sigma_k$.
* **Fisica II – onde classiche**:
  la descrizione di pacchetti d’onda in una corda vibrante usa la stessa matematica di Fourier e porta a una limitazione analoga tra ampiezza temporale e larghezza spettrale.

---

## 2. Equazione di Schrödinger

### 2.1 Contesto e forma generale

L’equazione di Schrödinger è la versione quantistica dell’equazione d’onda, che governa l’evoluzione temporale della **funzione d’onda** $\Psi(\mathbf r,t)$.

#### 2.1.1 Forma dipendente dal tempo

$$
  i\hbar\,\frac{\partial}{\partial t}\,\Psi(\mathbf r,t)
  = \hat H\,\Psi(\mathbf r,t),
  \quad
  \hat H = -\frac{\hbar^2}{2m}\nabla^2 + V(\mathbf r).
$$

#### 2.1.2 Equazione stazionaria

Se cerchiamo soluzioni del tipo
$\Psi(\mathbf r,t)=\psi(\mathbf r)\,e^{-iEt/\hbar}$,
allora

$$
  \hat H\,\psi(\mathbf r) = E\,\psi(\mathbf r).
$$

### 2.2 Da dove viene

1. **Sostituzioni energia–operatore**

   * **Energia classica** $E = T + V = p^2/(2m) + V(\mathbf r)$.
   * In QM si fa la “regola di quantizzazione”:

     $$
       E \;\to\; i\hbar\,\frac{\partial}{\partial t},
       \quad
       \mathbf p \;\to\; -\,i\hbar\nabla.
     $$
2. **Principio di Soviet–de Broglie**
   Louis de Broglie propose $\lambda = h/p$, ossia ogni particella ha lunghezza d’onda $\lambda$.
3. **Lineare e unitarietà**
   Si richiede che l’evoluzione mantenga $\langle\Psi|\Psi\rangle=1$ (conservazione della probabilità) e sia lineare (sovrapposizione di soluzioni).

### 2.3 La costante di Planck $h$

* **Scoperta (1900)**: Max Planck, studiando lo spettro di radiazione del corpo nero, introdusse $E=h\nu$.
* **Valore**: $h\approx6.626\times10^{-34}\,\mathrm J\cdot\mathrm s$.
* **Perché $\hbar=h/2\pi$?**

  * Nella rappresentazione tramite trasformate di Fourier in coordinate angolari e nei momenti angolari, i fattori $2\pi$ compaiono naturalmente.
  * Usando $\hbar$ le formule diventano più compatte (es. $[\hat x,\hat p]=i\hbar$ anziché $i\,h/2\pi$).

---

## 3. Collegamenti interdisciplinari

| Dominio                  | Equazione tipica                                  | Analogia quantistica                                                       |
| ------------------------ | ------------------------------------------------- | -------------------------------------------------------------------------- |
| Segnali (Time–Frequency) | $\tilde f(\omega)=\int f(t)e^{-i\omega t}dt$      | $\Psi(\mathbf k)=\int\Psi(\mathbf r)\,e^{-i\mathbf k\cdot\mathbf r}\,d^3r$ |
| Onde classiche           | $\frac{\partial^2y}{\partial t^2} = v^2\nabla^2y$ | $\hat H\Psi = i\hbar\,\partial_t\Psi$                                      |
| Meccanica classica       | $L=T-V$, equazioni di Lagrange                    | Principio di azione → formulazione di Feynman                              |

1. **Pacchetto d’onda** (Fisica II):
   la somma di sinusoidi di diverse frequenze crea un “pacchetto” con ampiezza concentrata; la sua dispersione nel tempo è analoga al collasso quantistico.
2. **Risonanza e autovalori**:
   i modi normali di una corda o di un tubo sonoro sono autostati di un operatore lineare, come gli stati stazionari di $\hat H$.

---

### Conclusione estesa

* Il **principio di indeterminazione** e l’**equazione di Schrödinger** sono i pilastri matematici e concettuali della meccanica quantistica.
* Entrambi hanno **ombre** (il collasso, la misura, la decoerenza) che aprono le porte a interpretazioni filosofiche e spirituali, ma la loro **solida base fisico-matematica** è la stessa utilizzata in segnali, onde classiche e teoria dei campi.
* Per chi si avvia al **quantum engineering**, padroneggiare questi concetti significa saper tradurre fra **Fenomeno⟷Matematica⟷Applicazione Tecnologica**.

Spero che questo approfondimento ti dia un quadro chiaro, ricco di collegamenti e – al tempo stesso – pronto ad essere esteso sia sul piano teorico sia pratico. Se vuoi ulteriori dettagli (esempi di risoluzione per pozzi infiniti, oscillatori armonici quantistici, trasformata di Fourier discreta, canale di decoerenza, ecc.), fammi sapere!

