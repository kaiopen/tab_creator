import csv
from pathlib import Path

from tab import TAB

from utils import round


tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

tr = 0
tr_0400 = 0
tr_0800 = 0
tr_1200 = 0
tr_1600 = 0
tr_2000 = 0
tr_2400 = 0
tr_2800 = 0
tr_3200 = 0
tr_3600 = 0
tr_4000 = 0
tr_4400 = 0
tr_4800 = 0
for f in tab_train:
    bounds = tab_train.get_boundaries(f)
    tr += len(bounds)
    for bound in bounds:
        if (num := len(bound['points'])) < 400:
            tr_0400 += 1
        elif num < 800:
            tr_0800 += 1
        elif num < 1200:
            tr_1200 += 1
        elif num < 1600:
            tr_1600 += 1
        elif num < 2000:
            tr_2000 += 1
        elif num < 2400:
            tr_2400 += 1
        elif num < 2800:
            tr_2800 += 1
        elif num < 3200:
            tr_3200 += 1
        elif num < 3600:
            tr_3600 += 1
        elif num < 4000:
            tr_4000 += 1
        elif num < 4400:
            tr_4400 += 1
        else:
            tr_4800 += 1


v = 0
v_0400 = 0
v_0800 = 0
v_1200 = 0
v_1600 = 0
v_2000 = 0
v_2400 = 0
v_2800 = 0
v_3200 = 0
v_3600 = 0
v_4000 = 0
v_4400 = 0
v_4800 = 0
for f in tab_val:
    bounds = tab_val.get_boundaries(f)
    v += len(bounds)
    for bound in bounds:
        if (num := len(bound['points'])) < 400:
            v_0400 += 1
        elif num < 800:
            v_0800 += 1
        elif num < 1200:
            v_1200 += 1
        elif num < 1600:
            v_1600 += 1
        elif num < 2000:
            v_2000 += 1
        elif num < 2400:
            v_2400 += 1
        elif num < 2800:
            v_2800 += 1
        elif num < 3200:
            v_3200 += 1
        elif num < 3600:
            v_3600 += 1
        elif num < 4000:
            v_4000 += 1
        elif num < 4400:
            v_4400 += 1
        else:
            v_4800 += 1

tv = tr + v
tv_0400 = tr_0400 + v_0400
tv_0800 = tr_0800 + v_0800
tv_1200 = tr_1200 + v_1200
tv_1600 = tr_1600 + v_1600
tv_2000 = tr_2000 + v_2000
tv_2400 = tr_2400 + v_2400
tv_2800 = tr_2800 + v_2800
tv_3200 = tr_3200 + v_3200
tv_3600 = tr_3600 + v_3600
tv_4000 = tr_4000 + v_4000
tv_4400 = tr_4400 + v_4400
tv_4800 = tr_4800 + v_4800

te = 0
te_0400 = 0
te_0800 = 0
te_1200 = 0
te_1600 = 0
te_2000 = 0
te_2400 = 0
te_2800 = 0
te_3200 = 0
te_3600 = 0
te_4000 = 0
te_4400 = 0
te_4800 = 0
for f in tab_test:
    bounds = tab_test.get_boundaries(f)
    te += len(bounds)
    for bound in bounds:
        if (num := len(bound['points'])) < 400:
            te_0400 += 1
        elif num < 800:
            te_0800 += 1
        elif num < 1200:
            te_1200 += 1
        elif num < 1600:
            te_1600 += 1
        elif num < 2000:
            te_2000 += 1
        elif num < 2400:
            te_2400 += 1
        elif num < 2800:
            te_2800 += 1
        elif num < 3200:
            te_3200 += 1
        elif num < 3600:
            te_3600 += 1
        elif num < 4000:
            te_4000 += 1
        elif num < 4400:
            te_4400 += 1
        else:
            te_4800 += 1

t = tv + te
t_0400 = tv_0400 + te_0400
t_0800 = tv_0800 + te_0800
t_1200 = tv_1200 + te_1200
t_1600 = tv_1600 + te_1600
t_2000 = tv_2000 + te_2000
t_2400 = tv_2400 + te_2400
t_2800 = tv_2800 + te_2800
t_3200 = tv_3200 + te_3200
t_3600 = tv_3600 + te_3600
t_4000 = tv_4000 + te_4000
t_4400 = tv_4400 + te_4400
t_4800 = tv_4800 + te_4800


dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('length.csv').open('w')).writerows(
    (
        (
            '',
            '#. 0400', '%. 0400', '#. 0800', '%. 0800', '#. 1200', '%. 1200',
            '#. 1600', '%. 1600', '#. 2000', '%. 2000', '#. 2400', '%. 2400',
            '#. 2800', '%. 2800', '#. 3200', '%. 3200', '#. 3600', '%. 3600',
            '#. 4000', '%. 4000', '#. 4400', '%. 4400', '#. 4800', '%. 4800',
            'TOTAL'
        ),
        (
            'TRAIN',
            tr_0400, round(tr_0400 / tr * 100.),
            tr_0800, round(tr_0800 / tr * 100.),
            tr_1200, round(tr_1200 / tr * 100.),
            tr_1600, round(tr_1600 / tr * 100.),
            tr_2000, round(tr_2000 / tr * 100.),
            tr_2400, round(tr_2400 / tr * 100.),
            tr_2800, round(tr_2800 / tr * 100.),
            tr_3200, round(tr_3200 / tr * 100.),
            tr_3600, round(tr_3600 / tr * 100.),
            tr_4000, round(tr_4000 / tr * 100.),
            tr_4400, round(tr_4400 / tr * 100.),
            tr_4800, round(tr_4800 / tr * 100.),
            tr
        ),
        (
            'VAL',
            v_0400, round(v_0400 / v * 100.),
            v_0800, round(v_0800 / v * 100.),
            v_1200, round(v_1200 / v * 100.),
            v_1600, round(v_1600 / v * 100.),
            v_2000, round(v_2000 / v * 100.),
            v_2400, round(v_2400 / v * 100.),
            v_2800, round(v_2800 / v * 100.),
            v_3200, round(v_3200 / v * 100.),
            v_3600, round(v_3600 / v * 100.),
            v_4000, round(v_4000 / v * 100.),
            v_4400, round(v_4400 / v * 100.),
            v_4800, round(v_4800 / v * 100.),
            v
        ),
        (
            'TRAINVAL',
            tv_0400, round(tv_0400 / tv * 100.),
            tv_0800, round(tv_0800 / tv * 100.),
            tv_1200, round(tv_1200 / tv * 100.),
            tv_1600, round(tv_1600 / tv * 100.),
            tv_2000, round(tv_2000 / tv * 100.),
            tv_2400, round(tv_2400 / tv * 100.),
            tv_2800, round(tv_2800 / tv * 100.),
            tv_3200, round(tv_3200 / tv * 100.),
            tv_3600, round(tv_3600 / tv * 100.),
            tv_4000, round(tv_4000 / tv * 100.),
            tv_4400, round(tv_4400 / tv * 100.),
            tv_4800, round(tv_4800 / tv * 100.),
            tv
        ),
        (
            'TEST',
            te_0400, round(te_0400 / te * 100.),
            te_0800, round(te_0800 / te * 100.),
            te_1200, round(te_1200 / te * 100.),
            te_1600, round(te_1600 / te * 100.),
            te_2000, round(te_2000 / te * 100.),
            te_2400, round(te_2400 / te * 100.),
            te_2800, round(te_2800 / te * 100.),
            te_3200, round(te_3200 / te * 100.),
            te_3600, round(te_3600 / te * 100.),
            te_4000, round(te_4000 / te * 100.),
            te_4400, round(te_4400 / te * 100.),
            te_4800, round(te_4800 / te * 100.),
            te
        ),
        (
            'TOTAL',
            t_0400, round(t_0400 / t * 100.),
            t_0800, round(t_0800 / t * 100.),
            t_1200, round(t_1200 / t * 100.),
            t_1600, round(t_1600 / t * 100.),
            t_2000, round(t_2000 / t * 100.),
            t_2400, round(t_2400 / t * 100.),
            t_2800, round(t_2800 / t * 100.),
            t_3200, round(t_3200 / t * 100.),
            t_3600, round(t_3600 / t * 100.),
            t_4000, round(t_4000 / t * 100.),
            t_4400, round(t_4400 / t * 100.),
            t_4800, round(t_4800 / t * 100.),
            t
        )
    )
)
