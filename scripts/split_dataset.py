#!/usr/bin/env python3
"""Create a deterministic, group-aware YOLO train/valid/test split."""

from __future__ import annotations

import argparse
import csv
import random
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
CLASS_NAMES = {0: "Ambulanza", 1: "Carabinieri", 2: "VigiliDelFuoco"}
SPLITS = ("train", "valid", "test")


@dataclass(frozen=True)
class Sample:
    image: Path
    label: Path
    canonical_stem: str
    bucket: str
    group_id: str
    box_count: int
    class_ids: tuple[int, ...]


def canonical_stem(image: Path) -> str:
    """Recover the original stem from a Roboflow-renamed file."""
    stem = re.sub(r"\.rf\.[^.]+$", "", image.stem, flags=re.IGNORECASE)
    return re.sub(r"_(?:png|jpe?g|bmp|webp)$", "", stem, flags=re.IGNORECASE)


def classify_and_group(stem: str) -> tuple[str, str]:
    bucket_match = re.match(r"^(amb|car|vdf|neg)_", stem, flags=re.IGNORECASE)
    if not bucket_match:
        raise ValueError(f"Nome non riconosciuto: {stem}")
    bucket = bucket_match.group(1).lower()

    video_match = re.match(
        r"^((?:amb|car|vdf)(?:_old)?_video_\d+)_frame_\d+$",
        stem,
        flags=re.IGNORECASE,
    )
    if video_match:
        return bucket, video_match.group(1).lower()

    series_match = re.match(
        r"^((?:amb|car|vdf)_old_series_\d+)_view_\d+$",
        stem,
        flags=re.IGNORECASE,
    )
    if series_match:
        return bucket, series_match.group(1).lower()

    return bucket, stem.lower()


def read_label(label: Path) -> tuple[int, tuple[int, ...]]:
    class_ids: list[int] = []
    for line_number, line in enumerate(label.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Riga YOLO non valida: {label}:{line_number}")
        class_id = int(fields[0])
        if class_id not in CLASS_NAMES:
            raise ValueError(f"Classe {class_id} inattesa: {label}:{line_number}")
        coordinates = [float(value) for value in fields[1:]]
        if not all(0.0 <= value <= 1.0 for value in coordinates):
            raise ValueError(f"Coordinate fuori intervallo: {label}:{line_number}")
        class_ids.append(class_id)
    return len(class_ids), tuple(sorted(set(class_ids)))


def load_samples(source: Path) -> list[Sample]:
    image_dir = source / "train" / "images"
    label_dir = source / "train" / "labels"
    if not image_dir.is_dir() or not label_dir.is_dir():
        raise FileNotFoundError("La sorgente deve contenere train/images e train/labels")

    images = sorted(
        path for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )
    samples: list[Sample] = []
    for image in images:
        label = label_dir / f"{image.stem}.txt"
        if not label.is_file():
            raise FileNotFoundError(f"Label mancante per {image.name}")
        stem = canonical_stem(image)
        bucket, group_id = classify_and_group(stem)
        box_count, class_ids = read_label(label)
        samples.append(
            Sample(image, label, stem, bucket, group_id, box_count, class_ids)
        )

    labels = {path.stem for path in label_dir.glob("*.txt")}
    image_stems = {sample.image.stem for sample in samples}
    orphan_labels = sorted(labels - image_stems)
    if orphan_labels:
        raise ValueError(f"Trovate {len(orphan_labels)} label senza immagine")
    return samples


def closest_group_subset(
    groups: list[tuple[str, list[Sample]]], target: int, rng: random.Random
) -> set[str]:
    """Subset-sum over group sizes, with seeded tie-breaking."""
    shuffled = groups[:]
    rng.shuffle(shuffled)
    reachable: dict[int, tuple[int, ...]] = {0: ()}
    for index, (_, samples) in enumerate(shuffled):
        size = len(samples)
        additions: dict[int, tuple[int, ...]] = {}
        for current_sum, selection in list(reachable.items()):
            new_sum = current_sum + size
            if new_sum not in reachable and new_sum not in additions:
                additions[new_sum] = selection + (index,)
        reachable.update(additions)

    best_sum = min(reachable, key=lambda value: (abs(value - target), value > target, value))
    return {shuffled[index][0] for index in reachable[best_sum]}


def assign_splits(samples: list[Sample], seed: int) -> dict[str, str]:
    by_bucket: dict[str, dict[str, list[Sample]]] = defaultdict(lambda: defaultdict(list))
    for sample in samples:
        by_bucket[sample.bucket][sample.group_id].append(sample)

    assignment: dict[str, str] = {}
    for bucket in sorted(by_bucket):
        groups = sorted(by_bucket[bucket].items())
        total = sum(len(items) for _, items in groups)
        rng = random.Random(f"{seed}:{bucket}")

        test_groups = closest_group_subset(groups, round(total * 0.10), rng)
        remaining = [group for group in groups if group[0] not in test_groups]
        valid_groups = closest_group_subset(remaining, round(total * 0.15), rng)

        for group_id, _ in groups:
            if group_id in test_groups:
                assignment[group_id] = "test"
            elif group_id in valid_groups:
                assignment[group_id] = "valid"
            else:
                assignment[group_id] = "train"
    return assignment


def write_dataset(samples: list[Sample], assignment: dict[str, str], output: Path) -> None:
    if output.exists() and any(output.iterdir()):
        raise FileExistsError(f"La destinazione non è vuota: {output}")

    for split in SPLITS:
        (output / split / "images").mkdir(parents=True, exist_ok=True)
        (output / split / "labels").mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str | int]] = []
    for sample in samples:
        split = assignment[sample.group_id]
        shutil.copy2(sample.image, output / split / "images" / sample.image.name)
        shutil.copy2(sample.label, output / split / "labels" / sample.label.name)
        rows.append(
            {
                "split": split,
                "bucket": sample.bucket,
                "group_id": sample.group_id,
                "canonical_stem": sample.canonical_stem,
                "image": sample.image.name,
                "label": sample.label.name,
                "box_count": sample.box_count,
                "class_ids": ",".join(map(str, sample.class_ids)),
            }
        )

    with (output / "split_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (str(row["split"]), str(row["image"]))))

    (output / "data.yaml").write_text(
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n\n"
        "names:\n"
        "  0: Ambulanza\n"
        "  1: Carabinieri\n"
        "  2: VigiliDelFuoco\n",
        encoding="utf-8",
    )

    split_counts = Counter(assignment[sample.group_id] for sample in samples)
    bucket_counts = {
        split: Counter(sample.bucket for sample in samples if assignment[sample.group_id] == split)
        for split in SPLITS
    }
    readme_lines = [
        "# SemaforoSmart dataset v1",
        "",
        "Split locale deterministico e senza contaminazione tra frame correlati.",
        "",
        "- Ripartizione obiettivo: 75% train, 15% valid, 10% test",
        "- Seed: 42",
        "- I frame dello stesso video e le viste della stessa serie restano nello stesso split.",
        "- I file label vuoti rappresentano immagini negative (Null in Roboflow).",
        "- `split_manifest.csv` documenta l'assegnazione di ogni immagine.",
        "",
        "## Conteggi",
        "",
        "| Split | Totale | Ambulanza | Carabinieri | VDF | Negative |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for split in SPLITS:
        counts = bucket_counts[split]
        readme_lines.append(
            f"| {split} | {split_counts[split]} | {counts['amb']} | {counts['car']} | "
            f"{counts['vdf']} | {counts['neg']} |"
        )
    (output / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    samples = load_samples(args.source)
    assignment = assign_splits(samples, args.seed)
    write_dataset(samples, assignment, args.output)

    counts = Counter(assignment[sample.group_id] for sample in samples)
    print(f"Totale: {len(samples)}")
    for split in SPLITS:
        print(f"{split}: {counts[split]}")


if __name__ == "__main__":
    main()
