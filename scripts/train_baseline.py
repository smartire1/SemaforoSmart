#!/usr/bin/env python3
"""Training baseline YOLO per SemaforoSmart."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = PROJECT_ROOT / "data" / "datasets" / "v1.3" / "data.yaml"
DEFAULT_OUTPUT = PROJECT_ROOT / "experiments" / "Train"
DEFAULT_MODEL = PROJECT_ROOT / "models" / "pretrained" / "yolov8n.pt"


def project_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


def select_device(requested: str, torch_module) -> str | int:
    if requested != "auto":
        return int(requested) if requested.isdigit() else requested
    if torch_module.cuda.is_available():
        return 0
    mps = getattr(torch_module.backends, "mps", None)
    if mps is not None and mps.is_available():
        return "mps"
    return "cpu"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Addestra una baseline YOLO Nano SemaforoSmart.")
    parser.add_argument("--data", default=str(DEFAULT_DATASET), help="Percorso del data.yaml")
    parser.add_argument("--model", default=str(DEFAULT_MODEL), help="Pesi iniziali o nome modello")
    parser.add_argument("--name", default="baseline_v1_3_yolov8n", help="Nome dell'esperimento")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--patience", type=int, default=25)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--device", default="auto", help="auto, 0, cpu oppure mps")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--multi-scale",
        type=float,
        default=0.0,
        help="Variazione casuale della risoluzione per batch (0 disabilita; es. 0.25)",
    )
    parser.add_argument("--project", default=str(DEFAULT_OUTPUT), help="Cartella degli esperimenti")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not 0.0 <= args.multi_scale <= 1.0:
        raise SystemExit("--multi-scale deve essere compreso tra 0.0 e 1.0")

    try:
        import torch
        from ultralytics import YOLO
    except ImportError as error:
        raise SystemExit(
            "Dipendenze mancanti. Attiva l'ambiente ed esegui: "
            "python -m pip install -r requirements.txt"
        ) from error

    dataset = project_path(args.data).resolve()
    output = project_path(args.project).resolve()
    if not dataset.is_file():
        raise SystemExit(f"Dataset non trovato: {dataset}")
    for split in ("train", "valid", "test"):
        if not (dataset.parent / split / "images").is_dir():
            raise SystemExit(f"Split mancante: {dataset.parent / split / 'images'}")

    device = select_device(args.device, torch)
    output.mkdir(parents=True, exist_ok=True)
    model_candidate = project_path(args.model)
    model_source = str(model_candidate.resolve()) if model_candidate.is_file() else args.model
    device_description = (
        f"CUDA 0 - {torch.cuda.get_device_name(0)}" if device == 0 else str(device)
    )

    print("Configurazione baseline")
    print(f"  dataset: {dataset}")
    print(f"  modello: {model_source}")
    print(f"  dispositivo: {device_description}")
    print(f"  epoche/imgsz/batch: {args.epochs}/{args.imgsz}/{args.batch}")
    print(f"  multi-scale: {args.multi_scale}")
    print(f"  output: {output / args.name}")

    model = YOLO(model_source)
    model.train(
        data=str(dataset),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        patience=args.patience,
        workers=args.workers,
        device=device,
        seed=args.seed,
        multi_scale=args.multi_scale,
        deterministic=True,
        pretrained=True,
        plots=True,
        project=str(output),
        name=args.name,
        exist_ok=False,
    )


if __name__ == "__main__":
    main()
