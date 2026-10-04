"""Evaluate the new and old models on the v1 test set grouped by user distance tags."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

import torch
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parents[3]
TEST = ROOT / "data" / "datasets" / "v1" / "test"
OLD_TEST = ROOT / "data" / "datasets" / "v1_eval_old_mapping" / "test"
TAGS = TEST / "percentuali_far_mid_close.txt"
OUT = ROOT / "experiments" / "Test" / "evaluation_distance_v1"

MODELS = {
    "new": (
        ROOT / "experiments" / "Train" / "baseline_v1_yolov8n" / "weights" / "best.pt",
        TEST / "labels",
        ["Ambulanza", "Carabinieri", "VigiliDelFuoco"],
    ),
    "old": (
        ROOT / "experiments" / "Train" / "baseline_v1_yolov8n" / "weights" / "bestOLD.pt",
        OLD_TEST / "labels",
        ["Carabinieri", "FireFighter", "ambulance"],
    ),
}


def select_device() -> str | int:
    if torch.cuda.is_available():
        return 0
    mps = getattr(torch.backends, "mps", None)
    if mps is not None and mps.is_available():
        return "mps"
    return "cpu"


def normalize_tag(raw: str) -> str:
    tag = raw.strip().lower()
    if tag in {"far", "very far"}:
        return "far"
    if tag in {"mid", "medium", "mid/far", "medium/close", "mid/close"}:
        return "medium"
    if tag in {"close", "very close"}:
        return "close"
    raise ValueError(f"Tag non riconosciuto: {raw!r}")


def read_tags() -> dict[str, str]:
    result: dict[str, str] = {}
    for line in TAGS.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        parts = re.split(r"\s+(?:->|-Z)\s+", line.strip(), maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Riga non valida: {line}")
        result[parts[0]] = normalize_tag(parts[1])
    return result


def bbox_area_stats(names: list[str]) -> dict[str, float]:
    values: list[float] = []
    for name in names:
        label = TEST / "labels" / f"{name}.txt"
        areas = []
        for row in label.read_text(encoding="utf-8").splitlines():
            fields = row.split()
            if len(fields) >= 5:
                areas.append(float(fields[3]) * float(fields[4]) * 100)
        if areas:
            values.append(max(areas))
    values.sort()
    return {
        "min_pct": round(values[0], 2),
        "median_pct": round(values[len(values) // 2], 2),
        "max_pct": round(values[-1], 2),
    }


def prepare_subset(model_key: str, category: str, names: list[str], labels: Path, classes: list[str]) -> Path:
    base = OUT / "datasets" / model_key / category
    images_out = base / "test" / "images"
    labels_out = base / "test" / "labels"
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    for name in names:
        image_matches = list((TEST / "images").glob(f"{name}.*"))
        if len(image_matches) != 1:
            raise FileNotFoundError(f"Immagine non trovata o ambigua: {name}")
        shutil.copy2(image_matches[0], images_out / image_matches[0].name)
        shutil.copy2(labels / f"{name}.txt", labels_out / f"{name}.txt")

    yaml_path = base / "data.yaml"
    yaml_path.write_text(
        "path: " + str(base.resolve()).replace("\\", "/") + "\n"
        "train: test/images\n"
        "val: test/images\n"
        "test: test/images\n"
        f"nc: {len(classes)}\n"
        "names:\n" + "".join(f"  {i}: {name}\n" for i, name in enumerate(classes)),
        encoding="utf-8",
    )
    return yaml_path


def main() -> None:
    device = select_device()
    print(f"Dispositivo: {device}")
    tags = read_tags()
    groups = {category: sorted(name for name, value in tags.items() if value == category)
              for category in ("far", "medium", "close")}

    report: dict[str, object] = {
        "grouping_rule": {
            "far": ["far", "very far"],
            "medium": ["mid", "medium", "mid/far", "medium/close", "mid/close"],
            "close": ["close", "very close"],
        },
        "groups": {
            category: {
                "images": len(names),
                "bbox_area": bbox_area_stats(names),
            }
            for category, names in groups.items()
        },
        "models": {},
    }

    for model_key, (model_path, labels, classes) in MODELS.items():
        model = YOLO(model_path)
        model_results = {}
        for category, names in groups.items():
            yaml_path = prepare_subset(model_key, category, names, labels, classes)
            metrics = model.val(
                data=str(yaml_path),
                split="test",
                imgsz=640,
                batch=16,
                device=device,
                plots=False,
                project=str(OUT),
                name=f"{model_key}_{category}",
                exist_ok=True,
                verbose=False,
            )
            model_results[category] = {
                "precision": round(float(metrics.box.mp), 4),
                "recall": round(float(metrics.box.mr), 4),
                "map50": round(float(metrics.box.map50), 4),
                "map50_95": round(float(metrics.box.map), 4),
            }
        report["models"][model_key] = model_results

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "distance_results.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
