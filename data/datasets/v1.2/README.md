# SemaforoSmart dataset v1.2

Dataset cumulativo: i 517 file della v1.1 mantengono esattamente il proprio split; il test resta congelato.

- Export originale Roboflow: `v1.2.zip` (586 immagini; 517 gia' in v1.1, 69 aggiunte).
- Aggiunte per nome: Ambulanza 22, Carabinieri 10, VDF 18, Multiclasse 1, Negative 18.
- Totali per bucket: Ambulanza 169, Carabinieri 139, VDF 203, Multiclasse 1, Negative 74.
- Aggiunte assegnate: train 61, valid 8, test 0.
- Tutti i frame delle due compilation di Roma centro, positivi e NULL, formano un unico gruppo in train.
- Nessuna immagine v1.2 e' stata aggiunta al test.
- `split_manifest.csv` documenta file, gruppo e split.

| Split | v1.1 | Aggiunte | Totale |
|---|---:|---:|---:|
| train | 397 | 61 | 458 |
| valid | 77 | 8 | 85 |
| test | 43 | 0 | 43 |

## Esperimento associato

- Training: `../../../experiments/Train/baseline_v1_2_yolov8n/`
- Early stopping: epoca 57; checkpoint migliore: epoca 32.
- Valutazione sul test congelato: `../../../experiments/Test/evaluation_test_v1_2_new/`
- Risultato test: Precision 0.930, Recall 0.763, mAP50 0.890,
  mAP50-95 0.723.
- Feedback sui sei benchmark:
  `../../../experiments/video_tests/v1.2/feedback bench v1.2.txt`.

Il test statico migliora globalmente rispetto alla v1.1, ma i benchmark mostrano
una regressione locale su Carabinieri notte e difficolta' ancora presenti su VDF
notte e occlusioni dinamiche.
