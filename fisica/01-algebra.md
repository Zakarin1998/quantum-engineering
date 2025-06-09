# Spazi e sottospazi vettoriali, basi, dimensione e cambio di base

Di seguito una **lezione strutturata** in Markdown sui concetti di **spazi vettoriali**, **sottospazi**, **basi**, **dimensione** e **cambi di base**.

---

## 1. Spazi vettoriali

### Definizione

Uno **spazio vettoriale** $V$ su un campo $ \Bbb K$ (tipicamente $\R$ o $\C$) è un insieme dotato di due operazioni:

1. **Somma** $+: V \times V \to V$
2. **Moltiplicazione per scalare** $\cdot: \Bbb K \times V \to V$

che soddisfano gli 8 assiomi (associatività, commutatività, elemento neutro, inverso, e distributività rispetto a somma vettoriale e somma di scalari, e compatibilità).

> **Esempio:** $\R^n$ con la somma componente-per-componente e la moltiplicazione scalare usuale è uno spazio vettoriale su $\R$.

---

## 2. Sottospazi vettoriali

### Definizione

Un sottoinsieme $W \subseteq V$ è un **sottospazio vettoriale** se, con le stesse operazioni di $V$:

1. **Chiusura sotto somma:** se $u,v\in W$ allora $u+v\in W$.
2. **Chiusura sotto moltiplicazione scalare:** se $u\in W$ e $\alpha\in \Bbb K$, allora $\alpha u\in W$.
3. (Equivalente) $W$ contiene lo $0$ di $V$ e chiusura per combinazioni lineari.

> **Esempio:**
>
> * In $\R^3$, il piano «$z=0$» è sottospazio vettoriale.
> * L’insieme delle soluzioni di un sistema omogeneo $A\,x=0$ è sempre un sottospazio.

---

## 3. Basi di uno spazio vettoriale

### Definizione di **vettore linearmente indipendente**

Un insieme $\{v_1,\dots,v_k\}\subset V$ è **linearmente indipendente** se

$$
\alpha_1 v_1 + \cdots + \alpha_k v_k = 0
\;\Longrightarrow\;
\alpha_1 = \alpha_2 = \cdots = \alpha_k = 0.
$$

### Definizione di **spanning set**

Un insieme $\{v_1,\dots,v_m\}$ **genera** (o span) $V$ se ogni $v\in V$ si scrive come combinazione lineare di essi:

$$
v = \beta_1 v_1 + \cdots + \beta_m v_m.
$$

### Base di $V$

Una **base** di $V$ è un insieme di vettori $\{e_1,\dots,e_n\}$ che è contemporaneamente:

1. **Linearmente indipendente**,
2. **Generatore** di $V$.

> **Proprietà fondamentale:**
> Ogni vettore $v\in V$ si esprime in modo **unico** tramite coordinate relative alla base:
>
> $$
> v = x_1 e_1 + x_2 e_2 + \cdots + x_n e_n.
> $$

---

## 4. Dimensione

### Definizione

La **dimensione** di uno spazio vettoriale $V$, denotata $\dim V$, è il **numero** di vettori in **qualsiasi** sua base.

* Se $V$ ha base finita, $\dim V = n$.
* Se non esiste base finita, si dice che $V$ ha dimensione infinita.

> **Esempio:**
>
> * $\dim\R^3 = 3$.
> * Lo spazio di tutti i polinomi reali ha dimensione infinita.

---

## 5. Cambi di base

### Coordinate in basi diverse

Siano $\mathcal{E} = \{e_1,\dots,e_n\}$ e $\mathcal{F} = \{f_1,\dots,f_n\}$ due basi di $V$.

* A un vettore $v$ corrispondono coordinate $[v]_{\mathcal{E}} = (x_1,\dots,x_n)^T$ tali che $v = \sum x_i e_i$.
* Analogamente $[v]_{\mathcal{F}} = (y_1,\dots,y_n)^T$.

### Matrice di cambio di base

Esiste una **matrice invertibile** $P\in M_{n\times n}(\Bbb K)$ tale che

$$
[v]_{\mathcal{E}} \;=\; P\, [v]_{\mathcal{F}}.
$$

* Le **colonne** di $P$ sono le coordinate dei vettori $f_j$ espresse nella base $\mathcal{E}$:

  $$
  f_j = \sum_{i=1}^n P_{ij}\,e_i.
  $$
* Invertendo: $[v]_{\mathcal{F}} = P^{-1}\,[v]_{\mathcal{E}}$.

### Esempio pratico

1. In $\R^2$, prendi
   $\mathcal{E} = \{e_1=(1,0),\,e_2=(0,1)\}$ (base canonica),
   $\mathcal{F} = \{f_1=(1,1),\,f_2=(-1,2)\}$.
2. Calcola le coordinate di $f_1,f_2$ rispetto a $\mathcal{E}$:

   $$
   f_1 = 1\cdot e_1 + 1\cdot e_2,\quad
   f_2 = -1\cdot e_1 + 2\cdot e_2.
   $$
3. La matrice di cambio $P$ da $\mathcal{F}$ a $\mathcal{E}$ è

   $$
   P = \begin{pmatrix}
     1 & -1\\
     1 &  2
   \end{pmatrix},\quad
   [v]_{\mathcal{E}} = P\,[v]_{\mathcal{F}}.
   $$

---

## 6. Esercizi consigliati

1. **Verifica sottospazio:**
   $\{(x,y,z)\in\R^3 : x + 2y - z = 0\}$.
2. **Costruisci una base** per lo spazio dei polinomi di grado ≤ 2.
3. **Dimensione e indipendenza:**
   Dimostra che in uno spazio vettoriale di dimensione $n$ ogni insieme di più di $n$ vettori è linearmente dipendente.
4. **Cambio di base**:
   Data $\mathcal{E}$ e $\mathcal{F}$ in $\R^3$, calcola la matrice di cambio e trasforma le coordinate di un vettore.


## Esercizio 1

Perfetto: iniziamo con il **Primo esercizio** — verificare che

$$
W = \{(x,y,z)\in\R^3 : x + 2y - z = 0\}
$$

sia un **sottospazio vettoriale** di $\R^3$. Procediamo passo-passo seguendo la definizione.

---

## Esercizio 1: $W = \{(x,y,z): x + 2y - z = 0\}$

Per dimostrare che $W\subseteq \R^3$ è un sottospazio, verifichiamo i tre criteri:

1. **Zero**: lo $0$ di $\R^3$ appartiene a $W$.
2. **Chiusura per somma**: se $u,v\in W$, allora $u+v\in W$.
3. **Chiusura per moltiplicazione scalare**: se $u\in W$ e $\alpha\in\R$, allora $\alpha\,u\in W$.

---

### 1. Il vettore zero

* Lo zero di $\R^3$ è $\mathbf{0} = (0,0,0)$.
* Calcolo: $0 + 2\cdot0 - 0 = 0$.
* Quindi $\mathbf{0}$ soddisfa l’equazione e $\mathbf{0}\in W$.

> **Conclusione:** $W$ contiene lo $0$.

---

### 2. Chiusura per somma

Siano

$$
u = (x_1,y_1,z_1),\quad v = (x_2,y_2,z_2)
$$

due elementi di $W$. Allora:

1. Poiché $u\in W$, $x_1 + 2y_1 - z_1 = 0$.
2. Poiché $v\in W$, $x_2 + 2y_2 - z_2 = 0$.

Consideriamo la loro somma:

$$
u + v = (x_1 + x_2,\;y_1 + y_2,\;z_1 + z_2).
$$

Verifichiamo l’equazione per $u+v$:

$$
(x_1 + x_2) \;+\; 2(y_1 + y_2)\;-\; (z_1 + z_2)
= (x_1 + 2y_1 - z_1)\;+\;(x_2 + 2y_2 - z_2)
= 0 + 0 = 0.
$$

Quindi $u + v$ appartiene ancora a $W$.

> **Conclusione:** $W$ è chiuso rispetto alla somma.

---

### 3. Chiusura per moltiplicazione scalare

Sia $u = (x,y,z)\in W$ e $\alpha\in\R$. Allora $x + 2y - z = 0$. Consideriamo:

$$
\alpha\,u = (\alpha x,\;\alpha y,\;\alpha z).
$$

Verifichiamo:

$$
(\alpha x) \;+\; 2(\alpha y)\;-\; (\alpha z)
= \alpha (x + 2y - z)
= \alpha \cdot 0 = 0.
$$

Quindi $\alpha\,u \in W$.

> **Conclusione:** $W$ è chiuso rispetto alla moltiplicazione per scalare.

---

## Conclusione complessiva

Avendo verificato:

1. $\mathbf{0} \in W$,
2. $u,v\in W \implies u+v\in W$,
3. $u\in W,\,\alpha\in\R \implies \alpha u\in W$,

possiamo affermare che **$W$ è un sottospazio vettoriale di $\R^3$**.

---

Se tutto chiaro, procediamo con l’**Esercizio 2**!

## Esercizio 2
