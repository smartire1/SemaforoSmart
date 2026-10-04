#!/usr/bin/env python3
"""Build v1.1 from the frozen v1 split plus new Roboflow-exported samples.

Usage from the project root:
    python scripts/archive/dataset_builders/build_v1_1_dataset.py \
        --base data/datasets/v1 \
        --export data/datasets/v1.1/v1.1.zip \
        --output data/datasets/v1.1

The v1 files and their splits are copied unchanged. New frames are assigned by
source group; new negatives stay in train because their source links are unknown.
"""

from __future__ import annotations

import argparse
import csv
import random
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

SCRIPTS_DIR = Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from split_dataset import CLASS_NAMES, canonical_stem, classify_and_group, closest_group_subset


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
EXPECTED_CLASSES = "names: ['Ambulanza', 'Carabinieri', 'VigiliDelFuoco']"


@dataclass(frozen=True)
class AddedSample:
    image_entry: str
    label_entry: str
    image_name: str
    label_name: str
    canonical: str
    bucket: str
    group_id: str
    box_count: int
    class_ids: tuple[int, ...]


def parse_label(text: str, filename: str) -> tuple[int, tuple[int, ...]]:
    ids: list[int] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Label non valida: {filename}:{line_number}")
        class_id = int(fields[0])
        if class_id not in CLASS_NAMES:
            raise ValueError(f"Classe inattesa: {filename}:{line_number}")
        coordinates = [float(value) for value in fields[1:]]
        if not all(0.0 <= value <= 1.0 for value in coordinates):
            raise ValueError(f"Coordinate fuori intervallo: {filename}:{line_number}")
        if coordinates[2] <= 0 or coordinates[3] <= 0:
            raise ValueError(f"Box senza area: {filename}:{line_number}")
        ids.append(class_id)
    return len(ids), tuple(sorted(set(ids)))


def group_new(stem: str) -> tuple[str, str]:
    if not stem.startswith("v11_"):
        return classify_and_group(stem)

    match = re.fullmatch(r"v11_(amb|car|vdf)_video_(\d+)_frame_\d+", stem)
    if match:
        return match.group(1), f"v11_{match.group(1)}_video_{match.group(2)}"

    match = re.fullmatch(r"v11_car_source_unknown_video_(\d+)_frame_\d+", stem)
    if match:
        return "car", f"v11_car_source_unknown_video_{match.group(1)}"

    if re.fullmatch(r"v11_null_\d+", stem):
        return "neg", stem

    raise ValueError(f"Nome v1.1 non riconosciuto: {stem}")


def load_base(base: Path) -> tuple[list[dict[str, str]], set[str], dict[str, str]]:
    manifest = base / "split_manifest.csv"
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 426:
        raise ValueError(f"Attese 426 immagini v1, trovate {len(rows)}")

    stems: set[str] = set()
    groups: dict[str, str] = {}
    for row in rows:
        split = row["split"]
        if split not in ("train", "valid", "test"):
            raise ValueError(f"Split v1 non valido: {split}")
        image = base / split / "images" / row["image"]
        label = base / split / "labels" / row["label"]
        if not image.is_file() or not label.is_file():
            raise FileNotFoundError(f"Coppia v1 mancante: {row['image']}")
        stem = row["canonical_stem"]
        if stem in stems:
            raise ValueError(f"Nome originale duplicato in v1: {stem}")
        stems.add(stem)
        group_id = row["group_id"]
        previous = groups.setdefault(group_id, split)
        if previous != split:
            raise ValueError(f"Gruppo v1 in split diversi: {group_id}")
    return rows, stems, groups


def load_additions(
    archive: zipfile.ZipFile, base_stems: set[str]
) -> tuple[list[AddedSample], int]:
    names = set(archive.namelist())
    yaml_name = "data.yaml"
    if yaml_name not in names or EXPECTED_CLASSES not in archive.read(yaml_name).decode("utf-8"):
        raise ValueError("Classi dell'export diverse da quelle della v1")

    image_entries = sorted(
        name for name in names
        if name.startswith("train/images/")
        and name.count("/") == 2
        and PurePosixPath(name).suffix.lower() in IMAGE_EXTENSIONS
    )
    if len(image_entries) != 517:
        raise ValueError(f"Attese 517 immagini nello ZIP, trovate {len(image_entries)}")

    additions: list[AddedSample] = []
    seen_stems: set[str] = set()
    shared = 0
    for image_entry in image_entries:
        image_name = PurePosixPath(image_entry).name
        stem = canonical_stem(Path(image_name))
        if stem in seen_stems:
            raise ValueError(f"Nome originale duplicato nello ZIP: {stem}")
        seen_stems.add(stem)
        label_name = f"{Path(image_name).stem}.txt"
        label_entry = f"train/labels/{label_name}"
        if label_entry not in names:
            raise FileNotFoundError(f"Label mancante nello ZIP: {label_entry}")
        if stem in base_stems:
            shared += 1
            continue

        bucket, group_id = group_new(stem)
        box_count, class_ids = parse_label(
            archive.read(label_entry).decode("utf-8-sig"), label_entry
        )
        if bucket == "neg" and box_count != 0:
            raise ValueError(f"Negativa con box: {image_name}")
        if bucket != "neg" and box_count == 0:
            raise ValueError(f"Positiva senza box: {image_name}")
        additions.append(
            AddedSample(
                image_entry, label_entry, image_name, label_name, stem,
                bucket, group_id, box_count, class_ids,
            )
        )

    if shared != 426 or len(additions) != 91 or base_stems - seen_stems:
        raise ValueError(
            f"Composizione inattesa: {shared} gia' in v1, {len(additions)} nuove"
        )
    return additions, shared


def assign_new(
    additions: list[AddedSample], base_groups: dict[str, str], seed: int
) -> dict[str, str]:
    by_bucket: dict[str, dict[str, list[AddedSample]]] = defaultdict(lambda: defaultdict(list))
    for sample in additions:
        by_bucket[sample.bucket][sample.group_id].append(sample)

    assignments: dict[str, str] = {}
    for bucket, groups in sorted(by_bucket.items()):
        if bucket == "neg":
            assignments.update({group_id: "train" for group_id in groups})
            continue

        fixed_valid = 0
        candidates: list[tuple[str, list[AddedSample]]] = []
        for group_id, samples in sorted(groups.items()):
            if group_id in base_groups:
                split = base_groups[group_id]
                if split == "test":
                    raise ValueError(f"Nuovi frame dalla fonte del test v1: {group_id}")
                assignments[group_id] = split
                if split == "valid":
                    fixed_valid += len(samples)
            else:
                candidates.append((group_id, samples))

        target = max(0, round(sum(map(len, groups.values())) * 0.15) - fixed_valid)
        valid_groups = closest_group_subset(
            candidates, target, random.Random(f"{seed}:{bucket}:v1.1")
        )
        for group_id, _ in candidates:
            assignments[group_id] = "valid" if group_id in valid_groups else "train"
    return assignments


def build(
    base: Path, export: Path, output: Path, seed: int
) -> None:
    if not base.is_dir() or not export.is_file():
        raise FileNotFoundError("Base v1 o ZIP v1.1 mancante")
    if output.exists():
        raise FileExistsError(f"La destinazione esiste gia': {output}")

    base_rows, base_stems, base_groups = load_base(base)
    with zipfile.ZipFile(export) as archive:
        additions, shared = load_additions(archive, base_stems)
        assignment = assign_new(additions, base_groups, seed)
        if assignment.get("car_old_video_001") != "train":
            raise ValueError("Il nuovo frame car_old_video_001 non e' in train")

        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".v1.1-build-", dir=output.parent) as scratch:
            staged = Path(scratch) / "dataset"
            shutil.copytree(base, staged)
            rows = list(base_rows)
            for sample in additions:
                split = assignment[sample.group_id]
                image_target = staged / split / "images" / sample.image_name
                label_target = staged / split / "labels" / sample.label_name
                if image_target.exists() or label_target.exists():
                    raise FileExistsError(f"Collisione di nome: {sample.image_name}")
                with archive.open(sample.image_entry) as source, image_target.open("wb") as target:
                    shutil.copyfileobj(source, target)
                with archive.open(sample.label_entry) as source, label_target.open("wb") as target:
                    shutil.copyfileobj(source, target)
                rows.append({
                    "split": split,
                    "bucket": sample.bucket,
                    "group_id": sample.group_id,
                    "canonical_stem": sample.canonical,
                    "image": sample.image_name,
                    "label": sample.label_name,
                    "box_count": str(sample.box_count),
                    "class_ids": ",".join(map(str, sample.class_ids)),
                })

            with (staged / "split_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(base_rows[0]))
                writer.writeheader()
                writer.writerows(sorted(rows, key=lambda row: (row["split"], row["image"])))

            old_counts = Counter(row["split"] for row in base_rows)
            new_counts = Counter(assignment[sample.group_id] for sample in additions)
            new_buckets = Counter(sample.bucket for sample in additions)
            total_buckets = Counter(row["bucket"] for row in rows)
            (staged / "README.md").write_text(
                "# SemaforoSmart dataset v1.1\n\n"
                "Dataset cumulativo: i 426 file della v1 sono copiati senza modifiche e "
                "mantengono esattamente il loro split.\n\n"
                f"- Export Roboflow: `{export.name}` (517 immagini; {shared} gia' in v1, "
                "91 aggiunte).\n"
                f"- Nuove per tipo: Ambulanza {new_buckets['amb']}, Carabinieri "
                f"{new_buckets['car']}, VDF {new_buckets['vdf']}, Negative {new_buckets['neg']}.\n"
                f"- Totale v1.1 per tipo: Ambulanza {total_buckets['amb']}, "
                f"Carabinieri {total_buckets['car']}, VDF {total_buckets['vdf']}, "
                f"Negative {total_buckets['neg']}.\n"
                f"- Nuove assegnate: train {new_counts['train']}, "
                f"valid {new_counts['valid']}, test {new_counts['test']}.\n"
                "- Le nuove negative sono in train: la loro fonte/gruppo non e' documentata.\n"
                "- `car_old_video_001_frame_001` e' in train con gli altri frame "
                "della stessa fonte gia' presenti in v1.\n"
                "- `v11_car_video_009_frame_001` e `car_old_video_003_frame_005` "
                "sono esclusi dopo review.\n"
                "- Il test v1 resta intatto; i sei video benchmark restano esterni al training.\n"
                "- `split_manifest.csv` documenta ogni file e gruppo.\n\n"
                "| Split | v1 | Aggiunte | Totale |\n"
                "|---|---:|---:|---:|\n"
                + "".join(
                    f"| {split} | {old_counts[split]} | {new_counts[split]} | "
                    f"{old_counts[split] + new_counts[split]} |\n"
                    for split in ("train", "valid", "test")
                ),
                encoding="utf-8",
            )
            staged.rename(output)

    print("Dataset v1.1 creato:", output)
    print("Vecchie immagini mantenute:", shared)
    print("Nuove immagini:", len(additions))
    print("Nuovi split:", dict(Counter(assignment[s.group_id] for s in additions)))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    build(args.base.resolve(), args.export.resolve(), args.output.resolve(), args.seed)


if __name__ == "__main__":
    main()
