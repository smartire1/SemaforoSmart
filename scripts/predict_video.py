#!/usr/bin/env python3
"""Inferenza YOLO su un video e salvataggio del risultato annotato."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "experiments" / "video_tests"


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
    parser = argparse.ArgumentParser(description="Testa un modello SemaforoSmart su un video.")
    parser.add_argument("--model", required=True, help="Percorso di best.pt")
    parser.add_argument("--source", required=True, help="Video, stream URL o indice webcam")
    parser.add_argument("--name", default=None, help="Nome del test; default: nome del video")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidenza minima")
    parser.add_argument("--iou", type=float, default=0.70, help="Soglia IoU della NMS")
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--vid-stride", type=int, default=1, help="Analizza un frame ogni N")
    parser.add_argument("--device", default="auto", help="auto, 0, cpu oppure mps")
    parser.add_argument("--project", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--show", action="store_true", help="Mostra anche una finestra live")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        import torch
        from ultralytics import YOLO
    except ImportError as error:
        raise SystemExit(
            "Dipendenze mancanti. Attiva l'ambiente ed esegui: "
            "python -m pip install -r requirements.txt"
        ) from error

    model_path = project_path(args.model).resolve()
    if not model_path.is_file():
        raise SystemExit(f"Modello non trovato: {model_path}")

    source: str | int = int(args.source) if args.source.isdigit() else args.source
    if isinstance(source, str) and "://" not in source:
        source_path = project_path(source).resolve()
        if not source_path.exists():
            raise SystemExit(f"Sorgente non trovata: {source_path}")
        source = str(source_path)

    output = project_path(args.project).resolve()
    output.mkdir(parents=True, exist_ok=True)
    source_name = Path(args.source).stem if not args.source.isdigit() else f"camera_{args.source}"
    run_name = args.name or source_name
    device = select_device(args.device, torch)

    print(f"Modello: {model_path}")
    print(f"Sorgente: {source}")
    print(f"Dispositivo: {device}")

    model = YOLO(str(model_path))
    results = model.predict(
        source=source,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        vid_stride=args.vid_stride,
        device=device,
        save=True,
        save_txt=True,
        save_conf=True,
        show=args.show,
        stream=True,
        project=str(output),
        name=run_name,
        exist_ok=False,
        verbose=False,
    )
    frame_count = sum(1 for _ in results)
    save_dir = getattr(model.predictor, "save_dir", output / run_name)
    print(f"Frame elaborati: {frame_count}")
    print(f"Risultati salvati in: {save_dir}")


if __name__ == "__main__":
    main()
