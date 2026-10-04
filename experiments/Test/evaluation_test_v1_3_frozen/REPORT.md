# Valutazione congelata v1.3

Valutazione di `baseline_v1_3_yolov8n/weights/best.pt` sullo stesso test storico
di 43 immagini usato per v1, v1.1 e v1.2.

| Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| v1.2 | 0,930 | 0,763 | 0,890 | 0,723 |
| v1.3 | **0,962** | **0,832** | **0,926** | **0,764** |

## Lettura per classe

| Classe | Precision | Recall | mAP50-95 |
|---|---:|---:|---:|
| Ambulanza | 0,928 | 0,992 | 0,853 |
| Carabinieri | 1,000 | 0,557 | 0,657 |
| VigiliDelFuoco | 0,959 | 0,947 | 0,781 |

La v1.3 e' migliore globalmente. Ambulanza registra il progresso piu' netto;
VDF recupera recall ma perde leggermente localizzazione severa rispetto a v1.2;
Carabinieri rimane il punto debole del piccolo test statico. I benchmark video
sono necessari per interpretare questi risultati in condizioni temporali reali.
