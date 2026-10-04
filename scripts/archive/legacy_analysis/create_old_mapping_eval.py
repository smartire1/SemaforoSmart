#!/usr/bin/env python3
"""Crea una copia del test v1 con gli ID compatibili con bestOLD.pt."""

from __future__ import annotations

import shutil
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SOURCE = PROJECT_ROOT / "data" / "datasets" / "v1" / "test"
OUTPUT_ROOT = PROJECT_ROOT / "data" / "datasets" / "v1_eval_old_mapping"
ID_MAPPING = {0: 2, 1: 0, 2: 1}


def main() -> None:
    if OUTPUT_ROOT.exists() and any(OUTPUT_ROOT.iterdir()):
        raise SystemExit(f"Destinazione già esistente e non vuota: {OUTPUT_ROOT}")

    output_images = OUTPUT_ROOT / "test" / "images"
    output_labels = OUTPUT_ROOT / "test" / "labels"
    output_images.mkdir(parents=True, exist_ok=True)
    output_labels.mkdir(parents=True, exist_ok=True)

    images = sorted(path for path in (SOURCE / "images").iterdir() if path.is_file())
    labels = sorted((SOURCE / "labels").glob("*.txt"))
    counts: Counter[int] = Counter()

    for image in images:
        shutil.copy2(image, output_images / image.name)

    for label in labels:
        converted: list[str] = []
        for line_number, line in enumerate(label.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            fields = line.split()
            if len(fields) != 5:
                raise ValueError(f"Riga YOLO non valida: {label}:{line_number}")
            old_id = int(fields[0])
            if old_id not in ID_MAPPING:
                raise ValueError(f"Classe inattesa {old_id}: {label}:{line_number}")
            new_id = ID_MAPPING[old_id]
            counts[new_id] += 1
            converted.append(" ".join([str(new_id), *fields[1:]]))
        text = "\n".join(converted)
        if text:
            text += "\n"
        (output_labels / label.name).write_text(text, encoding="utf-8")

    (OUTPUT_ROOT / "data.yaml").write_text(
        "train: test/images\n"
        "val: test/images\n"
        "test: test/images\n\n"
        "names:\n"
        "  0: Carabinieri\n"
        "  1: FireFighter\n"
        "  2: ambulance\n",
        encoding="utf-8",
    )
    (OUTPUT_ROOT / "README.md").write_text(
        "# v1 evaluation mapping for bestOLD.pt\n\n"
        "Copia derivata esclusivamente per confrontare `bestOLD.pt` sul test di v1.\n"
        "Il dataset originale non è stato modificato.\n\n"
        "Rimappatura delle label: `0 Ambulanza -> 2 ambulance`, "
        "`1 Carabinieri -> 0 Carabinieri`, "
        "`2 VigiliDelFuoco -> 1 FireFighter`.\n\n"
        "Non usare questa cartella per il training.\n",
        encoding="utf-8",
    )

    print(f"Immagini copiate: {len(images)}")
    print(f"Label copiate: {len(labels)}")
    print(f"Oggetti per ID vecchio: {dict(sorted(counts.items()))}")
    print(f"Output: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
