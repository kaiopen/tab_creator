import csv
from pathlib import Path

from tab import TAB

from utils import round


tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

tr = 0
c_tr = 0
for f in tab_train:
    bounds = tab_train.get_boundaries(f)
    tr += len(bounds)
    for bound in bounds:
        for p in bound['points']:
            if p['curve']:
                c_tr += 1
                break
s_tr = tr - c_tr

v = 0
c_v = 0
for f in tab_val:
    bounds = tab_val.get_boundaries(f)
    v += len(bounds)
    for bound in bounds:
        for p in bound['points']:
            if p['curve']:
                c_v += 1
                break
s_v = v - c_v

s_tv = s_tr + s_v
u_tv = c_tr + c_v
tv = s_tv + u_tv

te = 0
c_te = 0
for f in tab_test:
    bounds = tab_test.get_boundaries(f)
    te += len(bounds)
    for bound in bounds:
        for p in bound['points']:
            if p['curve']:
                c_te += 1
                break
s_te = te - c_te

s_t = s_tv + s_te
u_t = u_tv + c_te
t = s_t + u_t

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('shape.csv').open('w')).writerows(
    (
        ('', '# straight', '% straight', '# curve', '% curve', '# total'),
        (
            'TRAIN',
            s_tr, round(s_tr / tr * 100.), c_tr, round(c_tr / tr * 100.), tr
        ),
        (
            'VAL',
            s_v, round(s_v / v * 100.), c_v, round(c_v / v * 100.), v
        ),
        (
            'TRAINVAL',
            s_tv, round(s_tv / tv * 100.), u_tv, round(u_tv / tv * 100.), tv
        ),
        (
            'TEST',
            s_te, round(s_te / te * 100.), c_te, round(c_te / te * 100.), te
        ),
        (
            'TOTAL',
            s_t, round(s_t / t * 100.), u_t, round(u_t / t * 100.), t
        )
    )
)
