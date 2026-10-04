# Esperimenti

Gli output sono separati per funzione. Non rinominare o mescolare manualmente i
file interni prodotti da Ultralytics.

```text
experiments/
├── Train/        training e relativi checkpoint
├── Test/         valutazioni formali sui test set
└── video_tests/  inferenze e feedback sui benchmark video
```

Per il training, `weights/best.pt` è il checkpoint con le migliori metriche di
validazione; grafici, configurazione e risultati restano nella stessa cartella.

Le valutazioni sul test set vanno salvate sotto `Test/evaluation_*`, mentre le
inferenze sui video restano sotto `video_tests/`.

## Baseline corrente

La baseline corrente e' `Train/baseline_v1_3_yolov8n/`. Il confronto statico usa
`Test/evaluation_test_v1_3_frozen/`; gli output video e il feedback completo sono
in `video_tests/v1.3/`. La v1.3 supera globalmente la v1.2 sul test congelato e
nei benchmark, quindi i risultati precedenti restano riferimenti storici e non
devono essere sovrascritti.

## Varianti sperimentali v1.2

`Train/exp_v1_2_aug_base/` e `Train/exp_v1_2_multiscale/` sono esperimenti
conclusi e non promossi a baseline. Il primo aumenta eccessivamente falsi
positivi e confusioni; il secondo e' piu' equilibrato e migliora VDF notte, ma
non abbastanza da superare operativamente la v1.2. I relativi confronti sono in
`Test/evaluation_test_v1_2_aug_base/` e
`Test/evaluation_test_v1_2_multiscale/`.

`video_tests/OLD/` contiene l'unico output video conservato del modello storico
`bestOLD.pt`; le cartelle `v1/`, `v1.1/`, `v1.2/`, `v1.2_Aug/` e
`v1.2_Multiscale/` raccolgono invece benchmark ordinati per esperimento. La
cartella `v1.3/` comprende anche il nuovo benchmark VDF notte ordinario; il
precedente video difficile e' mantenuto come `vdf_notte_stress`.

## Esperimento Copy-Paste v1.3

`Train/exp_v1_3_cp_day_001/` usa la v1.3 con 60 composizioni DAY aggiunte al
solo train. Il test congelato e' in
`Test/evaluation_test_v1_3_cp_day_001/`; i sei benchmark eseguiti sono ordinati
in `video_tests/v1.3_cp/day_001/`.

Il modello migliora VDF e alcuni casi qualitativi, in particolare Carabinieri
notte, ma regredisce nelle metriche aggregate e aumenta i falsi positivi video.
Non e' promosso: la baseline resta `baseline_v1_3_yolov8n`.
