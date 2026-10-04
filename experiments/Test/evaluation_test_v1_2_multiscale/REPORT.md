# Valutazione v1.2 Multi-scale

Valutazione sul test congelato della v1.2: 43 immagini, 42 istanze e 4
background. Il training usa il dataset v1.2 originale e modifica soltanto
`multi_scale`, impostato a `0.25`.

## Confronto complessivo

| Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| baseline v1.2 | 0.930 | 0.763 | **0.890** | 0.723 |
| v1.2_Aug base | 0.960 | **0.789** | 0.851 | 0.724 |
| v1.2 Multi-scale | **0.984** | 0.774 | 0.880 | **0.768** |

## Risultati per classe Multi-scale

| Classe | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| Ambulanza | 0.980 | 0.846 | 0.901 | 0.809 |
| Carabinieri | 1.000 | 0.529 | 0.749 | 0.656 |
| VigiliDelFuoco | 0.973 | 0.947 | 0.988 | 0.840 |

## Lettura

Rispetto alla baseline, Precision aumenta di 0.054, Recall di 0.011 e
mAP50-95 di 0.045; mAP50 diminuisce di 0.010. Ambulanza migliora nettamente
nella precisione delle box, VDF migliora in tutte le metriche principali,
mentre Carabinieri perde Recall ma guadagna leggermente mAP50-95. Il risultato
giustifica la verifica sui sei benchmark video e un'analisi per distanza.

## Verdetto sui benchmark video

Il miglioramento statico non si traduce in un salto operativo generale. Rispetto
alla baseline v1.2, il modello introduce piu' falsi positivi e una maggiore
confusione tra classi, pur restando piu' equilibrato della variante v1.2_Aug.
Le occlusioni migliorano soltanto in misura lieve. Il progresso chiaramente
visibile riguarda VDF notte, dove le confusioni diventano nulle o molto rare.
Il modello resta quindi un esperimento utile, ma non sostituisce la baseline
v1.2 come riferimento generale.
