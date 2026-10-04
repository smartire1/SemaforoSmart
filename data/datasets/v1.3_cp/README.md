# SemaforoSmart dataset v1.3_cp

Variante sperimentale della baseline v1.3. Al train reale vengono aggiunte 60
composizioni Copy-Paste DAY; immagini e label di validation e test sono copie
byte-identiche della v1.3. I file `labels.cache`, rigenerabili da Ultralytics,
possono differire perche' contengono percorsi locali. Questa variante non
sostituisce la baseline.

| Voce | v1.3 reale | Sintetiche | Totale v1.3_cp |
|---|---:|---:|---:|
| Train | 524 | 60 | 584 |
| Validation | 97 | 0 | 97 |
| Test congelato | 43 | 0 | 43 |
| Totale | 664 | 60 | 724 |

Le sintetiche costituiscono il 10,3% del train finale: 20 Ambulanza, 20
Carabinieri e 20 VigiliDelFuoco; 36 FAR e 24 MID. Derivano da sei PNG reali e
sei sfondi NULL appartenenti al train v1.3.

## Integrita' e manifest

- Ogni immagine possiede una label con lo stesso nome; non risultano coppie
  mancanti nei tre split.
- I 664 file reali mantengono contenuto e split della v1.3.
- `split_manifest.csv` e' il manifest storico dei soli file reali v1.3.
- `synthetic_manifest.csv` documenta le 60 aggiunte ed e' copia byte-identica
  del manifest generativo conservato sotto `data/raw/v1.3_cp/manifests/`.
- `v1.3.zip` e i README Roboflow sono archivi ereditati dalla versione reale;
  non contengono le 60 immagini sintetiche.

## Esperimento associato

- Training: `../../../experiments/Train/exp_v1_3_cp_day_001/`
- Log: `../../../docs/logs/7. LOG_TRAIN_V1.3_CP.txt`
- Test congelato: `../../../experiments/Test/evaluation_test_v1_3_cp_day_001/`
- Benchmark video: `../../../experiments/video_tests/v1.3_cp/day_001/`
- Diario completo: `../../raw/v1.3_cp/README.md`

Sul test congelato CP DAY ottiene Precision 0,980, Recall 0,772, mAP50 0,864 e
mAP50-95 0,735, contro 0,962 / 0,832 / 0,926 / 0,764 della baseline. VDF
migliora, ma il risultato aggregato regredisce; il modello non e' promosso.
