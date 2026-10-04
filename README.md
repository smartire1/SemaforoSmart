# SemaforoSmart

Nuovo spazio di lavoro ordinato per il progetto di rilevamento dei veicoli di emergenza.

La cartella `SemaforoSmart OLD`, affiancata a questa, conserva integralmente il materiale precedente e va considerata come archivio storico.

## Struttura

### `data/raw/`

Materiale originale, separato per ciclo di raccolta: `OLDraw/` conserva i 13 ZIP
storici; `v1/` conserva le immagini sorgente della prima versione; `v1.1/`
contiene, in quattro cartelle di classe, le immagini aggiunte con la v1.1;
`v1.2/` e `v1.3/` contengono il materiale sorgente delle raccolte correttive;
`v1.3_cp/` conserva materiali, configurazioni e risultati generati del ramo
Copy-Paste DAY;
`v2/` e' riservata alle raccolte future ed e' ancora vuota. Il registro trasversale delle fonti e' in
`docs/project/FONTI_DATASET.txt`; la mappa completa e le regole d'uso sono in
`data/raw/README.md`.

Qui non vanno inserite esportazioni YOLO. L'unica eccezione alle immagini raw e'
`v1.3_cp/`, area sperimentale esplicitamente documentata che contiene ritagli,
sfondi e composizioni sintetiche; i dataset addestrabili restano in
`data/datasets/`.

### `data/datasets/`

Esportazioni complete e versionate provenienti da Roboflow. Ogni versione conterrà il proprio `data.yaml` e gli split YOLO con le rispettive cartelle `images` e `labels`.

Struttura adottata per ogni versione:

```text
data/datasets/v1/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

La cartella `v1` contiene gia' il primo export. Le versioni successive avranno
cartelle separate, senza sovrascrivere la v1.
`v1.1/` contiene 517 immagini: le 426 della v1 con split invariato e 91 aggiunte;
il test v1 di 43 immagini resta identico. Dettagli in `data/datasets/v1.1/README.md`.
`v1.2/` contiene 586 immagini: conserva integralmente lo split v1.1 e aggiunge
69 immagini (61 in train e 8 in valid); il test storico di 43 immagini resta
ancora invariato. Dettagli e manifest in `data/datasets/v1.2/README.md`.
`v1.2_Aug/` e' una variante esclusivamente sperimentale: usa due versioni
Exposure/Blur per ogni sorgente train della v1.2, mentre validation e test
restano originali e congelati. Dettagli in `data/datasets/v1.2_Aug/README.md`.
`v1.3/` contiene 664 immagini: conserva il test storico di 43 immagini e
aggiunge 78 elementi mirati alla v1.2 (52 positivi e 26 NULL), assegnati solo a
train e validation. Dettagli e manifest sono in `data/datasets/v1.3/README.md`.
`v1.3_cp/` e' la variante sperimentale DAY: train v1.3 + 60 composizioni
Copy-Paste, con validation e test identici alla baseline. Non e' stata promossa;
il README dedicato e' in `data/datasets/v1.3_cp/README.md`.
Gli ZIP originali Roboflow sono conservati dentro le rispettive cartelle da
`v1/` a `v1.3/`, separati dagli split locali train/valid/test. `v1.3_cp/`
riutilizza lo ZIP v1.3 come base reale e documenta a parte le aggiunte sintetiche.

### `scripts/`

Codice Python separato per utilizzo: gli strumenti generali restano nella root,
gli script di esperimenti attivi sono in `scripts/experiments/` e i costruttori
o controlli storici in `scripts/archive/`. La mappa completa e i comandi sono in
`scripts/README.md`.

### `experiments/`

`Train/` contiene training e checkpoint, `Test/` le valutazioni formali e
`video_tests/` le inferenze sui benchmark. Ogni esperimento mantiene una propria
cartella identificabile.

### `docs/`

Documentazione ordinata per funzione: `project/` contiene stato, metadata e
fonti; `guides/` le procedure; `logs/` gli output dei training; `handoff/` il
contesto condiviso e le regole di sincronizzazione; `archive/` i documenti
storici. L'indice completo e' in `docs/README.md`.

### `models/`

Pesi di partenza ed eventuali modelli esportati per PC, Mac o sistema embedded.
Il peso preaddestrato iniziale è conservato in `models/pretrained/yolov8n.pt`;
i checkpoint dei training restano sotto `experiments/Train/`.

### `weights/`

Cache tecnica creata automaticamente da Ultralytics per controlli interni, come il modello temporaneo usato nel test AMP. Non contiene i risultati del progetto.
Puo' essere esclusa dalla sincronizzazione e ricreata automaticamente.

### `requirements.txt`

Dipendenze Python minime del progetto. Resta nella root per consentire
`python -m pip install -r requirements.txt` su entrambi i sistemi; `.venv/`
rimane invece locale e non va copiata.

## Regola di lavoro

Il flusso previsto è: `raw/vN` -> Roboflow -> `datasets/vN` -> training -> `experiments` e `models`.

Ogni esperimento dovrà indicare chiaramente quale versione `vN` del dataset ha utilizzato.

La baseline sperimentale corrente e' la **v1.3**. Ha migliorato test congelato e
benchmark video soprattutto su NIGHT, FAR e occlusioni, pur lasciando errori
mirati su veicoli rossi, Carabinieri lontani/notturni e VDF illuminati dai
lampeggianti. La v2 resta riservata a cambiamenti strutturali, come nuove classi
o un nuovo dominio visivo.

La fase attuale usa `carabinieri`, `vigili_del_fuoco` e `ambulanza`; la tassonomia
futura dovra' includere altre classi, tra cui Polizia e Guardia di Finanza.

Le istruzioni operative per il primo addestramento sono in `docs/guides/AVVIO_TRAINING.md`.
La spiegazione di confidence, IoU, precision, recall, F1, mAP, loss, curve e
matrice di confusione e' in `docs/guides/GUIDA_LETTURA_METRICHE_YOLO.md`.
Il riepilogo quantitativo, il diario delle versioni e il backlog corrente sono in
`docs/project/STATO_PROGETTO.md`.

Il contesto per una nuova chat e' in `docs/handoff/CONTESTO_CODEX.md`; le regole
provvisorie per sincronizzare Windows e macOS sono in
`docs/handoff/SYNC_PC_MAC.md`. Il vecchio audit di trasferimento e il prompt
originario sono conservati in `docs/archive/`.
