#!/usr/bin/env python3
"""Build the leakage-free v1.2 augmentation experiment.

Roboflow v4 contains two exposure/blur variants for every one of the 586 v1.2
sources, all exported under ``train``.  This builder keeps only variants whose
source belongs to the frozen v1.2 training split.  Validation and test are
copied unchanged from v1.2, so evaluation remains comparable with the baseline.
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

SCRIPTS_DIR = Path(__file__).resolve().parents[2]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from split_dataset import CLASS_NAMES, IMAGE_EXTENSIONS, canonical_stem


ROOT = Path(__file__).resolve().parents[3]
EXPECTED_CLASSES = "names: ['Ambulanza', 'Carabinieri', 'VigiliDelFuoco']"


def project_path(value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else ROOT / path


def parse_label(text: str, name: str) -> tuple[int, str]:
    ids: set[int] = set()
    count = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split()
        if len(fields) != 5:
            raise ValueError(f"Label non valida: {name}:{line_number}")
        class_id = int(fields[0])
        if class_id not in CLASS_NAMES:
            raise ValueError(f"Classe inattesa: {name}:{line_number}")
        coordinates = [float(value) for value in fields[1:]]
        if not all(0.0 <= value <= 1.0 for value in coordinates):
            raise ValueError(f"Coordinate fuori intervallo: {name}:{line_number}")
        if coordinates[2] <= 0 or coordinates[3] <= 0:
            raise ValueError(f"Box senza area: {name}:{line_number}")
        ids.add(class_id)
        count += 1
    return count, ";".join(str(value) for value in sorted(ids))


def load_manifest(base: Path) -> list[dict[str, str]]:
    path = base / "split_manifest.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 586:
        raise ValueError(f"Attese 586 sorgenti v1.2, trovate {len(rows)}")
    counts = Counter(row["split"] for row in rows)
    if counts != Counter({"train": 458, "valid": 85, "test": 43}):
        raise ValueError(f"Split base inatteso: {dict(counts)}")
    if len({row["canonical_stem"] for row in rows}) != 586:
        raise ValueError("Canonical stem duplicato nel manifest v1.2")
    return rows


def load_augmented(
    archive: zipfile.ZipFile,
) -> dict[str, list[tuple[str, str, str, str, int, str]]]:
    names = set(archive.namelist())
    yaml_text = archive.read("data.yaml").decode("utf-8-sig")
    if EXPECTED_CLASSES not in yaml_text:
        raise ValueError("Classi dell'export augmentation inattese")

    image_entries = sorted(
        name
        for name in names
        if name.startswith("train/images/")
        and name.count("/") == 2
        and PurePosixPath(name).suffix.lower() in IMAGE_EXTENSIONS
    )
    if len(image_entries) != 1172:
        raise ValueError(f"Attese 1172 immagini augmentate, trovate {len(image_entries)}")

    grouped: dict[str, list[tuple[str, str, str, str, int, str]]] = defaultdict(list)
    for image_entry in image_entries:
        image_name = PurePosixPath(image_entry).name
        label_name = f"{Path(image_name).stem}.txt"
        label_entry = f"train/labels/{label_name}"
        if label_entry not in names:
            raise FileNotFoundError(f"Label mancante: {label_entry}")
        label_text = archive.read(label_entry).decode("utf-8-sig")
        box_count, class_ids = parse_label(label_text, label_entry)
        grouped[canonical_stem(Path(image_name))].append(
            (image_entry, label_entry, image_name, label_name, box_count, class_ids)
        )

    bad = {stem: len(items) for stem, items in grouped.items() if len(items) != 2}
    if len(grouped) != 586 or bad:
        raise ValueError(
            f"Attese 586 sorgenti con due varianti; sorgenti={len(grouped)}, anomalie={bad}"
        )
    return grouped


def write_yaml(root: Path) -> None:
    (root / "data.yaml").write_text(
        "train: train/images\n"
        "val: valid/images\n"
        "test: test/images\n\n"
        "names:\n"
        "  0: Ambulanza\n"
        "  1: Carabinieri\n"
        "  2: VigiliDelFuoco\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="data/datasets/v1.2")
    parser.add_argument("--export", default="data/datasets/v1.2_Aug/v1.2_Aug.zip")
    parser.add_argument("--output", default="data/datasets/v1.2_Aug")
    args = parser.parse_args()

    base = project_path(args.base).resolve()
    export = project_path(args.export).resolve()
    output = project_path(args.output).resolve()
    if not export.is_file():
        raise FileNotFoundError(export)

    rows = load_manifest(base)
    source_split = {row["canonical_stem"]: row["split"] for row in rows}

    with zipfile.ZipFile(export) as archive:
        augmented = load_augmented(archive)
        if set(augmented) != set(source_split):
            missing = sorted(set(source_split) - set(augmented))
            extra = sorted(set(augmented) - set(source_split))
            raise ValueError(f"Mapping incompleto. Mancanti={missing}, extra={extra}")

        with tempfile.TemporaryDirectory(prefix=".v1.2-aug-build-", dir=output.parent) as tmp:
            staged = Path(tmp)
            manifest_rows: list[dict[str, object]] = []
            for split in ("train", "valid", "test"):
                (staged / split / "images").mkdir(parents=True)
                (staged / split / "labels").mkdir(parents=True)

            for row in rows:
                split = row["split"]
                stem = row["canonical_stem"]
                if split == "train":
                    for variant_index, item in enumerate(augmented[stem], 1):
                        image_entry, label_entry, image_name, label_name, boxes, ids = item
                        (staged / split / "images" / image_name).write_bytes(
                            archive.read(image_entry)
                        )
                        (staged / split / "labels" / label_name).write_bytes(
                            archive.read(label_entry)
                        )
                        manifest_rows.append(
                            {
                                "split": split,
                                "source_split": split,
                                "canonical_stem": stem,
                                "variant": f"roboflow_aug_{variant_index}",
                                "image": image_name,
                                "label": label_name,
                                "box_count": boxes,
                                "class_ids": ids,
                            }
                        )
                else:
                    image_source = base / split / "images" / row["image"]
                    label_source = base / split / "labels" / row["label"]
                    shutil.copy2(image_source, staged / split / "images" / row["image"])
                    shutil.copy2(label_source, staged / split / "labels" / row["label"])
                    boxes, ids = parse_label(
                        label_source.read_text(encoding="utf-8"), str(label_source)
                    )
                    manifest_rows.append(
                        {
                            "split": split,
                            "source_split": split,
                            "canonical_stem": stem,
                            "variant": "original_frozen",
                            "image": row["image"],
                            "label": row["label"],
                            "box_count": boxes,
                            "class_ids": ids,
                        }
                    )

            expected = {"train": 916, "valid": 85, "test": 43}
            for split, count in expected.items():
                images = list((staged / split / "images").iterdir())
                labels = list((staged / split / "labels").glob("*.txt"))
                if len(images) != count or len(labels) != count:
                    raise ValueError(
                        f"Conteggio {split} errato: immagini={len(images)}, label={len(labels)}"
                    )

            write_yaml(staged)
            with (staged / "split_manifest.csv").open(
                "w", newline="", encoding="utf-8"
            ) as handle:
                writer = csv.DictWriter(handle, fieldnames=list(manifest_rows[0]))
                writer.writeheader()
                writer.writerows(manifest_rows)

            (staged / "README.md").write_text(
                "# SemaforoSmart dataset v1.2_Aug\n\n"
                "Variante sperimentale della v1.2 senza nuove sorgenti. Roboflow v4 "
                "ha generato due versioni per immagine con Exposure tra -15% e +15% "
                "e Gaussian Blur tra 0 e 1.4 px.\n\n"
                "- Train: 916 immagini augmentate, due per ciascuna delle 458 sorgenti train.\n"
                "- Validation: 85 originali congelate dalla v1.2.\n"
                "- Test: 43 originali congelate dalla v1.2.\n"
                "- Le 256 augmentation derivate dalle 128 sorgenti validation/test sono escluse.\n"
                "- `split_manifest.csv` documenta origine, variante e split.\n"
                "- `v1.2_Aug.zip` conserva l'export Roboflow integrale da 1172 immagini.\n\n"
                "Questa versione serve soltanto a esperimenti controllati e non sostituisce "
                "la baseline v1.2.\n",
                encoding="utf-8",
            )

            for split in ("train", "valid", "test"):
                destination = output / split
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.move(str(staged / split), destination)
            shutil.copy2(staged / "data.yaml", output / "data.yaml")
            shutil.copy2(staged / "split_manifest.csv", output / "split_manifest.csv")
            shutil.copy2(staged / "README.md", output / "README.md")

    print(f"Dataset creato: {output}")
    print("Split: train=916, valid=85, test=43")
    print("Validation e test sono originali e identici alla v1.2.")


if __name__ == "__main__":
    main()
