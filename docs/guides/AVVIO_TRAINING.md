# Avvio training, valutazione e test video

Eseguire tutto dalla root `SemaforoSmart`. La baseline corrente e' v1.3.

## 1. Preparare l'ambiente

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Non copiare `.venv` tra Windows e macOS. I pesi iniziali sono in
`models/pretrained/yolov8n.pt`. Verificare il dispositivo con:

```bash
python scripts/testGPU.py
```

## 2. Avviare un training confrontabile

```bash
python scripts/train_baseline.py --data data/datasets/v1.3/data.yaml --model models/pretrained/yolov8n.pt --name NOME_ESPERIMENTO --epochs 100 --imgsz 640 --batch 16 --patience 25 --workers 4 --device auto --seed 42
```

Il training riparte da YOLOv8n preaddestrato, non dal `best.pt` precedente.
Gli output sono in `experiments/Train/NOME_ESPERIMENTO/`; il checkpoint da
valutare e' `weights/best.pt`. Usare `--multi-scale` soltanto per un esperimento
esplicitamente separato.

## 3. Valutare sul test congelato

```bash
python scripts/evaluate_model.py --model experiments/Train/NOME_ESPERIMENTO/weights/best.pt --data data/datasets/v1.3/data.yaml --split test --imgsz 640 --batch 16 --device auto --name evaluation_NOME_ESPERIMENTO
```

I risultati vengono salvati in `experiments/Test/evaluation_NOME_ESPERIMENTO/`.
Per confronti corretti non modificare test, dimensione immagine o altri
parametri tra i modelli.

## 4. Ripetere i benchmark video

```bash
python scripts/predict_video.py --model experiments/Train/NOME_ESPERIMENTO/weights/best.pt --source data/test_videos/benchmark_ambulanza_giorno.mp4 --conf 0.60 --name NOME_TEST --show
```

Senza `--show` il video viene comunque elaborato e salvato. Webcam e stream IP
sono accettati come `--source 0` e `--source "URL_STREAM_IP"`. Usare sempre gli
stessi video e la stessa soglia `--conf` nei confronti.

Per l'elenco sintetico di tutti i comandi consultare `COMANDI_OPERATIVI.md`.
