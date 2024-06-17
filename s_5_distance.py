import csv
from pathlib import Path

import numpy as np
from tab import TAB

from utils import round


tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

tr = 0
tr_02 = 0
tr_04 = 0
tr_06 = 0
tr_08 = 0
tr_10 = 0
tr_12 = 0
tr_14 = 0
tr_16 = 0
tr_18 = 0
tr_20 = 0
for f in tab_train:
    bounds = tab_train.get_boundaries(f)
    tr += len(bounds)
    for bound in bounds:
        points = []
        for p in bound['points']:
            points.append(p['xy'])
        points = np.asarray(points)
        d = np.sqrt(np.max(np.sum(points * points, axis=-1)))
        if d < 2:
            tr_02 += 1
        elif d < 4:
            tr_04 += 1
        elif d < 6:
            tr_06 += 1
        elif d < 8:
            tr_08 += 1
        elif d < 10:
            tr_10 += 1
        elif d < 12:
            tr_12 += 1
        elif d < 14:
            tr_14 += 1
        elif d < 16:
            tr_16 += 1
        elif d < 18:
            tr_18 += 1
        else:
            tr_20 += 1

v = 0
v_02 = 0
v_04 = 0
v_06 = 0
v_08 = 0
v_10 = 0
v_12 = 0
v_14 = 0
v_16 = 0
v_18 = 0
v_20 = 0
for f in tab_val:
    bounds = tab_val.get_boundaries(f)
    v += len(bounds)
    for bound in bounds:
        points = []
        for p in bound['points']:
            points.append(p['xy'])
        points = np.asarray(points)
        d = np.sqrt(np.max(np.sum(points * points, axis=-1)))
        if d < 2:
            v_02 += 1
        elif d < 4:
            v_04 += 1
        elif d < 6:
            v_06 += 1
        elif d < 8:
            v_08 += 1
        elif d < 10:
            v_10 += 1
        elif d < 12:
            v_12 += 1
        elif d < 14:
            v_14 += 1
        elif d < 16:
            v_16 += 1
        elif d < 18:
            v_18 += 1
        else:
            v_20 += 1

tv = tr + v
tv_02 = tr_02 + v_02
tv_04 = tr_04 + v_04
tv_06 = tr_06 + v_06
tv_08 = tr_08 + v_08
tv_10 = tr_10 + v_10
tv_12 = tr_12 + v_12
tv_14 = tr_14 + v_14
tv_16 = tr_16 + v_16
tv_18 = tr_18 + v_18
tv_20 = tr_20 + v_20

te = 0
te_02 = 0
te_04 = 0
te_06 = 0
te_08 = 0
te_10 = 0
te_12 = 0
te_14 = 0
te_16 = 0
te_18 = 0
te_20 = 0
for f in tab_test:
    bounds = tab_test.get_boundaries(f)
    te += len(bounds)
    for bound in bounds:
        points = []
        for p in bound['points']:
            points.append(p['xy'])
        points = np.asarray(points)
        d = np.sqrt(np.max(np.sum(points * points, axis=-1)))
        if d < 2:
            te_02 += 1
        elif d < 4:
            te_04 += 1
        elif d < 6:
            te_06 += 1
        elif d < 8:
            te_08 += 1
        elif d < 10:
            te_10 += 1
        elif d < 12:
            te_12 += 1
        elif d < 14:
            te_14 += 1
        elif d < 16:
            te_16 += 1
        elif d < 18:
            te_18 += 1
        else:
            te_20 += 1

t = tv + te
t_02 = tv_02 + te_02
t_04 = tv_04 + te_04
t_06 = tv_06 + te_06
t_08 = tv_08 + te_08
t_10 = tv_10 + te_10
t_12 = tv_12 + te_12
t_14 = tv_14 + te_14
t_16 = tv_16 + te_16
t_18 = tv_18 + te_18
t_20 = tv_20 + te_20

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('distance.csv').open('w')).writerows(
    (
        (
            '',
            '#. 02', '%. 02', '#. 04', '%. 04',
            '#. 06', '%. 06', '#. 08', '%. 08',
            '#. 10', '%. 10', '#. 12', '%. 12',
            '#. 14', '%. 14', '#. 16', '%. 16',
            '#. 18', '%. 18', '#. 20', '%. 20',
            'TOTAL'
        ),
        (
            'TRAIN',
            tr_02, round(tr_02 / tr * 100.), tr_04, round(tr_04 / tr * 100.),
            tr_06, round(tr_06 / tr * 100.), tr_08, round(tr_08 / tr * 100.),
            tr_10, round(tr_10 / tr * 100.), tr_12, round(tr_12 / tr * 100.),
            tr_14, round(tr_14 / tr * 100.), tr_16, round(tr_16 / tr * 100.),
            tr_18, round(tr_18 / tr * 100.), tr_20, round(tr_20 / tr * 100.),
            tr
        ),
        (
            'VAL',
            v_02, round(v_02 / v * 100.), v_04, round(v_04 / v * 100.),
            v_06, round(v_06 / v * 100.), v_08, round(v_08 / v * 100.),
            v_10, round(v_10 / v * 100.), v_12, round(v_12 / v * 100.),
            v_14, round(v_14 / v * 100.), v_16, round(v_16 / v * 100.),
            v_18, round(v_18 / v * 100.), v_20, round(v_20 / v * 100.),
            v
        ),
        (
            'TRAINVAL',
            tv_02, round(tv_02 / tv * 100.), tv_04, round(tv_04 / tv * 100.),
            tv_06, round(tv_06 / tv * 100.), tv_08, round(tv_08 / tv * 100.),
            tv_10, round(tv_10 / tv * 100.), tv_12, round(tv_12 / tv * 100.),
            tv_14, round(tv_14 / tv * 100.), tv_16, round(tv_16 / tv * 100.),
            tv_18, round(tv_18 / tv * 100.), tv_20, round(tv_20 / tv * 100.),
            tv
        ),
        (
            'TEST',
            te_02, round(te_02 / te * 100.), te_04, round(te_04 / te * 100.),
            te_06, round(te_06 / te * 100.), te_08, round(te_08 / te * 100.),
            te_10, round(te_10 / te * 100.), te_12, round(te_12 / te * 100.),
            te_14, round(te_14 / te * 100.), te_16, round(te_16 / te * 100.),
            te_18, round(te_18 / te * 100.), te_20, round(te_20 / te * 100.),
            te
        ),
        (
            'TOTAL',
            t_02, round(t_02 / t * 100.), t_04, round(t_04 / t * 100.),
            t_06, round(t_06 / t * 100.), t_08, round(t_08 / t * 100.),
            t_10, round(t_10 / t * 100.), t_12, round(t_12 / t * 100.),
            t_14, round(t_14 / t * 100.), t_16, round(t_16 / t * 100.),
            t_18, round(t_18 / t * 100.), t_20, round(t_20 / t * 100.),
            t
        )
    )
)
