# Benchmark video v1.3

Inferenze eseguite con
`experiments/Train/baseline_v1_3_yolov8n/weights/best.pt` e soglia minima
`conf=0.60`. I video non hanno ground truth frame per frame: le conclusioni sono
qualitative e vanno incrociate con il test statico congelato.

## Verdetto sintetico

La v1.3 migliora globalmente la v1.2. I vantaggi piu' chiari riguardano
Ambulanza occlusa, rilevamenti FAR notturni, Carabinieri notte, stabilita'
geometrica delle box e il vecchio stress test VDF notte.

| Benchmark | Risultato | Residuo principale |
|---|---|---|
| Ambulanza giorno | occlusioni nettamente migliori | auto rossa CLOSE/PARTIAL come VDF |
| Ambulanza notte | FAR e passaggio vicino migliorati | iniziale confusione con VDF |
| Carabinieri giorno | quasi ottimale | stessa auto nera in 4 frame FP |
| Carabinieri notte | miglioramento evidente e box piu' omogenee | FAR e distinzione notturna tra classi |
| VDF giorno | sostanzialmente stabile | pickup FAR e pullman rosso |
| VDF notte | nuovo benchmark complessivamente positivo | lampeggianti bassi inducono box dimezzati; auto grigia come FP |
| VDF notte stress | miglioramento netto | box completa ancora instabile |

## Interpretazione

- Il batch reale e mirato ha prodotto benefici maggiori delle regressioni.
- I nuovi errori rossi sono coerenti con una possibile sovra-associazione fra
  colore/pickup e classe VDF.
- Nelle scene NIGHT i lampeggianti ON restano un indizio troppo dominante: nei
  frame OFF il modello e' meno sicuro.
- Le occlusioni estreme non sono una priorita' automatica: vanno incluse soltanto
  se la classe rimane riconoscibile e sono utili allo scenario operativo.
- Va definita la distanza minima operativa richiesta prima di inseguire ogni
  mancato rilevamento FAR.

Il resoconto osservativo completo dell'autore e' conservato in
`feedback bench v1.3.txt`.
