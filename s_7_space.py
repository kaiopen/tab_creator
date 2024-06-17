import csv
import math
from pathlib import Path

import torch

from kaitorch.data import Group, mask_in_range, xy_to_rt, PI

from tab import TAB


tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

group = Group(
    lower_bound=(TAB.RANGE_RHO[0], TAB.RANGE_THETA[0]),
    upper_bound=(TAB.RANGE_RHO[1], TAB.RANGE_THETA[1]),
    cell=(2, 10 * PI / 180)
)

r = list(TAB.RANGE_RHO) + list(TAB.RANGE_THETA)

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)

points = []
for f in tab_train:
    for bound in tab_train.get_boundaries(f):
        for p in bound['points']:
            points.append(p['xy'])
for f in tab_val:
    for bound in tab_val.get_boundaries(f):
        for p in bound['points']:
            points.append(p['xy'])
points = xy_to_rt(torch.as_tensor(points))
groups = group(points[mask_in_range(points, r)])

ids = 18 * groups[:, 0] + groups[:, 1]
ids, indices = torch.sort(ids)
ids, counts = torch.unique_consecutive(ids, return_counts=True)

table = []
indices = indices.tolist()
groups = groups.tolist()
i = 0
for c in counts.tolist():
    table.append((*groups[indices[i]], c, math.log(c)))
    i += c
csv.writer(dst.joinpath('space_tv.csv').open('w')).writerows(table)

points = []
for f in tab_test:
    for bound in tab_test.get_boundaries(f):
        for p in bound['points']:
            points.append(p['xy'])
points = xy_to_rt(torch.as_tensor(points))
groups = group(points[mask_in_range(points, r)])
ids = 18 * groups[:, 0] + groups[:, 1]
ids, indices = torch.sort(ids)
ids, counts = torch.unique_consecutive(ids, return_counts=True)

table = []
indices = indices.tolist()
groups = groups.tolist()
i = 0
for c in counts.tolist():
    table.append((*groups[indices[i]], c, math.log(c)))
    i += c
csv.writer(dst.joinpath('space_te.csv').open('w')).writerows(table)
