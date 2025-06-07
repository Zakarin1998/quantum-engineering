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
