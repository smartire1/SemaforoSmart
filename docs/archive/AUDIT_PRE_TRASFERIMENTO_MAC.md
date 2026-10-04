# Audit pre-trasferimento Mac

> Nota successiva all'audit (22 settembre 2026): le copie
> `data/raw/v1/ready_for_roboflow/` e `weights/yolo26n.pt` sono state eliminate;
> i 13 ZIP di `v1/OLDbatch/` sono stati spostati in `data/raw/OLDraw/`; le
> raccolte `v1/` e `v1.1/` sono state appiattite. Le sezioni sotto restano come
> fotografia tecnica dello stato rilevato prima della pulizia.

Audit eseguito il **22 settembre 2026** senza cancellare o spostare file e senza
ispezionare visivamente le immagini.

## Esito sintetico

- Struttura dei dataset valida.
- Tutte le immagini di v1, v1.1 e v1.2 hanno la label corrispondente.
- Nessun duplicato esatto interno agli split dei tre dataset.
- Nessun duplicato esatto tra le raccolte raw v1, v1.1 e v1.2.
- Nessun file immagine corrotto durante il controllo automatico.
- Unica duplicazione massiva confermata: `data/raw/v1/ready_for_roboflow/`.

## Verifica immagini

Sono state analizzate 2.607 immagini sotto `data/`, per circa 1,59 GB, tramite
SHA-256 e impronta percettiva automatica. Le immagini non sono state aperte a
video.

| Area | Immagini | Gruppi duplicati interni | Esito |
|---|---:|---:|---|
| raw v1 | 873 | 384 | copie attese `ready_for_roboflow` ↔ sorgenti |
| raw v1.1 | 91 | 0 | pulito |
| raw v1.2 | 71 | 0 | pulito; include 69 usate + 2 reserve |
| dataset v1 | 426 | 0 | pulito |
| dataset v1.1 | 517 | 0 | pulito |
| dataset v1.2 | 586 | 0 | pulito |
| mapping storico OLD | 43 | 0 | copia derivata intenzionale |

I 384 gruppi raw v1 sono formati da una copia in
`data/raw/v1/ready_for_roboflow/` e dalla corrispondente sorgente in
`data/raw/v1/images/`. Non sono stati trovati altri pattern duplicati nella raw
v1.

Gli export Roboflow non sono byte-identici alle raw perché vengono ricodificati e
rinominati. Questo e' previsto e non equivale a un duplicato anomalo.

## Coerenza immagini/label

| Dataset | Train | Validation | Test | Differenze immagini/label |
|---|---:|---:|---:|---:|
| v1 | 319 | 64 | 43 | 0 |
| v1.1 | 397 | 77 | 43 | 0 |
| v1.2 | 458 | 85 | 43 | 0 |

## Eliminabili senza perdita informativa

Questi elementi sono rigenerabili, vuoti oppure superati:

- `scripts/__pycache__/` — bytecode Python rigenerabile;
- tutti i `labels.cache` sotto `data/datasets/` — cache Ultralytics;
- i `labels.cache` sotto `experiments/evaluation_distance_v1/datasets/`;
- `runs/` — contiene soltanto cartelle vuote residue;
- `experiments/evaluation_distance_v1/new_close/` — vuota;
- `experiments/evaluation_distance_v1/new_far/` — vuota;
- `experiments/evaluation_distance_v1/new_medium/` — vuota;
- `experiments/evaluation_distance_v1/old_close/` — vuota;
- `experiments/evaluation_distance_v1/old_far/` — vuota;
- `experiments/evaluation_distance_v1/old_medium/` — vuota;
- `weights/yolo26n.pt` — cache tecnica Ultralytics, non e' uno dei modelli del
  progetto;
- `docs/METADATA_V1_2_TEMP.txt` — foglio temporaneo ormai riversato nel metadata
  cumulativo;
- `Comandi utili.txt` — riferimenti prevalentemente alla v1, a `device=0` e a
  PowerShell; sostituito per il Mac da `HANDOFF_MAC/COMANDI_MAC.md`.

## Ridondante ma da eliminare solo se si vuole alleggerire

### Copia raw v1

- `data/raw/v1/ready_for_roboflow/`
- 384 file, circa 473,7 MB.
- Tutti i file sono copie SHA-256 esatte di immagini gia' presenti sotto
  `data/raw/v1/images/`.
- La cartella era una vecchia preparazione per l'upload, non una fonte autonoma.

Puo' essere esclusa dal trasferimento Mac senza perdere immagini uniche.

### Dataset temporanei della valutazione per distanza

- `experiments/evaluation_distance_v1/datasets/`
- 168 file, circa 11,6 MB.
- Copie generate dallo script di analisi.
- Il risultato utile e' `experiments/evaluation_distance_v1/distance_results.json`.

Puo' essere rigenerata con
`scripts/archive/legacy_analysis/analyze_test_by_distance.py`.

### Mapping storico bestOLD

- `data/datasets/v1_eval_old_mapping/`
- circa 6,5 MB.
- Copia derivata intenzionalmente per rimappare gli ID delle classi del vecchio
  `bestOLD.pt`.

Non e' necessaria per v1.2/v1.3. Mantenerla solo se si vuole ripetere il confronto
con il modello OLD.

## Materiale storico pesante: non inutile

Questi elementi possono essere esclusi da una copia Mac leggera, ma non vanno
considerati errori o duplicati:

- `data/raw/v1/OLDbatch/` — 13 ZIP storici unici, circa 370,2 MB;
- `experiments/video_tests/nuovo_conf025_live_ambulanza_notte/` — prova iniziale,
  circa 9 MB;
- `experiments/video_tests/nuovo_conf025_live_carabinieri_notte/` — prova
  iniziale, circa 61,1 MB;
- `experiments/video_tests/nuovo_conf060OLD/` — inferenza storica bestOLD, circa
  211,7 MB.

I test versionati sotto `experiments/video_tests/v1/`, `v1.1/` e `v1.2/` sono
invece confronti controllati e conviene conservarli in un trasferimento completo.

## Duplicazioni intenzionali da mantenere

- ZIP originali Roboflow `v1.zip`, `v1.1.zip`, `v1.2.zip` insieme agli split
  estratti;
- raw selezionate insieme agli export annotati;
- test congelato replicato nelle tre versioni;
- `best.pt` e `last.pt` di ogni training;
- immagini e label del mapping OLD se si conserva il confronto storico;
- sei video benchmark originali insieme agli output predetti versionati.

## Cartelle vuote intenzionali

- `data/raw/v2/` e' predisposta per una futura revisione strutturale e puo'
  restare vuota.

La prossima raccolta e' v1.3, ma non e' stata ancora creata per evitare cartelle
premature.

## Nome fuorviante ma file necessario

`METADATA_DA_COMPILARE.md` e' ormai compilato fino alla v1.2. Il nome e'
storicamente superato, ma il file e' il catalogo cumulativo corrente. Non
eliminarlo. Un'eventuale rinomina richiede l'aggiornamento coordinato di README,
script e prompt di handoff.

## Ordine di pulizia consigliato

1. eliminare cache, `__pycache__`, cartelle vuote residue e `runs/`;
2. eliminare i due file temporanei/obsoleti indicati;
3. escludere `ready_for_roboflow/` dalla copia Mac;
4. decidere se trasferire archivio OLDbatch, mapping OLD e inferenze esplorative;
5. conservare integralmente dataset v1.2, modello v1.2, benchmark originali,
   feedback e documentazione.

Nessuna cancellazione e' stata eseguita durante l'audit.
