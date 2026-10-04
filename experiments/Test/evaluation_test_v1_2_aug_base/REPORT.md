# Valutazione v1.2_Aug base

Valutazione eseguita sul test congelato della v1.2: 43 immagini, 42 istanze,
incluse 4 immagini negative. Il modello e' stato addestrato sulle due varianti
Roboflow Exposure/Blur delle sole 458 sorgenti train.

## Confronto complessivo

| Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| baseline v1.2 | 0.930 | 0.763 | **0.890** | 0.723 |
| v1.2_Aug base | **0.960** | **0.789** | 0.851 | **0.724** |

## Risultati per classe della v1.2_Aug

| Classe | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| Ambulanza | 0.935 | 0.846 | 0.927 | 0.850 |
| Carabinieri | 1.000 | 0.596 | 0.673 | 0.570 |
| VigiliDelFuoco | 0.946 | 0.925 | 0.952 | 0.752 |

## Lettura

La variante migliora precision e recall complessivi, mentre mAP50 diminuisce e
mAP50-95 resta sostanzialmente invariata. Ambulanza ottiene un forte incremento
di precision e mAP50-95; Carabinieri peggiora nelle due mAP; VDF aumenta il
recall ma perde precisione di localizzazione. Il modello non sostituisce ancora
la baseline: deve essere verificato sugli stessi sei benchmark video, con
particolare attenzione a Carabinieri notte e VDF notte.

## Verdetto sui benchmark video

Il modello si comporta in modo piu' aggressivo della baseline: tenta di
mantenere o produrre box anche su mezzi parzialmente visibili, con un lieve
miglioramento delle occlusioni. Il costo e' un aumento marcato dei falsi
positivi e delle confusioni tra classi in quasi tutti i benchmark. Il picco
della curva F1 e' circa 0.84 a confidence 0.597, quindi i test a `conf=0.60`
sono coerenti con la validation; la regressione video non dipende da una soglia
scelta male. La variante non sostituisce la baseline v1.2.
