# Comandi operativi

Eseguire i comandi dalla root `SemaforoSmart`. La baseline corrente e' v1.3;
`v1.3_cp` e' un esperimento separato e non promosso.

## Ambiente

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Windows CMD:

```bat
.venv\Scripts\activate.bat
```

macOS:

```bash
source .venv/bin/activate
```

Installazione e controllo dispositivo:

```bash
python -m pip install -r requirements.txt
python scripts/testGPU.py
```

## Training controllato

Usare un nome nuovo per ogni esperimento:

```bash
python scripts/train_baseline.py --data data/datasets/v1.3/data.yaml --model models/pretrained/yolov8n.pt --name NOME_ESPERIMENTO --epochs 100 --imgsz 640 --batch 16 --patience 25 --workers 4 --device auto --seed 42
```

`--multi-scale 0.25` va aggiunto soltanto a un esperimento dichiarato. Gli output
finiscono in `experiments/Train/<nome>/`.

## Valutazione sul test congelato

```bash
python scripts/evaluate_model.py --model experiments/Train/NOME_ESPERIMENTO/weights/best.pt --data data/datasets/v1.3/data.yaml --split test --imgsz 640 --batch 16 --device auto --name evaluation_NOME_ESPERIMENTO
```

Gli output finiscono in `experiments/Test/<nome>/`. Per varianti come
`v1.3_cp`, cambiare soltanto il percorso `--data` mantenendo gli altri parametri.

## Inferenza video, webcam e IP camera

Video:

```bash
python scripts/predict_video.py --model experiments/Train/baseline_v1_3_yolov8n/weights/best.pt --source data/test_videos/benchmark_ambulanza_giorno.mp4 --conf 0.60 --name NOME_TEST --show
```

Webcam locale:

```bash
python scripts/predict_video.py --model experiments/Train/baseline_v1_3_yolov8n/weights/best.pt --source 0 --conf 0.60 --name webcam_test --show
```

Stream IP:

```bash
python scripts/predict_video.py --model experiments/Train/baseline_v1_3_yolov8n/weights/best.pt --source "URL_STREAM_IP" --conf 0.60 --name test_ip_camera --show
```

I risultati vengono salvati in `experiments/video_tests/<nome>/`.

## Dataset e script specializzati

Gli split versionati non vanno rigenerati senza motivo. Lo strumento generico e':

```bash
python scripts/split_dataset.py --help
```

I costruttori usati una sola volta sono conservati in
`scripts/archive/dataset_builders/`; gli strumenti Copy-Paste correnti sono in
`scripts/experiments/`. Consultare `scripts/README.md` prima di usarli.

## Uscita dall'ambiente

```bash
deactivate
```
