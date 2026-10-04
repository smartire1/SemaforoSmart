"""Generate or verify the DAY Copy-Paste batch, without touching real datasets."""
import argparse
import csv
import hashlib
import io
import json
import math
import random
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, __version__ as PILLOW_VERSION

ROOT = Path(__file__).resolve().parents[2]
AREA = ROOT / 'data/raw/v1.3_cp'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def png(im):
    stream = io.BytesIO()
    im.save(stream, format='PNG')
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', default='data/raw/v1.3_cp/configs/day_batch_001.json')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    config_path = ROOT / args.config
    config = json.loads(config_path.read_text(encoding='utf-8'))
    rng = random.Random(config['seed'])
    batch = config['batch_id']
    if not batch.replace('_', '').isalnum():
        raise ValueError('Unsafe batch ID')
    ds = ROOT / 'data/datasets/v1.3'
    with (ds / 'split_manifest.csv').open(encoding='utf-8-sig') as f:
        split_rows = list(csv.DictReader(f))
    by_image = {r['image']: r for r in split_rows}

    def train_source(name):
        row = by_image[name]
        if row['split'] != 'train':
            raise ValueError(f'Non-train source: {name}')
        return row

    backgrounds = {}
    for bg in config['backgrounds']:
        path = ROOT / bg['path']
        row = train_source(path.name)
        if path.read_bytes() != (ds / 'train/images' / path.name).read_bytes():
            raise ValueError('Background changed')
        if (ds / 'train/labels' / row['label']).read_text().strip():
            raise ValueError('Background contains target labels')
        backgrounds[bg['id']] = (bg, Image.open(path).convert('RGBA'), sha(path.read_bytes()), row['group_id'])

    records, thumbnails, hashes = [], [], set()
    class_counts, distance_counts = Counter(), Counter()
    output = AREA / 'generated' / batch

    def emit(path, data):
        if path.exists():
            if path.read_bytes() != data:
                raise ValueError(f'Output differs, refusing overwrite: {path}')
        elif args.verify_only:
            raise FileNotFoundError(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)

    for asset in config['cutouts']:
        src = train_source(asset['source_image'])
        source_label = ds / 'train/labels' / src['label']
        classes = {int(line.split()[0]) for line in source_label.read_text().splitlines() if line.strip()}
        if asset['class_id'] not in classes:
            raise ValueError('Source class mismatch')
        path = ROOT / asset['path']
        cutout = Image.open(path)
        if 'A' not in cutout.getbands() or cutout.getchannel('A').getextrema() != (0, 255):
            raise ValueError('Expected genuine transparent cutout')
        crop = cutout.getchannel('A').getbbox()
        patch = cutout.convert('RGBA').crop(crop)
        ratio = patch.width / patch.height
        previous = []
        # Each cutout contributes six FAR and four MID, in shuffled order.
        bands = ['FAR'] * config['far_per_cutout'] + ['MID'] * config['mid_per_cutout']
        rng.shuffle(bands)
        for index, band in enumerate(bands):
            for attempt in range(1000):
                bg_id = rng.choice(asset['compatible_backgrounds'])
                bg, canvas, bg_hash, bg_group = backgrounds[bg_id]
                W, H = canvas.size
                fraction = rng.uniform(*config['area_ranges'][band])
                width = round(math.sqrt(fraction * W * H * ratio))
                height = round(width / ratio)
                # Couple larger objects with a lower road contact point.
                bottom = round(H * (bg['bottom_range'][0] + (bg['bottom_range'][1]-bg['bottom_range'][0]) * min(1, fraction/.16) + rng.uniform(-.025, .025)))
                lo = max(bg['center_range'][0]*W, width/2 + .015*W)
                hi = min(bg['center_range'][1]*W, W-width/2-.015*W)
                if lo > hi or bottom-height < 0 or bottom > H:
                    continue
                x = round(rng.uniform(lo, hi)-width/2)
                y = bottom-height
                if any(old_bg == bg_id and abs(old_x-x/W)<.06 and abs(old_y-bottom/H)<.05 and abs(old_area-fraction)<.015 for old_bg,old_x,old_y,old_area in previous):
                    continue
                resized = patch.resize((width, height), Image.Resampling.LANCZOS)
                a,b,d,e = resized.getchannel('A').getbbox()
                box = (x+a,y+b,x+d,y+e)
                l,t,r,bot = box
                actual_area = (r-l)*(bot-t)/(W*H)
                actual_band = 'FAR' if actual_area < .1 else 'MID' if actual_area <= .3 else 'CLOSE'
                if actual_band != band:
                    continue
                previous.append((bg_id,x/W,bottom/H,fraction))
                break
            else:
                raise ValueError(f'Cannot place {asset["id"]} {band}')
            values = ((l+r)/2/W,(t+bot)/2/H,(r-l)/W,(bot-t)/H)
            if not (0 <= l < r <= W and 0 <= t < bot <= H):
                raise ValueError('Out-of-frame box')
            ident = f'{batch}_{len(records)+1:03d}'
            label = f'{asset["class_id"]} ' + ' '.join(f'{v:.10f}' for v in values) + '\n'
            composed = canvas.copy()
            composed.alpha_composite(resized,(x,y))
            composed = composed.convert('RGB')
            data = png(composed)
            image_hash = sha(data)
            if image_hash in hashes:
                raise ValueError('Duplicate composition')
            hashes.add(image_hash)
            emit(output/'images'/f'{ident}.png',data)
            emit(output/'labels'/f'{ident}.txt',label.encode())
            preview = composed.copy()
            draw = ImageDraw.Draw(preview)
            draw.rectangle((l,t,r-1,bot-1),outline='#00ff66',width=max(2,W//500))
            emit(output/'previews'/f'{ident}_boxes.png',png(preview))
            preview.thumbnail((310,205))
            thumbnails.append((ident,band,preview))
            class_counts[asset['class_id']] += 1
            distance_counts[band] += 1
            records.append(dict(
                id=ident,class_id=asset['class_id'],class_name=asset['class_name'],light='DAY',distance=band,
                seed=config['seed'],cutout=asset['path'],cutout_sha256=sha(path.read_bytes()),
                source_image=src['image'],source_group=src['group_id'],source_split=src['split'],
                source_image_sha256=sha((ds/'train/images'/src['image']).read_bytes()),
                source_label_sha256=sha(source_label.read_bytes()),
                background=bg['path'],background_group=bg_group,background_sha256=bg_hash,
                crop_xyxy=json.dumps(crop),width_px=width,height_px=height,left_px=x,top_px=y,
                scale_x=width/patch.width,scale_y=height/patch.height,
                canvas_width=W,canvas_height=H,box_xyxy=json.dumps(box),box_area_fraction=actual_area,
                yolo=label.strip(),transforms='alpha crop; proportional LANCZOS resize; translation; alpha composite',
                image_sha256=image_hash,label_sha256=sha(label.encode()),
                config_sha256=sha(config_path.read_bytes()),script_sha256=sha(Path(__file__).read_bytes()),
                pillow_version=PILLOW_VERSION))

    if dict(class_counts) != {0:20,1:20,2:20} or dict(distance_counts) != {'FAR':36,'MID':24}:
        raise ValueError('Batch quotas not met')
    manifest_path = AREA/'manifests'/f'{batch}.csv'
    if manifest_path.exists():
        with manifest_path.open(encoding='utf-8', newline='') as existing_file:
            historical = {row['id']: row for row in csv.DictReader(existing_file)}
        for record in records:
            if record['id'] in historical:
                # Moving or extending the script must not rewrite the hash that
                # documents the generator used for an already-created sample.
                record['script_sha256'] = historical[record['id']]['script_sha256']
    stream = io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=list(records[0]))
    writer.writeheader(); writer.writerows(records)
    emit(manifest_path,stream.getvalue().encode('utf-8'))
    # Stable sample: 20 images spread across every cutout and class.
    sample_rng=random.Random(config['seed']+1)
    sample=sorted(sample_rng.sample(range(len(thumbnails)),20))
    for page, indices in [('sample',sample),('all_01',list(range(30))),('all_02',list(range(30,60)))]:
        sheet=Image.new('RGB',(1600,240*math.ceil(len(indices)/5)),'#eeeeee')
        draw=ImageDraw.Draw(sheet)
        for slot,j in enumerate(indices):
            ident,band,thumb=thumbnails[j]; x=slot%5*320; y=slot//5*240
            draw.text((x+5,y+5),f'{ident} {band}',fill='black')
            sheet.paste(thumb,(x+(320-thumb.width)//2,y+28))
        emit(AREA/'review'/f'{batch}_{page}.png',png(sheet))
    print(json.dumps(dict(status='verified byte-identical' if args.verify_only else 'generated',
                         total=len(records),classes=dict(class_counts),distance=dict(distance_counts),
                         unique_images=len(hashes),output=str(output)),indent=2))


if __name__ == '__main__':
    main()
