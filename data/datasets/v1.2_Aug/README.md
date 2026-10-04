# SemaforoSmart dataset v1.2_Aug

Variante sperimentale della v1.2 senza nuove sorgenti. Roboflow v4 ha generato due versioni per immagine con Exposure tra -15% e +15% e Gaussian Blur tra 0 e 1.4 px.

- Train: 916 immagini augmentate, due per ciascuna delle 458 sorgenti train.
- Validation: 85 originali congelate dalla v1.2.
- Test: 43 originali congelate dalla v1.2.
- Le 256 augmentation derivate dalle 128 sorgenti validation/test sono escluse.
- `split_manifest.csv` documenta origine, variante e split.
- `v1.2_Aug.zip` conserva l'export Roboflow integrale da 1172 immagini.

Questa versione serve soltanto a esperimenti controllati e non sostituisce la baseline v1.2.

## Primo esperimento

- Training: `../../../experiments/Train/exp_v1_2_aug_base/`
- Training completato: 100 epoche; checkpoint migliore intorno all'epoca 80.
- Test congelato: `../../../experiments/Test/evaluation_test_v1_2_aug_base/`
- Risultato complessivo: Precision 0.960, Recall 0.789, mAP50 0.851,
  mAP50-95 0.724.
- Rispetto alla baseline v1.2 aumentano Precision e Recall; mAP50 diminuisce da
  0.890 a 0.851 e mAP50-95 resta sostanzialmente invariata.
