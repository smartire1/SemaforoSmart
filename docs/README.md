# Documentazione SemaforoSmart

La documentazione e' separata per funzione, così da distinguere lo stato
corrente dai materiali storici.

```text
docs/
├── project/   stato formale, metadata e fonti del dataset
├── guides/    procedure e comandi operativi
├── logs/      output integrali dei training
├── handoff/   contesto Codex e sincronizzazione Windows/macOS
└── archive/   documenti storici non piu' operativi
```

## Da consultare normalmente

- `project/STATO_PROGETTO.md`: baseline, risultati, limiti e backlog;
- `project/METADATA_CLASSI.md`: catalogo delle condizioni delle immagini;
- `project/FONTI_DATASET.txt`: provenienza del materiale;
- `guides/COMANDI_OPERATIVI.md`: comandi Windows e macOS;
- `guides/AVVIO_TRAINING.md`: procedura di training;
- `guides/GUIDA_LETTURA_METRICHE_YOLO.md`: lettura delle metriche;
- `handoff/CONTESTO_CODEX.md`: contesto completo per una nuova chat;
- `handoff/SYNC_PC_MAC.md`: regole per riportare le modifiche tra computer.

La baseline corrente e' **v1.3**. Il riepilogo formale e il backlog aggiornato
sono in `project/STATO_PROGETTO.md`; il feedback operativo e' in
`../experiments/video_tests/v1.3/`.

Il primo esperimento Copy-Paste e' concluso ma non promosso. Il diario completo
resta in `../data/raw/v1.3_cp/README.md`; dataset e risultati sono collegati dai
rispettivi README.

`archive/` non descrive necessariamente lo stato attuale: conserva il prompt
originario, l'audit precedente al primo trasferimento e lo snapshot del vecchio
ambiente Mac.
