# Valutazione congelata v1.3_cp DAY 001

Valutazione del checkpoint
`experiments/Train/exp_v1_3_cp_day_001/weights/best.pt` sul test reale e
congelato della v1.3: 43 immagini, 42 istanze e 4 NULL.

| Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| v1.3 baseline | 0,962 | **0,832** | **0,926** | **0,764** |
| CP DAY 001 | **0,980** | 0,772 | 0,864 | 0,735 |

| Classe | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| Ambulanza | 0,962 | 0,769 | 0,944 | 0,821 |
| Carabinieri | 0,988 | 0,600 | 0,668 | 0,576 |
| VigiliDelFuoco | 0,990 | 0,947 | 0,980 | 0,808 |

Il modello diventa piu' selettivo e VDF migliora, ma perde recall e mAP
complessive, soprattutto per Ambulanza e nella localizzazione di Carabinieri.
Non e' promosso: la baseline resta v1.3. I valori completi stampati dal comando
sono riassunti in `metrics_summary.csv`; il diario e l'analisi video sono in
`data/raw/v1.3_cp/README.md`.
