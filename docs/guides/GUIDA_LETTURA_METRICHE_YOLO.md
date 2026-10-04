# Guida alla lettura delle metriche YOLO

Questa guida spiega come interpretare i risultati prodotti durante training,
validation, test e inferenza video di SemaforoSmart. Gli esempi fanno riferimento
alle classi `Ambulanza`, `Carabinieri` e `VigiliDelFuoco`.

## 1. Da dove nascono le metriche

Su un'immagine annotata esistono:

- una o piu' **ground truth**, cioe' le classi e i bounding box corretti;
- le **predizioni** prodotte dal modello, ciascuna con classe, bounding box e
  confidence.

Per decidere se una predizione corrisponde davvero a un oggetto annotato si
considerano insieme:

1. la classe prevista;
2. la sovrapposizione tra box previsto e box annotato, misurata tramite IoU;
3. la soglia minima di confidence scelta.

Da questo confronto derivano tre casi principali:

- **True Positive (TP)**: il mezzo viene trovato con classe e box accettabili;
- **False Positive (FP)**: il modello segnala un mezzo che non esiste oppure gli
  assegna la classe sbagliata;
- **False Negative (FN)**: un mezzo reale non viene rilevato correttamente.

Esempi concreti:

- un'ambulanza riconosciuta come Ambulanza e localizzata correttamente e' un TP;
- un furgone bianco riconosciuto come Ambulanza e' un FP;
- un mezzo VDF presente ma ignorato e' un FN;
- un'ambulanza riconosciuta come VDF produce una confusione tra classi: per la
  classe Ambulanza conta come FN e per VDF come FP.

## 2. Confidence

La **confidence** e' il punteggio con cui YOLO esprime quanto considera credibile
una singola predizione. Il valore visualizzato nei benchmark, per esempio:

```text
Ambulanza 0.87
```

e' la confidence assegnata a quel rilevamento in quel frame.

Il comando:

```text
--conf 0.60
```

mantiene soltanto le predizioni con confidence maggiore o uguale a `0.60`.

- soglia bassa: vengono mostrati piu' rilevamenti, aumentando sia il recall sia
  il rischio di falsi positivi;
- soglia alta: vengono scartate piu' predizioni dubbie, aumentando generalmente
  la precision ma rischiando di perdere mezzi reali difficili.

La confidence **non e' necessariamente una probabilita' calibrata**. Un valore
`0.80` non garantisce che esattamente 80 predizioni su 100 siano corrette. Va
usato soprattutto per ordinare le predizioni e scegliere una soglia operativa.

## 3. IoU: qualita' geometrica del bounding box

L'**Intersection over Union (IoU)** misura quanto il box previsto coincide con il
box annotato:

```text
IoU = area di sovrapposizione / area complessiva occupata dai due box
```

- `IoU = 1.00`: box perfettamente coincidenti;
- `IoU = 0.70`: buona sovrapposizione;
- `IoU = 0.50`: localizzazione accettabile ma non precisa;
- `IoU = 0.00`: nessuna sovrapposizione.

Confidence e IoU misurano aspetti diversi. Il modello puo' mostrare
`Ambulanza 0.95` ma disegnare un box impreciso: confidence alta, IoU bassa.

Nei video benchmark privi di annotazioni corrette si puo' leggere la confidence,
ma non e' possibile calcolare la vera IoU.

### Attenzione ai due usi della soglia IoU

Durante la valutazione, la soglia IoU stabilisce quanto deve sovrapporsi una
predizione alla ground truth per essere considerata corretta. In altri contesti,
come la NMS, una soglia IoU serve invece a eliminare box duplicati sullo stesso
oggetto. Sono due impieghi distinti della stessa misura geometrica.

## 4. Precision

La **precision** risponde alla domanda:

> Tra tutti i mezzi segnalati dal modello, quanti erano rilevamenti corretti?

```text
Precision = TP / (TP + FP)
```

Esempio: il modello produce 10 segnalazioni Ambulanza. Otto sono ambulanze reali
e due sono furgoni comuni:

```text
Precision = 8 / (8 + 2) = 0.80
```

Precision alta significa pochi falsi allarmi. Nel progetto, una precision bassa
si manifesta quando auto, autobus, furgoni o elementi dello sfondo vengono
classificati come mezzi di soccorso.

## 5. Recall

Il **recall** risponde alla domanda:

> Tra tutti i mezzi reali presenti, quanti ne ha trovati il modello?

```text
Recall = TP / (TP + FN)
```

Esempio: nel test sono presenti 10 ambulanze e il modello ne rileva correttamente
otto:

```text
Recall = 8 / (8 + 2) = 0.80
```

Recall alto significa pochi mezzi persi. Per SemaforoSmart e' particolarmente
importante, perche' un mezzo di emergenza ignorato puo' essere piu' grave di un
falso allarme. La precision deve comunque restare sufficiente a evitare
attivazioni frequenti su veicoli comuni.

## 6. F1-score

L'**F1-score** combina precision e recall in un unico valore:

```text
F1 = 2 * (Precision * Recall) / (Precision + Recall)
```

E' alto soltanto quando entrambe le metriche sono buone:

| Precision | Recall | F1 approssimativo | Interpretazione |
|---:|---:|---:|---|
| 0.90 | 0.90 | 0.90 | equilibrio molto buono |
| 1.00 | 0.50 | 0.67 | pochi falsi allarmi, ma molti mezzi persi |
| 0.50 | 1.00 | 0.67 | trova tutto, ma produce molti falsi allarmi |

### Curva F1-Confidence

Nel file `BoxF1_curve.png`:

- asse orizzontale: soglia di confidence;
- asse verticale: F1 ottenuto usando quella soglia.

Il picco indica la soglia che produce il miglior compromesso matematico tra
precision e recall sul dataset valutato.

La lettura corretta distingue due elementi:

- **altezza del picco**: qualita' del miglior equilibrio raggiungibile;
- **posizione del picco**: soglia di confidence alla quale si ottiene.

Un picco F1 alto e' positivo. Un picco molto a sinistra non e' automaticamente
migliore: indica soltanto che il compromesso massimo richiede una soglia bassa,
quindi il modello assegna punteggi relativamente bassi anche a rilevamenti utili.

Il picco tratta FP e FN con la stessa importanza. Il sistema finale puo' scegliere
una soglia leggermente piu' bassa per privilegiare il recall oppure piu' alta per
ridurre i falsi allarmi.

## 7. AP, mAP50 e mAP50-95

L'**Average Precision (AP)** riassume la curva Precision-Recall di una singola
classe. Non fotografa una sola soglia di confidence: valuta il comportamento del
modello facendo variare la soglia.

La **mAP** e' la media dell'AP tra le classi. Nel progetto:

```text
mAP = media(AP Ambulanza, AP Carabinieri, AP VigiliDelFuoco)
```

Le due metriche piu' comuni sono:

- **mAP50**: considera valida la localizzazione a partire da IoU `0.50`; e' la
  misura piu' permissiva;
- **mAP50-95**: calcola l'AP con soglie IoU da `0.50` a `0.95`, a intervalli di
  `0.05`, e ne fa la media; e' molto piu' severa sulla precisione dei box.

Interpretazione tipica:

- mAP50 alta e mAP50-95 sensibilmente piu' bassa: il modello trova spesso i
  mezzi, ma i bounding box non sono sempre molto precisi;
- entrambe alte: buone classificazione e localizzazione;
- AP bassa soltanto per una classe: il problema e' concentrato, per esempio sui
  Carabinieri, e non riguarda necessariamente l'intero modello.

Le mAP sono normalmente le metriche migliori per confrontare globalmente due
checkpoint sullo **stesso identico test set**.

## 8. Loss di training e validation

La loss e' un errore matematico ottimizzato durante l'addestramento. Non e' una
percentuale e non va interpretata come precision o probabilita'. In
`results.png` compaiono:

- `box_loss`: errore relativo alla posizione e alle dimensioni dei box;
- `cls_loss`: errore nella classificazione;
- `dfl_loss`: errore usato da YOLO per affinare i bordi dei bounding box.

Ogni loss appare sia per il train sia per la validation:

- `train/...`: calcolata sulle immagini usate per apprendere;
- `val/...`: calcolata su immagini non usate per aggiornare i pesi.

Andamento desiderato:

- le loss di train scendono;
- anche le loss di validation scendono o si stabilizzano;
- precision, recall e mAP salgono e poi raggiungono un plateau.

Possibile overfitting:

- la loss di train continua a scendere;
- la loss di validation inizia a salire in modo persistente;
- le metriche di validation peggiorano.

Oscillazioni moderate sono normali, soprattutto con validation piccole. Conta la
tendenza generale, non il singolo punto.

## 9. Come leggere `results.png`

Ogni punto rappresenta un'epoca. La linea blu mostra i valori misurati; la linea
arancione tratteggiata ne mostra l'andamento smussato.

### Riga superiore

1. `train/box_loss`: localizzazione dei box sul train;
2. `train/cls_loss`: classificazione sul train;
3. `train/dfl_loss`: precisione dei bordi sul train;
4. `metrics/precision(B)`: precision sulla validation;
5. `metrics/recall(B)`: recall sulla validation.

### Riga inferiore

1. `val/box_loss`: localizzazione dei box sulla validation;
2. `val/cls_loss`: classificazione sulla validation;
3. `val/dfl_loss`: precisione dei bordi sulla validation;
4. `metrics/mAP50(B)`: mAP con IoU 0.50;
5. `metrics/mAP50-95(B)`: mAP con soglie IoU piu' severe.

Il checkpoint `best.pt` non deve necessariamente coincidere con l'ultima epoca.
Ultralytics conserva l'epoca con il miglior risultato complessivo sulla
validation. `last.pt` contiene invece lo stato dell'ultima epoca eseguita.

## 10. Come leggere le curve generate

### `BoxP_curve.png` — Precision-Confidence

Mostra come cambia la precision aumentando la soglia. In genere, scartando le
predizioni meno sicure, diminuiscono i falsi positivi e la precision sale.

### `BoxR_curve.png` — Recall-Confidence

Mostra come cambia il recall aumentando la soglia. In genere il recall scende,
perche' vengono eliminati anche mezzi reali con confidence bassa.

### `BoxF1_curve.png` — F1-Confidence

Mostra il compromesso tra precision e recall per ogni soglia. Il picco suggerisce
un punto di partenza per la soglia operativa, da verificare poi sui video reali.

### `BoxPR_curve.png` — Precision-Recall

Mostra quanto recall si puo' ottenere mantenendo una certa precision. Una curva
vicina all'angolo superiore destro e' migliore. L'area riassunta sotto questa
curva contribuisce all'AP.

Le curve colorate rappresentano le singole classi; la curva piu spessa riassume
il comportamento medio del modello.

## 11. Matrice di confusione

Nelle matrici generate da Ultralytics in questo progetto:

- le righe indicano la classe **predetta**;
- le colonne indicano la classe **reale**;
- la diagonale contiene le classificazioni corrette;
- le celle fuori diagonale mostrano confusioni tra classi;
- la riga `background` indica oggetti reali non rilevati correttamente;
- la colonna `background` indica rilevamenti prodotti dove non esisteva una
  ground truth corrispondente.

Esempi:

- cella riga VDF, colonna Ambulanza: una vera ambulanza e' stata classificata
  come VDF;
- cella riga background, colonna Carabinieri: un vero Carabiniere e' stato perso;
- cella riga Ambulanza, colonna background: falso positivo Ambulanza.

La versione normalizzata mostra proporzioni; quella non normalizzata mostra il
numero effettivo di casi. Con test piccoli e' importante consultare entrambe:
anche un solo errore puo' spostare molto una percentuale.

## 12. Validation, test e benchmark video

- **Validation**: guida la scelta del checkpoint durante il training.
- **Test**: misura il modello su dati congelati e mai usati per scegliere i pesi.
- **Benchmark video**: verifica qualitativamente il comportamento temporale e in
  condizioni realistiche.

Per confrontare correttamente due versioni devono restare uguali almeno:

- test set;
- video benchmark;
- risoluzione di inferenza;
- soglia di confidence;
- impostazioni principali del modello.

Nei benchmark senza ground truth frame per frame non si possono calcolare in
modo formale precision, recall, IoU o mAP. Si possono invece osservare:

- confidence delle predizioni;
- continuita' dei rilevamenti;
- cambi di classe tra frame;
- falsi positivi evidenti;
- mezzi persi durante distanza, sfocatura o occlusione;
- stabilita' e forma dei bounding box.

## 13. Esempio completo

Supponiamo che in un test siano presenti 10 ambulanze. Il modello:

- ne riconosce correttamente 8;
- ne perde 2;
- segnala anche 2 furgoni come Ambulanza.

Risultato:

```text
TP = 8
FN = 2
FP = 2
Precision = 8 / (8 + 2) = 0.80
Recall    = 8 / (8 + 2) = 0.80
F1        = 0.80
```

Se i box corretti hanno tutti IoU superiore a `0.50`, contribuiranno bene
all'AP50. Se alcuni box sono larghi, stretti o spostati rispetto alle annotazioni,
il risultato sara' penalizzato maggiormente nella AP50-95.

Aumentando la soglia confidence da `0.30` a `0.80` potrebbero sparire i due falsi
positivi, ma potrebbe scomparire anche una delle otto ambulanze corrette. La
soglia migliore dipende quindi dal costo operativo dei falsi positivi e dei mezzi
persi.

## 14. Procedura rapida di lettura

1. Verificare che le loss di train e validation abbiano un andamento sano.
2. Individuare epoca migliore ed eventuale early stopping.
3. Leggere mAP50 e soprattutto mAP50-95 sul test congelato.
4. Controllare precision e recall complessivi e per classe.
5. Esaminare la matrice di confusione per capire la natura degli errori.
6. Consultare le curve confidence per scegliere una soglia iniziale.
7. Ripetere gli stessi benchmark video con la medesima soglia.
8. Trasformare gli errori ricorrenti in interventi mirati sul dataset.

## 15. Regola fondamentale

Nessuna singola metrica descrive da sola il modello:

- confidence valuta la sicurezza assegnata alla singola predizione;
- IoU valuta la precisione geometrica del box;
- precision misura i falsi allarmi;
- recall misura i mezzi persi;
- F1 bilancia precision e recall;
- mAP riassume il comportamento attraverso molte soglie;
- loss descrive l'andamento dell'apprendimento;
- benchmark video e test di dominio verificano il comportamento operativo.

La scelta del modello migliore deve incrociare tutte queste informazioni con i
requisiti reali di SemaforoSmart.
