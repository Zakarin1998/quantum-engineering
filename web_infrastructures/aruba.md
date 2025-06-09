# Sistema dei DNS Aruba

Aruba ha un sistema DNS un po’ particolare che può creare confusione, ma ti aiuto passo per passo.

### Cambio link per Shopify

* **CNAME**: `www` → `shops.myshopify.com`
* **A**: `@` → `23.227.38.65`
* **AAAA**: `@` → `2620:127:f00f:5::`

I record A e AAAA li hai già aggiornati, quindi ci concentriamo sul **CNAME** per `www`.

---

### Aruba – come aggiungere un CNAME per `www`

1. **Vai alla gestione DNS**:
   Dal pannello di Aruba, entra nella gestione DNS del dominio `mellyskombucha.com`.

2. **Aggiungi un nuovo record CNAME**:

   * **Tipo**: CNAME
   * **Nome host**: **www**
     Questo campo a volte è già preimpostato e può apparire come “[www.mellyskombucha.com”](http://www.mellyskombucha.com”) (va bene così!).
   * **Valore** (o “Punta a” / “Destinazione”): `shops.myshopify.com`

3. **Salva le modifiche**.

4. **"Esiste già un record con questo nome"** Error Message:

    Se vedi questo messaggio, significa che su Aruba esiste già un record per `www.miodominio.com`. Probabilmente un CNAME o un A record. In questo caso, procedo con i punti 5 e 6:

5. **Elimina il record esistente** per `www`

    * Vai alla lista completa dei record DNS.
    * Trova quello con `www` come **Nome host**.
    * Dovrebbe essere un record A o CNAME esistente.
    * Cancellalo (ci sarà un’icona di cestino o un pulsante “Elimina”).

6. **Aggiungi il nuovo record CNAME**

    * Dopo aver eliminato quello vecchio, torna su “Aggiungi nuovo record”.
    * Scegli “CNAME”, Nome host `www`, Valore `shops.myshopify.com`.
    * Salva.


### 💡 Note importanti:

Aruba non permette di avere due record con lo stesso nome, ecco perché bisogna prima cancellare quello vecchio.

* Su Aruba, **Nome host = www** significa che stai modificando il `www.mellyskombucha.com` (perfetto!).
* Il **campo Nome** non deve essere modificato in altro: lascia proprio `www`.
* Il valore (o destinazione) del CNAME è quello che deve essere `shops.myshopify.com`.

---

### Esempio Aruba

Ecco come appare visivamente:

| Tipo  | Nome host | Valore              |
| ----- | --------- | ------------------- |
| CNAME | www       | shops.myshopify.com |

Se Aruba ti mostra un altro campo, tipo “Priorità” o simile, lascialo vuoto o su valore predefinito.

---

### DNS propagation

Dopo aver salvato, ci vorranno da pochi minuti fino a 24-48 ore perché la propagazione DNS si completi.

### Differenze tra i vari tipi di record DNS

Ti spiego infine il limite tecnico: **non puoi avere contemporaneamente un record A e un record CNAME per lo stesso nome**. Ecco le differenze tra i vari tipi di record DNS.

---

### 📌 Differenza tra record A, AAAA e CNAME

✅ **A record** → associa un hostname (es. `@` o `www`) a un indirizzo IPv4
✅ **AAAA record** → fa lo stesso, ma con un indirizzo IPv6
✅ **CNAME record** → dice che un hostname (`www`) deve comportarsi come un alias di un altro hostname (es. `shops.myshopify.com`)

---

### 🔥 Il limite “A/AAAA + CNAME”

* Puoi avere contemporaneamente un record A **e** un record AAAA per lo stesso nome (`@`, `www`…): uno IPv4, l’altro IPv6.
* **Ma** **non puoi avere un record CNAME per lo stesso nome** se esiste già un record A o AAAA.

💡 La RFC (le regole tecniche di Internet) dice:

> "CNAME non può coesistere con altri record per lo stesso nome"

Perché?
Il CNAME dice: “`www` è un alias, vai a chiedere direttamente a `shops.myshopify.com`.”
Se c’è anche un A/AAAA per `www`, la regola va in conflitto: chi è il “vero” destinatario?

---

### 🔑 Impostazioni iniziali di default alla creazione su Aruba e sintesi aggiornamento

* Puoi avere contemporaneamente:

  * A **e** AAAA (IPv4 e IPv6)
* Ma **CNAME** va da solo:

  * O **CNAME**
  * O **A/AAAA**

Quindi:
👉 Cancella A per `www`
👉 Inserisci il CNAME come Shopify ti chiede
👉 Il dominio `www.miodominio.com` punterà a Shopify

Fammi sapere se vuoi che ti aiuti a controllare i passaggi finali! 🚀

