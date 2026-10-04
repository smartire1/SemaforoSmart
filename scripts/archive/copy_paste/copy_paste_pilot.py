"""Deterministic, single-object Copy-Paste pilot. Paths are project-relative."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as pillow_version

ROOT = Path(__file__).resolve().parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='data/raw/v1.3_cp/archive/pilot/configs/pilot_001.json')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    config_path = ROOT / args.config
    c = json.loads(config_path.read_text(encoding='utf-8'))
    paths = {k: ROOT / c[k] for k in ('background', 'cutout', 'source_image', 'source_label')}
    if not paths['background'].exists():
        paths['background'] = ROOT / c['background'].replace('/backgroud/', '/backgrounds/')
    dataset = ROOT / 'data/datasets/v1.3'
    with (dataset / 'split_manifest.csv').open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    for key, field in [('background', 'image'), ('source_image', 'image')]:
        matches = [r for r in rows if r[field] == paths[key].name]
        if len(matches) != 1 or matches[0]['split'] != 'train':
            raise ValueError(f'{key}: expected unique train provenance')
        if digest(paths[key]) != digest(dataset / 'train/images' / paths[key].name):
            raise ValueError(f'{key}: source differs from train')
    label_path = dataset / 'train/labels' / paths['source_image'].with_suffix('.txt').name
    if digest(label_path) != digest(paths['source_label']):
        raise ValueError('Source label mismatch')
    source_classes = {int(line.split()[0]) for line in label_path.read_text().splitlines() if line.strip()}
    if c['class_id'] not in source_classes or c['class_id'] not in (0, 1, 2):
        raise ValueError('Invalid class')
    bg_label = dataset / 'train/labels' / paths['background'].with_suffix('.txt').name
    if bg_label.read_text().strip():
        raise ValueError('Background must have an empty label')

    background = Image.open(paths['background']).convert('RGBA')
    cutout = Image.open(paths['cutout'])
    if 'A' not in cutout.getbands() or cutout.getchannel('A').getextrema() != (0, 255):
        raise ValueError('Expected cutout with real transparency')
    cutout = cutout.convert('RGBA')
    crop_box = cutout.getchannel('A').getbbox()
    patch = cutout.crop(crop_box)
    width = c['object_width_px']
    height = round(patch.height * width / patch.width)
    if width <= 0 or height <= 0:
        raise ValueError('Invalid scale')
    patch = patch.resize((width, height), Image.Resampling.LANCZOS)
    x, bottom = c['left_px'], c['bottom_px']
    y = bottom - height
    W, H = background.size
    if not (0 <= x < x + width <= W and 0 <= y < y + height <= H):
        raise ValueError('Object must be entirely inside the image')
    # Include every nonzero-alpha pixel after resampling; ignore transparent margins.
    a, b, d, e = patch.getchannel('A').getbbox()
    box = (x + a, y + b, x + d, y + e)
    l, t, r, bot = box
    values = ((l+r)/2/W, (t+bot)/2/H, (r-l)/W, (bot-t)/H)
    if not all(0 <= v <= 1 for v in values) or min(values[2:]) <= 0:
        raise ValueError('Invalid YOLO box')
    label = f"{c['class_id']} " + ' '.join(f'{v:.10f}' for v in values) + '\n'
    background.alpha_composite(patch, (x, y))
    result = background.convert('RGB')
    preview = result.copy()
    draw = ImageDraw.Draw(preview)
    draw.rectangle((l, t, r-1, bot-1), outline='#00ff66', width=3)
    draw.text((l, max(0, t-16)), c['class_name'], fill='#00ff66', stroke_width=1, stroke_fill='black')

    out = ROOT / c['output_root']
    if out.resolve() != (ROOT / 'data/raw/v1.3_cp').resolve():
        raise ValueError('Pilot outputs must remain in the experimental area')
    out = out / 'archive/pilot'
    ident = c['id']
    if not ident.replace('_', '').isalnum():
        raise ValueError('Invalid output id')
    payloads = {}
    for rel, im in [(f'generated/images/{ident}.png', result), (f'generated/previews/{ident}_boxes.png', preview)]:
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        payloads[rel] = buf.getvalue()
    payloads[f'generated/labels/{ident}.txt'] = label.encode()
    record = {
        'id': ident, 'seed': c['seed'], 'randomness': 'none; fixed placement',
        'class_id': c['class_id'], 'class_name': c['class_name'],
        **{k: c[k] for k in paths}, **{k+'_sha256': digest(p) for k, p in paths.items()},
        'config_sha256': digest(config_path), 'script_sha256': digest(Path(__file__)),
        'pillow_version': pillow_version, 'crop_xyxy': json.dumps(crop_box),
        'scale_x': width/(crop_box[2]-crop_box[0]), 'scale_y': height/(crop_box[3]-crop_box[1]),
        'left_px': x, 'top_px': y, 'width_px': width, 'height_px': height,
        'canvas_width': W, 'canvas_height': H, 'box_xyxy': json.dumps(box),
        'transforms': 'alpha crop; proportional resize (rounded pixels); translation; alpha composite',
        'yolo': label.strip(), 'image_sha256': hashlib.sha256(payloads[f'generated/images/{ident}.png']).hexdigest(),
        'label_sha256': hashlib.sha256(label.encode()).hexdigest(),
    }
    manifest_path = out / 'manifest.csv'
    existing = []
    if manifest_path.exists():
        with manifest_path.open(encoding='utf-8', newline='') as f:
            existing = list(csv.DictReader(f))
    serialized = {k: str(v) for k, v in record.items()}
    matching = [row for row in existing if row['id'] == ident]
    # Historical rows retain the script hash used when they were generated.
    # Verification still regenerates and checks every image/label byte.
    if args.verify_only and len(matching) == 1:
        serialized['script_sha256'] = matching[0]['script_sha256']
    if matching and (len(matching) != 1 or matching[0] != serialized):
        raise FileExistsError(f'Manifest already contains a different recipe: {ident}')
    if args.verify_only and not matching:
        raise ValueError(f'Manifest record missing: {ident}')
    if not matching:
        existing.append(serialized)
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(record))
    writer.writeheader()
    writer.writerows(existing)
    manifest_bytes = stream.getvalue().encode('utf-8')
    # Never silently replace existing work. Re-running identical inputs is safe.
    for rel, data in payloads.items():
        p = out / rel
        if p.exists() and p.read_bytes() != data:
            raise FileExistsError(f'Existing output differs: {p}')
        if args.verify_only and not p.exists():
            raise FileNotFoundError(p)
    if not args.verify_only:
        for rel, data in payloads.items():
            p = out / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_bytes(data)
        manifest_path.write_bytes(manifest_bytes)
    print(json.dumps({'status': 'verified byte-identical' if args.verify_only else 'generated', 'image': str(out / f'generated/images/{ident}.png'), 'box': box, 'yolo': label.strip()}, indent=2))


if __name__ == '__main__':
    main()
