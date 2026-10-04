#!/usr/bin/env python3
"""Valuta un modello YOLO su uno split e salva metriche e grafici ordinati."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT = ROOT / "experiments" / "Test"


def project_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else ROOT / path


def select_device(requested: str, torch_module) -> str | int:
    if requested != "auto":
        return int(requested) if requested.isdigit() else requested
    if torch_module.cuda.is_available():
        return 0
    mps = getattr(torch_module.backends, "mps", None)
    if mps is not None and mps.is_available():
        return "mps"
    return "cpu"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Percorso del checkpoint best.pt")
    parser.add_argument("--data", required=True, help="Percorso del data.yaml")
    parser.add_argument("--name", required=True, help="Nome della valutazione")
    parser.add_argument("--split", default="test", choices=("train", "val", "test"))
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--device", default="auto", help="auto, 0, cpu oppure mps")
    parser.add_argument("--project", default=str(DEFAULT_PROJECT))
    args = parser.parse_args()

    try:
        import torch
        from ultralytics import YOLO
    except ImportError as error:
        raise SystemExit(
            "Dipendenze mancanti. Attiva l'ambiente ed esegui: "
            "python -m pip install -r requirements.txt"
        ) from error

    model_path = project_path(args.model).resolve()
    data_path = project_path(args.data).resolve()
    output = project_path(args.project).resolve()
    if not model_path.is_file():
        raise SystemExit(f"Modello non trovato: {model_path}")
    if not data_path.is_file():
        raise SystemExit(f"Dataset non trovato: {data_path}")

    device = select_device(args.device, torch)
    output.mkdir(parents=True, exist_ok=True)
    print(f"Modello: {model_path}")
    print(f"Dataset: {data_path}")
    print(f"Split/dispositivo: {args.split}/{device}")

    model = YOLO(str(model_path))
    model.val(
        data=str(data_path),
        split=args.split,
        imgsz=args.imgsz,
        batch=args.batch,
        device=device,
        plots=True,
        project=str(output),
        name=args.name,
        exist_ok=False,
    )


if __name__ == "__main__":
    main()
