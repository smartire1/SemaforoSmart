# SemaforoSmart dataset v1.3

Dataset cumulativo v1.2 + 78 nuove immagini v1.3. Il test storico resta
invariato; le aggiunte sono state assegnate soltanto a train e validation.

| Voce | Valore |
|---|---:|
| Totale immagini | 664 |
| Positive | 564 |
| NULL | 100 |
| Train | 524 |
| Validation | 97 |
| Test congelato | 43 |

Le aggiunte v1.3 comprendono 52 positive e 26 NULL. Tra le positive: 28 FAR,
14 MID, 5 CLOSE e 5 MIXED; 34 NIGHT e 18 DAY; 44 STREET e 8 ELEVATED. Il batch
e' quindi coerente con l'obiettivo di rafforzare notte, distanza e contesti
difficili senza modificare il test storico.

## Regole di riproducibilita'

- Seed: 42
- `split_manifest.csv` documenta file, gruppo e split.
- I frame della stessa fonte restano nello stesso split.
- Nessuna immagine v1.3 e' presente nel test.
- Lo ZIP Roboflow originale e' conservato come `v1.3.zip`.

## Artefatti collegati

- Training: `../../../experiments/Train/baseline_v1_3_yolov8n/`
- Test congelato: `../../../experiments/Test/evaluation_test_v1_3_frozen/`
- Benchmark: `../../../experiments/video_tests/v1.3/`
- Metadata: `../../../docs/project/METADATA_CLASSI.md`
