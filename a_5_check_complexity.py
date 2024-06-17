import json
from pathlib import Path

from utils import read_seq, BOUNDARY


fs = []
for f in Path.cwd().joinpath('data', 'raw', 'bev', read_seq()).glob('*.json'):
    fs.append(f)
fs.sort()

errs = []
for f in fs:
    print(f)

    for shape in json.load(f.open('r'))['shapes']:
        lab = shape['label']
        if 'curb' == lab or lab in BOUNDARY:
            continue

        if not (
            lab[0] in ('s', 'u')
            and lab[1] in ('s', 'c')
            and lab[2] in ('v', 'l', 'b', 'o', 'd', 'i')
            and lab[3] in ('m', 's')
        ):
            errs.append(f'{str(f)}: an invalid attribute.')
            continue

        match shape['shape_type']:
            case 'linestrip':
                if len(shape['points']) < 3:
                    errs.append(f'{str(f)}: an invalid linestrip.')
            case 'line':
                if len(shape['points']) != 2:
                    errs.append(f'{str(f)}: an invalid line.')
            case 'point':
                if len(shape['points']) != 1:
                    errs.append(f'{str(f)}: an invalid point.')
            case _:
                errs.append(f'{str(f)}: an invalid shape.')

print('\nERROR:')
for e in errs:
    print(e)
