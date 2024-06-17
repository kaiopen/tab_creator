from pathlib import Path
import json

import torch

from kaitorch.pcd import PointCloudXYZIRID, PointCloudReaderXYZIRID
from kaitorch.data import Group, cell_from_size

from utils import read_seq, RANGE_X_E, RANGE_Y_E, SIZE, ERROR, CLOSED


seq = read_seq()
dst = Path.cwd().joinpath('data', 'raw', 'bev', seq)
dst.mkdir(parents=True, exist_ok=True)

lower_bound = torch.as_tensor((RANGE_X_E[0], RANGE_Y_E[0]))
upper_bound = torch.as_tensor((RANGE_X_E[1], RANGE_Y_E[1]))
group = Group(
    lower_bound, cell_from_size(
        lower_bound, upper_bound, SIZE, ERROR, CLOSED
    ),
    ERROR, CLOSED, upper_bound
)

for f in Path.cwd().joinpath('data', 'raw', 'ground', seq).glob('*.pcd'):
    print(f)

    # Search curbs.
    pcd = PointCloudXYZIRID.from_similar(PointCloudReaderXYZIRID(f))
    points_xy = pcd.xy_
    points_theta = pcd.theta_.squeeze()
    points_ring = pcd.ring_.squeeze()
    points_id = pcd.id_.squeeze()

    curbs = []
    for ring in range(16):
        mask = ring == points_ring
        _, indices = torch.sort(points_theta[mask])
        _points_xy = points_xy[mask][indices].tolist()
        _points_id = points_id[mask][indices].tolist()

        g = True
        for i, id in enumerate(_points_id):
            if 0 == id:
                if not g:
                    curbs.append(_points_xy[max(i - 1, 0)])
                    g = True
            else:
                if g:
                    curbs.append(_points_xy[i])
                    g = False

    shapes = []
    for p in group(torch.as_tensor(curbs)).tolist():
        shapes.append(
            {
                'label': 'curb',
                'points': [p],
                'group_id': None,
                'description': None,
                'shape_type': 'point',
                'flags': {}
            }
        )

    stem = f.stem
    data = {
        'version': '5.3.1',
        'flags': {},
        'shapes': shapes,
        'imagePath': stem + '.png',
        'imageData': None,
        'imageHeight': 4200,
        'imageWidth': 2200,
    }

    json.dump(data, dst.joinpath(stem + '.json').open('w'), indent=2)
