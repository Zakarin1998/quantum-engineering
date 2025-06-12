# Teoria dei Segnali

Questa immagine mostra una **visualizzazione della Serie di Fourier** applicata a un'**onda quadra**.

![image](https://github.com/user-attachments/assets/caadc7cf-aca3-411c-93cb-ff451071ee27)

### Descrizione dettagliata:

* In alto, si vedono **cerchi rotanti** colorati: rappresentano i **termini della serie di Fourier** come **vettori complessi** (in forma di esponenziali complessi o seni e coseni) che si sommano per ricostruire una funzione.

* Il punto finale dei vettori disegna la **funzione risultante** lungo il tempo: nel grafico in basso, vediamo l’**approssimazione di un’onda quadra**.

* L’onda quadra viene ricostruita tramite la **somma infinita di seni** con coefficienti decrescenti e frequenze dispari:

  $$
  f(x) = \frac{4}{\pi} \sum_{n=1}^{\infty} \frac{1}{2n - 1} \sin((2n - 1)x)
  $$

* La funzione rappresentata è definita a tratti:

  $$
  f(x) = 
  \begin{cases}
    -1, & -\pi < x < 0 \\
    0, & x = 0, -\pi, \pi \\
    1, & 0 < x < \pi
  \end{cases}
  $$

  È un’**onda quadra periodica** centrata sull’origine.

* Il punto in cui i cerchi si uniscono forma l'approssimazione nel dominio del tempo, e scorrendo a destra si vede come l'onda viene ricostruita via via con più termini.

### Curiosità:

* Questo tipo di animazione mostra bene **come funziona la trasformata di Fourier**, ed è spesso usato per spiegare come anche segnali complessi possono essere ottenuti da una somma di onde semplici (sine waves).
* L’effetto di “rimbalzo” vicino ai salti si chiama **fenomeno di Gibbs**.

## Trasformata di Fourier

La **Trasformata di Fourier** è uno strumento matematico fondamentale in teoria dei segnali: permette di passare dalla descrizione di un segnale nel dominio del tempo a quella nel dominio della frequenza, scomponendolo nelle sue componenti sinusoidali.

---

## 1. Definizione (segnale continuo)

Per un segnale $x(t)$ (solitamente con condizioni di “energia finita” o di tipo “segnale a tempo limitato”), la **Trasformata di Fourier** $X(f)$ è definita come

$$
X(f) \;=\; \int_{-\infty}^{\infty} x(t)\,e^{-j2\pi f t}\,\mathrm{d}t
$$

e la trasformata inversa (per ricostruire $x(t)$) è

$$
x(t) \;=\; \int_{-\infty}^{\infty} X(f)\,e^{j2\pi f t}\,\mathrm{d}f.
$$

Qui $f$ è la frequenza in Hz (oppure si usa la variabile angolare $\omega = 2\pi f$, con fattori $e^{-j\omega t}$ e $\tfrac{1}{2\pi}$ nelle formule).

---

## 2. Proprietà principali

1. **Linearità**
   $\mathcal{F}\{a\,x_1(t) + b\,x_2(t)\} = a\,X_1(f) + b\,X_2(f)$.

2. **Shifting**

   * **Tempo**: $x(t - t_0) \longleftrightarrow X(f)\,e^{-j2\pi f t_0}$.
   * **Frequenza**: $x(t)\,e^{j2\pi f_0 t} \longleftrightarrow X(f - f_0)$.

3. **Convoluzione**

   $$
   x(t) * h(t) \;\longleftrightarrow\; X(f)\,\cdot H(f).
   $$

   Utile perché il comportamento di un sistema lineare-invariante nel tempo (LTI) si studia in frequenza moltiplicando la sua risposta in frequenza $H(f)$ per $X(f)$.

4. **Dualità**
   Se $x(t)\leftrightarrow X(f)$, allora (formalmente) $X(t)\leftrightarrow x(-f)$.

5. **Parseval/Plancherel** (energia)

   $$
   \int_{-\infty}^\infty |x(t)|^2\,dt \;=\; \int_{-\infty}^\infty |X(f)|^2\,df.
   $$

6. **Proprietà di simmetria** (real signals)
   Se $x(t)$ è reale ⇒ $X(-f) = X^*(f)$.

---

## 3. Perché è utile in teoria dei segnali

* **Analisi spettrale**: vedere quali frequenze compongono un segnale (utile in acustica, elettronica, telecomunicazioni, radar…).
* **Progettazione di filtri**: in frequenza definisci $H(f)$ (passa-basso, passa-banda…), e applicando la convoluzione in tempo ottieni il filtraggio.
* **Modulazione**: spostare un segnale in banda (es. AM, FM), grazie allo shifting in frequenza.
* **Rilevazione di disturbi**: disturbi periodici o rumore si identificano facilmente nello spettro.
* **Compressione**: tecniche tipo MP3 o JPEG sfruttano la rappresentazione spettrale per eliminare componenti meno percepite.

---

## 4. Segnali campionati e DFT

Nel mondo digitale i segnali sono campionati a intervalli $\Delta t = 1/F_s$. Si usa la **Trasformata Discreta di Fourier (DFT)**:

$$
X[k] = \sum_{n=0}^{N-1} x[n]\,e^{-j2\pi\,\tfrac{kn}{N}}\,,\quad k=0,\dots,N-1
$$

e la **Fast Fourier Transform (FFT)** è l’algoritmo efficiente per calcolarla. Con la DFT otteniamo uno spettro a frequenze discrete $\displaystyle f_k = \frac{k}{N}\,F_s$.

---

## 5. Condizioni di esistenza

* **Segnali a energia finita** ($\int |x(t)|^2 < \infty$): si definisce la **Trasformata di Fourier in senso di energia**.
* **Segnali a potenza finita (periodici)**: si ricorre invece alle **serie di Fourier** (come nell’esempio che hai postato).

---

### Esempio pratico

1. **Rumore bianco**: ha spettro piatto—ogni frequenza è presente con uguale potenza.
2. **Sweep sinusoidale**: un “chirp” che aumenta la frequenza nel tempo; esaminando la sua FT si ottiene un’intensa curva in diagonale.
3. **Filtro passa-basso**: in frequenza tagli le componenti oltre una certa soglia; nel dominio del tempo l’effetto è una risposta all’impulso con sinc.

---

❓ Se ti interessa un dettaglio su un’applicazione specifica—ad es. progettazione di un filtro FIR/IIR, analisi modulazione digitale, o metodi numerici per FFT—dimmi pure!

---

```python
import numpy as np
import matplotlib.pyplot as plt

# Parameters
R = 1e3  # Resistance in Ohms
C = 1e-6  # Capacitance in Farads
RC = R * C
f = np.logspace(1, 6, 500)  # Frequency array from 10 Hz to 1 MHz
omega = 2 * np.pi * f

# Transfer functions
H_lp = 1 / (1 + 1j * omega * RC)
H_hp = (1j * omega * RC) / (1 + 1j * omega * RC)
H_bp = H_hp * H_lp

# Plot Low-Pass Filter Response
plt.figure()
plt.semilogx(f, 20 * np.log10(np.abs(H_lp)))
plt.title('Low-Pass RC Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)

# Plot High-Pass Filter Response
plt.figure()
plt.semilogx(f, 20 * np.log10(np.abs(H_hp)))
plt.title('High-Pass RC Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)

# Plot Band-Pass Filter Response
plt.figure()
plt.semilogx(f, 20 * np.log10(np.abs(H_bp)))
plt.title('Band-Pass RC Filter Frequency Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)

plt.show()
```

## Filtri Passa-Basso
Ecco un report tecnico esaustivo sui filtri passa-basso, passa-alto e passa-banda basati su RC (Resistenza-Condensatore), con formule, grafici di risposta in frequenza e cenni di elettronica.

---

## 1. Introduzione

Un **filtro** è un circuito che permette o attenua determinate bande di frequenza di un segnale. In elettronica passiva, i filtri più semplici si ottengono combinando resistori (R) e condensatori (C).

Gli elementi fondamentali:

* **Passa-basso (Low-Pass, LPF)**: lascia passare le basse frequenze, attenua le alte.
* **Passa-alto (High-Pass, HPF)**: lascia passare le alte frequenze, attenua le basse.
* **Passa-banda (Band-Pass, BPF)**: lascia passare una banda intermedia, attenua al di sotto e al di sopra.

---

## 2. Filtro Passa-Basso RC

### 2.1 Circuito

Un resistore e un condensatore in serie, l’uscita sul condensatore:

```
 Vin --- R ---+--- Vout
              |
              C
              |
             GND
```

### 2.2 Funzione di Trasferimento

$$
H_{LP}(j\omega)
= \frac{V_{out}}{V_{in}}
= \frac{1}{1 + j\,\omega\,R\,C}
= \frac{1}{1 + j\,\omega\,\tau}
$$

con $\tau = RC$.

* **Frequenza di taglio** $f_c$:

  $$
  f_c = \frac{1}{2\pi\,R\,C}
  $$

  a $\omega_c = 2\pi f_c$, $|H_{LP}| = 1/\sqrt{2}$ (\~ −3 dB).

### 2.3 Risposta in Frequenza

Grafico in dB (vedi figura “Low-Pass RC Filter Frequency Response” sopra):

* Guadagno vicino a 0 dB per $f\ll f_c$.
* Pendenza di −20 dB/decade per $f\gg f_c$.

---

## 3. Filtro Passa-Alto RC

### 3.1 Circuito

Un resistore e un condensatore in serie, l’uscita sul resistore:

```
 Vin --- C ---+--- Vout
              |
              R
              |
             GND
```

### 3.2 Funzione di Trasferimento

$$
H_{HP}(j\omega)
= \frac{j\,\omega\,R\,C}{1 + j\,\omega\,R\,C}
= \frac{j\,\omega\,\tau}{1 + j\,\omega\,\tau}
$$

* **Stessa frequenza di taglio** del passa-basso.

### 3.3 Risposta in Frequenza

Grafico in dB (figura “High-Pass RC Filter Frequency Response”):

* Attenua per $f\ll f_c$ con pendenza +20 dB/decade.
* Plateau a 0 dB per $f\gg f_c$.

---

## 4. Filtro Passa-Banda RC

### 4.1 Realizzazione

Si ottiene in cascata un HPF seguito da un LPF (o viceversa), con frequenze di taglio diverse $f_{c1}$ e $f_{c2}$:

$$
H_{BP}(j\omega)
= H_{HP}(j\omega; \tau_1)\,\times\,H_{LP}(j\omega; \tau_2).
$$

Nel nostro esempio abbiano usato $\tau_1 = \tau_2 = RC$ per dimostrazione, ottenendo un picco intorno a $f_c$.

### 4.2 Risposta in Frequenza

Grafico in dB (figura “Band-Pass RC Filter Frequency Response”):

* Attenuazione forte fuori banda.
* Banda passante centrata attorno a $f_c$, con guadagno massimo < 0 dB (somma di due −3 dB).

---

## 5. Analisi Elettronica

* **Componentistica**:
  - Resistenze standard e condensatori ceramici/elettrolitici.
  - Tolleranze e temperatura influenzano $f_c$.

* **Impedanza**:

  $$
  Z_C = \frac{1}{j\,\omega\,C}, 
  \quad Z_R = R.
  $$

* **Risposta al gradino**:

  * LPF: carica/esaurisce il condensatore con costante $\tau$.
  * HPF: breve picco seguito da zero, perché il condensatore si carica e blocca il DC.

* **Ordine del filtro**:

  * I RC sono del **primo ordine** (slope ±20 dB/decade).
  * Filtri di ordine superiore si ottengono in catena o usando amplificatori operazionali (active filters) per pendenze più ripide.

---

## 6. Conclusioni

I filtri RC sono il punto di partenza in teoria dei segnali e in elettronica:

* **Semplicità** e costo basso.
* **Base** per progetti più complessi (filtri attivi, Butterworth, Chebyshev, ecc.).
* Fondamentali in elaborazione digitale (limitazione banda, antialiasing) ed elettronica analogica.

Se ti servono approfondimenti su:

* Progettazione di filtri attivi (op-amp).
* Filtri di ordine superiore (Butterworth, Bessel, Chebyshev).
* Analisi di fase e risposta temporale.

fammi sapere!


