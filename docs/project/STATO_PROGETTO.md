# SemaforoSmart — stato formale del progetto

Aggiornato al **27 settembre 2026**. Questo documento e' il punto di riferimento
sintetico per consistenza del dataset, risultati sperimentali, limiti conosciuti e
backlog. I conteggi delle condizioni derivano da `docs/project/METADATA_CLASSI.md`; non
sono stati ricavati riesaminando visivamente le immagini.

## 1. Obiettivo e stato attuale

La fase sperimentale attuale addestra YOLOv8n tramite fine-tuning su tre classi:

- `Ambulanza`
- `Carabinieri`
- `VigiliDelFuoco`

Queste non costituiscono la tassonomia definitiva. In futuro il progetto dovra'
includere altre forze e categorie di emergenza, tra cui Polizia e Guardia di
Finanza. L'estensione delle classi sara' un cambiamento strutturale e quindi un
possibile punto naturale di passaggio alla v2.

La **v1.3 e' attualmente la baseline di riferimento**. Sul test congelato supera
la v1.2 in tutte le metriche aggregate e nei benchmark produce miglioramenti
visibili su NIGHT, FAR, occlusioni e stabilita' dei box. Il progresso non e'
uniforme: Carabinieri resta la classe meno solida nel piccolo test statico e
persistono falsi positivi mirati su veicoli rossi, furgoni bianchi e veicoli
illuminati dai lampeggianti. Non e' ancora una versione definitiva.

## 2. Percorso svolto

### Fase storica

- Conservato il progetto precedente in `SemaforoSmart OLD`.
- Recuperate immagini storiche, immagini nuove e vecchi pesi `bestOLD.pt`.
- Abbandonato il riuso sistematico delle vecchie label quando il loro recupero e
  abbinamento sarebbe costato piu' della riannotazione pulita.

### Dataset v1

- Raccolta, selezione e annotazione di 426 immagini.
- Introduzione di immagini negative senza bounding box.
- Split locale deterministico e per gruppi correlati, con seed 42.
- Addestramento della prima baseline YOLOv8n.
- Valutazione statica e sei benchmark video esterni.
- Problemi principali rilevati: basso recall Ambulanza, notte debole, confusione
  Ambulanza/VDF, falsi positivi su veicoli e oggetti comuni.

### Dataset v1.1

- Aggiunte 91 immagini mirate: 79 positive e 12 negative.
- Il test v1 e' rimasto invariato; nessuna nuova immagine e' stata inserita nel
  test.
- Tutte le 517 immagini sono state censite nei metadata.
- Addestramento completato per 100 epoche; il checkpoint migliore e' quello
  selezionato all'epoca 82.
- Nuova valutazione sullo stesso test v1 e ripetizione degli stessi sei benchmark
  video con soglia minima `conf=0.60`.

### Dataset v1.2

- Aggiunte 69 immagini mirate: 51 positive e 18 negative.
- Incrementi per sorgente nominale: 22 Ambulanza, 10 Carabinieri, 18 VDF, una
  immagine multiclasse e 18 NULL.
- Split cumulativo: 458 train, 85 validation e 43 test; il test storico resta
  identico byte per byte.
- Training fermato dall'early stopping all'epoca 57; checkpoint migliore
  selezionato all'epoca 32.
- Valutazione statica e ripetizione dei sei benchmark a `conf=0.60`.
- Obiettivo falsi positivi centrato; migliorata Ambulanza notte e recuperato il
  pickup VDF giorno. Restano critici Carabinieri notte, VDF notte e occlusioni
  dinamiche FAR/MID.

### Dataset v1.3

- Aggiunte 78 immagini mirate: 52 positive e 26 NULL.
- Il batch positivo contiene 28 FAR, 14 MID, 5 CLOSE e 5 MIXED; 34 NIGHT e 18
  DAY; 44 STREET e 8 ELEVATED.
- Split cumulativo: 524 train, 97 validation e 43 test; il test storico resta
  invariato.
- Training completato per 100 epoche con gli stessi parametri di confronto;
  checkpoint migliore selezionato all'epoca 99.
- Valutazione formale sul test congelato e benchmark video completati a
  `conf=0.60`.
- Obiettivo mirato sostanzialmente raggiunto: progressi su notte, distanza,
  occlusioni e continuita' geometrica delle box; regressioni residue circoscritte
  soprattutto agli hard negative rossi e ad alcuni casi VDF notturni.

## 3. Composizione dei dataset v1.1, v1.2 e v1.3

### Versioni e split

| Voce | v1 | Aggiunte v1.1 | Totale v1.1 |
|---|---:|---:|---:|
| Immagini | 426 | 91 | 517 |
| Positive | 382 | 79 | 461 |
| Negative | 44 | 12 | 56 |
| Train | 319 | 78 | 397 (76,8%) |
| Validation | 64 | 13 | 77 (14,9%) |
| Test | 43 | 0 | 43 (8,3%) |

I 43 file del test v1 e v1.1 sono stati verificati come identici byte per byte.
Il test contiene 42 istanze annotate e 4 immagini negative.

### Classi

| Tipo | Immagini | % sul totale | % tra le positive |
|---|---:|---:|---:|
| Ambulanza | 147 | 28,4% | 31,9% |
| Carabinieri | 129 | 25,0% | 28,0% |
| VigiliDelFuoco | 185 | 35,8% | 40,1% |
| Negative | 56 | 10,8% | — |

La differenza numerica tra classi non va corretta automaticamente: i prossimi
inserimenti devono dipendere dagli errori osservati, non dalla sola parita' dei
conteggi.

### Aggiornamento cumulativo v1.2

| Voce | v1.1 | Aggiunte v1.2 | Totale v1.2 |
|---|---:|---:|---:|
| Immagini | 517 | 69 | 586 |
| Positive | 461 | 51 | 512 |
| Negative | 56 | 18 | 74 |
| Train | 397 | 61 | 458 |
| Validation | 77 | 8 | 85 |
| Test | 43 | 0 | 43 |

Tra le nuove positive, 25 sono NIGHT, 23 FAR, 13 MID, 27 contengono occlusioni
e 14 sono multiveicolo. Nel totale v1.2 NIGHT sale da 116 a 141, OCCLUDED da 52
a 79, PARTIAL da 23 a 31 e multiveicolo da 38 a 52. La distribuzione delle
distanze rimane sostanzialmente stabile, evitando un nuovo sbilanciamento verso
i primi piani.

La quantita' non coincide pero' con la diversita': le 18 negative provengono da
un unico ambiente logico; le immagini NIGHT derivano da 3 gruppi Ambulanza, 2
Carabinieri e 3 VDF. Questo limita la generalizzazione dei miglioramenti.

### Aggiornamento cumulativo v1.3

| Voce | v1.2 | Aggiunte v1.3 | Totale v1.3 |
|---|---:|---:|---:|
| Immagini | 586 | 78 | 664 |
| Positive | 512 | 52 | 564 |
| Negative | 74 | 26 | 100 |
| Train | 458 | 66 | 524 |
| Validation | 85 | 12 | 97 |
| Test | 43 | 0 | 43 |

Le 52 nuove positive sono intenzionalmente concentrate sulle lacune osservate:
53,8% FAR, 26,9% MID, 65,4% NIGHT e 84,6% STREET. Le 8 immagini ELEVATED
introducono un piccolo incremento di diversita' del punto di vista, senza pero'
risolvere il divario rispetto alla futura telecamera del semaforo.

## 4. Distribuzione delle condizioni

Le tabelle dettagliate seguenti descrivono il censimento consolidato della
**v1.1 (461 immagini positive)**. Gli incrementi v1.2 e v1.3 sono riportati
separatamente nelle sezioni precedenti per evitare di confondere valori storici
con campi compositi o ancora `UNKNOWN`. La distanza deriva dall'area normalizzata
delle bounding box: `FAR < 10%`, `MID
10–30%`, `CLOSE > 30%`; `MIXED` indica fasce diverse nella stessa immagine.

### Distanza

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| FAR | 209 | 45,3% |
| MID | 110 | 23,9% |
| CLOSE | 118 | 25,6% |
| MIXED | 24 | 5,2% |

La v1.1 ha corretto molto la scarsita' iniziale di esempi lontani: 48 delle 79
nuove positive sono `FAR` e 26 sono `MID`.

### Illuminazione

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| DAY | 334 | 72,5% |
| NIGHT | 116 | 25,2% |
| DUSK | 11 | 2,4% |

Le 79 nuove positive comprendono 46 immagini notturne. Per classe, la quota
notturna e' Ambulanza 40/147 (27,2%), Carabinieri 44/129 (34,1%) e VDF 32/185
(17,3%). **VDF notte resta la lacuna piu' evidente**.

### Meteo

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| CLEAR | 435 | 94,4% |
| RAIN | 12 | 2,6% |
| FOG | 6 | 1,3% |
| SNOW | 1 | 0,2% |
| UNKNOWN | 7 | 1,5% |

La copertura meteo e' fortemente sbilanciata. E' un limite reale, ma diventa una
priorita' alta solo se pioggia/nebbia sono condizioni richieste nello scenario
operativo del progetto.

### Lampeggianti

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| ON | 277 | 60,1% |
| OFF | 174 | 37,7% |
| UNKNOWN | 10 | 2,2% |

### Angolazione

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| FRONT | 132 | 28,6% |
| OBLIQUE | 94 | 20,4% |
| REAR | 86 | 18,7% |
| MIXED | 84 | 18,2% |
| SIDE | 60 | 13,0% |
| UNKNOWN | 5 | 1,1% |

### Altezza della ripresa

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| STREET | 388 | 84,2% |
| ELEVATED | 35 | 7,6% |
| TOP_DOWN | 31 | 6,7% |
| LOW | 7 | 1,5% |

Questo e' il principale rischio di dominio visivo: dataset e benchmark sono
dominati da video STREET ripresi da persone, mentre l'impiego finale prevede una
telecamera associata al semaforo.

### Visibilita'

| Condizione | Immagini | Percentuale |
|---|---:|---:|
| OK | 350 | 75,9% |
| OCCLUDED | 50 | 10,8% |
| BLUR | 36 | 7,8% |
| PARTIAL | 23 | 5,0% |
| OCCLUDED+OK | 2 | 0,4% |

La v1.1 ha aggiunto 17 immagini `OCCLUDED` e 7 `PARTIAL`. Nei benchmark il
modello gestisce meglio le coperture leggere, ma continua a perdere il mezzo con
occlusioni importanti.

## 5. Risultati formali sul test identico

Tutti i modelli sono confrontati sulle stesse 43 immagini. Il confronto con
`bestOLD.pt` usa una copia delle label con ID rimappati, necessaria per il diverso
ordine storico delle classi.

| Modello | Precision | Recall | mAP50 | mAP50–95 |
|---|---:|---:|---:|---:|
| bestOLD.pt | 0,739 | 0,536 | 0,645 | 0,476 |
| v1 | 0,845 | 0,614 | 0,763 | 0,590 |
| v1.1 | **0,983** | **0,770** | 0,850 | 0,705 |
| v1.2 | 0,930 | 0,763 | 0,890 | 0,723 |
| v1.3 | **0,962** | **0,832** | **0,926** | **0,764** |

### v1 contro v1.1 per classe

| Classe | Modello | Precision | Recall | mAP50 | mAP50–95 |
|---|---|---:|---:|---:|---:|
| Ambulanza | v1 | 0,680 | 0,308 | 0,696 | 0,552 |
| Ambulanza | v1.1 | **0,976** | **0,769** | **0,896** | **0,723** |
| Carabinieri | v1 | 1,000 | 0,592 | 0,675 | 0,516 |
| Carabinieri | v1.1 | 1,000 | 0,594 | 0,666 | **0,554** |
| VigiliDelFuoco | v1 | 0,856 | 0,942 | 0,918 | 0,703 |
| VigiliDelFuoco | v1.1 | **0,974** | **0,947** | **0,988** | **0,836** |

Il risultato piu' importante e' il recall Ambulanza, salito da 0,308 a 0,769.
Carabinieri e' sostanzialmente stabile sul piccolo test statico; VDF migliora
quasi ovunque. Con 43 immagini questi valori sono evidenze utili, non una stima
definitiva del comportamento reale.

### v1.1 contro v1.2 per classe

| Classe | Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|
| Ambulanza | v1.1 | **0,976** | 0,769 | 0,896 | 0,723 |
| Ambulanza | v1.2 | 0,821 | **0,846** | **0,932** | **0,737** |
| Carabinieri | v1.1 | **1,000** | 0,594 | 0,666 | 0,554 |
| Carabinieri | v1.2 | **1,000** | **0,600** | **0,756** | **0,636** |
| VigiliDelFuoco | v1.1 | **0,974** | **0,947** | **0,988** | **0,836** |
| VigiliDelFuoco | v1.2 | 0,971 | 0,842 | 0,981 | 0,797 |

La v1.2 migliora le mAP complessive e rafforza Ambulanza e Carabinieri. VDF
regredisce soprattutto nel recall. La precision complessiva inferiore non annulla
il miglioramento dei falsi positivi osservato nei video: il test e' piccolo e le
metriche aggregate non corrispondono esattamente al comportamento operativo a
`conf=0.60`.

### v1.2 contro v1.3 per classe

| Classe | Modello | Precision | Recall | mAP50-95 |
|---|---|---:|---:|---:|
| Ambulanza | v1.2 | 0,821 | 0,846 | 0,737 |
| Ambulanza | v1.3 | **0,928** | **0,992** | **0,853** |
| Carabinieri | v1.2 | **1,000** | **0,600** | 0,636 |
| Carabinieri | v1.3 | **1,000** | 0,557 | **0,657** |
| VigiliDelFuoco | v1.2 | **0,971** | 0,842 | **0,797** |
| VigiliDelFuoco | v1.3 | 0,959 | **0,947** | 0,781 |

Il miglioramento aggregato e' forte, soprattutto per Ambulanza. Carabinieri
perde recall sul piccolo test statico pur migliorando qualitativamente nel video
notturno; VDF recupera recall ma perde leggermente precisione e localizzazione
severa. Questa divergenza conferma che test statico e benchmark devono restare
entrambi obbligatori.

## 6. Risultati qualitativi sui benchmark video

I sei video esterni non hanno ground truth frame per frame. Le conclusioni sono
quindi qualitative, ma il confronto e' controllato: stessi video e soglia minima
`conf=0.60`.

| Benchmark | Andamento v1.1 rispetto a v1 | Limite residuo |
|---|---|---|
| Ambulanza giorno | miglioramento molto forte | occlusioni importanti; rari scambi con VDF |
| Ambulanza notte | miglioramento netto | FAR occluso; scambio iniziale con VDF |
| Carabinieri giorno | miglioramento netto | auto nere come falsi positivi |
| Carabinieri notte | miglioramento molto forte | FAR, side partial e qualche esitazione |
| VDF giorno | stabile/leggero peggioramento locale | pickup riconosciuto piu' tardi |
| VDF notte | miglioramento parziale | box iniziale instabile; Ambulanza/VDF |

Sono diminuiti sensibilmente i falsi positivi su stazione di servizio e fermata
bus. Restano casi ricorrenti su auto scure, bus rossi, furgoni bianchi o veicoli
affiancati. La box che si restringe durante un'occlusione e' coerente con la
regola di annotare la sola parte visibile.

### Esito v1.2 rispetto alla v1.1

| Benchmark | Esito v1.2 | Limite residuo |
|---|---|---|
| Ambulanza giorno | FP nettamente ridotti; MID/CLOSE molto sicuri | FAR, occlusioni e furgone bianco affiancato |
| Ambulanza notte | miglioramento netto e minore confusione con VDF | confidence instabile e alcuni frame persi |
| Carabinieri giorno | sostanzialmente stabile; FP leggermente ridotti | auto nera e occlusioni forti |
| Carabinieri notte | leggera regressione | box instabile, FAR/rear e nuova confusione con VDF |
| VDF giorno | pickup nuovamente riconosciuto | autobus rosso ancora falso positivo saltuario |
| VDF notte | stabile o leggermente peggiore | confusione a tre classi e scenario estremamente difficile |

Il risultato piu' solido della v1.2 e' la riduzione dei falsi positivi ottenuta
con sole 18 nuove NULL. L'aumento generico di immagini `OCCLUDED` non ha invece
prodotto la stessa crescita: i benchmark contengono occlusioni dinamiche,
movimento, blur e variazioni FAR/MID diverse dalle scene prevalentemente statiche
aggiunte al dataset. La detection e' inoltre eseguita indipendentemente su ogni
frame e non ottimizza direttamente la stabilita' temporale del box.

### Esito v1.3 rispetto alla v1.2

| Benchmark | Esito v1.3 | Limite residuo |
|---|---|---|
| Ambulanza giorno | netto miglioramento delle occlusioni; rilevamento complessivamente solido | occlusioni estreme, limite FAR da definire, nuovo FP su auto rossa CLOSE/PARTIAL |
| Ambulanza notte | FAR migliorato e seconda meta' molto stabile | scambio iniziale con VDF |
| Carabinieri giorno | rapporto frame/predizione quasi ottimale; lieve progresso occluded | quattro frame FP sulla stessa auto nera |
| Carabinieri notte | box piu' omogenei e IoU visivamente migliore; meno FP | FAR e distinzione notturna tra Carabinieri, VDF e Ambulanza |
| VDF giorno | sostanzialmente stabile rispetto a v1.2 | pickup FAR rilevato tardi; pullman rosso ancora FP |
| VDF notte ordinario | rilevamento prevalente corretto dopo la fase iniziale | iniziale Ambulanza; box dimezzato dai lampeggianti bassi; auto grigia illuminata come FP |
| VDF notte stress | miglioramento netto e confusione quasi eliminata dopo l'ingresso | box dell'intero mezzo ancora instabile |

Il batch v1.3 ha quindi corretto molte lacune per cui era stato costruito. I
peggioramenti non sono generici: convergono sulla relazione fra colore rosso,
pickup/bus e classe VDF, oltre che sull'uso molto frequente dei lampeggianti
accesi nelle scene NIGHT. Il modello sembra talvolta usare i lampeggianti come
forte indizio di classe e perfino di estensione verticale del mezzo.

## 7. Backlog ordinato per priorita'

### Alta — misurare il dominio visivo reale

- Creare almeno un benchmark rappresentativo della **telecamera del semaforo**,
  mantenuto fuori dal training.
- Se possibile includere le tre classi, almeno DAY e NIGHT, con ingresso,
  avvicinamento e allontanamento del mezzo.
- Valutare la v1.3 prima di raccogliere dati appositamente per quel punto di
  vista. Solo un fallimento misurato giustifica un nuovo batch dedicato.

### Separata — portabilita' dell'inferenza locale

- Usare il **T4** come banco di prova di un ambiente autonomo e chiuso, simile
  all'architettura finale in cui una CPU esegue il modello localmente sul
  semaforo.
- Questa prova riguarda compatibilita', prestazioni e autonomia della pipeline;
  non rende il T4 il dominio visivo prioritario del dataset.
- Misurare almeno tempo per frame/FPS, stabilita', uso della memoria e formato di
  esportazione del modello sulla CPU scelta.

### Alta — errori gia' dimostrati

- Priorita' 1: Carabinieri NIGHT `FAR`/`MID`, con lampeggianti sia ON sia OFF e
  viste che distinguano Carabinieri da Polizia/GDF, Ambulanza e VDF.
- Priorita' 2: VDF NIGHT con lampeggianti a diverse altezze e fasi ON/OFF,
  annotando sempre l'intera porzione visibile del mezzo per non rinforzare box
  dimezzati attorno alle sole luci.
- Priorita' 3: hard negative esattamente corrispondenti agli errori osservati:
  auto e pickup rossi CLOSE/PARTIAL, autobus rossi affiancati al VDF, auto nere,
  furgoni bianchi e auto grigie illuminate di blu.
- Priorita' 4: Ambulanza FAR e occlusioni dinamiche ancora riconoscibili; prima
  definire pero' la distanza operativa oltre la quale il rilevamento non serve.
- Diversificare le fonti: pochi frame realmente differenti per ciascuna scena,
  senza concentrare tutto il batch in una sola compilation.

### Media — robustezza

- Aggiungere occlusioni graduali con il mezzo ancora riconoscibile, indicativamente
  20–50% coperto; scartare i casi in cui anche un umano non puo' determinare con
  affidabilita' classe e box.
- Rafforzare `SIDE`, `REAR` e `PARTIAL` dove i benchmark mostrano esitazioni.
- Bilanciare meglio NIGHT con lampeggianti spenti: oggi le luci accese sono un
  indizio troppo dominante nei nuovi esempi notturni.
- Cercare sorgenti non STREET; nel censimento v1.1 STREET pesa l'84,2% e anche
  le nuove positive v1.3 restano STREET per l'84,6%.

### Condizionata allo scenario finale

- Aumentare `RAIN`, `FOG` e altre condizioni meteo solo se fanno parte dei
  requisiti operativi. Nel censimento v1.1 `CLEAR` era gia' al 94,4% e le
  aggiunte v1.3 sono ancora interamente `CLEAR`.
- Valutare in seguito una soglia di confidenza operativa per dispositivo e
  scenario; `0.60` e' al momento una soglia di confronto, non necessariamente
  quella definitiva.

### Esperimenti senza nuove immagini — conclusi, non promossi

Sono state provate due varianti controllate della v1.2:

- `v1.2_Aug`: due versioni Roboflow per sorgente train con Exposure tra -15% e
  +15% e Gaussian Blur fino a 1.4 px;
- `v1.2 Multi-scale`: dataset originale con `multi_scale=0.25` e tutti gli
  altri parametri invariati.

Entrambe aumentano la tendenza a rilevare il mezzo e migliorano lievemente le
occlusioni, ma introducono falsi positivi e confusioni tra classi assenti o meno
frequenti nella baseline. Multi-scale e' piu' equilibrato e migliora chiaramente
VDF notte, senza pero' produrre un progresso generale evidente nei sei
benchmark. Le buone metriche statiche non compensano la regressione operativa.

Conclusione aggiornata: gli esperimenti restano non promossi; la baseline e'
ora la v1.3 reale e mirata. Non combinare automaticamente augmentation e
multi-scale con essa.

### Esperimento separato — Copy-Paste augmentation

Il primo ramo Copy-Paste controllato e' stato completato come `v1.3_cp`. Parte
dalla v1.3 e aggiunge al solo train 60 composizioni DAY: 20 per classe, 36 FAR e
24 MID. Validation (97 immagini), test congelato (43) e benchmark sono rimasti
identici alla baseline; il train passa da 524 a 584 immagini.

Sul test congelato il risultato aggregato e' inferiore alla v1.3:

| Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| v1.3 baseline | 0.962 | **0.832** | **0.926** | **0.764** |
| v1.3_cp DAY | **0.980** | 0.772 | 0.864 | 0.735 |

VDF migliora localmente, mentre il calo complessivo di recall e mAP impedisce
la promozione. Nei sei benchmark video sono comparsi vantaggi qualitativi su
Carabinieri notte e su alcune occlusioni di Ambulanza, accompagnati pero' da un
aumento dei falsi positivi. Lo stress test VDF notte aggiuntivo non e' stato
eseguito per questo ramo.

Conclusione: `v1.3_cp` resta un esperimento riproducibile e separato; la baseline
corrente rimane v1.3. Il candidato successivo, se si vuole proseguire, e' una
ablazione piccola che aggiunga soltanto le 20 composizioni Carabinieri gia'
generate, senza creare automaticamente altro materiale sintetico o NIGHT.

## 8. Criterio per la prossima versione

La prossima revisione non deve nascere dal semplice obiettivo di pareggiare le
classi o aumentare il numero totale. Ogni immagine candidata dovrebbe rispondere
ad almeno una lacuna documentata:

1. corregge un falso positivo ricorrente;
2. copre notte/FAR/MID e lampeggianti OFF per Carabinieri o VDF;
3. corregge box VDF dimezzati o introduce un tipo VDF poco rappresentato;
4. migliora Ambulanza FAR/MID con occlusione dinamica riconoscibile;
5. rappresenta il vero punto di vista della telecamera finale.

Prima di chiamarla `v2` conviene stabilire una modifica sostanziale del dominio o
dell'obiettivo. L'introduzione delle future classi, come Polizia e Guardia di
Finanza, e' uno dei candidati naturali per questo passaggio. Un ulteriore
intervento piccolo e mirato sulle tre classi attuali puo' invece essere
versionato come `v1.4`; una variante Copy-Paste resta un esperimento separato e
non determina da sola il passaggio di versione.

## 9. Riferimenti

- Dataset v1.1: `data/datasets/v1.1/README.md`
- Dataset v1.2: `data/datasets/v1.2/README.md`
- Dataset v1.3: `data/datasets/v1.3/README.md`
- Dataset sperimentale v1.3_cp: `data/datasets/v1.3_cp/README.md`
- Materiali e generazione Copy-Paste: `data/raw/v1.3_cp/README.md`
- Report v1.2_Aug: `experiments/Test/evaluation_test_v1_2_aug_base/REPORT.md`
- Report v1.2 Multi-scale: `experiments/Test/evaluation_test_v1_2_multiscale/REPORT.md`
- Metadata completi: `docs/project/METADATA_CLASSI.md`
- Registro fonti di tutte le versioni: `docs/project/FONTI_DATASET.txt`
- Primo confronto con bestOLD: `experiments/Test/confronto_v1_old/REPORT.md`
- Log training v1: `docs/logs/1. LOG_TRAIN_V1.txt`
- Log training v1.1: `docs/logs/2. LOG_TRAIN_V1.1.txt`
- Log training v1.2: `docs/logs/3. LOG_TRAIN_V1.2.txt`
- Log training v1.2_Aug: `docs/logs/4. LOG_TRAIN_V1.2_AUG.txt`
- Log training v1.2 Multi-scale: `docs/logs/5. LOG_TRAIN_V1.2_MULTISCALE.txt`
- Feedback benchmark v1.2: `experiments/video_tests/v1.2/feedback bench v1.2.txt`
- Log training v1.3: `docs/logs/6. LOG_TRAIN_V1.3.txt`
- Log training v1.3_cp: `docs/logs/7. LOG_TRAIN_V1.3_CP.txt`
- Feedback benchmark v1.3: `experiments/video_tests/v1.3/feedback bench v1.3.txt`
- Valutazione v1.3_cp: `experiments/Test/evaluation_test_v1_3_cp_day_001/REPORT.md`
- Benchmark v1.3_cp: `experiments/video_tests/v1.3_cp/README.md`
- Pesi correnti: `experiments/Train/baseline_v1_3_yolov8n/weights/best.pt`
- Valutazione corrente: `experiments/Test/evaluation_test_v1_3_frozen/`
