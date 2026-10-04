#!/usr/bin/env python3
"""Build v1.2 preserving the complete v1.1 split and its frozen test set.

The Roboflow v1.2 export contains all 586 images in ``train``. This script
recognizes the 517 samples already present in v1.1, copies them without changing
their split, then assigns only the 69 v1.2 additions to train/validation by
source group. No new sample is allowed into test.
"""

from __future__ import annotations

import argparse
import csv
import random
import re
import shutil
import sys
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

SCRIPTS_DIR = Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from split_dataset import CLASS_NAMES, canonical_stem, closest_group_subset


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
EXPECTED_CLASSES = "names: ['Ambulanza', 'Carabinieri', 'VigiliDelFuoco']"
ROMA_GROUP = "v12_roma_centro"


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


def classify_v12(stem: str) -> tuple[str, str]:
    if re.fullmatch(r"v12_null_roma_centro_part_\d+_frame_\d+", stem):
        return "neg", ROMA_GROUP

    match = re.fullmatch(
        r"v12_(amb|car|vdf)_comp_\d+(?:_clip_\d+)?_frame_\d+", stem
    )
    if match:
        return match.group(1), ROMA_GROUP

    match = re.fullmatch(r"v12_(car|vdf)_video_(\d+)_frame_\d+", stem)
    if match:
        return match.group(1), f"v12_{match.group(1)}_video_{match.group(2)}"

    match = re.fullmatch(r"v12_amb_old_recovery_(\d+)", stem)
    if match:
        number = int(match.group(1))
        # The descriptions identify 006 and 007 as two views of the same scene.
        if number in {6, 7}:
            return "amb", "v12_amb_old_recovery_scene_006_007"
        return "amb", stem

    if stem == "v12_multiclass_source_unknown_001":
        return "multi", stem

    raise ValueError(f"Nome v1.2 non riconosciuto: {stem}")


def load_base(base: Path) -> tuple[list[dict[str, str]], set[str]]:
    manifest = base / "split_manifest.csv"
    if not manifest.is_file():
        raise FileNotFoundError(manifest)
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 517:
        raise ValueError(f"Attese 517 immagini v1.1, trovate {len(rows)}")

    stems: set[str] = set()
    groups: dict[str, str] = {}
    for row in rows:
        split = row["split"]
        if split not in ("train", "valid", "test"):
            raise ValueError(f"Split v1.1 non valido: {split}")
        image = base / split / "images" / row["image"]
        label = base / split / "labels" / row["label"]
        if not image.is_file() or not label.is_file():
            raise FileNotFoundError(f"Coppia v1.1 mancante: {row['image']}")
        stem = row["canonical_stem"]
        if stem in stems:
            raise ValueError(f"Canonical stem duplicato nella v1.1: {stem}")
        stems.add(stem)
        previous = groups.setdefault(row["group_id"], split)
        if previous != split:
            raise ValueError(f"Gruppo v1.1 distribuito su piu' split: {row['group_id']}")
    return rows, stems


def load_additions(
    archive: zipfile.ZipFile, base_stems: set[str]
) -> tuple[list[AddedSample], int]:
    names = set(archive.namelist())
    if "data.yaml" not in names:
        raise FileNotFoundError("data.yaml mancante nello ZIP")
    yaml_text = archive.read("data.yaml").decode("utf-8-sig")
    if EXPECTED_CLASSES not in yaml_text:
        raise ValueError("Classi dell'export diverse dalla v1.1")

    image_entries = sorted(
        name
        for name in names
        if name.startswith("train/images/")
        and name.count("/") == 2
        and PurePosixPath(name).suffix.lower() in IMAGE_EXTENSIONS
    )
    if len(image_entries) != 586:
        raise ValueError(f"Attese 586 immagini nello ZIP, trovate {len(image_entries)}")

    additions: list[AddedSample] = []
    seen_stems: set[str] = set()
    shared = 0
    for image_entry in image_entries:
        image_name = PurePosixPath(image_entry).name
        stem = canonical_stem(Path(image_name))
        if stem in seen_stems:
            raise ValueError(f"Canonical stem duplicato nello ZIP: {stem}")
        seen_stems.add(stem)

        label_name = f"{Path(image_name).stem}.txt"
        label_entry = f"train/labels/{label_name}"
        if label_entry not in names:
            raise FileNotFoundError(f"Label mancante nello ZIP: {label_entry}")
        if stem in base_stems:
            shared += 1
            continue

        bucket, group_id = classify_v12(stem)
        box_count, class_ids = parse_label(
            archive.read(label_entry).decode("utf-8-sig"), label_entry
        )
        if bucket == "neg" and box_count != 0:
            raise ValueError(f"Negativa con box: {image_name}")
        if bucket != "neg" and box_count == 0:
            raise ValueError(f"Positiva senza box: {image_name}")
        additions.append(
            AddedSample(
                image_entry,
                label_entry,
                image_name,
                label_name,
                stem,
                bucket,
                group_id,
                box_count,
                class_ids,
            )
        )

    if shared != 517 or len(additions) != 69 or base_stems - seen_stems:
        raise ValueError(
            f"Composizione inattesa: {shared} gia' in v1.1, "
            f"{len(additions)} nuove"
        )
    return additions, shared


def assign_additions(additions: list[AddedSample], seed: int) -> dict[str, str]:
    by_bucket: dict[str, dict[str, list[AddedSample]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for sample in additions:
        by_bucket[sample.bucket][sample.group_id].append(sample)

    assignments: dict[str, str] = {ROMA_GROUP: "train"}
    for bucket, groups in sorted(by_bucket.items()):
        candidates = [
            (group_id, samples)
            for group_id, samples in sorted(groups.items())
            if group_id != ROMA_GROUP
        ]
        target = round(sum(len(samples) for samples in groups.values()) * 0.15)
        valid_groups = closest_group_subset(
            candidates, target, random.Random(f"{seed}:{bucket}:v1.2")
        )
        for group_id, _ in candidates:
            assignments[group_id] = "valid" if group_id in valid_groups else "train"

    if set(assignments.values()) - {"train", "valid"}:
        raise ValueError("Assegnazione inattesa")
    return assignments


def copy_base(base: Path, staged: Path) -> None:
    for split in ("train", "valid", "test"):
        shutil.copytree(base / split / "images", staged / split / "images")
        shutil.copytree(base / split / "labels", staged / split / "labels")


def write_data_yaml(staged: Path) -> None:
    (staged / "data.yaml").write_text(
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n\n"
        "names:\n"
        "  0: Ambulanza\n"
        "  1: Carabinieri\n"
        "  2: VigiliDelFuoco\n",
        encoding="utf-8",
    )


def build(base: Path, export: Path, output: Path, seed: int) -> None:
    if not base.is_dir() or not export.is_file():
        raise FileNotFoundError("Base v1.1 o ZIP v1.2 mancante")
    if output.exists():
        raise FileExistsError(f"La destinazione esiste gia': {output}")

    base_rows, base_stems = load_base(base)
    with zipfile.ZipFile(export) as archive:
        additions, shared = load_additions(archive, base_stems)
        assignments = assign_additions(additions, seed)

        staged = output
        staged.mkdir(parents=True)
        copy_base(base, staged)
        rows = list(base_rows)
        for sample in additions:
            split = assignments[sample.group_id]
            image_target = staged / split / "images" / sample.image_name
            label_target = staged / split / "labels" / sample.label_name
            if image_target.exists() or label_target.exists():
                raise FileExistsError(f"Collisione di nome: {sample.image_name}")
            with archive.open(sample.image_entry) as source, image_target.open("wb") as target:
                shutil.copyfileobj(source, target)
            with archive.open(sample.label_entry) as source, label_target.open("wb") as target:
                shutil.copyfileobj(source, target)
            rows.append(
                {
                    "split": split,
                    "bucket": sample.bucket,
                    "group_id": sample.group_id,
                    "canonical_stem": sample.canonical,
                    "image": sample.image_name,
                    "label": sample.label_name,
                    "box_count": str(sample.box_count),
                    "class_ids": ",".join(map(str, sample.class_ids)),
                }
            )

    with (staged / "split_manifest.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(base_rows[0]))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (row["split"], row["image"])))
    write_data_yaml(staged)

    old_counts = Counter(row["split"] for row in base_rows)
    new_counts = Counter(assignments[sample.group_id] for sample in additions)
    new_buckets = Counter(sample.bucket for sample in additions)
    total_buckets = Counter(row["bucket"] for row in rows)
    (staged / "README.md").write_text(
        "# SemaforoSmart dataset v1.2\n\n"
        "Dataset cumulativo: i 517 file della v1.1 mantengono esattamente il "
        "proprio split; il test resta congelato.\n\n"
        f"- Export originale Roboflow: `{export.name}` (586 immagini; {shared} "
        "gia' in v1.1, 69 aggiunte).\n"
        f"- Aggiunte per nome: Ambulanza {new_buckets['amb']}, Carabinieri "
        f"{new_buckets['car']}, VDF {new_buckets['vdf']}, Multiclasse "
        f"{new_buckets['multi']}, Negative {new_buckets['neg']}.\n"
        f"- Totali per bucket: Ambulanza {total_buckets['amb']}, Carabinieri "
        f"{total_buckets['car']}, VDF {total_buckets['vdf']}, Multiclasse "
        f"{total_buckets['multi']}, Negative {total_buckets['neg']}.\n"
        f"- Aggiunte assegnate: train {new_counts['train']}, valid "
        f"{new_counts['valid']}, test 0.\n"
        "- Tutti i frame delle due compilation di Roma centro, positivi e "
        "NULL, formano un unico gruppo in train.\n"
        "- Nessuna immagine v1.2 e' stata aggiunta al test.\n"
        "- `split_manifest.csv` documenta file, gruppo e split.\n\n"
        "| Split | v1.1 | Aggiunte | Totale |\n"
        "|---|---:|---:|---:|\n"
        + "".join(
            f"| {split} | {old_counts[split]} | {new_counts[split]} | "
            f"{old_counts[split] + new_counts[split]} |\n"
            for split in ("train", "valid", "test")
        ),
        encoding="utf-8",
    )

    print("Dataset v1.2 creato:", output)
    print("Immagini v1.1 mantenute:", shared)
    print("Nuove immagini:", len(additions))
    print("Nuovi split:", dict(new_counts))


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
