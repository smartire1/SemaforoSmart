# Script SemaforoSmart

La root contiene soltanto strumenti operativi generali e riutilizzabili:

| Script | Funzione |
|---|---|
| `train_baseline.py` | training YOLO riproducibile |
| `evaluate_model.py` | valutazione su train, validation o test |
| `predict_video.py` | inferenza su video, webcam e stream IP |
| `split_dataset.py` | split YOLO deterministico e per gruppi |
| `testGPU.py` | controllo CUDA, MPS o CPU |

## Esperimenti attivi

`scripts/experiments/copy_paste_batch.py` genera o verifica il batch sintetico DAY
documentato in `data/raw/v1.3_cp/README.md`. E' separato dagli strumenti
generali perche' dipende da configurazione, quote e struttura di quello
specifico esperimento.

## Archivio riproducibile

`scripts/archive/` contiene script conclusi o eseguiti una sola volta:

- `scripts/archive/dataset_builders/`: ricostruzione storica di v1.1, v1.2,
  v1.2_Aug e v1.3;
- `scripts/archive/legacy_analysis/`: rimappatura bestOLD e analisi per distanza
  della v1;
- `scripts/archive/copy_paste/`: generatore delle sei prove pilota precedenti al
  batch DAY.

Non sono file inutili: permettono di ricostruire decisioni e artefatti storici,
ma non fanno parte del flusso quotidiano. Eseguire sempre i comandi dalla root
del progetto. Gli split gia' validati non vanno rigenerati senza una ragione
esplicita.
