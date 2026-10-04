# Raccolte raw

Questa cartella conserva le immagini prima dell'annotazione/esportazione YOLO.
Non e' il dataset di training: gli export versionati stanno in `../datasets/`.

```text
data/raw/
├── OLDraw/                     13 ZIP dei batch storici del vecchio progetto
├── v1/                         materiale sorgente della prima versione
│   ├── OLDannotate/            162 immagini recuperate dal vecchio lavoro; qui non ci sono label
│   ├── OLDnon_annotate/         61 immagini vecchie non selezionate per v1
│   ├── NEWambulanza/            75 immagini nuove raccolte per v1
│   ├── NEWcarabinieri/          50 immagini nuove raccolte per v1
│   ├── NEWvigiliDelFuoco/       97 immagini nuove raccolte per v1
│   └── NEWnegative/             44 immagini negative della raccolta v1
├── v1.1/
│   ├── Ambulanza/              32 immagini candidate per v1.1
│   ├── Carabinieri/            33 immagini candidate per v1.1
│   ├── VDF/                    14 immagini candidate per v1.1
│   └── Negative/               12 immagini senza veicoli target
├── v1.2/
│   ├── Ambulanza/              23 immagini, incluso lo screen multiclasse
│   ├── Carabinieri/            10 immagini da video/compilation
│   ├── VDF/                    18 immagini da video/compilation
│   ├── Negative/               18 hard negative da Roma centro
│   ├── z. reserve/             2 immagini Ambulanza escluse dal batch
│   └── README.md               inventario e istruzioni del batch v1.2
├── v1.3/
│   ├── Ambulanza/               13 immagini ordinate per fonte/frame
│   ├── Carabinieri/             21 immagini ordinate per fonte/frame
│   ├── VDF/                     19 immagini ordinate per fonte/frame
│   ├── NULL/                    26 hard negative senza fonte puntuale
│   └── README.md                inventario e istruzioni del batch v1.3
├── v1.3_cp/                     ramo sintetico Copy-Paste derivato dalla v1.3
│   ├── backgrounds/             sei sfondi NULL reali
│   ├── cutouts/                 sei ritagli PNG e relative sorgenti
│   ├── generated/               batch DAY e prove archiviate
│   └── README.md                diario completo dell'esperimento
└── v2/                        riservata a raccolte successive; ancora vuota
```

## Come usare le cartelle

- Le quattro sottocartelle di `v1.1/` conservano i batch caricati su Roboflow:
  tre batch positivi per classe e un batch
  separato per le negative, senza bounding box. Le cartelle agevolano l'upload;
  sono i nomi dei file a conservare l'ID della fonte. I nomi
  `v11_<classe>_video_<fonte>_frame_<n>` mantengono insieme i frame della
  stessa fonte; `v11_car_source_unknown_video_001_frame_*` e' una coppia con link
  perso ma comunque da tenere nello stesso gruppo. I dettagli sono in
  `../../docs/project/FONTI_DATASET.txt`, registro centrale condiviso tra le versioni.
- La vecchia cartella duplicata `ready_for_roboflow/` e' stata rimossa dopo
  verifica SHA-256: non conteneva immagini uniche.
- Le negative della v1 sono in `v1/NEWnegative/`. Le 12 negative aggiunte nel
  ciclo successivo sono in `v1.1/Negative/`.
- Il raw del batch v1.1 conserva anche `v11_car_video_009_frame_001`, escluso
  dopo review. Nell'export entra invece `car_old_video_001_frame_001`, conservato
  in `v1/OLDannotate/` ma mai incluso nel dataset v1: per questo
  l'export aggiunge 91 immagini pur avendo una sostituzione rispetto ai 91 raw
  del batch. `car_old_video_003_frame_005` era in reject ed e' escluso.
- Non usare `v2/` per il batch attuale: e' soltanto uno spazio predisposto.
- `v1.2/` conserva le sorgenti del ciclo correttivo ormai completato. Il relativo
  export YOLO e lo split definitivo sono in `data/datasets/v1.2/`; criteri di
  selezione ed esito sono documentati nel `README.md` della raccolta.
- `v1.3/` conserva la raccolta correttiva ormai completata: 53 candidate
  positive e 26 candidate NULL. Dopo il controllo, 78 immagini sono entrate
  nell'export cumulativo (52 positive e 26 NULL); `v13_null_hn_001` era solo uno
  screen di riferimento ed e' rimasto escluso. Dataset e split definitivi sono
  in `data/datasets/v1.3/`.
- `v1.3_cp/` non e' una nuova versione reale: contiene il collaudo e il primo
  batch sintetico DAY da 60 composizioni. Dataset, training, test e feedback
  sono descritti nel suo README unico; la baseline v1.3 resta invariata.
- `OLDraw/` e' un archivio storico separato: non viene letto dagli script di
  training o costruzione dei dataset.
- Non eliminare il materiale storico da `v1/`; per addestrare si usa l'export in
  `data/datasets/`, non queste cartelle raw.
