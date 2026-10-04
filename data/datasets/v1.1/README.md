# SemaforoSmart dataset v1.1

Dataset cumulativo: i 426 file della v1 sono copiati senza modifiche e mantengono esattamente il loro split.

- Export originale Roboflow conservato qui: `v1.1.zip` (517 immagini;
  426 gia' in v1, 91 aggiunte). Le cartelle train/valid/test qui accanto
  costituiscono lo split locale usato per il training, non l'export grezzo.
- Nuove per tipo: Ambulanza 32, Carabinieri 33, VDF 14, Negative 12.
- Totale v1.1 per tipo: Ambulanza 147, Carabinieri 129, VDF 185, Negative 56.
- Nuove assegnate: train 78, valid 13, test 0.
- Le nuove negative sono in train: la loro fonte/gruppo non e' documentata.
- `car_old_video_001_frame_001` e' in train con gli altri frame della stessa fonte gia' presenti in v1.
- `v11_car_video_009_frame_001` e `car_old_video_003_frame_005` sono esclusi dopo review.
- Il test v1 resta intatto; i sei video benchmark restano esterni al training.
- `split_manifest.csv` documenta ogni file e gruppo.

| Split | v1 | Aggiunte | Totale |
|---|---:|---:|---:|
| train | 319 | 78 | 397 |
| valid | 64 | 13 | 77 |
| test | 43 | 0 | 43 |
