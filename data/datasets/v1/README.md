# SemaforoSmart dataset v1

Split locale deterministico e senza contaminazione tra frame correlati.

`v1.zip` e' l'export originale Roboflow (426 immagini, prima dello split locale).
Le cartelle `train/`, `valid/` e `test/` qui accanto sono invece il dataset v1
effettivamente usato per il training. Lo ZIP non va estratto sopra di esse.

- Ripartizione obiettivo: 75% train, 15% valid, 10% test
- Seed: 42
- I frame dello stesso video e le viste della stessa serie restano nello stesso split.
- I file label vuoti rappresentano immagini negative (Null in Roboflow).
- `split_manifest.csv` documenta l'assegnazione di ogni immagine.

## Conteggi

| Split | Totale | Ambulanza | Carabinieri | VDF | Negative |
|---|---:|---:|---:|---:|---:|
| train | 319 | 86 | 72 | 128 | 33 |
| valid | 64 | 17 | 14 | 26 | 7 |
| test | 43 | 12 | 10 | 17 | 4 |
