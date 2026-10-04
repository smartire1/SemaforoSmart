#!/usr/bin/env python3
"""Build v1.3 while preserving the complete v1.2 split and frozen test."""

from __future__ import annotations

import argparse
import csv
import random
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from split_dataset import IMAGE_EXTENSIONS, CLASS_NAMES, closest_group_subset, canonical_stem


def read_label(path: Path) -> tuple[int, tuple[int, ...]]:
    ids: list[int] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Label non valida: {path}")
        class_id = int(fields[0])
        if class_id not in CLASS_NAMES:
            raise ValueError(f"Classe inattesa: {path}")
        values = [float(value) for value in fields[1:]]
        if not all(0.0 <= value <= 1.0 for value in values):
            raise ValueError(f"Coordinate fuori intervallo: {path}")
        ids.append(class_id)
    return len(ids), tuple(sorted(set(ids)))


def classify(stem: str) -> tuple[str, str]:
    match = re.fullmatch(r"v13_(amb|car|vdf)_video_(\d+)_frame_\d+", stem)
    if match:
        bucket, number = match.groups()
        return bucket, f"v13_{bucket}_video_{int(number):03d}"
    if re.fullmatch(r"v13_null_hn_\d+", stem):
        return "neg", stem
    raise ValueError(f"Nome v1.3 non riconosciuto: {stem}")


def load_base(base: Path) -> tuple[list[dict[str, str]], set[str]]:
    rows = list(csv.DictReader((base / "split_manifest.csv").open(newline="", encoding="utf-8")))
    if len(rows) != 586:
        raise ValueError(f"Attese 586 immagini v1.2, trovate {len(rows)}")
    stems: set[str] = set()
    for row in rows:
        if row["split"] not in {"train", "valid", "test"}:
            raise ValueError(f"Split non valido: {row['split']}")
        stems.add(row["canonical_stem"])
        if not (base / row["split"] / "images" / row["image"]).is_file():
            raise FileNotFoundError(row["image"])
        if not (base / row["split"] / "labels" / row["label"]).is_file():
            raise FileNotFoundError(row["label"])
    return rows, stems


def load_additions(export: Path, base_stems: set[str]) -> list[dict[str, object]]:
    image_dir, label_dir = export / "train" / "images", export / "train" / "labels"
    additions: list[dict[str, object]] = []
    for image in sorted(image_dir.iterdir()):
        if image.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        stem = canonical_stem(image)
        if stem in base_stems:
            continue
        label = label_dir / f"{image.stem}.txt"
        if not label.is_file():
            raise FileNotFoundError(label)
        bucket, group = classify(stem)
        box_count, class_ids = read_label(label)
        if bucket == "neg" and box_count:
            raise ValueError(f"NULL con bounding box: {image.name}")
        if bucket != "neg" and not box_count:
            # Roboflow conserva il file nel batch Carabinieri, ma l'annotazione
            # corretta lo rende NULL (v13_car_video_001_frame_001).
            bucket = "neg"
            group = f"neg_{group}"
        additions.append({"image": image, "label": label, "stem": stem,
                          "bucket": bucket, "group": group,
                          "box_count": box_count, "class_ids": class_ids})
    if len(additions) != 78:
        raise ValueError(f"Attese 78 nuove immagini, trovate {len(additions)}")
    return additions


def assign(additions: list[dict[str, object]], seed: int) -> dict[str, str]:
    by_bucket: dict[str, dict[str, list[dict[str, object]]]] = defaultdict(lambda: defaultdict(list))
    for sample in additions:
        by_bucket[str(sample["bucket"])][str(sample["group"])].append(sample)
    assignments: dict[str, str] = {}
    for bucket, groups in sorted(by_bucket.items()):
        items = sorted(groups.items())
        target = round(sum(len(v) for _, v in items) * 0.15)
        valid = closest_group_subset(items, target, random.Random(f"{seed}:v1.3:{bucket}"))
        for group, _ in items:
            assignments[group] = "valid" if group in valid else "train"
    return assignments


def build(base: Path, export: Path, output: Path, seed: int) -> None:
    if output.exists():
        raise FileExistsError(output)
    base_rows, base_stems = load_base(base)
    additions = load_additions(export, base_stems)
    assignments = assign(additions, seed)
    output.mkdir(parents=True)
    for split in ("train", "valid", "test"):
        shutil.copytree(base / split / "images", output / split / "images")
        shutil.copytree(base / split / "labels", output / split / "labels")
    rows = list(base_rows)
    for sample in additions:
        split = assignments[str(sample["group"])]
        image: Path = sample["image"]  # type: ignore[assignment]
        label: Path = sample["label"]  # type: ignore[assignment]
        shutil.copy2(image, output / split / "images" / image.name)
        shutil.copy2(label, output / split / "labels" / label.name)
        rows.append({"split": split, "bucket": str(sample["bucket"]),
                     "group_id": str(sample["group"]), "canonical_stem": str(sample["stem"]),
                     "image": image.name, "label": label.name,
                     "box_count": str(sample["box_count"]),
                     "class_ids": ",".join(map(str, sample["class_ids"]))})
    with (output / "split_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(sorted(rows, key=lambda r: (r["split"], r["image"])))
    (output / "data.yaml").write_text(
        "train: train/images\nval: valid/images\ntest: test/images\n\n"
        "names:\n  0: Ambulanza\n  1: Carabinieri\n  2: VigiliDelFuoco\n", encoding="utf-8")
    counts = Counter(r["split"] for r in rows)
    (output / "README.md").write_text(
        "# SemaforoSmart dataset v1.3\n\n"
        "Dataset cumulativo v1.2 + 78 nuove immagini v1.3. Il test storico v1.2 "
        "resta invariato; le aggiunte sono state assegnate solo a train/valid.\n\n"
        f"- Seed: {seed}\n- train: {counts['train']}\n- valid: {counts['valid']}\n- test: {counts['test']}\n"
        "- `split_manifest.csv` documenta file, gruppo e split.\n", encoding="utf-8")
    print(f"Totale: {len(rows)}; train={counts['train']}; valid={counts['valid']}; test={counts['test']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    build(args.base, args.export, args.output, args.seed)
