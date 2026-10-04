# Confronto tra modello v1 e bestOLD.pt

## Metodo

I due modelli sono stati valutati sulle stesse 43 immagini del test set v1,
contenenti 42 oggetti e 4 immagini negative. Per `bestOLD.pt` è stata creata una
copia di sola valutazione con gli ID delle classi rimappati:

- `0 Ambulanza` -> `2 ambulance`
- `1 Carabinieri` -> `0 Carabinieri`
- `2 VigiliDelFuoco` -> `1 FireFighter`

Le immagini della copia sono identiche byte per byte a quelle originali. Entrambe
le valutazioni usano `imgsz=640`, `batch=16`, `device=0` e lo split `test`.

## Risultati complessivi

| Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| Nuovo v1 | 0.845 | 0.614 | 0.763 | 0.590 |
| bestOLD.pt | 0.739 | 0.536 | 0.645 | 0.476 |
| Differenza nuovo - old | +0.106 | +0.078 | +0.118 | +0.114 |

## Risultati per classe

| Classe | Modello | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|
| Ambulanza | Nuovo v1 | 0.680 | 0.308 | 0.696 | 0.552 |
| Ambulanza | bestOLD.pt | 0.607 | 0.477 | 0.548 | 0.409 |
| Carabinieri | Nuovo v1 | 1.000 | 0.592 | 0.675 | 0.516 |
| Carabinieri | bestOLD.pt | 0.642 | 0.500 | 0.495 | 0.426 |
| Vigili del Fuoco | Nuovo v1 | 0.856 | 0.942 | 0.918 | 0.703 |
| Vigili del Fuoco | bestOLD.pt | 0.969 | 0.632 | 0.892 | 0.593 |

## Interpretazione

Sul test statico v1 il nuovo modello è complessivamente migliore. Il vantaggio è
netto per Carabinieri e nella capacità di trovare i Vigili del Fuoco. Il nuovo
modello migliora anche l'AP delle ambulanze, ma il recall operativo delle ambulanze
rimane molto basso: ne perde troppe alla soglia scelta automaticamente dalla
valutazione.

`bestOLD.pt` conserva una maggiore sensibilità alle ambulanze, coerente con la
maggiore stabilità osservata sul video esterno, ma commette più errori sulle altre
classi. Nella matrice di confusione riconosce come `ambulance` quattro veri mezzi dei
Vigili del Fuoco e perde metà dei Carabinieri.

Il confronto tra test statico e video mostra un limite del benchmark: 43 immagini e
42 oggetti non rappresentano completamente movimento, sfocatura, variazioni tra
frame e allontanamento del veicolo. Le metriche statiche favoriscono il nuovo
modello, mentre il video evidenzia una migliore continuità temporale del vecchio
modello sulle ambulanze.

## Conclusione operativa

Il nuovo v1 è il candidato migliore come base generale. `bestOLD.pt` non va però
scartato: dimostra che esempi o augmentation del vecchio dataset aiutavano la
stabilità video delle ambulanze. La prossima revisione del dataset dovrebbe quindi
concentrarsi su ambulanze in movimento, laterali, lontane e progressivamente più
piccole, usando video diversi da quelli conservati come benchmark.
