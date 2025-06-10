## **Lezione Universitaria: Equazione d’Onda Classica nella Teoria dei Campi**

---

## 1. Introduzione alla Teoria dei Campi e alle Onde

* **Definizione di campo**: funzione continua (o distribuzione) che associa ad ogni punto dello spazio-tempo una o più grandezze fisiche (es. spostamento, potenziale, intensità di campo).
* **Fenomenologia delle onde**: propagazione di perturbazioni di un campo; esemplificata dal suono, dalle onde elettromagnetiche, dalle vibrazioni meccaniche.
* **Obiettivo**: derivare e studiare l’equazione d’onda, un’equazione alle derivate parziali lineare del secondo ordine, che governa la dinamica di tali perturbazioni in un mezzo continuo.

---

## 2. Derivazione dell’Equazione d’Onda Unidimensionale

Consideriamo una corda elastica tensionata, di densità lineare \$\rho\$ e tensione \$T\$, parametrizzata dalla coordinata spaziale \$x\$ e dal tempo \$t\$.

1. **Equilibrio delle forze**
   Su un elemento infinitesimo di corda di lunghezza \$dx\$, le forze orizzontali di tensione ai due estremi sono

   $$
     T\,\frac{\partial y}{\partial x}\bigg|_{x+dx}
     \;-\;
     T\,\frac{\partial y}{\partial x}\bigg|_{x}
     \;\approx\;
     T\,\frac{\partial^2 y}{\partial x^2}\,dx.
   $$

2. **Forza di massa inerziale**
   La massa dell’elemento è \$\rho,dx\$, perciò la sua accelerazione verticale \$\partial\_{tt}y\$ genera una forza

   $$
     F_{\rm inerziale}
     =
     \rho\,dx\;\frac{\partial^2 y}{\partial t^2}.
   $$

3. **Applicazione della Seconda Legge di Newton**
   Ponendo somma delle forze uguale a massa per accelerazione:

   $$
     \rho\,dx\;\frac{\partial^2 y}{\partial t^2}
     =
     T\,\frac{\partial^2 y}{\partial x^2}\,dx.
   $$

   Semplificando \$dx\$ su entrambi i membri otteniamo l’**equazione d’onda unidimensionale**:

   $$
     \boxed{
       \frac{\partial^2 y(x,t)}{\partial t^2}
       =
       v^2 \;\frac{\partial^2 y(x,t)}{\partial x^2}
       \,\quad
       v = \sqrt{\frac{T}{\rho}}\;.
     }
   $$

In questa forma, \$v\$ è la velocità di propagazione delle onde lungo la corda.

---

### Spiegazione dettagliata passo per passo

Per completezza, ecco un’esposizione più approfondita dei singoli passaggi:

1. **Elemento infinitesimo e massa**

   * Tratto di corda di lunghezza \$dx\$ centrato in \$x\$.
   * Massa \$m = \rho,dx\$.

2. **Forze di tensione**

   * All'angolo \$\theta(x)\$, \$\sin\theta(x) \approx \partial\_x y(x,t)\$.
   * Componente verticale al punto \$x\$: \$T\sin\theta(x) \approx T,\partial\_x y(x,t)\$.
   * Risultante verticale tra \$x\$ e \$x+dx\$:

     $$
       T\,\partial_x y(x+dx,t) - T\,\partial_x y(x,t) \approx T\,\partial_{xx}y(x,t)\,dx.
     $$

3. **Forza d’inerzia**

   * Accelerazione verticale \$\partial\_{tt}y(x,t)\$.
   * Forza: \$m,\partial\_{tt}y = \rho,dx;\partial\_{tt}y(x,t)\$.

4. **Seconda legge**

   * \$\rho,dx;\partial\_{tt}y = T,\partial\_{xx}y,dx\$.
   * Divide per \$dx\$ e introduce \$v=\sqrt{T/\rho}\$.

5. **Equazione d’onda**

   * Forma finale \$\partial\_{tt}y = v^2,\partial\_{xx}y\$.

6. **Interpretazione**

   * \$\partial\_{xx}y\$ è la curvatura: con curvatura verso il basso, la tensione genera forza verso l’alto.
   * La velocità di propagazione \$v\$ cresce con la tensione e diminuisce con la densità.

---

### Principi fondamentali

Considerando quindi una corda elastica tensionata, di densità lineare $\rho$ e tensione $T$, parametrizzata dalla coordinata spaziale $x$ e dal tempo $t$, entrano in gioco i seguenti fattori:

1. **Equilibrio delle forze**
   Su un elemento infinitesimo di corda di lunghezza $dx$, le forze orizzontali di tensione ai due estremi sono

   $$
     T\,\frac{\partial y}{\partial x}\bigg|_{x+dx}
     \;-\;
     T\,\frac{\partial y}{\partial x}\bigg|_{x}
     \;\approx\;
     T\,\frac{\partial^2 y}{\partial x^2}\;dx.
   $$

2. **Forza di massa inerziale**
   La massa dell’elemento è $\rho\,dx$, perciò la sua accelerazione verticale $\partial_{tt}y$ genera una forza

   $$
     F_{\rm inertia}
     =
     \rho\,dx\;\frac{\partial^2 y}{\partial t^2}.
   $$

3. **Applicazione della Seconda Legge di Newton**
   Ponendo somma delle forze uguale a massa per accelerazione:

   $$
     \rho\,dx\;\frac{\partial^2 y}{\partial t^2}
     =
     T\,\frac{\partial^2 y}{\partial x^2}\;dx.
   $$

   Semplificando $dx$ su entrambi i membri otteniamo l’**equazione d’onda unidimensionale**:

   $$
     \boxed{
       \frac{\partial^2 y(x,t)}{\partial t^2}
       =
       v^2 \;\frac{\partial^2 y(x,t)}{\partial x^2}
       \,,\quad
       v \;=\;\sqrt{\frac{T}{\rho}}\;.
     }
   $$

In questa forma, $v$ è la velocità di propagazione delle onde lungo la corda.
---

## 3. Forma Generale in Più Dimensioni

Per un campo scalare \$\phi(\mathbf{r},t)\$ in uno spazio euclideo tridimensionale, l’equazione d’onda libera (assenza di sorgenti) è
$\boxed{\partial_{tt}\phi(\mathbf{r},t) = c^2\,\nabla^2\phi(\mathbf{r},t)\,,}$
dove \$\nabla^2\$ è il Laplaciano spaziale e \$c\$ la velocità di propagazione nel campo.

---

## 4. Soluzioni Generali: Metodo di d’Alembert (1D)

Nel caso unidimensionale, definendo le variabili caratteristiche
$\xi = x - vt\,,\quad \eta = x + vt\,, $
la soluzione generale è
$\phi(x,t) = f(\xi) + g(\eta),$
con \$f\$ e \$g\$ funzioni arbitrarie determinabili dalle condizioni iniziali:

* **Condizioni iniziali**: \$\phi(x,0)=\phi\_0(x)\$ e \$\partial\_t\phi(x,0)=\psi\_0(x)\$.
* **Espressioni di d’Alembert**:
  \begin{align\*}
  f(\xi) &= \tfrac12\Bigl\[\phi\_0(\xi)+\tfrac{1}{v}!\int^{\xi} \psi\_0(s),ds\Bigr],\\
  g(\eta)&=\tfrac12\Bigl\[\phi\_0(\eta)-\tfrac{1}{v}!\int^{\eta} \psi\_0(s),ds\Bigr].
  \end{align\*}

---

## 5. Condizioni al Contorno e Modali Normali

* **Corda con estremi fissi** (\$x=0,L\$):
  $y(0,t)=y(L,t)=0.$
  Le soluzioni stazionarie (modi normali) sono
  $y_n(x,t)=A_n\sin\!\Bigl(\tfrac{n\pi x}{L}\Bigr)\cos(\omega_n t+\delta_n)\,,\quad \omega_n = \tfrac{n\pi v}{L},\;n\in\mathbb{N}^+.$
* Ogni modo si propaga con frequenza propria, illustrando la **quantizzazione** delle frequenze in un dominio finito.

---

## 6. Energia dell’Onda

La densità di energia (per unità di lunghezza o di volume) è la somma di energia cinetica e potenziale elastiche:
$\mathcal{E} = \underbrace{\tfrac12\,\rho\;(\partial_t\phi)^2}_{\text{cinetica}} + \underbrace{\tfrac12\,T\;(\partial_x\phi)^2}_{\text{potenziale}}.$
Il flusso di energia (l’intensità dell’onda) lungo la corda è
$S = -\,T\,\partial_t\phi\,\partial_x\phi\,,$
e soddisfa l’equazione di conservazione
$\partial_t\mathcal{E} + \partial_x S = 0.$

---

## 7. Onde Elettromagnetiche: Equazione d’Onda del Potenziale

Nel vuoto, a partire dalle equazioni di Maxwell si ottiene per il potenziale vettore \$\mathbf{A}\$ in gauge di Lorentz:
$\Box\,\mathbf{A} = \bigl(\nabla^2 - \tfrac{1}{c^2}\partial_{tt}\bigr)\mathbf{A} = -\mu_0\,\mathbf{J},$
e analogamente per il potenziale scalare \$\Phi\$. In assenza di correnti cariche:
$\Box\,\mathbf{A} = 0,\quad \Box\,\Phi = 0,$
cioè onde piane elettromagnetiche che viaggiano alla velocità \$c\$.

---

## 8. Velocità di Fase e di Gruppo

Per soluzioni armoniche del tipo
$\phi(\mathbf{r},t)=\mathrm{Re}\{A\,e^{i(\mathbf{k}\cdot\mathbf{r}-\omega t)}\},$

* **Relazione di dispersione**: \$\omega=\omega(\mathbf{k})\$.
* **Velocità di fase**: \$v\_p=\omega/|\mathbf{k}|\$.
* **Velocità di gruppo**: \$v\_g = \nabla\_{\mathbf{k}}\omega(\mathbf{k})\$.
  In un mezzo non dispersivo \$\omega = c|\mathbf{k}|\$, dunque \$v\_p = v\_g = c\$.

---

## 9. Onde Stazionarie e Onde Progressive

* **Onda progressiva**: spostamento costante del profilo nel tempo (p.es. senoide che si propaga).
* **Onda stazionaria**: sovrapposizione di onde progressive contrarie, tipica nei sistemi risonanti.

---

## 10. Esempi Applicativi

1. **Cordiera sonora**: vibrazione di corde di strumenti musicali.
2. **Onde elettromagnetiche**: propagazione di segnali radio e luce.
3. **Onde sismiche**: propagazione delle onde di compressione e taglio nel substrato terrestre (equazioni del tipo elastodinamico).

---

## 11. Conclusioni e Spunti Avanzati

* L’equazione d’onda classica è un caso particolare di campo libero lineare.
* In teoria quantistica dei campi, si quantizzano le soluzioni modali per ottenere fotoni, fononi, ecc.
* In mezzi non lineari o non omogenei si ottengono fenomeni più ricchi: **solitoni**, **dispersive shocks**, **scattering**.

---

### Bibliografia Consigliata

* L.D. Landau, E.M. Lifshitz, *Teoria dei Campi*.
* J.D. Jackson, *Classical Electrodynamics*.
* G. B. Arfken, H. J. Weber, *Mathematical Methods for Physicists*.

**Alla prossima lezione**: approfondiremo la quantizzazione delle onde e i concetti di campo quantistico.
