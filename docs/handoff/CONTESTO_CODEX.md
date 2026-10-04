# Contesto operativo Codex — SemaforoSmart

Il progetto viene portato avanti tra Windows e macOS. Considera questo documento
come il contesto operativo principale di una nuova chat. Non ripartire da zero e
non ricostruire decisioni gia' documentate.

## Prima azione obbligatoria

Prima di proporre modifiche, visita la root del progetto e leggi, in questo
ordine:

1. `docs/handoff/CONTESTO_CODEX.md`;
2. `docs/project/STATO_PROGETTO.md`;
3. `README.md`;
4. `data/raw/README.md`;
5. `data/datasets/v1.3/README.md`;
6. `experiments/README.md`;
7. `docs/project/METADATA_CLASSI.md` solo nelle sezioni necessarie;
8. `docs/project/FONTI_DATASET.txt` quando si lavora sulle fonti;
9. `docs/guides/GUIDA_LETTURA_METRICHE_YOLO.md` quando si discutono metriche;
10. `docs/archive/PROMPT_ORIGINALE.txt` soltanto come contesto storico.

Controlla poi che esistano il modello corrente, il dataset v1.3 e i sei video
benchmark. Non aprire in massa immagini o video durante questa ricognizione.

## Obiettivo del progetto

SemaforoSmart e' un progetto universitario di object detection realtime. Lo
scopo finale e' riconoscere veicoli di emergenza italiani da una telecamera
associata a un semaforo, così da supportare una futura gestione intelligente del
traffico agli incroci.

La fase attuale usa YOLOv8n e tre classi:

```text
0: Ambulanza
1: Carabinieri
2: VigiliDelFuoco
```

Polizia, Guardia di Finanza e altre classi arriveranno in futuro. Non inserirle
silenziosamente nel dataset attuale: l'espansione della tassonomia sara' un
cambiamento strutturale e un possibile passaggio alla v2.

Il TurtleBot 4 e' stato usato come prova di ambiente autonomo e chiuso, ma non e'
la priorita' visiva del dataset. L'obiettivo finale e' una CPU che esegue il
modello localmente sul semaforo. Windows con RTX 3070 Ti e' stato usato per il
training; il Mac viene usato per inferenza, test sul campo e collegamento allo
stream del T4/IP camera.

## Livello e stile di collaborazione

L'utente sta imparando computer vision e machine learning durante il progetto.
Non dare per scontati i termini tecnici, ma non trattarlo come se non avesse gia'
costruito tre versioni del dataset. Spiega i concetti collegandoli sempre a casi
concreti di Ambulanza, Carabinieri e VDF.

Modus operandi richiesto:

- ragionare insieme prima delle decisioni strutturali;
- risposte dirette quando la domanda e' semplice;
- analisi ricche di contesto ma non prolisse;
- piccoli passi verificabili, niente overengineering;
- motivare ogni aggiunta al dataset con un errore osservato;
- distinguere chiaramente fatti, inferenze e ipotesi;
- non proporre percentuali ideali astratte come legge universale;
- privilegiare diversita' di fonti e scenari rispetto al semplice numero;
- mantenere ordine, nomi leggibili, versioni separate e README aggiornati;
- preservare materiale storico e modifiche dell'utente;
- usare path relativi e `pathlib`, garantendo compatibilita' Windows/macOS;
- quando mancano informazioni nei metadata usare `UNKNOWN`, senza inventarle.

### Regola importante sulle immagini

L'utente preferisce investire tempo personale per descrivere e categorizzare le
immagini, così da risparmiare utilizzo Codex. Non aprire o ispezionare
singolarmente intere cartelle di immagini per dedurne il contesto.

Usare prima:

- nomi dei file;
- metadata;
- label YOLO;
- dimensioni e hash;
- registro delle fonti;
- descrizioni fornite dall'utente.

L'ispezione visiva e' consentita quando:

- l'utente chiede esplicitamente di analizzare una determinata immagine;
- una decisione non puo' essere presa dai dati disponibili;
- si tratta di pochissimi casi dubbi.

Negli altri casi chiedere prima all'utente oppure lasciare `UNKNOWN`. Non
reinterpretare visivamente tutte le immagini gia' categorizzate: sarebbe lavoro
duplicato.

## Organizzazione del progetto

La root corrente e' `SemaforoSmart/`. Le aree principali sono:

- `data/raw/`: sorgenti selezionate, ordinate per versione;
- `data/datasets/`: export YOLO completi e split locali versionati;
- `data/test_videos/`: benchmark esterni, mai usati nel training;
- `scripts/`: strumenti riproducibili;
- `experiments/Train/`: training e checkpoint;
- `experiments/Test/`: valutazioni formali sui test set;
- `experiments/video_tests/`: inferenze e feedback sui benchmark;
- `models/pretrained/`: peso iniziale `yolov8n.pt`;
- `docs/project/`: stato formale, metadata e fonti;
- `docs/guides/`: procedure e comandi operativi;
- `docs/logs/`: log integrali dei training;
- `docs/handoff/`: contesto Codex e sincronizzazione Windows/macOS;
- `docs/project/METADATA_CLASSI.md`: catalogo cumulativo delle immagini.

Il flusso corretto e':

```text
raw/vN -> Roboflow -> datasets/vN -> split locale -> training -> test -> benchmark
```

Le cartelle raw non sono dataset di training. Non mescolare export Roboflow,
immagini raw e risultati degli esperimenti.

## Regole consolidate sul dataset

1. Roboflow serve principalmente per annotare ed esportare.
2. Le versioni pulite non usano augmentation Roboflow indiscriminata.
3. Il download puo' essere esportato tutto in train; lo split definitivo viene
   costruito localmente e documentato.
4. Frame provenienti dallo stesso video o scena devono restare nello stesso
   split per evitare leakage.
5. Il test storico di 43 immagini e' congelato e identico tra v1, v1.1 e v1.2.
6. Le nuove immagini correttive entrano soltanto in train/validation, salvo una
   futura decisione esplicita di costruire un nuovo benchmark.
7. Le negative non hanno bounding box: il relativo file label YOLO e' vuoto.
8. `NULL` nei metadata significa immagine negativa senza classi target.
9. Non pareggiare automaticamente il numero delle classi: intervenire sugli
   errori dimostrati da test e benchmark.
10. Evitare molti frame quasi consecutivi; usare pochi frame realmente diversi.
11. Casi estremamente ambigui, non riconoscibili neppure da un umano, vanno
    esclusi o conservati come riserva, non forzati nel training.
12. Le box sulle occlusioni devono seguire una convenzione coerente. Non cambiare
    regola a meta' dataset.

## Metadata

Formato corrente:

```text
DISTANCE, LIGHT, WEATHER, LIGHTS, ANGLE, CAMERA_HEIGHT, VISIBILITY, QUANTITY
```

Valori principali:

- distanza: `FAR`, `MID`, `CLOSE`, `MIXED`;
- luce: `DAY`, `NIGHT`, `DUSK`, `UNKNOWN`;
- meteo: `CLEAR`, `RAIN`, `FOG`, `SNOW`, `UNKNOWN`;
- lampeggianti: `ON`, `OFF`, `UNKNOWN`;
- angolo: `FRONT`, `REAR`, `SIDE`, `OBLIQUE`, `MIXED`, `UNKNOWN`;
- altezza: `LOW`, `STREET`, `ELEVATED`, `TOP_DOWN`, `UNKNOWN`;
- visibilita': `OK`, `BLUR`, `OCCLUDED`, `PARTIAL`, combinazioni o `UNKNOWN`;
- quantita': `S`, `M`;
- negative: `NULL`.

La distanza e' calcolabile automaticamente dall'area normalizzata delle box:

```text
FAR   < 10%
MID   10–30%
CLOSE > 30%
MIXED = box della stessa immagine in fasce diverse
```

## Cronologia affidabile

### Archivio precedente

Il vecchio progetto e' conservato separatamente come `SemaforoSmart OLD`. Era
disordinato e conteneva vecchi dataset, label difficili da ricongiungere e il
modello `bestOLD.pt`. Non usare quell'archivio come struttura corrente.

Il vecchio modello aveva ordine classi differente:

```text
0: Carabinieri
1: FireFighter
2: ambulance
```

Per confrontarlo con il dataset moderno e' stata creata una copia di valutazione
con mapping dedicato. Non confrontare direttamente label con ID diversi.

### v1

- 426 immagini;
- split: 319 train, 64 validation, 43 test;
- 44 negative;
- prima baseline pulita YOLOv8n;
- problemi: recall Ambulanza molto basso, notte debole, confusione Ambulanza/VDF
  e molti falsi positivi.

Test congelato v1:

| Precision | Recall | mAP50 | mAP50-95 |
|---:|---:|---:|---:|
| 0.845 | 0.614 | 0.763 | 0.590 |

### v1.1

- 517 immagini: 91 aggiunte rispetto alla v1;
- split: 397 train, 77 validation, 43 test;
- 461 positive e 56 negative;
- training completato per 100 epoche; `best.pt` all'epoca 82;
- grande miglioramento nei sei benchmark, soprattutto Ambulanza e Carabinieri.

Test congelato v1.1:

| Precision | Recall | mAP50 | mAP50-95 |
|---:|---:|---:|---:|
| 0.983 | 0.770 | 0.850 | 0.705 |

### v1.2 — baseline precedente

- 586 immagini: 69 aggiunte rispetto alla v1.1;
- split: 458 train, 85 validation, 43 test;
- 512 positive e 74 negative;
- aggiunte: 22 Ambulanza, 10 Carabinieri, 18 VDF, una multiclasse e 18 NULL;
- test storico invariato;
- training terminato per early stopping all'epoca 57;
- `best.pt` selezionato all'epoca 32.

Test congelato v1.2:

| Precision | Recall | mAP50 | mAP50-95 |
|---:|---:|---:|---:|
| 0.930 | 0.763 | 0.890 | 0.723 |

Confronto per classe v1.1 -> v1.2:

- Ambulanza: recall `0.769 -> 0.846`, mAP50 `0.896 -> 0.932`;
- Carabinieri: mAP50 `0.666 -> 0.756`, mAP50-95 `0.554 -> 0.636`;
- VDF: recall `0.947 -> 0.842`, mAP50-95 `0.836 -> 0.797`.

Verdetto storico: v1.2 ha preceduto la v1.3 come baseline generale, senza
dominare la v1.1 in ogni scenario.

### Esperimenti v1.2 senza nuove immagini

Sono state provate due varianti, entrambe archiviate ma non promosse:

- `v1.2_Aug`: Exposure/Blur Roboflow; aumenta recall e persistenza delle box,
  ma introduce troppi falsi positivi e confusioni;
- `v1.2 Multi-scale`: `multi_scale=0.25`; piu' equilibrato e migliore su VDF
  notte, ma il guadagno generale nei video e' troppo modesto.

Le due varianti restano archiviate e non promosse. Non combinarle
automaticamente con la baseline successiva.

### v1.3 — baseline corrente

- 664 immagini: 78 aggiunte rispetto alla v1.2;
- split: 524 train, 97 validation, 43 test;
- 564 positive e 100 NULL;
- nuove aggiunte: 52 positive e 26 NULL;
- profilo nuove positive: 28 FAR, 14 MID, 5 CLOSE, 5 MIXED; 34 NIGHT, 18 DAY;
- test storico invariato;
- training completato per 100 epoche; `best.pt` selezionato all'epoca 99.

Test congelato v1.3:

| Precision | Recall | mAP50 | mAP50-95 |
|---:|---:|---:|---:|
| 0.962 | 0.832 | 0.926 | 0.764 |

Verdetto: la v1.3 supera globalmente la v1.2 sul test e nei benchmark. I
progressi principali riguardano Ambulanza, notte, FAR, occlusioni e stabilita'
delle box. Restano mirati gli errori su veicoli rossi, Carabinieri notturni e
VDF con lampeggianti a diverse altezze.

## Benchmark video

I benchmark sono in `data/test_videos/`:

- Ambulanza giorno;
- Ambulanza notte;
- Carabinieri giorno;
- Carabinieri notte;
- VDF giorno;
- VDF notte ordinario;
- VDF notte stress.

Sono esterni al training e vengono eseguiti con `conf=0.60`. Non hanno ground
truth frame per frame: le conclusioni sono qualitative. I feedback completi
sono sotto `experiments/video_tests/<versione>/`.

Esito v1.2:

- Ambulanza giorno: falsi positivi nettamente ridotti; ancora debole FAR e
  occlusioni dinamiche;
- Ambulanza notte: miglioramento netto e minore confusione con VDF;
- Carabinieri giorno: sostanzialmente stabile, auto nera ancora problematica;
- Carabinieri notte: leggera regressione, box instabile e nuova confusione VDF;
- VDF giorno: pickup recuperato, bus rosso ancora FP saltuario;
- VDF notte: stabile o leggermente peggiore, confusione tra tutte e tre le classi.

Gli appena 18 nuovi NULL hanno migliorato chiaramente i falsi positivi. Le
occlusioni non sono migliorate quanto previsto, perche' molte aggiunte erano
statiche/close mentre i benchmark contengono occlusioni dinamiche, FAR/MID, blur
e movimento. `predict_video.py` esegue detection indipendente su ogni frame: non
e' tracking e non ottimizza direttamente la stabilita' temporale.

Il vecchio benchmark VDF notte e' conservato come stress test. Con v1.3 e' stato
aggiunto un secondo benchmark VDF notte piu' ordinario.

## Prossimo lavoro

La v1.3 e' completata e promossa a baseline. Prima di aprire una nuova versione
reale occorre definire uno dei due percorsi:

1. una piccola v1.4 mirata agli errori residui dimostrati;
2. il passaggio strutturale a v2, quando cambiano tassonomia o dominio visivo.

Backlog reale immediato: Carabinieri NIGHT FAR/MID con lampeggianti OFF; VDF
notte con lampeggianti a diverse altezze; hard negative rossi/neri/bianchi e
auto illuminate di blu; definizione della distanza operativa; benchmark della
telecamera finale.

Il primo esperimento Copy-Paste separato e' stato completato come `v1.3_cp`:
60 composizioni DAY (20 per classe; 36 FAR e 24 MID) sono state aggiunte solo
al train, lasciando validation, test e benchmark congelati. Sul test produce
P 0.980, R 0.772, mAP50 0.864 e mAP50-95 0.735, contro 0.962/0.832/0.926/0.764
della v1.3. Migliora localmente VDF e alcuni casi video, ma perde recall e mAP
e aumenta i falsi positivi: non e' promosso. Un eventuale passo successivo e'
un'ablazione con le sole 20 composizioni Carabinieri gia' generate.

## Modelli e artefatti principali

- peso preaddestrato: `models/pretrained/yolov8n.pt`;
- migliore v1.3: `experiments/Train/baseline_v1_3_yolov8n/weights/best.pt`;
- configurazione training: `experiments/Train/baseline_v1_3_yolov8n/args.yaml`;
- curve training: `experiments/Train/baseline_v1_3_yolov8n/results.png`;
- test v1.3: `experiments/Test/evaluation_test_v1_3_frozen/`;
- log v1.3: `docs/logs/6. LOG_TRAIN_V1.3.txt`;
- esperimento Aug: `experiments/Test/evaluation_test_v1_2_aug_base/REPORT.md`;
- esperimento Multi-scale: `experiments/Test/evaluation_test_v1_2_multiscale/REPORT.md`;
- metadata: `docs/project/METADATA_CLASSI.md`;
- manifest split: `data/datasets/v1.3/split_manifest.csv`;
- feedback benchmark: `experiments/video_tests/v1.3/feedback bench v1.3.txt`.
- dataset Copy-Paste: `data/datasets/v1.3_cp/`;
- generatore e manifest Copy-Paste: `data/raw/v1.3_cp/`;
- training Copy-Paste: `experiments/Train/exp_v1_3_cp_day_001/`;
- test Copy-Paste: `experiments/Test/evaluation_test_v1_3_cp_day_001/`;
- benchmark Copy-Paste: `experiments/video_tests/v1.3_cp/`;
- log Copy-Paste: `docs/logs/7. LOG_TRAIN_V1.3_CP.txt`.

## Training corrente

Il confronto tra versioni e' stato mantenuto controllato:

```text
model: yolov8n.pt preaddestrato
epochs: 100
imgsz: 640
batch: 16
patience: 25
workers: 4
seed: 42
deterministic: true
```

Per confrontare una futura baseline, ripartire dallo stesso `yolov8n.pt`, non
dal `best.pt` della v1.3, salvo esperimento separato esplicitamente dichiarato.

## Regole di interpretazione

- confidence: punteggio interno della singola predizione, non probabilita'
  calibrata;
- precision: quante predizioni prodotte sono corrette;
- recall: quanti mezzi reali vengono trovati;
- F1: media armonica che premia precision e recall entrambe alte; non richiede
  che siano uguali;
- IoU: sovrapposizione geometrica fra box predetto e ground truth;
- mAP50: valutazione permissiva con IoU 0.50;
- mAP50-95: valutazione piu' severa della classificazione/localizzazione;
- `best.pt`: miglior checkpoint sulla validation;
- `last.pt`: ultima epoca, non necessariamente migliore.

Consultare `docs/guides/GUIDA_LETTURA_METRICHE_YOLO.md` prima di ricostruire queste
spiegazioni.

## Compatibilita' Mac

Non copiare il `.venv` Windows. Crearne uno locale. Gli script principali usano
path relativi e selezione automatica `CUDA -> MPS -> CPU`. Anche `testGPU.py` e
`scripts/archive/legacy_analysis/analyze_test_by_distance.py` sono stati resi
multipiattaforma prima del trasferimento.

Il modello `.pt` e' portabile. Training eseguiti su CUDA e MPS possono produrre
risultati numericamente differenti anche con lo stesso seed; confrontare le
metriche, non gli hash dei pesi.

Attenzione ai file macOS:

```text
.DS_Store
._*.jpg
__MACOSX/
```

Non devono entrare nei batch o negli ZIP Roboflow.

## Comportamento richiesto alla nuova chat

Quando ricevi una richiesta:

1. stabilisci se e' una domanda, una diagnosi o una modifica;
2. per le domande, rispondi direttamente senza cambiare file;
3. per le diagnosi, raccogli prove dai log e dai metadata prima di concludere;
4. per le modifiche, preserva struttura, versioni e file dell'utente;
5. aggiorna i README pertinenti quando cambia realmente la struttura o lo stato;
6. non creare nuove cartelle/versioni senza una ragione concreta;
7. non eseguire training lungo o download massivi senza che siano necessari;
8. non aprire grandi quantita' di immagini per ricostruire dati gia' annotati;
9. quando proponi una raccolta, specifica quantita', condizioni, fonti e problema
   che vuole correggere;
10. prima di dichiarare migliore un modello, incrocia test congelato e benchmark.

La baseline resta v1.3. Il prossimo passo sperimentale possibile e' decidere se
eseguire l'ablazione Copy-Paste Carabinieri-only; il prossimo passo reale resta
una futura v1.4 guidata dagli errori residui. In entrambi i casi test e benchmark
storici restano congelati. Il porting macOS e' gia' funzionante; continuare a
sincronizzare soltanto file importanti, log, report e documentazione, senza
copiare i `.venv` fra sistemi.
